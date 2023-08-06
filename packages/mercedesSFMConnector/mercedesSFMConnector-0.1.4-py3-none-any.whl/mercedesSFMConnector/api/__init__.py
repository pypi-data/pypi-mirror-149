from mercedesSFMConnector.api.measure_groups import MeasureGroups
from mercedesSFMConnector.api.measures import Measures
from mercedesSFMConnector.api.external_values import ExternalValues
from mercedesSFMConnector.token_handler import TokenHandler
import os
import requests

#purpose is to handle api calls
class Api(Measures, MeasureGroups, ExternalValues):
    """
    Class to handle API calls to SFM

    Attributes:
        sfm_url (str): Base api url for SFM
        headers(obj): Headers for the api requests
    
    Methods: 
        generic_call
    """
    def __init__(
        self, 
        sfm_url: str = os.getenv('SFM_URL'), 
        gas_url: str = os.getenv('GAS_URL'), 
        client_id: str = os.getenv('SFM_TECH_USER_CLIENT_ID'), 
        client_secret: str = os.getenv('SFM_TECH_USER_CLIENT_SECRET')
        ) -> None:
        """
        __init__

        Args:
            sfm_url: BASE url for SFM. Ex. https://base-sfm-url.corpintra.net
            gas_url: BASE url for GAS.
            client_id: technical client id for SFM
            client_secret: technical client secret for SFM
        """
        if sfm_url == None or gas_url == None or client_id == None or client_secret == None:
            raise ValueError("Please specify parameters or place them in your .env file")
        self.__token_handler = TokenHandler(
            gas_url=gas_url, 
            sfm_url=sfm_url, 
            client_id=client_id, 
            client_secret=client_secret
            )
        self.sfm_url = f"{sfm_url}/rest/api"
        self.headers = {
            'Authorization': f"Bearer {self.__token_handler.access_token}"
        }
        
    def generic_call(self, endpoint: str, params:object = {}, body: object = {}, method: str ='GET') -> object:
        """
        Method to allow api calls if library ever outdated. Allows you to specify custom endpoints, methods, bodies, etc.

        Args:
            endpoint: the endpoint you wish to request
            params: query parameters 
            body: body for the request
            method: request method

        Returns:
            API response from query
        """
        api_resp = {}
        if method == 'GET':
            api_resp = requests.get(url=f"{self.sfm_url}/{endpoint}", params=params, headers=self.headers, verify=False).json()
        elif method == 'POST':
            api_resp = requests.post(url=f"{self.sfm_url}/{endpoint}", params=params, data=body, headers=self.headers, verify=False).json()

        return api_resp

