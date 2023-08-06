from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
import requests
requests.packages.urllib3.disable_warnings() 

#Get Gas Token
def get_gas_token(client_id, client_secret, gas_token_url):
    """
    Gets the token from GAS that validates the user. For this project, 
    the user is the SFM technical user. Token needs to be given to SFM in
    order to receive an access token from SFM.

    Returns: 
    string
        the access token from GAS needed to be passed to SFM.
    """

    #function that fetches the token.
    auth = HTTPBasicAuth(client_id, client_secret)
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=gas_token_url, auth=auth, headers={"Content-Type": "application/x-www-form-urlencoded"})
    return token['access_token']
#Format SFM Token Request
def get_SFM_token(client_id, client_secret, gas_token_url, SFM_token_url):
    """
    Gets the bearer token from SFM needed to authenticate API requests to SFM

    Returns:
    string
        returns the access token needed to authenticate future api requests
    """
    gas_token = get_gas_token(client_id, client_secret, gas_token_url)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    };
    creds = requests.post(url=SFM_token_url, headers=headers, data={'grant_type': 'token','access_token': gas_token}, verify=False)
    if creds.json()['access_token']:
        return creds.json()['access_token']
    else:
        raise Exception('No access token, bad techincal user credentials')