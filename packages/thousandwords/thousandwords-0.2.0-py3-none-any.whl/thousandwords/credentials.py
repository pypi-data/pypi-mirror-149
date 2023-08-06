import boto3
from thousandwords.config import CONFIG
from thousandwords.auth import CognitoAuth

class CognitoCredentials:
  def __init__(self):
    self._cognito = boto3.client('cognito-identity')
    self._credentials = None
  
  @property
  def credentials(self):
    if self._credentials is None:
      auth = CognitoAuth()
      jwt_token = auth.get_or_refresh_token()
      logins = {
        f"cognito-idp.{CONFIG.cognito_region}.amazonaws.com/{CONFIG.user_pool_id}": jwt_token
      }
      resp = self._cognito.get_id(
        IdentityPoolId=CONFIG.identity_pool_id,
        Logins=logins
      )
      identityId = resp['IdentityId']
      resp = self._cognito.get_credentials_for_identity(
        IdentityId=identityId,
        Logins=logins
      )
      self._credentials = resp
      
    return self._credentials