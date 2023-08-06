from typing import List
import requests
import asyncio
import concurrent.futures

class MeasureGroups:
    def get_measure_groups(self,forum_id: str):
        """
        Function to grab all measure groups for a forum structure

        Parameters:
            forum_id: forum structure to get measures from
        """
        api_resp = requests.get(
                        url=f"{self.sfm_url}/ForumStructures/{forum_id}/MeasureGroups", 
                        headers=self.headers, 
                        verify=False
                    )
        if api_resp.status_code == 200:
            return api_resp.json()
        else:
            return api_resp
    def create_measure_groups(self,forum_id: str, names: List[str]):
        """
        Checks if a measure group with name already exists. 
        If not, it makes a measure group with the specified name on the specified forum structure

        Paramters: 
            forum_id: the forum_id to create the measure group for
            names: the names of each measure group you want to create
        Returns:
            {success: [], failed: [], already_exist: []}
        
        """
        resp = {'success': [], 'failed':[], 'already_exist': []}
        try:
            measure_groups = requests.get(
                url=f"{self.sfm_url}/ForumStructures/{forum_id}/MeasureGroups", 
                headers=self.headers, 
                verify=False
            ).json()
            for name in names:
                temp = False
                for measure_group in measure_groups:
                    if measure_group['GroupName'] == name:
                        temp = True
                if not temp:
                    api_resp = requests.put(
                        url=f"{self.sfm_url}/ForumStructures/{forum_id}/MeasureGroups", 
                        params={'name': name}, 
                        headers=self.headers, 
                        verify=False
                    )
                    if api_resp.status_code < 300:
                        resp['success'].append(api_resp.json())
                    else:
                        resp['failed'].append(api_resp.json())
                else:
                    resp['already_exist'].append(name)
            if len(resp['already_exist']) > 0:
                print('These names already exist', resp['already_exist'])
        except Exception as e :
            print(e)
        return resp
    
    
    def delete_measure_groups(self, measure_groups: List[str] = []):
        resp = {'success': 0, 'failed':0, 'errors': []}
        for measure_group_id in measure_groups:
            try:
                api_resp = self.delete_measure_group(measure_group_id)

                if (200 == api_resp.status_code):
                    resp['success']+=1
                else:
                    raise Exception({'status_code': api_resp.status_code,'resp':api_resp.json()})
            except Exception as e:
                resp['failed']+=1
                resp['errors'].append(e)
        return resp
    
    def delete_measure_group(self, measure_group_id: str):
        
        if (self.DEBUG):
            print(f"Deleting measure group '{measure_group_id}'")
        api_resp = requests.delete(
            url=f"{self.sfm_url}/MeasureGroups/{measure_group_id}",
            headers=self.headers, 
            verify=False
        )
        if (api_resp.status_code in (400, 500)):
            self.clean_measure_group(measure_group_id)
            api_resp = requests.delete(
                url=f"{self.sfm_url}/MeasureGroups/{measure_group_id}",
                headers=self.headers, 
                verify=False
            )
        if (self.DEBUG):
            print('delete measure group resp',api_resp.json())
        return api_resp
    
    def move_measures(self, measure_group_id: str, measures: List[str] = []):
        
        if (self.DEBUG):
            print(f"Moving {len(measures)} measures into group {measure_group_id}")
        api_resp = requests.put(
            url=f"{self.sfm_url}/MeasureGroups/{measure_group_id}/Measures",
            json=measures,
            headers=self.headers,
            verify=False
        )
        if (self.DEBUG):
            print('move measure resp', api_resp.json())
        return api_resp

    
    # def delete_measure_groups(self, measure_groups: List[str] = []):
    #     resp = {'success': 0, 'failed':0, 'errors': []}
        
    #     async def looper(measure_groups):
    #         with concurrent.futures.ThreadPoolExecutor() as executor:
                
    #             loop = asyncio.get_event_loop()
    #             futures = [loop.run_in_executor(executor, self.delete_measure_group, measure_group_id) for measure_group_id in measure_groups]
    #             for response in await asyncio.gather(*futures):
    #                 try:
    #                     if (200 == response.status_code):
    #                         resp['success']+=1
    #                     else:
    #                         raise Exception({'status_code': response.status_code,'resp':response.json()})
    #                 except Exception as e:
    #                     resp['failed']+=1
    #                     resp['errors'].append(e)
                    
    #     asyncio.run(looper(measure_groups))
    #     return resp
    
    # def delete_measure_group(self, measure_group_id: str):
    #     if (self.DEBUG):
    #         print(f"Deleting measure group '{measure_group_id}'")
    #     api_resp = requests.delete(
    #         url=f"{self.sfm_url}/MeasureGroups/{measure_group_id}",
    #         headers=self.headers, 
    #         verify=False
    #     )
        
    #     if (400 == api_resp.status_code):
    #         if (self.DEBUG):
    #             print(api_resp.json())
    #         self.clean_measure_group(measure_group_id)
    #         api_resp = requests.delete(
    #             url=f"{self.sfm_url}/MeasureGroups/{measure_group_id}",
    #             headers=self.headers,
    #             verify=False
    #         )
    #     if (self.DEBUG):
    #         print(api_resp.json())
    #     return api_resp