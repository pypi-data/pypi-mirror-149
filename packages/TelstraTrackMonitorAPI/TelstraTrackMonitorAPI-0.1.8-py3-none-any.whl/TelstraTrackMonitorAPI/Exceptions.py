class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class TTMErrorHandler(object):
    """Handles Telstra Track And Monitor Exceptions"""
    def __init__(self,request):
        self.fault=request.json()
        if isinstance(self.fault,dict) and self.fault.get('fault'):
            if self.fault['fault']['detail']['errorcode']=='oauth.v2.InvalidAccessToken':
                raise OAuthV2InvalidAccessToken()
            elif self.fault['fault']['detail']['errorcode']=='keymanagement.service.invalid_access_token':
                raise KeyManagementInvalidAccessToken()
            #Catch for undefined Faults
            else:
                raise UndefinedFaultStringError(
                    self.fault,
                    self.fault['fault']['detail']['errorcode'])
        elif isinstance(self.fault,dict) and self.fault.get('error'):
            if self.fault['error'] == 'invalid_client':
                raise OAuth2InvalidClientError()
            #Catch for undefined Faults
            else:
                raise UndefinedFaultStringError(
                    self.fault,
                    self.fault['error'])
        elif isinstance(self.fault,dict) and self.fault.get('message'):
            if 'The query specified in the URI is not valid.' in self.fault['message']:
                raise ParameterSyntaxError(self.fault['message'])
            #Catch for undefined Faults
            else:
                raise UndefinedMessageError(self.fault['message'])
        else:
            raise IWasNotProgramedForThisError()



class OAuthV2InvalidAccessToken(Error):
    """Exception raised for errors related to Invalid access token.
        Observed causes:
            Missing Authentication header
    """
class KeyManagementInvalidAccessToken(Error):
    """Exception raised for errors related to Invalid access token.
        Observed causes:
            Invalid Token key used,
    """   
class ParameterSyntaxError(Error):
    """Exception raised for Syntax Errors in params of a request"""
    def __init__(self,message):
        self.message=message
class UndefinedMessageError(Error):
    """Exception raised for unhandled errors."""

    def __init__(self, message):
        self.message = message

class OAuth2InvalidClientError(Error):
    """Exception raised for an Invalid Client ID or Secret"""

class UndefinedFaultStringError(Error):
    """Exception raised for unhandled errors."""

    def __init__(self,expression, message):
        self.message = message
        self.expression = expression
class IWasNotProgramedForThisError():
    """Exception raised when the passed exception cannot be handled"""