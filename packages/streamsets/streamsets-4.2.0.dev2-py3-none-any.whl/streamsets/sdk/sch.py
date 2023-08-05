# Copyright 2021 StreamSets Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Abstractions for interacting with ControlHub."""
import copy
import json
import logging
import requests
import threading
import uuid
import warnings

from . import aster_api, sch_api, sdc_models
from .exceptions import JobInactiveError, UnsupportedMethodError, ValidationError
from .sch_models import (ActionAudits, AdminTool, Alert, ApiCredentialBuilder, ApiCredentials,
                         AWSEnvironment, AzureEnvironment, AzureVMDeployment, ClassificationRuleBuilder, Configuration,
                         ConnectionAudits, ConnectionBuilder, ConnectionTags, ConnectionVerificationResult,
                         Connections, DataCollector, DataSlaBuilder, DeploymentBuilder,
                         DeploymentEngineConfigurations, Deployments, EnvironmentBuilder, Environments,
                         EC2Deployment, GCEDeployment, GCPEnvironment, GroupBuilder, Groups,
                         Job, JobBuilder, Jobs, LegacyDeploymentBuilder, LegacyDeployments, LoginAudits,
                         MeteringUsage, OrganizationBuilder, Organizations, Pipeline,
                         PipelineBuilder, PipelineLabels, Pipelines, ProtectionMethodBuilder,
                         ProtectionPolicies, ProtectionPolicy, ProtectionPolicyBuilder, ProvisioningAgents,
                         ReportDefinitions, ScheduledTaskBuilder,
                         ScheduledTasks, SelfManagedDeployment, SelfManagedEnvironment,
                         StPipelineBuilder, SubscriptionAudit, SubscriptionBuilder,
                         Subscriptions, Topologies, Topology, TopologyBuilder, Transformer, UserBuilder, Users)
from .utils import (SDC_DEFAULT_EXECUTION_MODE, SeekableList, TRANSFORMER_EXECUTION_MODES,
                    wait_for_condition, reversed_dict, Version)

logger = logging.getLogger(__name__)

DEFAULT_ASTER_SERVER_URL = 'https://cloud.login.streamsets.com'
DEFAULT_DATA_COLLECTOR_STAGE_LIBS = ['windows', 'dataformats', 'basic', 'dev', 'stats']
DEFAULT_SESSION_ATTRIBUTES = {'verify': True}
DEFAULT_SYSTEM_SDC_ID = 'SYSTEM_SDC_ID'
DEFAULT_TRANSFORMER_STAGE_LIBS = ['basic', 'file']
DEFAULT_WAIT_FOR_STATUS_TIMEOUT = 300
DEFAULT_WAIT_FOR_METRIC_TIMEOUT = 200
SDC_EXECUTOR_TYPE = 'COLLECTOR'
SNOWFLAKE_EXECUTOR_TYPE = 'SNOWPARK'
SNOWFLAKE_ENGINE_ID = 'SYSTEM_SNOWPARK_ENGINE_ID'
TRANSFORMER_EXECUTOR_TYPE = 'TRANSFORMER'

class ControlHub:
    """Class to interact with StreamSets Control Hub.

    Args:
        credential_id (:obj:`str`): ControlHub credential ID.
        token (:obj:`str`): ControlHub token.
        use_websocket_tunneling (:obj:`bool`, optional): use websocket tunneling. Default: ``True``.
    """
    VERIFY_SSL_CERTIFICATES = True

    def __init__(self,
                 credential_id,
                 token,
                 use_websocket_tunneling=True,
                 **kwargs):
        self.credential_id = credential_id
        self.token = token
        self.use_websocket_tunneling = use_websocket_tunneling

        if self.use_websocket_tunneling:
            logger.info('Using WebSocket tunneling ...')

        session_attributes = {'verify': self.VERIFY_SSL_CERTIFICATES}
        self.api_client = sch_api.ApiClient(component_id=self.credential_id,
                                            auth_token=self.token,
                                            session_attributes=session_attributes,
                                            aster_url=kwargs.get('aster_url'))
        self.server_url = self.api_client.base_url

        self.organization = self.api_client.get_current_user().response.json()['organizationId']

        self._roles = {user_role['id']: user_role['label']
                       for user_role in self.api_client.get_all_user_roles()}
        # Manually updating labels that have changed - reference security_data_service.spec.ts
        self._roles.update({'datacollector:admin': 'Engine Administrator',
                            'datacollector:creator': 'Engine Creator',
                            'datacollector:guest': 'Engine Guest',
                            'datacollector:manager': 'Engine Manager',
                            'timeseries:reader': 'Metrics Reader'})

        self._data_protector_version = None

        # We keep the Swagger API definitions as attributes for later use by various
        # builders.
        self._connection_api = self.api_client.get_connection_api()
        self._job_api = self.api_client.get_job_api()
        self._pipelinestore_api = self.api_client.get_pipelinestore_api()
        self._provisioning_api = self.api_client.get_provisioning_api()
        self._security_api = self.api_client.get_security_api()
        self._topology_api = self.api_client.get_topology_api()
        self._scheduler_api = self.api_client.get_scheduler_api()
        self._notification_api = self.api_client.get_notification_api()

        self._en_translations = self.api_client.get_translations_json()

        self._data_collectors = {}
        self._transformers = {}
        thread = threading.Thread(target=self._call_data_collectors)
        thread.start()

    def _call_data_collectors(self):
        self.data_collectors
        self.transformers

    def _get_aster_api_client(self):
        # Allows us to retrieve an ApiClient from aster_api ad-hoc without having to instantiate one when we initialize
        # a ControlHub object.
        aster_api_client = aster_api.ApiClient(server_url=DEFAULT_ASTER_SERVER_URL,
                                               sch_auth_token=self.token,
                                               sch_credential_id=self.credential_id,
                                               session_attributes=DEFAULT_SESSION_ATTRIBUTES)
        aster_api_client.login()
        return aster_api_client

    @property
    def version(self):
        # The version of the ControlHub server, determined
        # by making a URL call to the server
        server_info = self.api_client.get_server_info()
        return server_info.response.json()['version']

    @property
    def ldap_enabled(self):
        """Indication if LDAP is enabled or not.

        Returns:
            An instance of :obj:`boolean`.
        """
        return self.api_client.is_ldap_enabled().response.json()

    @property
    def organization_global_configuration(self):
        organization_global_configuration = self.api_client.get_organization_global_configurations().response.json()

        # Some of the config names are a bit long, so shorten them slightly...
        ID_TO_REMAP = {'accountType': 'Organization account type',
                       'contractExpirationTime': 'Timestamp of the contract expiration',
                       'trialExpirationTime': 'Timestamp of the trial expiration'}
        return Configuration(configuration=organization_global_configuration,
                             update_callable=self.api_client.update_organization_global_configurations,
                             id_to_remap=ID_TO_REMAP)

    @organization_global_configuration.setter
    def organization_global_configuration(self, value):
        self.api_client.update_organization_global_configurations(value._data)

    def get_pipeline_builder(self, engine_type, engine_id=None, fragment=False):
        """Get a pipeline builder instance with which a pipeline can be created.

        Args:
            engine_type (:obj:`str`): The type of pipeline that will be created. The options are ``'data_collector'``,
                                      ``'snowflake'`` or ``'transformer'``.
            engine_id (:obj:`str`): The ID of the Data Collector or Transformer in which to author the pipeline if not
                                    using Transformer for Snowflake.
            fragment (:obj:`boolean`, optional): Specify if a fragment builder. Default: ``False``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.PipelineBuilder` or
            :py:class:`streamsets.sdk.sch_models.StPipelineBuilder`.
        """
        if engine_type == 'snowflake' and engine_id:
            raise ValueError("Pipelines of type 'snowflake' do not use an engine id.")
        if engine_type != 'snowflake' and not engine_id:
            raise ValueError("Pipelines of type 'data_collector' or 'transformer' require an engine id.")
        if engine_type == 'data_collector':
            authoring_engine = self.data_collectors.get(id=engine_id)
        elif engine_type == 'transformer':
            authoring_engine = self.transformers.get(id=engine_id)
        else:
            authoring_engine = None
        pipeline = {property: None
                    for property in self._pipelinestore_api['definitions']['PipelineJson']['properties']}
        if authoring_engine is not None:
            data_collector_instance = authoring_engine._instance
            if fragment:
                create_fragment_response = (data_collector_instance.api_client
                                            .create_fragment('Pipeline Builder',
                                                             draft=True).response.json())
                pipeline_definition = json.dumps(create_fragment_response['pipelineFragmentConfig'])
                library_definitions = (json.dumps(create_fragment_response['libraryDefinitions'])
                                       if create_fragment_response['libraryDefinitions'] else None)
                commit_pipeline_json = {'name': 'Pipeline Builder',
                                        'sdcId': authoring_engine.id,
                                        'fragment': True,
                                        'pipelineDefinition': pipeline_definition,
                                        'rulesDefinition': json.dumps(create_fragment_response['pipelineRules']),
                                        'libraryDefinitions': library_definitions}
                commit_pipeline_response = self.api_client.commit_pipeline(new_pipeline=True,
                                                                           import_pipeline=False,
                                                                           body=commit_pipeline_json,
                                                                           fragment=fragment).response.json()

                commit_id = commit_pipeline_response['commitId']
                pipeline_id = commit_pipeline_response['pipelineId']

                pipeline_commit = self.api_client.get_pipeline_commit(commit_id).response.json()
                pipeline_json = dict(pipelineFragmentConfig=json.loads(pipeline_commit['pipelineDefinition']),
                                     pipelineRules=json.loads(pipeline_commit['currentRules']['rulesDefinition']),
                                     libraryDefinitions=pipeline_commit['libraryDefinitions'])
                data_collector_instance._pipeline = pipeline_json
                self.api_client.delete_pipeline(pipeline_id)
            pipeline['sdcId'] = authoring_engine.id
            pipeline['sdcVersion'] = authoring_engine.version
        if engine_type == 'snowflake':
            # A :py:class:`streamsets.sdk.sdc_models.PipelineBuilder` instance takes an empty pipeline and a
            # dictionary of definitions as arguments. To get the former, we generate a pipeline, export it,
            # and then delete it. For the latter, we simply pass along `aux_definitions`.
            commit_pipeline_json = {'name': 'Pipeline Builder',
                                    'sdcId': SNOWFLAKE_ENGINE_ID,
                                    'executorType': SNOWFLAKE_EXECUTOR_TYPE,
                                    'fragment': fragment,
                                    'failIfExists': True
                                    }
            create_pipeline_response = self.api_client.commit_pipeline(new_pipeline=True,
                                                                       import_pipeline=False,
                                                                       execution_mode=SNOWFLAKE_EXECUTOR_TYPE,
                                                                       pipeline_type='SNOWPARK_PIPELINE',
                                                                       body=commit_pipeline_json,
                                                                       fragment=fragment).response.json()
            pipeline_id = create_pipeline_response['pipelineId']
            aux_definitions = self.api_client.get_pipelines_definitions(SNOWFLAKE_EXECUTOR_TYPE).response.json()

            pipeline_config = json.loads(create_pipeline_response['pipelineDefinition'])

            # pipeline cleanup to avoid showing errors
            pipeline_config['issues']['pipelineIssues'] = []
            pipeline_config['issues']['issueCount'] = 0
            pipeline_config['valid'] = True
            pipeline_config['previewable'] = True

            aux_pipeline = {'pipelineConfig': pipeline_config,
                            'pipelineRules': json.loads(create_pipeline_response['currentRules']['rulesDefinition']),
                            'libraryDefinitions': aux_definitions}
            self.api_client.delete_pipeline(pipeline_id)
            executor_pipeline_builder = sdc_models.PipelineBuilder(pipeline=aux_pipeline,
                                                                    definitions=aux_definitions,
                                                                    fragment=fragment)
            pipeline['sdcVersion'] = create_pipeline_response['sdcVersion']
            pipeline['sdcId'] = create_pipeline_response['sdcId']
            pipeline['executorType'] = create_pipeline_response['executorType']

        if authoring_engine:
            executor_pipeline_builder = data_collector_instance.get_pipeline_builder(fragment=fragment)
        if engine_type == 'transformer':
            pipeline['executorType'] = 'TRANSFORMER'
            return StPipelineBuilder(pipeline=pipeline,
                                     transformer_pipeline_builder=executor_pipeline_builder,
                                     control_hub=self,
                                     fragment=fragment)
        return PipelineBuilder(pipeline=pipeline,
                               data_collector_pipeline_builder=executor_pipeline_builder,
                               control_hub=self,
                               fragment=fragment)

    def publish_pipeline(self, pipeline, commit_message='New pipeline', draft=False):
        """Publish a pipeline.

        Args:
            pipeline (:py:obj:`streamsets.sdk.sch_models.Pipeline`): Pipeline object.
            commit_message (:obj:`str`, optional): Default: ``'New pipeline'``.
            draft (:obj:`boolean`, optional): Default: ``False``.
        """
        # Get the updated stage data and update it in the pipelineDefinition json string.
        pipeline_definition = pipeline._pipeline_definition
        pipeline_stages = pipeline.stages
        pipeline_definition['stages'] = []
        for stage in pipeline_stages:
            pipeline_definition['stages'].append(stage._data)
        pipeline._pipeline_definition = pipeline_definition
        pipeline._data['pipelineDefinition'] = pipeline_definition
        execution_mode = pipeline.configuration.get('executionMode', SDC_DEFAULT_EXECUTION_MODE)

        if execution_mode != SNOWFLAKE_EXECUTOR_TYPE:
            # A :py:class:`streamsets.sdk.sch_models.Pipeline` instance with no commit ID hasn't been
            # published to ControlHub before, so we do so first.
            if not pipeline.commit_id:
                commit_pipeline_json = {'name': pipeline._pipeline_definition['title'],
                                        'sdcId': pipeline.sdc_id}
                if pipeline.sdc_id != DEFAULT_SYSTEM_SDC_ID:
                    commit_pipeline_json.update({'pipelineDefinition': json.dumps(pipeline._pipeline_definition),
                                                 'rulesDefinition': json.dumps(pipeline._rules_definition)})
                # fragmentCommitIds property is not returned by :py:meth:`streamsets.sdk.sch_api.ApiClient.commit_pipeline
                # and hence have to store it and add it to pipeline data before publishing the pipeline.
                fragment_commit_ids = pipeline._data.get('fragmentCommitIds')

                if execution_mode in TRANSFORMER_EXECUTION_MODES:
                    commit_pipeline_json.update({'executorType': 'TRANSFORMER'})
                pipeline._data = self.api_client.commit_pipeline(new_pipeline=True,
                                                                 import_pipeline=False,
                                                                 fragment=pipeline.fragment,
                                                                 execution_mode=execution_mode,
                                                                 body=commit_pipeline_json).response.json()
                if fragment_commit_ids and not pipeline.fragment:
                    pipeline._data['fragmentCommitIds'] = fragment_commit_ids
            # If the pipeline does have a commit ID and is not a draft, we want to create a new draft and update the
            # existing one in the pipeline store instead of creating a new one.
            elif not getattr(pipeline, 'draft', False):
                pipeline._data = self.api_client.create_pipeline_draft(
                    commit_id=pipeline.commit_id,
                    authoring_sdc_id=pipeline.sdc_id,
                    authoring_sdc_version=pipeline.sdc_version
                ).response.json()
                # The pipeline name is overwritten when drafts are created, so we account for it here.
                pipeline.name = pipeline._pipeline_definition['title']

            pipeline.commit_message = commit_message
            pipeline.current_rules['rulesDefinition'] = json.dumps(pipeline._rules_definition)
            pipeline._pipeline_definition['metadata'].update({'dpm.pipeline.rules.id': pipeline.current_rules['id'],
                                                              'dpm.pipeline.id': pipeline.pipeline_id,
                                                              'dpm.pipeline.version': pipeline.version,
                                                              'dpm.pipeline.commit.id': pipeline.commit_id})
            pipeline._data['pipelineDefinition'] = json.dumps(pipeline._pipeline_definition)

        # Translated js code from https://git.io/fj1kr.
        # Call sdc api to import pipeline and libraryDefinitions.
        validate = False
        pipeline_definition = (pipeline._data['pipelineDefinition']
                               if isinstance(pipeline._data['pipelineDefinition'], dict)
                               else json.loads(pipeline._data['pipelineDefinition']))
        entity_id = 'fragmentId' if 'fragmentId' in pipeline_definition else 'pipelineId'
        sdc_pipeline_id = pipeline_definition[entity_id]

        if execution_mode == SNOWFLAKE_EXECUTOR_TYPE:
            if pipeline.commit_id and not getattr(pipeline, 'draft', False):
                pipeline._data = self.api_client.create_pipeline_draft(
                    commit_id=pipeline.commit_id,
                    authoring_sdc_id=pipeline.sdc_id,
                    authoring_sdc_version=pipeline.sdc_version
                ).response.json()
                # The pipeline name is overwritten when drafts are created, so we account for it here.
                pipeline.name = pipeline._pipeline_definition['title']
                pipeline.commit_id = pipeline._data['commitId']

            pipeline.execution_mode = execution_mode
            library_definitions = self.api_client.get_pipelines_definitions(SNOWFLAKE_EXECUTOR_TYPE).response.text
            pipeline_envelope = {'pipelineDefinition': json.dumps(pipeline._pipeline_definition),
                                 'rulesDefinition': json.dumps(pipeline._rules_definition),
                                 'executorType': execution_mode,
                                 'failIfExists': False,
                                 'commitMessage': commit_message,
                                 'name': pipeline._pipeline_definition['title'],
                                 'libraryDefinitions': library_definitions}
            config_key = 'pipelineDefinition'
            if not pipeline.commit_id:
                # fragmentCommitIds property is not returned by :py:meth:`streamsets.sdk.sch_api.ApiClient.commit_pipeline
                # and hence have to store it and add it to pipeline data before publishing the pipeline.
                fragment_commit_ids = pipeline._data.get('fragmentCommitIds')

                response_envelope = (self.api_client.commit_pipeline(new_pipeline=True,
                                                                     import_pipeline=False,
                                                                     fragment=pipeline.fragment,
                                                                     execution_mode=execution_mode,
                                                                     body=pipeline_envelope).response.json())
                if fragment_commit_ids and not pipeline.fragment:
                    pipeline._data['fragmentCommitIds'] = fragment_commit_ids
                pipeline.commit_id = response_envelope['commitId']
            else:
                response_envelope = pipeline_envelope
            response_envelope[config_key] = json.loads(response_envelope[config_key])
        else:
            config_key = 'pipelineFragmentConfig' if pipeline.fragment else 'pipelineConfig'
            pipeline_envelope = {config_key: pipeline._pipeline_definition,
                                 'pipelineRules': pipeline._rules_definition}
            executors = self.transformers if execution_mode in TRANSFORMER_EXECUTION_MODES else self.data_collectors
            # Import the pipeline
            if pipeline.fragment:
                response_envelope = (executors.get(id=pipeline.sdc_id)
                                     ._instance.api_client
                                     .import_fragment(fragment_id=sdc_pipeline_id,
                                                      fragment_json=pipeline_envelope,
                                                      include_library_definitions=True,
                                                      draft=True))
            else:
                response_envelope = (executors.get(id=pipeline.sdc_id)
                                     ._instance.api_client
                                     .import_pipeline(pipeline_id=sdc_pipeline_id,
                                                      pipeline_json=pipeline_envelope,
                                                      overwrite=True,
                                                      include_library_definitions=True,
                                                      auto_generate_pipeline_id=True,
                                                      draft=True))
        response_envelope[config_key]['pipelineId'] = sdc_pipeline_id
        if execution_mode in TRANSFORMER_EXECUTION_MODES:
            response_envelope[config_key].update({'executorType': 'TRANSFORMER'})
        pipeline._data['pipelineDefinition'] = json.dumps(response_envelope[config_key])
        if response_envelope['libraryDefinitions']:
            if type(response_envelope['libraryDefinitions']) is not str:
                pipeline._data['libraryDefinitions'] = json.dumps(response_envelope['libraryDefinitions'])
            else:
                pipeline._data['libraryDefinitions'] = response_envelope['libraryDefinitions']
        else:
            pipeline._data['libraryDefinitions'] = None
        if execution_mode == SNOWFLAKE_EXECUTOR_TYPE:
            if 'currentRules' in response_envelope:
                pipeline._data['currentRules'] = dict(
                    rulesDefinition=response_envelope['currentRules']['rulesDefinition'])
            elif 'rulesDefinition' in response_envelope:
                pipeline._data['currentRules'] = dict(rulesDefinition=response_envelope['rulesDefinition'])
        else:
            pipeline._data['currentRules']['rulesDefinition'] = json.dumps(response_envelope['pipelineRules'])
        save_pipeline_commit_command = self.api_client.save_pipeline_commit(commit_id=pipeline.commit_id,
                                                                            validate=validate,
                                                                            include_library_definitions=True,
                                                                            body=pipeline._data)
        if not draft:
            publish_pipeline_commit_command = self.api_client.publish_pipeline_commit(commit_id=pipeline.commit_id,
                                                                                      commit_message=commit_message)
        # Due to DPM-4470, we need to do one more REST API call to get the correct pipeline data.
        pipeline_commit = self.api_client.get_pipeline_commit(commit_id=pipeline.commit_id).response.json()

        pipeline._data = pipeline_commit
        if pipeline._builder is not None:
            pipeline._builder._sch_pipeline = pipeline_commit
        return save_pipeline_commit_command if draft else publish_pipeline_commit_command

    def delete_pipeline(self, pipeline, only_selected_version=False):
        """Delete a pipeline.

        Args:
            pipeline (:py:obj:`streamsets.sdk.sch_models.Pipeline`): Pipeline object.
            only_selected_version (:obj:`boolean`): Delete only current commit.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        if only_selected_version:
            return self.api_client.delete_pipeline_commit(pipeline.commit_id)
        return self.api_client.delete_pipeline(pipeline.pipeline_id)

    def duplicate_pipeline(self, pipeline, name=None, description='New Pipeline', number_of_copies=1):
        """Duplicate an existing pipeline.

        Args:
            pipeline (:py:obj:`streamsets.sdk.sch_models.Pipeline`): Pipeline object.
            name (:obj:`str`, optional): Name of the new pipeline(s). Default: ``None``.
            description (:obj:`str`, optional): Description for new pipeline(s). Default: ``'New Pipeline'``.
            number_of_copies (:obj:`int`, optional): Number of copies. Default: ``1``.

        Returns:
            A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.Pipeline`.
        """
        if name is None:
            name = '{} copy'.format(pipeline.name)
        # Add a unique name prefix to identify duplicated pipelines
        dummy_name_prefix = '{}:{}'.format(name, str(uuid.uuid4()))

        duplicated_pipelines = SeekableList()

        duplicate_body = {property: None
                          for property in self._pipelinestore_api['definitions']['DuplicatePipelineJson']['properties']}
        duplicate_body.update({'namePrefix': dummy_name_prefix,
                               'description': description,
                               'numberOfCopies': number_of_copies})
        self.api_client.duplicate_pipeline(pipeline.commit_id, duplicate_body)

        if number_of_copies == 1:
            dummy_names = [dummy_name_prefix]
        else:
            dummy_names = ['{}{}'.format(dummy_name_prefix, i) for i in range(1, number_of_copies+1)]
        # Update dummy names with actual names
        for i, dummy_name in enumerate(dummy_names):
            duplicated_pipeline = self.pipelines.get(only_published=False, name=dummy_name)
            if number_of_copies == 1:
                duplicated_pipeline.name = name
            else:
                duplicated_pipeline.name = '{}{}'.format(name, i+1)
            self.api_client.save_pipeline_commit(commit_id=duplicated_pipeline.commit_id,
                                                 include_library_definitions=True,
                                                 body=duplicated_pipeline._data)
            duplicated_pipelines.append(duplicated_pipeline)
        return duplicated_pipelines

    def update_pipelines_with_different_fragment_version(self, pipelines, from_fragment_version,
                                                         to_fragment_version):
        """Update pipelines with latest pipeline fragment commit version.

        Args:
            pipelines (:obj:`list`): List of :py:class:`streamsets.sdk.sch_models.Pipeline` instances.
            from_fragment_version (:py:obj:`streamsets.sdk.sch_models.PipelineCommit`): commit of fragment from which
                                                                                        the pipeline needs to be
                                                                                        updated.
            to_fragment_version (:py:obj:`streamsets.sdk.sch_models.PipelineCommit`): commit of fragment to which
                                                                                      the pipeline needs to be updated.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`
        """
        pipeline_commit_ids = [pipeline.commit_id for pipeline in pipelines]
        return self.api_client.update_pipelines_with_fragment_commit_version(pipeline_commit_ids,
                                                                             from_fragment_version.commit_id,
                                                                             to_fragment_version.commit_id)

    @property
    def pipeline_labels(self):
        """Pipeline labels.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.PipelineLabels`.
        """
        return PipelineLabels(self, organization=self.organization)

    def delete_pipeline_labels(self, *pipeline_labels):
        """Delete pipeline labels.

        Args:
            *pipeline_labels: One or more instances of :py:class:`streamsets.sdk.sch_models.PipelineLabel`.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        pipeline_label_ids = [pipeline_label.id for pipeline_label in pipeline_labels]
        logger.info('Deleting pipeline labels %s ...', pipeline_label_ids)
        delete_pipeline_label_command = self.api_client.delete_pipeline_labels(body=pipeline_label_ids)
        return delete_pipeline_label_command

    def duplicate_job(self, job, name=None, description=None, number_of_copies=1):
        """Duplicate an existing job.

        Args:
            job (:py:obj:`streamsets.sdk.sch_models.Job`): Job object.
            name (:obj:`str`, optional): Name of the new job(s). Default: ``None``. If not specified, name of the job
                                         with ``' copy'`` appended to the end will be used.
            description (:obj:`str`, optional): Description for new job(s). Default: ``None``.
            number_of_copies (:obj:`int`, optional): Number of copies. Default: ``1``.

        Returns:
            A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        if name is None:
            name = '{} copy'.format(job.job_name)
        # Add a unique name prefix to identify duplicated job
        dummy_name_prefix = '{}:{}'.format(name, str(uuid.uuid4()))

        duplicated_jobs = SeekableList()

        duplicate_body = {property: None
                          for property in self._job_api['definitions']['DuplicateJobJson']['properties']}
        duplicate_body.update({'namePrefix': dummy_name_prefix,
                               'description': description,
                               'numberOfCopies': number_of_copies})
        self.api_client.duplicate_job(job.job_id, duplicate_body)

        if number_of_copies == 1:
            dummy_names = [dummy_name_prefix]
        else:
            dummy_names = ['{}{}'.format(dummy_name_prefix, i) for i in range(1, number_of_copies+1)]
        # Update dummy names with actual names
        for i, dummy_name in enumerate(dummy_names):
            duplicated_job = self.jobs.get(job_name=dummy_name)
            if number_of_copies == 1:
                duplicated_job.job_name = name
            else:
                duplicated_job.job_name = '{}{}'.format(name, i+1)
            self.update_job(duplicated_job)
            duplicated_jobs.append(duplicated_job)
        return duplicated_jobs

    def get_user_builder(self):
        """Get a user builder instance with which a user can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.UserBuilder`.
        """
        user = {}
        # Update the UserJson with the API definitions from Swagger.
        user.update({property: None
                     for property in self._security_api['definitions']['UserJson']['properties']})

        # Set other properties based on defaults from the web UI.
        user_defaults = {'active': True,
                         'groups': ['all@{}'.format(self.organization)],
                         'organization': self.organization,
                         'passwordGenerated': False,
                         'roles': ['connection:user',
                                   'csp:deployment-manager',
                                   'csp:environment-manager',
                                   'datacollector:admin',
                                   'jobrunner:operator',
                                   'notification:user',
                                   'org-user',
                                   'pipelinestore:pipelineEditor',
                                   'provisioning:operator',
                                   'sla:editor',
                                   'timeseries:reader',
                                   'topology:editor',
                                   'user'],
                         'userDeleted': False}
        user.update(user_defaults)

        return UserBuilder(user=user, roles=self._roles, control_hub=self)

    def invite_user(self, user):
        """Invite a user to the DataOps Platform.

        Args:
            user (:py:class:`streamsets.sdk.sch_models.User`): User object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        logger.info('Adding a user %s ...', user.email_address)
        # First, invite the user via ASTER
        aster_api_client = self._get_aster_api_client()
        # User is an either an administrator for their organization ('ADMINISTRATOR') or a regular user ('OPERATOR').
        # The user's roles store either 'org-admin' or 'org-user' accordingly.
        user_data = {'email': user.email_address, 'role': 'ADMINISTRATOR' if 'org-admin' in user.roles else 'OPERATOR'}
        body = {'data': user_data, 'version': 2}
        aster_user = aster_api_client.invite_org_users(body=body).response.json()
        # Second, retrieve the user entry in DataOps and update the roles/groups selected during UserBuilder.build()
        sch_user_id = '{}@{}'.format(aster_user['data']['schUser'], self.organization)
        sch_user_json = self.api_client.get_user(org_id=self.organization,
                                                 user_id=sch_user_id).response.json()
        sch_user_json.update({'roles': user._data['roles'], 'groups': user._data['groups']})
        update_user_command = self.api_client.update_user(org_id=self.organization,
                                                          user_id=sch_user_id,
                                                          body=sch_user_json)
        user._data = update_user_command.response.json()
        return update_user_command

    def update_user(self, user):
        """Update a user. Some user attributes are updated by ControlHub such as
            last_modified_by,
            last_modified_on.

        Args:
            user (:py:class:`streamsets.sdk.sch_models.User`): User object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        logger.info('Updating a user %s ...', user)
        update_user_command = self.api_client.update_user(body=user._data,
                                                          org_id=self.organization,
                                                          user_id=user.id)
        user._data = update_user_command.response.json()
        return update_user_command

    def activate_user(self, *users):
        """Activate users for all given User IDs.

        Args:
            *users: One or more instance of :py:class:`streamsets.sdk.sch_models.User`.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        user_ids = [user.id.split('@')[0] for user in users]
        logger.info('Activating user(s) %s ...', user_ids)
        aster_api_client = self._get_aster_api_client()
        aster_user_ids = [aster_api_client.get_org_users(search='schUser=={}'.format(user_id)
                                                         ).response.json()['data']['content'][0]['id']
                          for user_id in user_ids]
        body = {'data': aster_user_ids, 'version': 2}
        return aster_api_client.activate_org_users(body)

    def deactivate_user(self, *users):
        """Deactivate Users for all given User IDs.

        Args:
            *users: One or more instances of :py:class:`streamsets.sdk.sch_models.User`.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        user_ids = [user.id.split('@')[0] for user in users]
        logger.info('Deactivating user(s) %s ...', user_ids)
        aster_api_client = self._get_aster_api_client()
        aster_user_ids = [aster_api_client.get_org_users(search='schUser=={}'.format(user_id)
                                                         ).response.json()['data']['content'][0]['id']
                          for user_id in user_ids]
        body = {'data': aster_user_ids, 'version': 2}
        return aster_api_client.deactivate_org_users(body=body)

    def delete_user(self, *users, deactivate=False):
        """Delete users. Deactivate users before deleting if configured.

        Args:
            *users: One or more instances of :py:class:`streamsets.sdk.sch_models.User`.
            deactivate (:obj:`bool`, optional): Default: ``False``.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        if deactivate:
            self.deactivate_user(*users)

        user_ids = [user.id.split('@')[0] for user in users]
        logger.info('Deleting user(s) %s ...', user_ids)
        aster_api_client = self._get_aster_api_client()
        aster_user_ids = [aster_api_client.get_org_users(search='schUser=={}'.format(user_id)
                                                         ).response.json()['data']['content'][0]['id']
                          for user_id in user_ids]
        body = {'data': aster_user_ids, 'version': 2}
        return aster_api_client.delete_org_users(body=body)

    def assign_administrator_role(self, user):
        """Designate the specified user as an Organization Administrator.

        Args:
            user (:py:class:`streamsets.sdk.sch_models.User`): User object.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        user_id = user.id.split('@')[0]
        logger.info('Giving admin rights to user %s', user_id)
        aster_api_client = self._get_aster_api_client()
        aster_user_json = aster_api_client.get_org_users(search='schUser=={}'.format(user_id)
                                                         ).response.json()['data']['content'][0]
        aster_user_json.update({'role': 'ADMINISTRATOR'})
        body = {'data': aster_user_json, 'version': 2}
        return aster_api_client.update_org_user(user_id=aster_user_json['id'], body=body)

    def remove_administrator_role(self, user):
        """Remove the Organization Administrator status from the specified user.

        Args:
            user (:py:class:`streamsets.sdk.sch_models.User`): User object.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        user_id = user.id.split('@')[0]
        logger.info('Removing admin rights from user %s', user_id)
        aster_api_client = self._get_aster_api_client()
        aster_user_json = aster_api_client.get_org_users(search='schUser=={}'.format(user_id)
                                                         ).response.json()['data']['content'][0]
        aster_user_json.update({'role': 'OPERATOR'})
        body = {'data': aster_user_json, 'version': 2}
        return aster_api_client.update_org_user(user_id=aster_user_json['id'], body=body)

    @property
    def users(self):
        """Users.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Users`.
        """
        return Users(self, self._roles, self.organization)

    @property
    def login_audits(self):
        """Login Audits.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.LoginAudits`.
        """
        return LoginAudits(self, self.organization)

    @property
    def action_audits(self):
        """Action Audits.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ActionAudits`.
        """
        return ActionAudits(self, self.organization)

    @property
    def connection_audits(self):
        """Connection Audits.

        Returns:
            An instance of :py:obj:`streamsets.sdk.sch_models.ConnectionAudits`.
        """
        return ConnectionAudits(self, self.organization)

    def get_group_builder(self):
        """Get a group builder instance with which a group can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.GroupBuilder`.
        """
        # Update the GroupJson with the API definitions from Swagger.
        group = {property: None
                 for property in self._security_api['definitions']['GroupJson']['properties']}

        # Set other properties based on defaults from the web UI.
        group_defaults = {'organization': self.organization,
                          'roles': ['timeseries:reader',
                                    'datacollector:manager',
                                    'jobrunner:operator',
                                    'pipelinestore:pipelineEditor',
                                    'topology:editor',
                                    'org-user',
                                    'sla:editor',
                                    'provisioning:operator',
                                    'user',
                                    'datacollector:creator',
                                    'notification:user'],
                          'users': []}
        group.update(group_defaults)

        return GroupBuilder(group=group, roles=self._roles)

    def add_group(self, group):
        """Add a group.

        Args:
            group (:py:class:`streamsets.sdk.sch_models.Group`): Group object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        logger.info('Adding a group %s ...', group)
        create_group_command = self.api_client.create_group(self.organization, group._data)
        # Update :py:class:`streamsets.sdk.sch_models.Group` with updated Group metadata.
        group._data = create_group_command.response.json()
        return create_group_command

    def update_group(self, group):
        """Update a group.

        Args:
            group (:py:class:`streamsets.sdk.sch_models.Group`): Group object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        logger.info('Updating a group %s ...', group)
        update_group_command = self.api_client.update_group(body=group._data,
                                                            org_id=self.organization,
                                                            group_id=group.id)
        group._data = update_group_command.response.json()
        return update_group_command

    def delete_group(self, *groups):
        """Delete groups.

        Args:
            *groups: One or more instances of :py:class:`streamsets.sdk.sch_models.Group`.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        if len(groups) == 1:
            logger.info('Deleting a group %s ...', groups[0])
            delete_group_command = self.api_client.delete_group(org_id=self.organization,
                                                                group_id=groups[0].id)
        else:
            group_ids = [group.id for group in groups]
            logger.info('Deleting groups %s ...', group_ids)
            delete_group_command = self.api_client.delete_groups(body=group_ids,
                                                                 org_id=self.organization)
        return delete_group_command

    @property
    def groups(self):
        """Groups.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Groups`.
        """
        return Groups(self, self._roles, self.organization)

    @property
    def data_collectors(self):
        """Data Collectors registered to the ControlHub instance.

        Returns:
            Returns a :py:class:`streamsets.sdk.utils.SeekableList` of
            :py:class:`streamsets.sdk.sch_models.DataCollector` instances.
        """
        self._get_update_executors_cache('COLLECTOR')
        return SeekableList(self._data_collectors.values())

    @property
    def transformers(self):
        """Transformers registered to the ControlHub instance.

        Returns:
            Returns a :py:class:`streamsets.sdk.utils.SeekableList` of
            :py:class:`streamsets.sdk.sch_models.Transformer` instances.
        """
        self._get_update_executors_cache('TRANSFORMER')
        return SeekableList(self._transformers.values())

    @property
    def provisioning_agents(self):
        """Provisioning Agents registered to the ControlHub instance.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ProvisioningAgents`.
        """
        return ProvisioningAgents(self, self.organization)

    def delete_provisioning_agent(self, provisioning_agent):
        """Delete provisioning agent.

        Args:
            provisioning_agent (:py:class:`streamets.sdk.sch_models.ProvisioningAgent`):

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        return self.api_client.delete_provisioning_agent(provisioning_agent.id)

    def deactivate_provisioning_agent(self, provisioning_agent):
        """Deactivate provisioning agent.

        Args:
            provisioning_agent (:py:class:`streamets.sdk.sch_models.ProvisioningAgent`):

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        return self.api_client.deactivate_components(org_id=self.organization,
                                                     components_json=[provisioning_agent.id])

    def activate_provisioning_agent(self, provisioning_agent):
        """Activate provisioning agent.

        Args:
            provisioning_agent (:py:class:`streamets.sdk.sch_models.ProvisioningAgent`):

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        return self.api_client.activate_components(org_id=self.organization,
                                                   components_json=[provisioning_agent.id])

    def delete_provisioning_agent_token(self, provisioning_agent):
        """Delete provisioning agent token.

        Args:
            provisioning_agent (:py:class:`streamets.sdk.sch_models.ProvisioningAgent`):

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        return self.api_client.delete_components(org_id=self.organization,
                                                 components_json=[provisioning_agent.id])

    @property
    def legacy_deployments(self):
        """Deployments.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.LegacyDeployments`.
        """
        return LegacyDeployments(self, self.organization)

    def get_legacy_deployment_builder(self):
        """Get a deployment builder instance with which a legacy deployment can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.LegacyDeploymentBuilder`.
        """
        deployment = {'name': None, 'description': None, 'labels': None, 'numInstances': None, 'spec': None,
                      'agentId': None}
        return LegacyDeploymentBuilder(dict(deployment))

    def add_legacy_deployment(self, deployment):
        """Add a legacy deployment.

        Args:
            deployment (:py:class:`streamsets.sdk.sch_models.LegacyDeployment`): Deployment object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        create_deployment_command = self.api_client.create_legacy_deployment(deployment._data)
        # Update :py:class:`streamsets.sdk.sch_models.LegacyDeployment` with updated Deployment metadata.
        deployment._data = create_deployment_command.response.json()
        deployment._control_hub = self
        return create_deployment_command

    def update_legacy_deployment(self, deployment):
        """Update a deployment.

        Args:
            deployment (:py:class:`streamsets.sdk.sch_models.LegacyDeployment`): Deployment object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        logger.info('Updating deployment %s ...', deployment)
        update_deployment_command = self.api_client.update_legacy_deployment(deployment_id=deployment.id,
                                                                             body=deployment._data)
        deployment._data = update_deployment_command.response.json()
        return update_deployment_command

    def scale_legacy_deployment(self, deployment, num_instances):
        """Scale up/down active deployment.

        Args:
            deployment (:py:class:`streamsets.sdk.sch_models.LegacyDeployment`): Deployment object.
            num_instances (:obj:`int`): Number of sdc instances.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        scale_deployment_command = self.api_client.scale_legacy_deployment(deployment_id=deployment.id,
                                                                           num_instances=num_instances)
        deployment._data = self.legacy_deployments.get(id=deployment.id)._data
        return scale_deployment_command

    def delete_legacy_deployment(self, *deployments):
        """Delete deployments.

        Args:
            *deployments: One or more instances of :py:class:`streamsets.sdk.sch_models.LegacyDeployment`.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        if len(deployments) == 1:
            logger.info('Deleting deployment %s ...', deployments[0])
            delete_deployment_command = self.api_client.delete_legacy_deployment(deployment_id=deployments[0].id)
        else:
            deployment_ids = [deployment.id for deployment in deployments]
            logger.info('Deleting deployments %s ...', deployment_ids)
            delete_deployment_command = self.api_client.delete_legacy_deployments(body=deployment_ids)
        return delete_deployment_command

    def start_legacy_deployment(self, deployment, **kwargs):
        """Start Deployment.

        Args:
            deployment (:py:class:`streamsets.sdk.sch_models.LegacyDeployment`): Deployment instance.
            wait (:obj:`bool`, optional): Wait for deployment to start. Default: ``True``.
            wait_for_statuses (:obj:`list`, optional): Deployment statuses to wait on. Default: ``['ACTIVE']``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.DeploymentStartStopCommand`.
        """
        provisioning_agent_id = deployment.provisioning_agent.id
        start_cmd = self.api_client.start_legacy_deployment(deployment.id, provisioning_agent_id)
        if kwargs.get('wait', True):
            start_cmd.wait_for_legacy_deployment_statuses(kwargs.get('wait_for_statuses', ['ACTIVE']))
        return start_cmd

    def stop_legacy_deployment(self, deployment, wait_for_statuses=['INACTIVE']):
        """Stop Deployment.

        Args:
            deployment (:py:class:`streamsets.sdk.sch_models.LegacyDeployment`): Deployment instance.
            wait_for_statuses (:obj:`list`, optional): List of statuses to wait for. Default: ``['INACTIVE']``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.DeploymentStartStopCommand`.
        """
        provisioning_agent_id = deployment.provisioning_agent.id
        stop_cmd = self.api_client.stop_legacy_deployment(deployment.id)
        if wait_for_statuses:
            stop_cmd.wait_for_legacy_deployment_statuses(wait_for_statuses)
        return stop_cmd

    def acknowledge_legacy_deployment_error(self, *deployments):
        """Acknowledge errors for one or more deployments.

        Args:
            *deployments: One or more instances of :py:class:`streamsets.sdk.sch_models.LegacyDeployment`.
        """
        deployment_ids = [deployment.id for deployment in deployments]
        logger.info('Acknowledging errors for deployment(s) %s ...', deployment_ids)
        self.api_client.legacy_deployments_acknowledge_errors(deployment_ids)

    def _get_update_executors_cache(self, executor_type):
        """Get or update the executors cache variables.

        Args:
            executor_type (:obj:`str`): Executor type.

        Returns:
            A :py:class:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.DataCollector` or
            :py:class:`streamsets.sdk.sch_models.Transformer` instances.
        """
        executors = self.api_client.get_all_registered_executors(organization=None,
                                                                 executor_type=executor_type,
                                                                 edge=None,
                                                                 label=None,
                                                                 version=None,
                                                                 offset=None,
                                                                 len_=None,
                                                                 order_by=None,
                                                                 order=None).response.json()
        executor_ids = {executor['id'] for executor in executors}

        if executor_type == 'COLLECTOR':
            local_executor_ids = set(self._data_collectors.keys())
        elif executor_type == 'TRANSFORMER':
            local_executor_ids = set(self._transformers.keys())
        if executor_ids - local_executor_ids:
            # Case where we have to add more DataCollector or Transformer instances
            ids_to_be_added = executor_ids - local_executor_ids
            # Doing an O(N^2) here because it is easy to do so and N is too small to consider time complexity.
            for executor in executors:
                for executor_id in ids_to_be_added:
                    if executor_id == executor['id']:
                        if executor_type == 'COLLECTOR':
                            self._data_collectors[executor_id] = DataCollector(executor, self)
                        elif executor_type == 'TRANSFORMER':
                            self._transformers[executor_id] = Transformer(executor, self)
        else:
            # This will handle both the cases when the set of ids are equal and local_executor_ids has more ids.
            ids_to_be_removed = local_executor_ids - executor_ids
            for executor_id in ids_to_be_removed:
                if executor_type == 'COLLECTOR':
                    del self._data_collectors[executor_id]
                elif executor_type == 'TRANSFORMER':
                    del self._transformers[executor_id]
        if executor_type == 'COLLECTOR':
            return SeekableList(self._data_collectors.values())
        elif executor_type == 'TRANSFORMER':
            return SeekableList(self._transformers.values())

    def deactivate_datacollector(self, data_collector):
        """Deactivate data collector.

         Args:
            data_collector (:py:class:`streamsets.sdk.sch_models.DataCollector`): Data Collector object.
        """
        logger.info('Deactivating data collector component from organization %s with component id %s ...',
                    self.organization, data_collector.id)
        self.api_client.deactivate_components(org_id=self.organization,
                                              components_json=[data_collector.id])

    def activate_datacollector(self, data_collector):
        """Activate data collector.

        Args:
            data_collector (:py:class:`streamsets.sdk.sch_models.DataCollector`): Data Collector object.
        """
        logger.info('Activating data collector component from organization %s with component id %s ...',
                    self.organization, data_collector.id)
        self.api_client.activate_components(org_id=self.organization,
                                            components_json=[data_collector.id])

    def delete_data_collector(self, data_collector):
        """Delete data collector.

        Args:
            data_collector (:py:class:`streamsets.sdk.sch_models.DataCollector`): Data Collector object.
        """
        logger.info('Deleting data dollector %s ...', data_collector.id)
        self.api_client.delete_sdc(data_collector_id=data_collector.id)

    def delete_and_unregister_data_collector(self, data_collector):
        """Delete and Unregister data collector.

        Args:
            data_collector (:py:class:`streamsets.sdk.sch_models.DataCollector`): Data Collector object.
        """
        logger.info('Deactivating data collector component from organization %s with component id %s ...',
                    data_collector.organization, data_collector.id)
        self.api_client.deactivate_components(org_id=self.organization,
                                              components_json=[data_collector.id])
        logger.info('Deleting data collector component from organization %s with component id %s ...',
                    data_collector.organization, data_collector.id)
        self.api_client.delete_components(org_id=self.organization,
                                          components_json=[data_collector.id])
        logger.info('Deleting data dollector from jobrunner %s ...', data_collector.id)
        self.api_client.delete_sdc(data_collector_id=data_collector.id)

    def update_data_collector_labels(self, data_collector):
        """Update data collector labels.

        Args:
            data_collector (:py:class:`streamsets.sdk.sch_models.DataCollector`): Data Collector object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.DataCollector`.
        """
        logger.info('Updating data collector %s with labels %s ...',
                    data_collector.id, data_collector.labels)
        return DataCollector(self.api_client.update_sdc_labels(
            data_collector_id=data_collector.id,
            data_collector_json=data_collector._data).response.json(), self)

    def get_data_collector_labels(self, data_collector):
        """Returns all labels assigned to data collector.

        Args:
            data_collector (:py:class:`streamsets.sdk.sch_models.DataCollector`): Data Collector object.

        Returns:
            A :obj:`list` of data collector assigned labels.
        """
        logger.info('Getting assigned labels for data collector %s ...', data_collector.id)
        return self.api_client.get_sdc_lables(data_collector_id=data_collector.id).response.json()

    def update_data_collector_resource_thresholds(self, data_collector, max_cpu_load=None, max_memory_used=None,
                                                  max_pipelines_running=None):
        """Updates data collector resource thresholds.

        Args:
            data_collector (:py:class:`streamsets.sdk.sch_models.DataCollector`): Data Collector object.
            max_cpu_load (:obj:`float`, optional): Max CPU load in percentage. Default: ``None``.
            max_memory_used (:obj:`int`, optional): Max memory used in MB. Default: ``None``.
            max_pipelines_running (:obj:`int`, optional): Max pipelines running. Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        thresholds = {'maxMemoryUsed': max_memory_used,
                      'maxCpuLoad': max_cpu_load,
                      'maxPipelinesRunning': max_pipelines_running}
        thresholds_to_be_updated = {k: v for k, v in thresholds.items() if v is not None}
        data_collector_json = data_collector._data
        data_collector_json.update(thresholds_to_be_updated)
        cmd = self.api_client.update_sdc_resource_thresholds(data_collector.id, data_collector_json)
        data_collector._refresh()
        return cmd

    def balance_data_collectors(self, *data_collectors):
        """Balance all jobs running on given Data Collectors.

        Args:
            *sdcs: One or more instances of :py:class:`streamsets.sdk.sch_models.DataCollector`.
        """
        data_collector_ids = [data_collector.id for data_collector in data_collectors]
        logger.info('Balancing all jobs on Data Collector(s) %s ...', data_collector_ids)
        self.api_client.balance_data_collectors(data_collector_ids)

    def delete_unregistered_auth_tokens(self, executor_type):
        """Delete auth tokens for engines that have been unregistered.

        Args:
            executor_type (:obj:`str`): The executor type. Acceptable values are 'DATACOLLECTOR' or 'TRANSFORMER'.
        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        return self.api_client.delete_non_registered_components(self.organization, executor_type)

    def shutdown_engines(self, *engines):
        """Call shutdown on the given engine(s).

        Args:
            *engines: One or more instances of :py:class:`streamsets.sdk.sch_models.DataCollector` or
                :py:class:`streamsets.sdk.sch_models.Transformer`.
        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        engine_ids = [engine.id for engine in engines]
        return self.api_client.shutdown_deployment_engines(engine_ids)

    def restart_engines(self, *engines):
        """Restart the given engine(s).

        Args:
            *engines:  One or more instances of :py:class:`streamsets.sdk.sch_models.DataCollector` or
                :py:class:`streamsets.sdk.sch_models.Transformer`.
        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        engine_ids = [engine.id for engine in engines]
        return self.api_client.restart_deployment_engines(engine_ids)

    def get_job_builder(self):
        """Get a job builder instance with which a job can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.JobBuilder`.
        """
        job = {property: None
               for property in self._job_api['definitions']['JobJson']['properties']}

        # Set other properties based on defaults from the web UI.
        JOB_DEFAULTS = {'forceStopTimeout': 120000,
                        'labels': ['all'],
                        'numInstances': 1,
                        'statsRefreshInterval': 60000,
                        'rawJobTags': []}
        job.update(JOB_DEFAULTS)
        return JobBuilder(job=job, control_hub=self)

    def get_components(self, component_type_id, offset=None, len_=None, order_by='LAST_VALIDATED_ON', order='ASC'):
        """Get components.

        Args:
            component_type_id (:obj:`str`): Component type id.
            offset (:obj:`str`, optional): Default: ``None``.
            len_ (:obj:`str`, optional): Default: ``None``.
            order_by (:obj:`str`, optional): Default: ``'LAST_VALIDATED_ON'``.
            order (:obj:`str`, optional): Default: ``'ASC'``.
        """
        return self.api_client.get_components(org_id=self.organization,
                                              component_type_id=component_type_id,
                                              offset=offset,
                                              len=len_,
                                              order_by=order_by,
                                              order=order)

    def create_components(self, component_type, number_of_components=1, active=True):
        """Create components.

        Args:
            component_type (:obj:`str`): Component type.
            number_of_components (:obj:`int`, optional): Default: ``1``.
            active (:obj:`bool`, optional): Default: ``True``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.CreateComponentsCommand`.
        """
        return self.api_client.create_components(org_id=self.organization,
                                                 component_type=component_type,
                                                 number_of_components=number_of_components,
                                                 active=active)

    def get_organization_builder(self):
        """Get an organization builder instance with which an organization can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.OrganizationBuilder`.
        """
        organization = {property: None
                        for property in self._security_api['definitions']['NewOrganizationJson']['properties']}

        # Set other properties based on defaults from the web UI.
        organization_defaults = {'active': True,
                                 'passwordExpiryTimeInMillis': 5184000000,  # 60 days
                                 'validDomains': '*'}
        organization_admin_user_defaults = {'active': True,
                                            'roles': ['user',
                                                      'org-admin',
                                                      'datacollector:admin',
                                                      'pipelinestore:pipelineEditor',
                                                      'jobrunner:operator',
                                                      'timeseries:reader',
                                                      'timeseries:writer',
                                                      'topology:editor',
                                                      'notification:user',
                                                      'sla:editor',
                                                      'provisioning:operator']}
        organization['organization'] = organization_defaults
        organization['organizationAdminUser'] = organization_admin_user_defaults

        return OrganizationBuilder(organization=organization['organization'],
                                   organization_admin_user=organization['organizationAdminUser'])

    def add_organization(self, organization):
        """Add an organization.

        Args:
            organization (:py:obj:`streamsets.sdk.sch_models.Organization`): Organization object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        logger.info('Adding organization %s ...', organization.name)
        body = {'organization': organization._data,
                'organizationAdminUser': organization._organization_admin_user}
        create_organization_command = self.api_client.create_organization(body)
        organization._data = create_organization_command.response.json()
        return create_organization_command

    def update_organization(self, organization):
        """Update an organization.

        Args:
            organization (:py:obj:`streamsets.sdk.sch_models.Organization`): Organization instance.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        logger.info('Updating organization %s ...', organization.name)
        update_organization_command = self.api_client.update_organization(org_id=organization.id,
                                                                          body=organization._data)
        organization._data = update_organization_command.response.json()
        return update_organization_command

    @property
    def organizations(self):
        """Organizations.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Organizations`.
        """
        return Organizations(self)

    @property
    def api_credentials(self):
        """Api Credentials.

        Returns:
            A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.ApiCredential`.
        """
        return ApiCredentials(self)

    def get_api_credential_builder(self):
        """Get api credential Builder.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ApiCredentialBuilder`.
        """
        api_credential = {property: None
                          for property in self._security_api['definitions']['ApiCredentialsJson']['properties']}
        api_credential.pop('authToken')
        api_credential.pop('componentId')
        api_credential.pop('userId')
        return ApiCredentialBuilder(api_credential=api_credential, control_hub=self)

    def add_api_credential(self, api_credential):
        """Add an api credential. Some api credential attributes are updated by ControlHub such as
            created_by.

        Args:
            api_credential (:py:class:`streamsets.sdk.sch_models.ApiCredential`): ApiCredential object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        logger.info('Adding an api credential %s ...', api_credential.name)
        create_api_credential_command = self.api_client.create_api_user_credential(self.organization,
                                                                                   api_credential._data)
        # Update :py:class:`streamsets.sdk.sch_models.ApiCredential` with updated ApiCredential metadata.
        api_credential._data = create_api_credential_command.response.json()

        return create_api_credential_command

    def regenerate_api_credential_auth_token(self, api_credential):
        """Regenerate the auth token for an api credential.

        Args:
            api_credential (:py:class:`streamsets.sdk.sch_models.ApiCredential`): ApiCredential object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        api_credential.generate_auth_token = True
        return self._update_api_credential(api_credential).response.json()

    def rename_api_credential(self, api_credential):
        """Rename an api credential.

        Args:
            api_credential (:py:class:`streamsets.sdk.sch_models.ApiCredential`): ApiCredential object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        api_credential.generate_auth_token = False
        return self._update_api_credential(api_credential)

    def _update_api_credential(self, api_credential):
        """Update an api credential.

        Args:
            api_credential (:py:class:`streamsets.sdk.sch_models.ApiCredential`): ApiCredential object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        logger.info('Updating an api credential %s ...', api_credential)
        current_api_credential = copy.deepcopy(api_credential._data)
        credential_id = api_credential.credential_id
        current_api_credential.pop('authToken')
        current_api_credential.pop('componentId')
        current_api_credential.pop('userId')

        data = current_api_credential
        create_api_credential_command = self.api_client.update_api_user_credential(org_id=self.organization,
                                                                                   credential_id=credential_id,
                                                                                   api_user_credential_json=data)
        api_credential._data = create_api_credential_command.response.json()
        return create_api_credential_command

    def activate_api_credential(self, api_credential):
        """Activate an api credential.

        Args:
            api_credential (:py:class:`streamsets.sdk.sch_models.ApiCredential`): ApiCredential object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        api_credential.generate_auth_token = False
        api_credential.active = True
        return self._update_api_credential(api_credential)

    def deactivate_api_credential(self, api_credential):
        """Deactivate an api credential.

        Args:
            api_credential (:py:class:`streamsets.sdk.sch_models.ApiCredential`): ApiCredential object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        api_credential.generate_auth_token = False
        api_credential.active = False
        return self._update_api_credential(api_credential)

    def delete_api_credentials(self, *api_credentials):
        """Delete api_credentials.

        Args:
            *api_credentials: One or more instances of :py:class:`streamsets.sdk.sch_models.ApiCredential`.
        """
        for api_credential in api_credentials:
            logger.info('Deleting api credential %s ...', api_credential)
            self.api_client.delete_api_user_credential(org_id=self.organization,
                                                       credential_id=api_credential.credential_id)

    @property
    def pipelines(self):
        """Pipelines.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Pipelines`.
        """
        return Pipelines(self, self.organization)

    def import_pipelines_from_archive(self, archive, commit_message, fragments=False):
        """Import pipelines from archived zip directory.

        Args:
            archive (:obj:`file`): file containing the pipelines.
            commit_message (:obj:`str`): Commit message.
            fragments (:obj:`bool`, optional): Indicates if pipeline contains fragments.

        Returns:
            A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.Pipeline`.
        """
        return SeekableList([Pipeline(pipeline,
                                      builder=None,
                                      pipeline_definition=json.loads(pipeline['pipelineDefinition']),
                                      rules_definition=json.loads(pipeline['currentRules']['rulesDefinition']),
                                      control_hub=self)
                             for pipeline in self.api_client.import_pipelines(commit_message=commit_message,
                                                                              pipelines_file=archive,
                                                                              fragments=fragments).response.json()])

    def import_pipeline(self, pipeline, commit_message, name=None, data_collector_instance=None):
        """Import pipeline from json file.

        Args:
            pipeline (:obj:`dict`): A python dict representation of ControlHub Pipeline.
            commit_message (:obj:`str`): Commit message.
            name (:obj:`str`, optional): Name of the pipeline. If left out, pipeline name from JSON object will be
                                         used. Default ``None``.
            data_collector_instance (:py:class:`streamsets.sdk.sch_models.DataCollector`): If excluded, system sdc will
                                                                                           be used. Default ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Pipeline`.
        """
        if name is None:
            name = pipeline['pipelineConfig']['title']
        sdc_id = data_collector_instance.id if data_collector_instance is not None else DEFAULT_SYSTEM_SDC_ID
        pipeline['pipelineConfig']['info']['sdcId'] = sdc_id
        commit_pipeline_json = {'name': name,
                                'commitMessage': commit_message,
                                'pipelineDefinition': json.dumps(pipeline['pipelineConfig']),
                                'libraryDefinitions': json.dumps(pipeline['libraryDefinitions']),
                                'rulesDefinition': json.dumps(pipeline['pipelineRules']),
                                'sdcId': sdc_id}
        commit_pipeline_response = self.api_client.commit_pipeline(new_pipeline=False,
                                                                   import_pipeline=True,
                                                                   body=commit_pipeline_json).response.json()
        commit_id = commit_pipeline_response['commitId']
        return self.pipelines.get(commit_id=commit_id)

    def export_pipelines(self, pipelines, fragments=False, include_plain_text_credentials=False):
        """Export pipelines.

        Args:
            pipelines (:obj:`list`): A list of :py:class:`streamsets.sdk.sch_models.Pipeline` instances.
            fragments (:obj:`bool`): Indicates if exporting fragments is needed.
            include_plain_text_credentials (:obj:`bool`): Indicates if plain text credentials should be included.

        Returns:
            An instance of type :py:obj:`bytes` indicating the content of zip file with pipeline json files.
        """
        commit_ids = [pipeline.commit_id for pipeline in pipelines]
        return (self.api_client.export_pipelines(body=commit_ids,
                                                 fragments=fragments,
                                                 include_plain_text_credentials=include_plain_text_credentials)
                .response.content)

    @property
    def jobs(self):
        """Jobs.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Jobs`.
        """
        return Jobs(self)

    @property
    def data_protector_enabled(self):
        """:obj:`bool`: Whether Data Protector is enabled for the current organization."""
        add_ons = self.api_client.get_available_add_ons().response.json()
        logger.debug('Add-ons: %s', add_ons)
        return all(app in add_ons['enabled'] for app in ['policy', 'sdp_classification'])

    @property
    def connection_tags(self):
        """Connection Tags.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ConnectionTags`.
        """
        return ConnectionTags(control_hub=self, organization=self.organization)

    @property
    def alerts(self):
        """Alerts.

        Returns:
            A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.Alert`.
        """
        # The SCH API requires fetching active and acknowledged alerts separately. As such we make two calls for each
        # of the active/acknowledged endpoints, combine them and sort chronologically by 'triggeredOn'.
        active_alerts = self.api_client.get_all_alerts(alert_status='ACTIVE').response.json()
        acknowledged_alerts = self.api_client.get_all_alerts(alert_status='ACKNOWLEDGED').response.json()

        return SeekableList(Alert(alert, control_hub=self) for alert in sorted(active_alerts + acknowledged_alerts,
                                                                               key=lambda x: x['triggeredOn']))

    def add_job(self, job):
        """Add a job.

        Args:
            job (:py:class:`streamsets.sdk.sch_models.Job`): Job object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        new_job_json = {property_: value
                        for property_, value in job._data.items()
                        if property_ in self._job_api['definitions']['NewJobJson']['properties']}
        logger.info('Adding job %s ...', job.job_name)
        create_job_command = self.api_client.create_job(body=new_job_json)
        # Update :py:class:`streamsets.sdk.sch_models.Job` with updated Job metadata.
        job._data = create_job_command.response.json()

        if self.data_protector_enabled:
            policies = dict(jobId=job.job_id)
            if job.read_policy:
                policies['readPolicyId'] = job.read_policy._id
            else:
                read_protection_policies = self._get_protection_policies('Read')
                if len(read_protection_policies) == 1:
                    logger.warning('Read protection policy not set for job (%s). Setting to %s ...',
                                   job.job_name,
                                   read_protection_policies[0].name)
                    policies['readPolicyId'] = read_protection_policies[0]._id
                else:
                    raise Exception('Read policy not selected.')

            if job.write_policy:
                policies['writePolicyId'] = job.write_policy._id
            else:
                write_protection_policies = self._get_protection_policies('Write')
                if len(write_protection_policies) == 1:
                    logger.warning('Write protection policy not set for job (%s). Setting to %s ...',
                                   job.job_name,
                                   write_protection_policies[0].name)
                    policies['writePolicyId'] = write_protection_policies[0]._id
                else:
                    raise Exception('Write policy not selected.')
            self.api_client.update_job_policies(body=policies)
        return create_job_command

    def edit_job(self, job):
        """Edit a job.

        Args:
            job (:py:class:`streamsets.sdk.sch_models.Job`): Job object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        logger.warning('This method has been superseded by update_job and will be removed in a future release.')
        logger.info('Editing job %s with job id %s ...', job.job_name, job.job_id)
        return Job(self.api_client.update_job(job_id=job.job_id, job_json=job._data).response.json())

    def update_job(self, job):
        """Update a job.

        Args:
            job (:py:class:`streamsets.sdk.sch_models.Job`): Job object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        logger.info('Updating job %s with job id %s ...', job.job_name, job.job_id)
        return Job(self.api_client.update_job(job_id=job.job_id, job_json=job._data).response.json())

    def upgrade_job(self, *jobs):
        """Upgrade job(s) to latest pipeline version.

        Args:
            *jobs: One or more instances of :py:class:`streamsets.sdk.sch_models.Job`.

        Returns:
            A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        job_ids = [job.job_id for job in jobs]
        self.api_client.upgrade_jobs(job_ids)
        return SeekableList(self.jobs.get(id=job_id) for job_id in job_ids)

    def import_jobs(self, archive, pipeline=True, number_of_instances=False, labels=False, runtime_parameters=False,
                    **kwargs):
        # update_migrate_offsets is not configurable through UI and is supported through kwargs.
        """Import jobs from archived zip directory.

        Args:
            archive (:obj:`file`): file containing the jobs.
            pipeline (:obj:`boolean`, optional): Indicate if pipeline should be imported. Default: ``True``.
            number_of_instances (:obj:`boolean`, optional): Indicate if number of instances should be imported.
                                                            Default: ``False``.
            labels (:obj:`boolean`, optional): Indicate if labels should be imported. Default: ``False``.
            runtime_parameters (:obj:`boolean`, optional): Indicate if runtime parameters should be imported.
                                                           Default: ``False``.

        Returns:
            A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        return SeekableList([Job(job['minimalJobJson'], control_hub=self)
                             for job in self.api_client.import_jobs(jobs_file=archive,
                                                                    update_pipeline_refs=pipeline,
                                                                    update_num_instances=number_of_instances,
                                                                    update_labels=labels,
                                                                    update_runtime_parameters=runtime_parameters,
                                                                    **kwargs).response.json()])

    def export_jobs(self, jobs):
        """Export jobs to a compressed archive.

        Args:
            jobs (:obj:`list`): A list of :py:class:`streamsets.sdk.sch_models.Job` instances.

        Returns:
            An instance of type :py:obj:`bytes` indicating the content of zip file with job json files.
        """
        job_ids = [job.job_id for job in jobs]
        return self.api_client.export_jobs(body=job_ids).response.content

    def reset_origin(self, *jobs):
        # It is called reset_origin instead of reset_offset in the UI because that is how sdc calls it. If we change it
        # to reset_offset in sdc, it would affect a lot of people.
        """Reset all pipeline offsets for given jobs.

        Args:
            *jobs: One or more instances of :py:class:`streamsets.sdk.sch_models.Job`.

        Returns:
            A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        job_ids = [job.job_id for job in jobs]
        self.api_client.reset_jobs_offset(job_ids)
        return SeekableList(self.jobs.get(id=job_id) for job_id in job_ids)

    def upload_offset(self, job, offset_file=None, offset_json=None):
        """Upload offset for given job.

        Args:
            job (:py:class:`streamsets.sdk.sch_models.Job`): Job object.
            offset_file (:obj:`file`, optional): File containing the offsets. Default: ``None``. Exactly one of
                                                 ``offset_file``, ``offset_json`` should specified.
            offset_json (:obj:`dict`, optional): Contents of offset. Default: ``None``. Exactly one of ``offset_file``,
                                                 ``offset_json`` should specified.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        # Comparing with None because, {} is also an accepted offset.
        if offset_file and offset_json is not None:
            raise ValueError("Cannot specify both the arguments offset_file and offset_json at the same time.")
        if not offset_file and offset_json is None:
            raise ValueError("Exactly one of the arguments offset_file and offset_json should be specified.")
        if offset_json is not None:
            job_json = self.api_client.upload_job_offset_as_json(job.job_id, offset_json).response.json()
        else:
            job_json = self.api_client.upload_job_offset(job.job_id, offset_file).response.json()
        return Job(job_json, self)

    def get_current_job_status(self, job):
        """Returns the current job status for given job id.

        Args:
            job (:py:class:`streamsets.sdk.sch_models.Job`): Job object.
        """
        logger.info('Fetching job status for job id %s ...', job.job_id)
        return self.api_client.get_current_job_status(job_id=job.job_id)

    def delete_job(self, *jobs):
        """Delete one or more jobs.

        Args:
            *jobs: One or more instances of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        job_ids = [job.job_id for job in jobs]
        logger.info('Deleting job(s) %s ...', job_ids)
        if len(job_ids) == 1:
            try:
                api_version = 2 if '/v2/job/{jobId}' in self._job_api['paths'] else 1
            except:
                # Ignore any improper swagger setup and fall back to default version in case of any errors
                api_version = 1
            self.api_client.delete_job(job_ids[0], api_version=api_version)
        else:
            self.api_client.delete_jobs(job_ids)

    def start_job(self, *jobs, wait=True, **kwargs):
        """Start one or more jobs.

        Args:
            *jobs: One or more instances of :py:class:`streamsets.sdk.sch_models.Job`.
            wait (:obj:`bool`, optional): Wait for pipelines to reach RUNNING status before returning.
                Default: ``True``.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.StartJobsCommand`.
        """
        # Preserve compatibility with previous 'wait_for_data_collectors' argument
        wait_for_data_collectors = kwargs.get('wait_for_data_collectors')
        if wait_for_data_collectors is not None:
            warnings.warn('The wait_for_data_collectors argument to ControlHub.start_job will be removed in a '
                          'future release. Please use wait argument instead.',
                          DeprecationWarning)
            wait = wait_for_data_collectors

        job_names = [job.job_name for job in jobs]
        logger.info('Starting %s (%s) ...', 'jobs' if len(job_names) > 1 else 'job', ', '.join(job_names))

        job_ids = [job.job_id for job in jobs]
        start_jobs_command = self.api_client.start_jobs(job_ids)
        # The startJobs endpoint in ControlHub returns an OK with no other data in the body. As such, we add
        #  the list of jobs passed to this method as an attribute to the StartJobsCommand returned by
        # :py:method:`streamsets.sdk.sch_api.ApiClient.start_jobs`.
        start_jobs_command.jobs = jobs

        if wait:
            start_jobs_command.wait_for_pipelines()
        return start_jobs_command

    def start_job_template(self, job_template, name=None, description=None, attach_to_template=True,
                           delete_after_completion=False, instance_name_suffix='COUNTER', number_of_instances=1,
                           parameter_name=None, raw_job_tags=None, runtime_parameters=None,
                           wait_for_data_collectors=False):
        """Start Job instances from a Job Template.

        Args:
            job_template (:py:class:`streamsets.sdk.sch_models.Job`): A Job instance with the property job_template set
                                                                      to ``True``.
            name (:obj:`str`, optional): Name of the new job(s). Default: ``None``. If not specified, name of the job
                                         template with ``' copy'`` appended to the end will be used.
            description (:obj:`str`, optional): Description for new job(s). Default: ``None``.
            attach_to_template (:obj:`bool`, optional): Default: ``True``.
            delete_after_completion (:obj:`bool`, optional): Default: ``False``.
            instance_name_suffix (:obj:`str`, optional): Suffix to be used for Job names in
                                                         {'COUNTER', 'TIME_STAMP', 'PARAM_VALUE'}. Default: ``COUNTER``.
            number_of_instances (:obj:`int`, optional): Number of instances to be started using given parameters.
                                                        Default: ``1``.
            parameter_name (:obj:`str`, optional): Specified when instance_name_suffix is 'PARAM_VALUE'.
                                                   Default: ``None``.
            raw_job_tags (:obj:`list`, optional): Default: ``None``.
            runtime_parameters (:obj:`dict`) or (:obj:`list`): Runtime Parameters to be used in the jobs. If a dict is
                                                               specified, ``number_of_instances`` jobs will be started.
                                                               If a list is specified, ``number_of_instances`` is
                                                               ignored and job instances will be started using the
                                                               elements of the list as Runtime Parameters for each job.
                                                               If left out, Runtime Parameters from Job Template will be
                                                               used. Default: ``None``.
            wait_for_data_collectors (:obj:`bool`, optional): Default: ``False``.

        Returns:
            A :py:class:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.Job` instances.
        """
        assert job_template.job_template, "Please specify a Job Template instance."
        if instance_name_suffix == 'PARAM_VALUE':
            assert parameter_name is not None, "Please specify a parameter name."

        start_job_template_json = {property: None
                                   for property in
                                   self._job_api['definitions']['JobTemplateCreationInfoJson']['properties']}

        if runtime_parameters is None:
            runtime_parameters = job_template.runtime_parameters._data
        if isinstance(runtime_parameters, dict):
            runtime_parameters = [runtime_parameters] * number_of_instances

        start_job_template_json.update({'attachToTemplate': attach_to_template,
                                        'deleteAfterCompletion': delete_after_completion,
                                        'description': description,
                                        'name': name,
                                        'namePostfixType': instance_name_suffix,
                                        'paramName': parameter_name,
                                        'rawJobTags':raw_job_tags,
                                        'runtimeParametersList': runtime_parameters
                                        })
        jobs_reponse = self.api_client.create_and_start_job_instances(job_template.job_id, start_job_template_json)

        jobs = SeekableList()
        for job_response in jobs_reponse.response.json():
            job = self.jobs.get(id=job_response['jobId'])
            self.api_client.wait_for_job_status(job_id=job.job_id, status='ACTIVE')
            if wait_for_data_collectors:
                def job_has_data_collector(job):
                    job.refresh()
                    job_data_collectors = job.data_collectors
                    logger.debug('Job Data Collectors: %s', job_data_collectors)
                    return len(job_data_collectors) > 0
                wait_for_condition(job_has_data_collector, [job], timeout=120)
            job.refresh()
            jobs.append(job)

        return jobs

    def stop_job(self, *jobs, force=False, timeout_sec=300):
        """Stop one or more jobs.

        Args:
            *jobs: One or more instances of :py:class:`streamsets.sdk.sch_models.Job`.
            force (:obj:`bool`, optional): Force job to stop. Default: ``False``.
            timeout_sec (:obj:`int`, optional): Timeout in secs. Default: ``300``.
        """
        jobs_ = {job.job_id: job for job in jobs}
        job_ids = list(jobs_.keys())
        logger.info('Stopping job(s) %s ...', job_ids)
        # At the end, we'll return the command from the job being stopped, so we hold onto it while we update
        # the underlying :py:class:`streamsets.sdk.sch_models.Job` instances.
        stop_jobs_command = self.api_client.force_stop_jobs(job_ids) if force else self.api_client.stop_jobs(job_ids)

        job_inactive_error = None
        for job_id in job_ids:
            try:
                self.api_client.wait_for_job_status(job_id=job_id, status='INACTIVE', timeout_sec=timeout_sec)
            except JobInactiveError as ex:
                job_inactive_error = ex
        updated_jobs = self.api_client.get_jobs(body=job_ids).response.json()
        for updated_job in updated_jobs:
            job_id = updated_job['id']
            jobs_[job_id]._data = updated_job
        if job_inactive_error:
            raise job_inactive_error
        return stop_jobs_command

    def get_protection_policy_builder(self):
        """Get a protection policy builder instance with which a protection policy can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ProtectionPolicyBuilder`.
        """
        protection_policy = self.api_client.get_new_protection_policy().response.json()['response']['data']
        protection_policy.pop('messages', None)
        id_ = protection_policy['id']

        policy_procedure = self.api_client.get_new_policy_procedure(id_).response.json()['response']['data']
        policy_procedure.pop('messages', None)
        return ProtectionPolicyBuilder(self, protection_policy, policy_procedure)

    def get_protection_method_builder(self):
        """Get a protection method builder instance with which a protection method can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ProtectionMethodBuilder`.
        """
        return ProtectionMethodBuilder(self.get_pipeline_builder())

    def get_classification_rule_builder(self):
        """Get a classification rule builder instance with which a classification rule can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ClassificationRuleBuilder`.
        """
        classification_rule = self.api_client.get_new_classification_rule(
            self._classification_catalog_id
        ).response.json()['response']['data']
        # Remove 'messages' from the classification rule JSON.
        classification_rule.pop('messages', None)
        classifier = self.api_client.get_new_classification_classifier(
            self._classification_catalog_id
        ).response.json()['response']['data']
        # Remove 'messages' from the classifier JSON.
        classifier.pop('messages', None)
        return ClassificationRuleBuilder(classification_rule, classifier)

    @property
    def _classification_catalog_id(self):
        """Get the classification catalog id for the org.

        Returns:
            An instance of :obj:`str`:.
        """
        classification_catalog_list_response = self.api_client.get_classification_catalog_list().response.json()
        # We assume it's the first (and only) classification catalog id for the org
        return classification_catalog_list_response['response'][0]['data']['id']

    def add_protection_policy(self, protection_policy):
        """Add a protection policy.

        Args:
            protection_policy (:py:obj:`streamsets.sdk.sch_models.ProtectionPolicy`): Protection Policy object.
        """
        protection_policy._id = self.api_client.create_protection_policy(
            {'data': protection_policy._data}
        ).response.json()['response']['data']['id']
        for procedure in protection_policy.procedures:
            new_policy_procedure = self.api_client.get_new_policy_procedure(
                protection_policy._id
            ).response.json()['response']['data']
            procedure._id = new_policy_procedure['id']
            procedure._policy_id = protection_policy._id
            self.api_client.create_policy_procedure({'data': procedure._data})

    def set_default_write_protection_policy(self, protection_policy):
        """Set a default write protection policy.

        Args:
            protection_policy
            (:py:obj:`streamsets.sdk.sch_models.ProtectionPolicy`): Protection
            Policy object to be set as the default write policy.

        Returns:
            An updated instance of :py:obj:`streamsets.sdk.sch_models.ProtectionPolicy`.

        """
        policy_id = protection_policy._data['id']
        self.api_client.set_default_write_protection_policy(policy_id)
        # Once the policy is updated, the local copy needs to be refreshed.
        # The post call itself doesn't return the latest data, so need to do
        # another lookup.  This mimics the UI in its behavior.
        return self.protection_policies.get(_id=policy_id)

    def set_default_read_protection_policy(self, protection_policy):
        """Set a default read protection policy.

        Args:
            protection_policy
            (:py:obj:`streamsets.sdk.sch_models.ProtectionPolicy`): Protection
            Policy object to be set as the default read policy.

        Returns:
            An updated instance of :py:obj:`streamsets.sdk.sch_models.ProtectionPolicy`.
        """
        policy_id = protection_policy._data['id']
        self.api_client.set_default_read_protection_policy(policy_id)
        # Once the policy is updated, the local copy needs to be refreshed.
        # The post call itself doesn't return the latest data, so need to do
        # another lookup.  This mimics the UI in its behavior.
        return self.protection_policies.get(_id=policy_id)

    def export_protection_policies(self, protection_policies):
        """Export protection policies to a compressed archive.

        Args:
            protection_policies (:obj:`list`): A list of :py:class:`streamsets.sdk.sch_models.ProtectionPolicy`
            instances.

        Returns:
            An instance of type :py:obj:`bytes` indicating the content of zip file with protection policy json files.
        """
        policy_ids = [policy._id for policy in protection_policies]
        return self.api_client.export_protection_policies(policy_ids=policy_ids).response.content

    def import_protection_policies(self, policies_archive):
        """Import protection policies from a compressed archive.

        Args:
            policies_archive (:obj:`file`): file containing the protection policies.

        Returns:
            A py:class:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.ProtectionPolicy`.
        """
        policies = self.api_client.import_protection_policies(policies_archive).response.json()['response']
        return SeekableList([ProtectionPolicy(policy['data']) for policy in policies])

    @property
    def protection_policies(self):
        """Protection policies.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ProtectionPolicies`.
        """
        return ProtectionPolicies(self)

    def validate_pipeline(self, pipeline):
        """Validate pipeline. Only Transformer for Snowflake pipelines are supported at this time.

        Args:
            pipeline (:py:obj:`streamsets.sdk.sch_models.Pipeline`): Pipeline instance.

        Raises:
            :py:obj:`streamsets.sdk.exceptions.ValidationError`: If validation fails.
            :py:obj:`NotImplementedError`: If used for a pipeline that isn't a Transformer for Snowflake pipeline.
        """
        if pipeline.executor_type != 'SNOWPARK':
            raise NotImplementedError('This method is currently only implemented for '
                                      'Transformer for Snowflake pipelines')
        _, engine_pipeline_id = self._add_pipeline_to_executor_if_not_exists(pipeline)
        validate_command = self.api_client.validate_snowflake_pipeline(engine_pipeline_id, timeout=500000).wait_for_validate()
        response = validate_command.response.json()
        if response['status'] != 'VALID':
            if response.get('issues'):
                raise ValidationError(response['issues'])
            elif response.get('message'):
                raise ValidationError(response['message'])
            else:
                raise ValidationError('Unknown validation failure with status as {}'.format(response['status']))

    def run_pipeline_preview(self, pipeline, batches=1, batch_size=10, skip_targets=True,
                             skip_lifecycle_events=True, timeout=120000, test_origin=False,
                             read_policy=None, write_policy=None, executor=None, **kwargs):
        """Run pipeline preview.

        Args:
            pipeline (:py:obj:`streamsets.sdk.sch_models.Pipeline`): Pipeline object.
            batches (:obj:`int`, optional): Number of batches. Default: ``1``.
            batch_size (:obj:`int`, optional): Batch size. Default: ``10``.
            skip_targets (:obj:`bool`, optional): Skip targets. Default: ``True``.
            skip_lifecycle_events (:obj:`bool`, optional): Skip life cycle events. Default: ``True``.
            timeout (:obj:`int`, optional): Timeout. Default: ``120000``.
            test_origin (:obj:`bool`, optional): Test origin. Default: ``False``.
            read_policy (:py:obj:`streamsets.sdk.sch_models.ProtectionPolicy`): Read Policy for preview.
                If not provided, uses default read policy if one available. Default: ``None``.
            write_policy (:py:obj:`streamsets.sdk.sch_models.ProtectionPolicy`): Write Policy for preview.
                If not provided, uses default write policy if one available. Default: ``None``.
            executor (:py:obj:`streamsets.sdk.sch_models.DataCollector`, optional): The Data Collector
                in which to preview the pipeline. If omitted, ControlHub's first executor SDC will be used.
                Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sdc_api.PreviewCommand`.
        """
        # Note: We only support SDC and Snowflake executor for now
        # Note: system data collector cannot be used for pipeline preview
        executor_type = getattr(pipeline, 'executor_type', 'COLLECTOR')
        if executor_type != SNOWFLAKE_EXECUTOR_TYPE and not executor and len(self.data_collectors) < 1:
            raise Exception('No executor found')
        else:
            if self.data_protector_enabled:
                executor_instance = (executor or self.data_collectors[0])._instance
                if not read_policy:
                    read_protection_policies = self._get_protection_policies('Read')
                    if len(read_protection_policies) == 1:
                        read_policy_id = read_protection_policies[0].id
                    else:
                        raise Exception('Read policy not selected.')
                else:
                    read_policy_id = read_policy.id

                if not write_policy:
                    write_protection_policies = self._get_protection_policies('Write')
                    if len(write_protection_policies) == 1:
                        write_policy_id = write_protection_policies[0].id
                    else:
                        raise Exception('Write policy not selected.')
                else:
                    write_policy_id = write_policy.id

                parameters = {
                    'pipelineCommitId': pipeline.commit_id,
                    'pipelineId': pipeline.pipeline_id,
                    'read.policy.id': read_policy_id,
                    'write.policy.id': write_policy_id,
                    'classification.catalogId': self._classification_catalog_id,
                }
                return executor_instance.run_dynamic_pipeline_preview(type='PROTECTION_POLICY',
                                                                      parameters=parameters,
                                                                      batches=batches,
                                                                      batch_size=batch_size,
                                                                      skip_targets=skip_targets,
                                                                      skip_lifecycle_events=skip_lifecycle_events,
                                                                      timeout=timeout,
                                                                      test_origin=test_origin)
            else:
                executor_instance, executor_pipeline_id = self._add_pipeline_to_executor_if_not_exists(pipeline)
                if executor_instance:
                    return executor_instance.run_pipeline_preview(pipeline_id=executor_pipeline_id,
                                                                  batches=batches,
                                                                  batch_size=batch_size,
                                                                  skip_targets=skip_targets,
                                                                  timeout=timeout,
                                                                  test_origin=test_origin,
                                                                  wait=kwargs.get('wait', True))
                else:
                    return self.run_snowflake_pipeline_preview(pipeline_id=executor_pipeline_id,
                                                               batches=batches,
                                                               batch_size=batch_size,
                                                               skip_targets=skip_targets,
                                                               timeout=timeout,
                                                               test_origin=test_origin,
                                                               wait=kwargs.get('wait', True))

    def run_snowflake_pipeline_preview(self, pipeline_id, rev=0, batches=1, batch_size=10, skip_targets=True,
                                       end_stage=None, timeout=2000, test_origin=False,
                                       stage_outputs_to_override_json=None, **kwargs):
        """Run Snowflake pipeline preview.

        Args:
            pipeline_id (:obj:`str`): The pipeline instance's ID.
            rev (:obj:`int`, optional): Pipeline revision. Default: ``0``.
            batches (:obj:`int`, optional): Number of batches. Default: ``1``.
            batch_size (:obj:`int`, optional): Batch size. Default: ``10``.
            skip_targets (:obj:`bool`, optional): Skip targets. Default: ``True``.
            end_stage (:obj:`str`, optional): End stage. Default: ``None``.
            timeout (:obj:`int`, optional): Timeout. Default: ``2000``.
            test_origin (:obj:`bool`, optional): Test origin. Default: ``False``
            stage_outputs_to_override_json (:obj:`str`, optional): Stage outputs to override. Default: ``None``.
            wait (:obj:`bool`, optional): Wait for pipeline preview to finish. Default: ``True``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sdc_api.PreviewCommand`.
        """
        logger.info('Running preview for %s ...', pipeline_id)
        preview_command = self.api_client.run_snowflake_pipeline_preview(pipeline_id, rev, batches, batch_size,
                                                                         skip_targets, end_stage, timeout, test_origin,
                                                                         stage_outputs_to_override_json)
        if kwargs.get('wait', True):
            preview_command.wait_for_finished()

        return preview_command

    def test_pipeline_run(self, pipeline, reset_origin=False, parameters=None):
        """Test run a pipeline.

        Args:
            pipeline (:py:obj:`streamsets.sdk.sch_models.Pipeline`): Pipeline object.
            reset_origin (:obj:`boolean`, optional): Default: ``False``.
            parameters (:obj:`dict`, optional): Pipeline parameters. Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sdc_api.StartPipelineCommand`.
        """
        executor_instance, executor_pipeline_id = self._add_pipeline_to_executor_if_not_exists(
                                                                                            pipeline=pipeline,
                                                                                            reset_origin=reset_origin,
                                                                                            parameters=parameters)
        # Update pipeline rules as seen at https://git.io/JURT4
        pipeline_rules_command = (executor_instance.api_client.get_pipeline_rules(pipeline_id=executor_pipeline_id))
        pipeline_rules = pipeline._rules_definition
        pipeline_rules['uuid'] = pipeline_rules_command.response.json()['uuid']
        update_rules_command = (executor_instance.api_client
                                .update_pipeline_rules(pipeline_id=executor_pipeline_id,
                                                       pipeline=pipeline_rules))
        start_pipeline_command = executor_instance.start_pipeline(executor_pipeline_id)
        start_pipeline_command.executor_pipeline = pipeline
        start_pipeline_command.executor_instance = executor_instance
        return start_pipeline_command

    def _add_pipeline_to_executor_if_not_exists(self, pipeline, reset_origin=False, parameters=None):
        """Util function to add ControlHub pipeline to executor.

        Args:
            pipeline (:py:obj:`streamsets.sdk.sch_models.Pipeline`): Pipeline object.
            reset_origin (:obj:`boolean`, optional): Default: ``False``.
            parameters (:obj:`dict`, optional): Pipeline parameters. Default: ``None``.

        Returns:
            An instance of :obj:`tuple` of (:py:obj:`streamsets.sdk.DataCollector` or
                :py:obj:`streamsets.sdk.Transformer` and :py:obj:`streamsets.sdk.sdc_models.Pipeline`)
        """
        executor_type = getattr(pipeline, 'executor_type', 'COLLECTOR') or 'COLLECTOR'
        if executor_type == SNOWFLAKE_EXECUTOR_TYPE:
            authoring_executor_instance = None
            principal_user_id = self.api_client.get_current_user().response.json()['principalId']
            executor_pipeline_id = 'testRun__{}__{}__{}'.format(pipeline.pipeline_id.split(':')[0], self.organization,
                                                                principal_user_id)
        else:
            authoring_executor = (self.data_collectors.get(id=pipeline.sdc_id) if executor_type == 'COLLECTOR' else
                                  self.transformers.get(id=pipeline.sdc_id))
            authoring_executor_instance = authoring_executor._instance
            executor_pipeline_id = 'testRun__{}__{}'.format(pipeline.pipeline_id.split(':')[0], self.organization)
        if authoring_executor_instance:
            pipeline_status_command = (authoring_executor_instance.api_client
                                       .get_pipeline_status(pipeline_id=executor_pipeline_id,
                                                            only_if_exists=True))
        else:
            pipeline_status_command = (self.api_client.get_snowflake_pipeline(pipeline_id=executor_pipeline_id,
                                                                              only_if_exists=True))
        if not pipeline_status_command.response.text:
            if authoring_executor_instance:
                create_pipeline_response = (authoring_executor_instance.api_client
                                            .create_pipeline(pipeline_title=executor_pipeline_id,
                                                             description="New Pipeline",
                                                             auto_generate_pipeline_id=False,
                                                             draft=False))
            else:
                create_pipeline_response = (self.api_client
                                            .create_snowflake_pipeline(pipeline_title=executor_pipeline_id,
                                                                       description="New Pipeline",
                                                                       auto_generate_pipeline_id=False,
                                                                       draft=False))
        elif reset_origin:
            if authoring_executor_instance:
                reset_origin_command = (authoring_executor_instance.api_client
                                        .reset_origin_offset(pipeline_id=executor_pipeline_id))
            else:
                reset_origin_command = (self.api_client
                                        .reset_snowflake_origin_offset(pipeline_id=executor_pipeline_id))
        if authoring_executor_instance:
            pipeline_info = (authoring_executor_instance.api_client
                             .get_pipeline_configuration(pipeline_id=executor_pipeline_id,
                                                         get='info'))
        else:
            pipeline_info = (self.api_client
                             .get_snowflake_pipeline_configuration(pipeline_id=executor_pipeline_id,
                                                                   get='info'))
        if parameters:
            pipeline.parameters = parameters
        executor_pipeline_json = pipeline._pipeline_definition
        executor_pipeline_json['uuid'] = pipeline_info['uuid']
        if authoring_executor_instance:
            update_pipeline_response = (authoring_executor_instance.api_client
                                        .update_pipeline(pipeline_id=executor_pipeline_id,
                                                         pipeline=executor_pipeline_json))
        else:
            update_pipeline_response = (self.api_client
                                        .update_snowflake_pipeline(pipeline_id=executor_pipeline_id,
                                                                   pipeline=executor_pipeline_json))
        return authoring_executor_instance, executor_pipeline_id

    def stop_test_pipeline_run(self, start_pipeline_command):
        """Stop the test run of pipeline.

        Args:
            start_pipeline_command (:py:class:`streamsets.sdk.sdc_api.StartPipelineCommand`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sdc_api.StopPipelineCommand`.
        """
        return start_pipeline_command.executor_instance.stop_pipeline(start_pipeline_command.executor_pipeline)

    def preview_classification_rule(self, classification_rule, parameter_data, data_collector=None):
        """Dynamic preview of a classification rule.

        Args:
            classification_rule (:py:obj:`streamsets.sdk.sch_models.ClassificationRule`): Classification Rule object.
            parameter_data (:obj:`dict`): A python dict representation of raw JSON parameters required for preview.
            data_collector (:py:obj:`streamsets.sdk.sch_models.DataCollector`, optional): The Data Collector
                in which to preview the pipeline. If omitted, ControlHub's first executor SDC will be used.
                Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sdc_api.PreviewCommand`.
        """
        if self.data_protector_enabled:
            # Note: system data collector cannot be used for dynamic preview
            if not data_collector and len(self.data_collectors) < 1:
                raise Exception('No executor DataCollector found')
            else:
                data_collector_instance = (data_collector or self.data_collectors[0])._instance
                parameters = {
                    'classification.catalogId': classification_rule.catalog_uuid,
                    'rawJson': json.dumps(parameter_data)
                }
                return data_collector_instance.run_dynamic_pipeline_preview(type='CLASSIFICATION_CATALOG',
                                                                            parameters=parameters)

    def add_classification_rule(self, classification_rule, commit=False):
        """Add a classification rule.

        Args:
            classification_rule (:py:obj:`streamsets.sdk.sch_models.ClassificationRule`): Classification Rule object.
            commit (:obj:`bool`, optional): Whether to commit the rule after adding it. Default: ``False``.
        """
        self.api_client.create_classification_rule({'data': classification_rule._data})
        default_classifier_ids = [classifier['data']['id']
                                  for classifier
                                  in self.api_client.get_classification_classifier_list(
                                                                                        classification_rule._data['id']
                                                                                        ).response.json()['response']]
        for classifier_id in default_classifier_ids:
            self.api_client.delete_classification_classifier(classifier_id)

        for classifier in classification_rule.classifiers:
            self.api_client.create_classification_classifier({'data': classifier._data})

        if commit:
            self.api_client.commit_classification_rules(self._classification_catalog_id)

    def get_snowflake_pipeline_defaults(self):
        """Get the Snowflake pipeline defaults for this user (if it exists).

        Returns:
            A :obj:`dict` of Snowflake pipeline defaults.
        """
        return self.api_client.get_snowflake_pipeline_defaults().response.json()

    def update_snowflake_pipeline_defaults(self, account_url=None, database=None, warehouse=None, schema=None,
                                           role=None):
        """Create or update the Snowflake pipeline defaults for this user.

        Args:
            account_url (:obj:`str`, optional): Snowflake account url. Default: ``None``
            database (:obj:`str`, optional): Snowflake database to query against. Default: ``None``
            warehouse (:obj:`str`, optional): Snowflake warehouse. Default: ``None``
            schema (:obj:`str`, optional): Schema used. Default: ``None``
            role (:obj:`str`, optional): Role used. Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        body = {'accountUrl': account_url,
                'database': database,
                'warehouse': warehouse,
                'schema': schema,
                'role': role}
        return self.api_client.update_snowflake_pipeline_defaults(body)

    def delete_snowflake_pipeline_defaults(self):
        """Delete the Snowflake pipeline defaults for this user.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        return self.api_client.delete_snowflake_pipeline_defaults()

    def get_snowflake_user_credentials(self):
        """Get the Snowflake user credentials (if they exist). They will be redacted.

        Returns:
            A :obj:`dict` of Snowflake user credentials (redacted).
        """
        return self.api_client.get_snowflake_user_credentials().response.json()

    def update_snowflake_user_credentials(self, username, snowflake_login_type, password=None, private_key=None,
                                          role=None):
        """Create or update the Snowflake user credentials.

        Args:
            username (:obj:`str`): Snowflake account username.
            snowflake_login_type (:obj:`str`): Snowflake login type to use. Options are ``password`` and
                ``privateKey``.
            password (:obj:`str`, optional): Snowflake account password. Default: ``None``
            private_key (:obj:`str`, optional): Snowflake account private key. Default: ``None``
            role (:obj:`str`, optional): Snowflake role of the account. Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        valid_snowflake_login_types = {'PASSWORD', 'PRIVATE_KEY'}
        if snowflake_login_type not in valid_snowflake_login_types:
            raise ValueError("snowflake_login_type must be either password or privateKey")
        elif snowflake_login_type == 'PASSWORD' and password is None:
            raise ValueError("password cannot be None when snowflake_login_type is 'PASSWORD'")
        elif snowflake_login_type == 'PRIVATE_KEY' and private_key is None:
            raise ValueError("private_key cannot be None when snowflake_login_type is 'PRIVATE_KEY'")

        body = {'username': username,
                'snowflakeLoginType': snowflake_login_type,
                'password': password,
                'privateKey': private_key,
                'role': role}
        return self.api_client.update_snowflake_user_credentials(body)

    def delete_snowflake_user_credentials(self):
        """Delete the Snowflake user credentials.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        return self.api_client.delete_snowflake_user_credentials()

    def get_scheduled_task_builder(self):
        """Get a scheduled task builder instance with which a scheduled task can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ScheduledTaskBuilder`.
        """
        job_selection_types = self.api_client.get_job_selection_types(api_version=2).response.json()['response']['data']
        return ScheduledTaskBuilder(job_selection_types, self)

    def publish_scheduled_task(self, task):
        """Send the scheduled task to ControlHub.

        Args:
            task (:py:class:`streamsets.sdk.sch_models.ScheduledTask`): Scheduled task object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        create_task_command = self.api_client.create_scheduled_task(data={'data': task._data}, api_version=2)
        task._data = create_task_command.response.json()['response']['data']
        return create_task_command

    @property
    def scheduled_tasks(self):
        """Scheduled Tasks.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ScheduledTasks`.
        """
        return ScheduledTasks(self)

    @property
    def subscriptions(self):
        """Event Subscriptions.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Subscriptions`.
        """
        return Subscriptions(self)

    def get_subscription_builder(self):
        """Get Event Subscription Builder.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.SubscriptionBuilder`.
        """
        subscription = {property: None
                        for property in self._notification_api['definitions']['EventSubscriptionJson']['properties']}
        subscription.update(dict(enabled=True, deleted=False, events=[]))
        return SubscriptionBuilder(subscription=subscription,
                                   control_hub=self)

    def add_subscription(self, subscription):
        """Add Subscription to ControlHub.

        Args:
            subscription (:py:obj:`streamsets.sdk.sch_models.Subscription`): A Subscription instance.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        event_types = self._en_translations['notifications']['subscriptions']['events']
        subscription._data['events'] = [{'eventType': reversed_dict(event_types)[event.event_type],
                                         'filter': event.filter} for event in subscription.events]
        action_config = subscription._data['externalActions'][0]['config']
        subscription._data['externalActions'][0]['config'] = (json.dumps(action_config)
                                                              if isinstance(action_config, dict) else action_config)
        create_subscription_command = self.api_client.create_event_subscription(body=subscription._data)
        subscription._data = create_subscription_command.response.json()
        return create_subscription_command

    def update_subscription(self, subscription):
        """Update an existing Subscription.

        Args:
            subscription (:py:obj:`streamsets.sdk.sch_models.Subscription`): A Subscription instance.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        event_types = self._en_translations['notifications']['subscriptions']['events']
        subscription._data['events'] = [{'eventType': reversed_dict(event_types)[event.event_type],
                                         'filter': event.filter} for event in subscription.events]
        action_config = subscription._data['externalActions'][0]['config']
        subscription._data['externalActions'][0]['config'] = (json.dumps(action_config)
                                                              if isinstance(action_config, dict) else action_config)
        update_subscription_command = self.api_client.update_event_subscription(body=subscription._data)
        subscription._data = update_subscription_command.response.json()
        return update_subscription_command

    def delete_subscription(self, subscription):
        """Delete an exisiting Subscription.

        Args:
            subscription (:py:obj:`streamsets.sdk.sch_models.Subscription`): A Subscription instance.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        return self.api_client.delete_event_subscription(subscription_id=subscription.id)

    def acknowledge_event_subscription_error(self, subscription):
        """Acknowledge an error on given Event Subscription.

        Args:
            subscription (:py:obj:`streamsets.sdk.sch_models.Subscription`): A Subscription instance.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        cmd = self.api_client.event_subscription_acknowledge_error(subscription.id)
        subscription._data = cmd.response.json()
        return cmd

    @property
    def subscription_audits(self):
        """Subscription audits.

        Returns:
            A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.SubscriptionAudit`.
        """
        cmd = self.api_client.get_all_subscription_audits()
        return SeekableList([SubscriptionAudit(audit) for audit in cmd.response.json()])

    def acknowledge_job_error(self, *jobs):
        """Acknowledge errors for one or more jobs.

        Args:
            *jobs: One or more instances of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        job_ids = [job.job_id for job in jobs]
        logger.info('Acknowledging errors for job(s) %s ...', job_ids)
        self.api_client.jobs_acknowledge_errors(job_ids)

    def sync_job(self, *jobs):
        """Sync one or more jobs.

        Args:
            *jobs: One or more instances of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        job_ids = [job.job_id for job in jobs]
        logger.info('Synchronizing job(s) %s ...', job_ids)
        self.api_client.sync_jobs(job_ids)

    def balance_job(self, *jobs):
        """Balance one or more jobs.

        Args:
            *jobs: One or more instances of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        job_ids = [job.job_id for job in jobs]
        logger.info('Balancing job(s) %s ...', job_ids)
        self.api_client.balance_jobs(job_ids)

    def get_topology_builder(self):
        """Get a topology builder instance with which a topology can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.TopologyBuilder`.
        """
        topology_json = {}
        # Update the topology_json with the API definitions from Swagger.
        topology_json.update({property: None
                              for property in self._topology_api['definitions']['TopologyJson']['properties']})
        topology_json['organization'] = self.organization
        topology_json['topologyDefinition'] = {}
        topology_json['topologyDefinition']['schemaVersion'] = '1'
        topology_json['topologyDefinition']['topologyNodes'] = []
        topology_json['topologyDefinition']['stageIcons'] = {}
        topology_json['topologyDefinition']['valid'] = True

        return TopologyBuilder(topology=topology_json, control_hub=self)

    def get_data_sla_builder(self):
        """Get a Data SLA builder instance with which a Data SLA can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.DataSlaBuilder`.
        """
        data_sla = {property: None
                    for property in self._sla_api['definitions']['DataSlaJson']['properties']}
        data_sla['organization'] = self.organization

        return DataSlaBuilder(data_sla, self)

    @property
    def topologies(self):
        """Topologies.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Topologies`.
        """
        return Topologies(self)

    def import_topologies(self, archive, import_number_of_instances=False, import_labels=False,
                          import_runtime_parameters=False, **kwargs):
        # update_migrate_offsets is not configurable through UI and is supported through kwargs.
        """Import topologies from archived zip directory.

        Args:
            archive (:obj:`file`): file containing the topologies.
            import_number_of_instances (:obj:`boolean`, optional): Indicate if number of instances should be imported.
                                                            Default: ``False``.
            import_labels (:obj:`boolean`, optional): Indicate if labels should be imported. Default: ``False``.
            import_runtime_parameters (:obj:`boolean`, optional): Indicate if runtime parameters should be imported.
                                                           Default: ``False``.

        Returns:
            A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.Topology`.
        """
        return SeekableList([Topology(topology, control_hub=self)
                             for topology in self.api_client
                            .import_topologies(topologies_file=archive,
                                               update_num_instances=import_number_of_instances,
                                               update_labels=import_labels,
                                               update_runtime_parameters=import_runtime_parameters,
                                               **kwargs).response.json()])

    def export_topologies(self, topologies):
        """Export topologies.

        Args:
            topologies (:obj:`list`): A list of :py:class:`streamsets.sdk.sch_models.Topology` instances.

        Returns:
            An instance of type :py:obj:`bytes` indicating the content of zip file with pipeline json files.
        """
        commit_ids = [topology.commit_id for topology in topologies]
        return self.api_client.export_topologies(body=commit_ids).response.content

    def delete_topology(self, topology, only_selected_version=False):
        """Delete a topology.

        Args:
            topology (:py:class:`streamsets.sdk.sch_models.Topology`): Topology object.
            only_selected_version (:obj:`boolean`): Delete only current commit.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        if only_selected_version:
            logger.info('Deleting topology version %s for topology %s ...', topology.commit_id, topology.topology_name)
            return self.api_client.delete_topology_versions(commits_json=[topology.commit_id])
        logger.info('Deleting topology %s with topology id %s ...', topology.topology_name, topology.topology_id)
        return self.api_client.delete_topologies(topologies_json=[topology.topology_id])

    def publish_topology(self, topology, commit_message=None):
        """Publish a topology.

        Args:
            topology (:py:class:`streamsets.sdk.sch_models.Topology`): Topology object to publish.
            commit_message (:obj:`str`, optional): Commit message to supply with the Topology. Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        # If the topology already has a commit_id but isn't in draft mode, we assume it exists and create a new draft
        # in order to update the existing instance before publishing
        if topology.commit_id and not topology.draft:
            try:
                draft_topology = self.api_client.create_topology_draft(commit_id=topology.commit_id).response.json()
            except requests.exceptions.HTTPError:
                raise
            draft_topology.update({'topologyDefinition': topology._data['topologyDefinition']})
            created_topology = self.api_client.update_topology(commit_id=draft_topology['commitId'],
                                                               topology_json=draft_topology).response.json()
            response = self.api_client.publish_topology(commit_id=created_topology['commitId'],
                                                        commit_message=commit_message)
        # This is a brand-new topology being created for the first time
        elif not topology.commit_id:
            created_topology = self.api_client.create_topology(topology_json=topology._data).response.json()
            response = self.api_client.publish_topology(commit_id=created_topology['commitId'],
                                                        commit_message=commit_message)
        # This is an existing topology that's already in draft mode
        else:
            response = self.api_client.publish_topology(commit_id=topology.commit_id,
                                                        commit_message=commit_message)
        # Refresh the in-memory representation of the topology
        topology.commit_id = response.response.json()['commitId']
        topology._refresh()

        return response

    @property
    def report_definitions(self):
        """Report Definitions.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ReportDefinitions`.
        """
        return ReportDefinitions(self)

    def add_report_definition(self, report_definition):
        """Add Report Definition to ControlHub.

        Args:
            report_definition (:py:class:`streamsets.sdk.sch_models.ReportDefinition`): Report Definition instance.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        create_report_definition_command = self.api_client.create_new_report_definition(report_definition._data)
        report_definition._data = create_report_definition_command.response.json()
        return create_report_definition_command

    def update_report_definition(self, report_definition):
        """Update an existing Report Definition.

        Args:
            report_definition (:py:class:`streamsets.sdk.sch_models.ReportDefinition`): Report Definition instance.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        update_report_definition_command = self.api_client.update_report_definition(report_definition.id,
                                                                                    report_definition._data)
        report_definition._data = update_report_definition_command.response.json()
        return update_report_definition_command

    def delete_report_definition(self, report_definition):
        """Delete an existing Report Definition.

        Args:
            report_definition (:py:class:`streamsets.sdk.sch_models.ReportDefinition`): Report Definition instance.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        return self.api_client.delete_report_definition(report_definition.id)

    def get_connection_builder(self):
        """Get a connection builder instance with which a connection can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ConnectionBuilder`.
        """
        # Update the ConnectionJson with the API definitions from Swagger.
        connection = {property: None
                      for property in self._connection_api['definitions']['ConnectionJson']['properties']}
        connection['organization'] = self.organization

        return ConnectionBuilder(connection=connection, control_hub=self)

    def add_connection(self, connection):
        """Add a connection.

        Args:
            connection (:py:class:`streamsets.sdk.sch_models.Connection`): Connection object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        logger.info('Adding a connection %s ...', connection)
        # Update _data with any changes made to the connection definition
        connection._data.update({'connectionDefinition': json.dumps(connection._connection_definition._data)})
        create_connection_command = self.api_client.create_connection(connection._data)
        # Update :py:class:`streamsets.sdk.sch_models.Connection` with updated Connection metadata.
        connection._data = create_connection_command.response.json()
        return create_connection_command

    @property
    def connections(self):
        """Connections.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Connections`.
        """
        return Connections(self, self.organization)

    def update_connection(self, connection):
        """Update a connection.

        Args:
            connection (:py:class:`streamsets.sdk.sch_models.Connection`): Connection object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        logger.info('Updating a connection %s ...', connection)
        # Update _data with any changes made to the connection definition
        connection._data.update({'connectionDefinition': json.dumps(connection._connection_definition._data)})
        update_connection_command = self.api_client.update_connection(connection_id=connection.id,
                                                                      body=connection._data)
        connection._data = update_connection_command.response.json()
        return update_connection_command

    def delete_connection(self, *connections):
        """Delete connections.

        Args:
            *connections: One or more instances of :py:class:`streamsets.sdk.sch_models.Connection`.
        """
        for connection in connections:
            logger.info('Deleting connection %s ...', connection)
            self.api_client.delete_connection(connection_id=connection.id)

    def verify_connection(self, connection):
        """Verify connection.

        Args:
            connection (:py:class:`streamsets.sdk.sch_models.Connection`): Connection object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ConnectionVerificationResult`.
        """
        logger.info('Running dynamic preview for %s type ...', type)
        library_definition = json.loads(connection.library_definition)
        # As configured by UI at https://git.io/JUkz8
        parameters = {'connection': {'configuration': connection.connection_definition.configuration,
                                     'connectionId': connection.id,
                                     'type': connection.connection_type,
                                     'verifierDefinition': library_definition['verifierDefinitions'][0],
                                     'version': library_definition['version']}}
        dynamic_preview_request = {'dynamicPreviewRequestJson': {'batches': 2,
                                                                 'batchSize': 100,
                                                                 'parameters': parameters,
                                                                 'skipLifecycleEvents': True,
                                                                 'skipTargets': False,
                                                                 'testOrigin': False,
                                                                 'timeout': 120*1000,  # 120 seconds
                                                                 'type': 'CONNECTION_VERIFIER'},
                                   'stageOutputsToOverrideJson': []}
        sdc = self.data_collectors.get(id=connection.sdc_id)._instance
        validate_command = sdc.api_client.run_dynamic_pipeline_preview_for_connection(dynamic_preview_request)
        return ConnectionVerificationResult(validate_command.wait_for_validate().response.json())

    @property
    def environments(self):
        """environments.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Environments`.
        """
        return Environments(self, self.organization)

    def activate_environment(self, *environments, timeout_sec=DEFAULT_WAIT_FOR_STATUS_TIMEOUT):
        """Activate environments.

        Args:
            *environments: One or more instances of :py:class:`streamsets.sdk.sch_models.Environment`.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command` or None.
        """
        if not environments:
            logger.info('No environments to activate. Returning')
            return
        environment_ids = [environment.environment_id for environment in environments]
        logger.info('Activating environments %s ...', environment_ids)
        activate_environments_command = self.api_client.enable_environments(environment_ids)

        activate_environment_exception = None
        for environment in environments:
            try:
                self.api_client.wait_for_environment_state_display_label(environment_id=environment.environment_id,
                                                                         state_display_label='ACTIVE',
                                                                         timeout_sec=timeout_sec)
            except Exception as ex:
                # just log the exceptions and ultimately raise the last one.
                logger.debug(ex)
                activate_environment_exception = ex
            # Update :py:class:`streamsets.sdk.sch_models.Environment` with updated data.
            environment.refresh()

        if activate_environment_exception:
            raise activate_environment_exception
        return activate_environments_command

    def deactivate_environment(self, *environments):
        """Deactivate environments.

        Args:
            *environments: One or more instances of :py:class:`streamsets.sdk.sch_models.Environment`.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        environment_ids = [environment.environment_id for environment in environments]
        logger.info('Deactivating environments %s ...', environment_ids)
        deactivate_environments_command = self.api_client.disable_environments(environment_ids)

        deactivate_environment_exception = None
        for environment in environments:
            try:
                self.api_client.wait_for_environment_state_display_label(environment_id=environment.environment_id,
                                                                         state_display_label='DEACTIVATED')
                # Update :py:class:`streamsets.sdk.sch_models.Environment` with updated Environment metadata.
            except Exception as ex:
                # just log the exceptions and ultimately raise the last one.
                logger.debug(ex)
                deactivate_environment_exception = ex
            # Update :py:class:`streamsets.sdk.sch_models.Environment` with updated data.
            environment.refresh()

        if deactivate_environment_exception:
            raise deactivate_environment_exception
        return deactivate_environments_command

    def add_environment(self, environment):
        """Add an environment.

        Args:
            environment (:py:class:`streamsets.sdk.sch_models.Environment`): Environment object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        logger.info('Adding an environment %s ...', environment.environment_name)
        complete = isinstance(environment, SelfManagedEnvironment)
        data = {'name': environment._data['name'], 'type': environment._data['type'],
                'allowSnapshotEngineVersions': environment._data['allowSnapshotEngineVersions'],
                'rawEnvironmentTags': environment._data['rawEnvironmentTags']}
        command = self.api_client.create_environment(data, complete=complete)
        fetched_data = command.response.json()

        # Update with updated Environment metadata.Note, this is not an overwrite. Rather it preserves
        # any relevant data which environment had it before create_environment command was issued.
        if isinstance(environment, AWSEnvironment):
            fields = ['credentialsType', 'credentials', 'defaultInstanceProfileArn', 'defaultManagedIdentity',
                      'region', 'vpcId', 'securityGroupId', 'subnetIds']
            created_dict = {field: environment._data.get(field, None) for field in fields}
        elif isinstance(environment, AzureEnvironment):
            fields = ['credentialsType', 'credentials', 'defaultResourceGroup', 'region', 'vpcId',
                      'securityGroupId', 'subnetId']
            created_dict = {field: environment._data.get(field, None) for field in fields}
        elif isinstance(environment, GCPEnvironment):
            fields = ['credentialsType', 'credentials', 'projectId', 'vpcId', 'vpcProjectId']
            created_dict = {field: environment._data.get(field, None) for field in fields}
        if not isinstance(environment, SelfManagedEnvironment):
            if created_dict.get('credentialsType'):
                # Map  the user entered value to internal constant
                ui_value_map = environment.get_ui_value_mappings()
                created_dict['credentialsType'] = ui_value_map['credentialsType'][created_dict['credentialsType']]
            fetched_data.update(created_dict)

        environment._data = fetched_data
        command = self.update_environment(environment)
        # Update :py:class:`streamsets.sdk.sch_models.Environment` with updated Environment metadata.
        environment._data = command.response.json()
        return command

    def update_environment(self, environment, timeout_sec=DEFAULT_WAIT_FOR_STATUS_TIMEOUT):
        """Update an environment.

        Args:
            environment (:py:class:`streamsets.sdk.sch_models.Environment`): environment object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        logger.info('Updating an environment %s ...', environment)
        is_env_complete = environment.complete()
        is_complete = is_env_complete if is_env_complete else 'undefined'
        command = self.api_client.update_environment(environment_id=environment.environment_id,
                                                     body=environment._data,
                                                     complete=is_complete,
                                                     process_if_enabled=is_complete)
        self.api_client.wait_for_environment_status(environment_id=environment.environment_id,
                                                    status='OK', timeout_sec=timeout_sec)

        environment._data = command.response.json()
        return command

    def delete_environment(self, *environments):
        """Delete environments.

        Args:
            *environments: One or more instances of :py:class:`streamsets.sdk.sch_models.Environment`.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        if not environments:
            logger.info('No environments to delete. Returning')
            return
        enabled_environments = [environment for environment in environments if environment.json_state == 'ENABLED']
        if enabled_environments:
            logger.info('Since only deactivated environments can be deleted, deactivating environment %s ...',
                        [environment.environment_name for environment in enabled_environments])
            self.deactivate_environment(*enabled_environments)

        environment_ids = [environment.environment_id for environment in environments]
        logger.info('Deleting environments %s ...', [environment.environment_name for environment in environments])
        self.api_client.delete_environments(environment_ids)

    def get_environment_builder(self, environment_type='SELF'):
        """Get an environment builder instance with which an environment can be created.

        Args:
            environment_type (:obj: `str`, optional) Valid values are 'AWS', 'GCP' and 'SELF'. Default ``'SELF'``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.EnvironmentBuilder`.
        """
        # Update the CSPEnvironmentJson with the API definitions from Swagger.
        properties = copy.deepcopy(self._provisioning_api['definitions']['CspEnvironmentJson']['properties'])
        if environment_type == 'AWS':
            properties.update(self._provisioning_api['definitions']['AwsCspEnvironmentJson']['allOf'][1]['properties'])
        elif environment_type == 'AZURE':
            properties.update(self._provisioning_api['definitions']
                              ['AzureCspEnvironmentJson']['allOf'][1]['properties'])
        elif environment_type == 'GCP':
            properties.update(self._provisioning_api['definitions']['GcpCspEnvironmentJson']['allOf'][1]['properties'])
        environment = {property: None for property in properties}

        return EnvironmentBuilder(environment=environment, control_hub=self)

    @property
    def engine_configurations(self):
        """Deployment engine configurations.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.DeploymentEngineConfiguration`.
        """
        return DeploymentEngineConfigurations(self)

    @property
    def deployments(self):
        """Deployments.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Deployments`.
        """
        return Deployments(self, self.organization)

    def start_deployment(self, *deployments):
        """Start Deployments.

        Args:
            *deployments: One or more instances of :py:class:`streamsets.sdk.sch_models.Deployment`.
        """
        deployment_ids = [deployment.deployment_id for deployment in deployments]
        logger.info('Starting deployments %s ...', deployment_ids)
        enable_deployments_command = self.api_client.enable_deployments(deployment_ids)

        start_deployment_exception = None
        for deployment in deployments:
            try:
                self.api_client.wait_for_deployment_state_display_label(deployment_id=deployment.deployment_id,
                                                                        state_display_label='ACTIVE')
            except Exception as ex:
                # just log the exceptions and ultimately raise the last one.
                logger.debug(ex)
                start_deployment_exception = ex
            # Update :py:class:`streamsets.sdk.sch_models.deployment` with updated data.
            deployment.refresh()

        if start_deployment_exception:
            raise start_deployment_exception
        return enable_deployments_command

    def stop_deployment(self, *deployments):
        """Stop Deployments.

        Args:
            *deployments: One or more instances of :py:class:`streamsets.sdk.sch_models.Deployment`.
        """
        deployment_ids = [deployment.deployment_id for deployment in deployments]
        logger.info('Stopping deployments %s ...', deployment_ids)
        stop_deployments_command = self.api_client.disable_deployments(deployment_ids)

        stop_deployment_exception = None
        for deployment in deployments:
            try:
                self.api_client.wait_for_deployment_state_display_label(deployment_id=deployment.deployment_id,
                                                                        state_display_label='DEACTIVATED')
            except Exception as ex:
                # just log the exceptions and ultimately raise the last one.
                logger.debug(ex)
                stop_deployment_exception = ex
            # Update :py:class:`streamsets.sdk.sch_models.deployment` with updated data.
            deployment.refresh()

        if stop_deployment_exception:
            raise stop_deployment_exception
        return stop_deployments_command

    def add_deployment(self, deployment):
        """Add a deployment.

        Args:
            deployment (:py:class:`streamsets.sdk.sch_models.Deployment`): Deployment object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        logger.info('Adding a deployment %s ...', deployment.deployment_name)

        if deployment._data['engineType'] == 'DC':
            # The engine_id is used only when engineBuild is not None. Otherwise, it is set to None, not affecting the
            # following query
            engine_id = (f'{deployment._data["engineType"]}:{deployment._data["engineVersion"]}::'
                         f'{deployment._data["engineBuild"]}' if deployment._data.get("engineBuild") else None)
            if deployment._data.get("engineBuild"):
                logger.info('The deployment has version %s and build %s', deployment._data["engineVersion"],
                            deployment._data["engineBuild"])
            engine_version = self.engine_configurations.get(engine_type=deployment._data['engineType'],
                                                            engine_version=deployment._data['engineVersion'],
                                                            id=engine_id,
                                                            disabled=False)
        elif deployment._data['engineType'] == 'TF':
            # The engine_id is used only when engineBuild is not None. Otherwise, it is set to None, not affecting the
            # following query
            engine_id = (f'{deployment._data["engineType"]}:{deployment._data["engineVersion"]}:'
                         f'{deployment._data["scalaBinaryVersion"]}:{deployment._data["engineBuild"]}'
                         if deployment._data.get("engineBuild") else None)
            if deployment._data.get("engineBuild"):
                logger.info('The deployment has version %s and build %s', deployment._data["engineVersion"],
                            deployment._data["engineBuild"])
            engine_version = self.engine_configurations.get(engine_type=deployment._data['engineType'],
                                                            engine_version=deployment._data['engineVersion'],
                                                            id=engine_id,
                                                            scala_binary_version=deployment._data['scalaBinaryVersion'],
                                                            disabled=False)
        data = {'name': deployment._data['name'],
                'type': deployment._data['type'],
                'engineType': deployment._data['engineType'],
                'engineVersion': deployment._data['engineVersion'],
                'engineVersionId': engine_version.id,
                'envId': deployment._data['envId'],
                'scalaBinaryVersion': deployment._data['scalaBinaryVersion'],
                'rawDeploymentTags': deployment._data['rawDeploymentTags']}
        command = self.api_client.create_deployment(data)
        fetched_data = command.response.json()

        # Fill up jvm_config: default jvm config with logic as per defind at https://git.io/JD2nf
        if deployment._data['engineConfiguration']['jvmConfig']:
            requested_jvm_config = deployment._data['engineConfiguration']['jvmConfig']
            # The part after or in the following takes care of the case,
            # if user specified some of the jvm_config and not all.
            jvm_config = {'jvmMinMemory': requested_jvm_config.get('jvmMinMemory', None) or 1024,
                          'jvmMinMemoryPercent': requested_jvm_config.get('jvmMinMemoryPercent', None) or 50,
                          'jvmMaxMemory': requested_jvm_config.get('jvmMaxMemory', None) or 1024,
                          'jvmMaxMemoryPercent': requested_jvm_config.get('jvmMaxMemoryPercent', None) or 50,
                          'extraJvmOpts': requested_jvm_config.get('extraJvmOpts', None) or '',
                          'memoryConfigStrategy': requested_jvm_config.get('memoryConfigStrategy', None) or
                                                  'PERCENTAGE'}
        # Fill up stage_libs: default_stage_libs logic as per defind at https://git.io/JDuwM
        if deployment._data['engineConfiguration']['stageLibs']:
            stage_libs = deployment._data['engineConfiguration']['stageLibs']
        else:
            if deployment._data['engineType'] == 'DC':
                stage_libs = DEFAULT_DATA_COLLECTOR_STAGE_LIBS
            elif deployment._data['engineType'] == 'TF':
                stage_libs = DEFAULT_TRANSFORMER_STAGE_LIBS
        # Process the stage_libs
        if deployment._data['engineType'] == 'DC':
            processed_stage_libs = ['streamsets-datacollector-{}-lib:{}'.format(lib,
                                                                                deployment._data['engineVersion'])
                                    for lib in stage_libs]
        elif deployment._data['engineType'] == 'TF':
            processed_stage_libs = ['streamsets-spark-{}-lib:{}'.format(lib, deployment._data['engineVersion'])
                                    for lib in stage_libs]
        # Fill up engine_labels
        engine_labels = deployment._data['engineConfiguration']['labels'] or [deployment._data['name']]
        # Fill up external_resource_source
        external_resource_source = deployment._data['engineConfiguration']['externalResourcesUri'] or ''
        # Fill up default advanced_configuration for the specified engine version
        response = self.api_client.get_engine_version(engine_version.id).response.json()
        fetched_data['engineConfiguration'].update({'advancedConfiguration': response['advancedConfiguration'],
                                                    'externalResourcesUri': external_resource_source,
                                                    'jvmConfig': jvm_config,
                                                    'labels': engine_labels,
                                                    'stageLibs': processed_stage_libs,
                                                    'scalaBinaryVersion': deployment._data['scalaBinaryVersion']})
        # Update with updated Deployment metadata. Note, this is not an overwrite. Rather it preserves
        # any relevant data which deployment had it before create_deployment command was issued.
        if isinstance(deployment, SelfManagedDeployment):
            fields = ['installType']
            created_dict = {field: deployment._data.get(field, None) for field in fields
                            if deployment._data.get(field, None) is not None}
            fetched_data.update(created_dict)
        elif isinstance(deployment, AzureVMDeployment):
            fields = ['attachPublicIp', 'desiredInstances', 'managedIdentity', 'resourceGroup', 'resourceTags',
                      'sshKeyPairName', 'sshKeySource', 'vmSize', 'zones']
            created_dict = {field: deployment._data.get(field, None) for field in fields}
            if created_dict.get('sshKeySource'):
                # Map  the user entered value to internal constant
                ui_value_map = deployment.get_ui_value_mappings()
                created_dict['sshKeySource'] = ui_value_map['sshKeySource'][created_dict['sshKeySource']]
            fetched_data.update(created_dict)
        elif isinstance(deployment, EC2Deployment):
            fields = ['desiredInstances', 'instanceProfileArn', 'instanceType', 'resourceTags', 'sshKeyPairName',
                      'sshKeySource', 'trackingUrl']
            created_dict = {field: deployment._data.get(field, None) for field in fields}
            fetched_data.update(created_dict)
        elif isinstance(deployment, GCEDeployment):
            fields = ['blockProjectSshKeys', 'desiredInstances', 'instanceServiceAccountEmail', 'machineType',
                      'tags', 'publicSshKey', 'region', 'trackingUrl', 'resourceLabels', 'zones', 'subnetwork']
            created_dict = {field: deployment._data.get(field, None) for field in fields}
            fetched_data.update(created_dict)
        deployment._data = fetched_data
        command = self.update_deployment(deployment)
        # Update :py:class:`streamsets.sdk.sch_models.Deployment` with updated Deployment metadata.
        deployment._data = command.response.json()
        return command

    def update_deployment(self, deployment):
        """Update a deployment.

        Args:
            deployment (:py:class:`streamsets.sdk.sch_models.Deployment`): deployment object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        logger.info('Updating a deployment %s ...', deployment)
        is_env_complete = deployment.complete()
        is_complete = is_env_complete if is_env_complete else 'undefined'
        command = self.api_client.update_deployment(deployment_id=deployment.deployment_id,
                                                    body=deployment._data,
                                                    complete=is_complete,
                                                    process_if_enabled=is_complete)
        self.api_client.wait_for_deployment_status(deployment_id=deployment.deployment_id, status='OK')
        deployment._data = command.response.json()
        return command

    def delete_deployment(self, *deployments):
        """Delete deployments.

        Args:
            *deployments: One or more instances of :py:class:`streamsets.sdk.sch_models.Deployment`.
        """
        if not deployments:
            logger.info('No deployments to delete. Returning')
            return
        enabled_deployments = [deployment for deployment in deployments if deployment.json_state == 'ENABLED']
        if enabled_deployments:
            logger.info('Since only disabled deployments can be deleted, disabling deployment %s ...',
                        [deployment.deployment_name for deployment in enabled_deployments])
            self.stop_deployment(*enabled_deployments)

        deployment_ids = [deployment.deployment_id for deployment in deployments]
        logger.info('Deleting deployments %s ...', [deployment.deployment_name for deployment in deployments])
        self.api_client.delete_deployments(deployment_ids)

    def get_self_managed_deployment_install_script(self, deployment, install_mechanism='DEFAULT'):
        """Get install script for a Self Managed deployment.

        Args:
            deployment (:py:class:`streamsets.sdk.sch_models.Deployment`): deployment object.
            install_mechanism (:obj:`str`, optional): Possible values for install are "DEFAULT", "BACKGROUND" and
                                                      "FOREGROUND". Default: ``DEFAULT``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        command = self.api_client.get_self_managed_deployment_install_command(deployment.deployment_id,
                                                                              install_mechanism)
        # Returned response header has content-type: text/plain, which returns as bytes, hence decode them to a string.
        return command.response.content.decode('utf-8')

    def get_deployment_builder(self, deployment_type='SELF'):
        """Get a deployment builder instance with which a deployment can be created.

        Args:
            deployment_type (:obj: `str`, optional) Valid values are 'AWS', 'GCP' and 'SELF'. Default ``'SELF'``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.DeploymentBuilder`.
        """
        # Update the CSPDeploymentJson with the API definitions from Swagger.
        definitions = self._provisioning_api['definitions']
        properties = copy.deepcopy(definitions['CspDeploymentJson']['properties'])
        if deployment_type == 'SELF':
            properties.update(definitions['SelfManagedCspDeploymentJson']['allOf'][1]['properties'])
        elif deployment_type == 'AZURE_VM':
            properties.update(definitions['AzureVmCspDeploymentJson']['allOf'][1]['properties'])
        elif deployment_type == 'EC2':
            properties.update(definitions['Ec2CspDeploymentJson']['allOf'][1]['properties'])
        elif deployment_type == 'GCE':
            properties.update(definitions['GceCspDeploymentJson']['allOf'][1]['properties'])
        # get engine configuration definitions
        engine_config_properties = definitions['EngineConfigurationJson']['properties']
        # get jvm config definitions
        jvm_config_properties = definitions['EngineJvmConfigJson']['properties']

        deployment = {property: None for property in properties}
        deployment['engineConfiguration'] = {property: None for property in engine_config_properties}
        deployment['engineConfiguration']['jvmConfig'] = {property: None for property in jvm_config_properties}

        return DeploymentBuilder(deployment=deployment, control_hub=self)

    @property
    def metering_and_usage(self):
        """Metering and usage for the Organization. By default, this will return a report for the last 30 days of
        metering data. A report for a custom time window can be retrieved by indexing this object with a slice that
        contains a datetime object for the start (required) and stop (optional, defaults to datetime.now()).

            ex. metering_and_usage[datetime(2022, 1, 1):datetime(2022, 1, 14)]
                metering_and_usage[datetime.now() - timedelta(7):]

        Returns:
              An instance of :py:class:`streamsets.sdk.sch_models.MeteringUsage`
        """
        return MeteringUsage(self)

    def _get_protection_policies(self, policy_type):
        """An internal function that returns a list of protection policies

        Args:
            policy_type (str): The type of policies to return (Read, Write)

        Returns:
            A list of :py:class:`streamsets.sdk.utils.SeekableList`
        """
        return (self.protection_policies.get_all(default_setting=policy_type) +
                self.protection_policies.get_all(default_setting='Both'))

    def get_admin_tool(self, base_url, username, password):
        """Get ControlHub admin tool.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.AdminTool`.
        """
        return AdminTool(base_url, username, password)

    def wait_for_job_status(self, job, status, timeout_sec=DEFAULT_WAIT_FOR_STATUS_TIMEOUT):
        """Block until a job reaches the desired status.

        Args:
            job (:py:class:`streamsets.sdk.sch_models.Job`): The job instance.
            status (:py:obj:`str`): The desired status to wait for.
            timeout_sec (:obj:`int`, optional): Timeout to wait for ``job`` to reach ``status``, in seconds.
                Default: :py:const:`streamsets.sdk.sch.DEFAULT_WAIT_FOR_STATUS_TIMEOUT`.

        Raises:
            TimeoutError: If ``timeout_sec`` passes without ``job`` reaching ``status``.
        """
        def condition():
            job.refresh()
            logger.debug('Job has current status %s ...', job.status)
            return job.status == status

        def failure(timeout):
            raise TimeoutError('Timed out after `{}` seconds waiting for Job `{}` '.format(timeout, job.job_name),
                               'to reach status {}'.format(status))

        wait_for_condition(condition=condition, timeout=timeout_sec, failure=failure)

    def wait_for_job_metrics_record_count(self, job, count, timeout_sec=DEFAULT_WAIT_FOR_METRIC_TIMEOUT):
        """Block until a job's metrics reaches the desired count.

        Args:
            job (:py:class:`streamsets.sdk.sch_models.Job`): The job instance.
            count (:obj:`int`): The desired value to wait for.
            timeout_sec (:obj:`int`, optional): Timeout to wait for ``metric`` to reach ``count``, in seconds.
                Default: :py:const:`streamsets.sdk.sch.DEFAULT_WAIT_FOR_METRIC_TIMEOUT`.

        Raises:
            TimeoutError: If ``timeout_sec`` passes without ``metric`` reaching ``value``.
        """
        def condition():
            job.refresh()
            current_value = job.metrics(metric_type='RECORD_COUNT', include_error_count=True).output_count['PIPELINE']
            logger.debug('Waiting for job metric `%s` status to become `%s`', current_value, count)
            return current_value == count

        def failure(timeout):
            raise Exception('Timed out after `{}` seconds waiting for Job metric `{}` to become {}'.format(
                timeout, job.metrics(metric_type='RECORD_COUNT', include_error_count=True).output_count['PIPELINE'],
                count))

        wait_for_condition(condition=condition, timeout=timeout_sec, failure=failure)

    def wait_for_job_metric(self, job, metric, value, timeout_sec=DEFAULT_WAIT_FOR_METRIC_TIMEOUT):
        """Block until a job's realtime summary reaches the desired value for the desired metric.

        Args:
            job (:py:class:`streamsets.sdk.sch_models.Job`): The job instance.
            metric (:py:obj:`str`): The desired metric (e.g. ``'output_record_count'`` or ``'input_record_count'``).
            value (:obj:`int`): The desired value to wait for.
            timeout (:obj:`int`, optional): Timeout to wait for ``metric`` to reach ``value``, in seconds.
                Default: :py:const:`streamsets.sdk.sch.DEFAULT_WAIT_FOR_METRIC_TIMEOUT`.

        Raises:
            TimeoutError: If ``timeout`` passes without ``metric`` reaching ``value``.
        """
        def condition():
            executor_type = job.executor_type if job.executor_type else SDC_EXECUTOR_TYPE
            if executor_type != SDC_EXECUTOR_TYPE:
                raise Exception('This method is not yet supported for job with executor type other than COLLECTOR')

            current_value = getattr(job.realtime_summary, metric)
            logger.debug('Job realtime summary %s has current value %s ...', metric, current_value)
            return current_value >= value

        def failure(timeout):
            raise Exception('Job realtime summary {} did not reach value {} after {} s'.format(metric, value, timeout))

        wait_for_condition(condition=condition, timeout=timeout_sec, failure=failure)
