from msilib.schema import Error
import os
import mercedesSFMConnector.token_handler.token_libs as libs 
    
class TokenHandler:
    """
    Class designed to handle gas and sfm token

    Attributes:
        gas_token_url: url used to get GAS token
        sfm_token_url: url used to get SFM token

    """
    def __init__(
        self, 
        gas_url: str = os.getenv('GAS_URL'), 
        sfm_url: str = os.getenv('SFM_URL'),
        client_id: str = os.getenv('SFM_TECH_USER_CLIENT_ID'),
        client_secret: str = os.getenv('SFM_TECH_USER_CLIENT_SECRET')
        ) -> None:
        self.gas_token_url = f"{gas_url}/as/token.oauth2"
        self.sfm_token_url = f"{sfm_url}/rest/api/token"
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.generate_access_token()
    
    @property
    def access_token(self):
        """
        str: Access token required in header in order to access SFM
        """
        return self.__access_token

    @access_token.setter
    def access_token(self, _value):
        raise Exception('Cannot set access_token. Run generate_access_token to generate a new token.')

    def generate_access_token(self):
        """
        Generates new SFM token. Used if token expires
        """
        self.__access_token = libs.get_SFM_token(
            client_id=self.__client_id, 
            client_secret=self.__client_secret,
            gas_token_url=self.gas_token_url,
            SFM_token_url=self.sfm_token_url
        )
