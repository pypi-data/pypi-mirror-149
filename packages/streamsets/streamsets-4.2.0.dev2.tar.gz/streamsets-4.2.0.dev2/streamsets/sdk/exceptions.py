# Copyright 2019 StreamSets Inc.

"""Common exceptions."""

from requests.exceptions import HTTPError


class InternalServerError(HTTPError):
    """Internal server error."""
    def __init__(self, response):
        self.status_code = response.status_code
        self.response = response.json()
        self.text = self.response['RemoteException']['localizedMessage']

        # Propagate message from the REST interface as message of the exception
        super().__init__(self.text)


class BadRequestError(HTTPError):
    """Bad request error (HTTP 400)."""
    def __init__(self, response):
        super().__init__(response.text)


class LegacyDeploymentInactiveError(Exception):
    """Legacy deployment status changed into INACTIVE_ERROR."""
    def __init__(self, message):
        self.message = message


class ValidationError(Exception):
    """Validation issues."""
    def __init__(self, issues):
        self.issues = issues


class JobInactiveError(Exception):
    """Job status changed into INACTIVE_ERROR."""
    def __init__(self, message):
        self.message = message


class JobRunnerError(Exception):
    """JobRunner errors."""
    def __init__(self, code, message):
        super().__init__('{}: {}'.format(code, message))
        self.code = code
        self.message = message


class UnsupportedMethodError(Exception):
    """An unsupported method was called."""
    def __init__(self, message):
        self.message = message


class TopologyIssuesError(Exception):
    """Topology has some issues."""
    def __init__(self, issues):
        self.message = issues


class InvalidCredentialsError(Exception):
    """Invalid credentials error."""
    def __init__(self, message):
        self.message = message


class ConnectionError(Exception):
    """Connection Catalog errors."""
    def __init__(self, code, message):
        super().__init__('{}: {}'.format(code, message))
        self.message = message
        self.code = code


class MultipleIssuesError(Exception):
    """Multiple errors were returned."""
    def __init__(self, errors):
        self.errors = errors
        self.message = 'Multiple issues encountered'
        super().__init__('{}: {}'.format(self.message, self.errors))

    def __getitem__(self, item):
        return self.errors[item]

    def __repr__(self):
        return str('{}: {}'.format(self.message, self.errors))


class UnprocessableEntityError(HTTPError):
    """Unprocessable Entity Error (HTTP 422)."""
    def __init__(self, response):
        self.response = response.json()
        # The error response from ASTER's API puts the error in a list, so we index into the list to get the message
        self.message = self.response['errors'][0]['message']
        self.code = self.response['status']

        # Propagate the message from the API interface
        super().__init__('{}: {}'.format(self.code, self.message))
