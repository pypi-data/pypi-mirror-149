import requests
from datetime import datetime
class ExternalValues:
    def upload_external_values(self, external_values, measure_type, measure_date = datetime.isoformat(datetime.now())):
        """
        Function to put external values 

        Parameters:
            external_values: array of external values to put
        """
        api_resp = requests.put(
                        url=f"{self.sfm_url}/Integration/ExternalValues", 
                        headers=self.headers, 
                        json=external_values,
                        params={'measureDate': measure_date, 'measureType': measure_type},
                        verify=False
                    )
        if api_resp.status_code < 300:
            return api_resp.json()
        else:
            raise Exception('Error with uploading: ', api_resp.json())
    