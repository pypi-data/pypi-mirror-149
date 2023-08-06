from typing import List, Union
import requests
class Measures:
    """
    Class containing methods to work with Measures through the SFM API
    """
    def get_measure_id(self, *object_ids: Union[str, List[str]]) -> List[str]:
        """
        Gets the measure id from SFM for a given object id in case you do
        not already have the measure id for the source you are getting values from. 
        This is needed because there is no api endpoint for trend data in SFM
        that takes object id as a paremeter, meaning you have to have the 
        measure id if you want trend data

        Args: 
            object_id (Union[str, List[str]]): The object id you want to get the measure_id for
            token (str): The token used to authenticate the api request
        
        Returns:
            measure_ids (List[str]): returns a list of measure ids
        """
        measure_ids = []
        for object_id in object_ids:
            measure_resp = requests.get(url=f"{self.sfm_url}/Measures", params={'dataobject_id': object_id}, headers=self.headers, verify=False).json()
            measure_id = measure_resp["Results"][0]['Id']
            measure_ids.append(measure_id)
        return measure_ids
    def update_measures(self, measures) -> object:
        
        """
        Creates a measure

        Args:
            measures: list of measure objects to create
            measure_group_id: Desired measure group to assign measure to
            title: desired title for the measure
            measure_type: Type of measure. Ex. 'Daily'
            description: Description of measure
            dependents (List[str], optional): list of the measure id's to include as dependents of this measure. Defaults to []
        """
        resp = {'success': [], 'failed': []}
        for measure in measures:
            params={
                "Title": measure['title'],
                "MeasureType": measure['measure_type'],
                "Definition": measure['definition'],
                "Description": measure['description'],
                "Source": measure['source'],
                "ValueSource": "External",
                "TargetSource": "None",
                "Category": measure['category'],
                "ShowLastValidValue": measure['show_last_valid_value'],
                "BaseType": measure['base_type'],
                "AggregateFunction": measure['aggregate_func'],
                "Dependents": measure['dependents'] if 'dependents' in measure else [],
                "TileDisplayType": "StandardTile",
                "TrendDisplayType": measure['trend_display_type'],
                "TargetType": measure['target_type'],
                "TargetBoundaries": measure['target_boundaries']
            }
            created_measure = requests.put(url=f"{self.sfm_url}/Measures/{measure['measure_id']}", json=params, headers=self.headers, verify=False)
            if created_measure.status_code <300:
                #201 is created
                resp['success'].append(created_measure.json())
            else:
                resp['failed'].append(created_measure.json())
        return resp
    
    def create_measure(self, measure) -> object:
        params={
                "Title": measure['title'],
                "MeasureType": measure['measure_type'],
                "Definition": measure['definition'],
                "Description": measure['description'],
                "Source": measure['source'],
                "ValueSource": "External",
                "TargetSource": "None",
                "Category": measure['category'],
                "ShowLastValidValue": measure['show_last_valid_value'],
                "BaseType": measure['base_type'],
                "AggregateFunction": measure['aggregate_func'],
                "Dependents": measure['dependents'] if 'dependents' in measure else [],
                "TileDisplayType": "StandardTile",
                "TrendDisplayType": measure['trend_display_type'],
                "TargetType": measure['target_type'],
                "TargetBoundaries": measure['target_boundaries']
            }
        return requests.post(url=f"{self.sfm_url}/MeasureGroups/{measure['measure_group_id']}/Measures", json=params, headers=self.headers, verify=False)
    
    def create_measures(self, measures) -> object:
        
        """
        Creates a measure

        Args:
            measures: list of measure objects to create
            measure_group_id: Desired measure group to assign measure to
            title: desired title for the measure
            measure_type: Type of measure. Ex. 'Daily'
            description: Description of measure
            dependents (List[str], optional): list of the measure id's to include as dependents of this measure. Defaults to []
        """
        resp = {'success': [], 'failed': []}
        for measure in measures:
            params={
                "Title": measure['title'],
                "MeasureType": measure['measure_type'],
                "Definition": measure['definition'],
                "Description": measure['description'],
                "Source": measure['source'],
                "ValueSource": "External",
                "TargetSource": "None",
                "Category": measure['category'],
                "ShowLastValidValue": measure['show_last_valid_value'],
                "BaseType": measure['base_type'],
                "AggregateFunction": measure['aggregate_func'],
                "Dependents": measure['dependents'] if 'dependents' in measure else [],
                "TileDisplayType": "StandardTile",
                "TrendDisplayType": measure['trend_display_type'],
                "TargetType": measure['target_type'],
                "TargetBoundaries": measure['target_boundaries']
            }
            created_measure = requests.post(url=f"{self.sfm_url}/MeasureGroups/{measure['measure_group_id']}/Measures", json=params, headers=self.headers, verify=False)
            if created_measure.status_code <300:
                #201 is created
                resp['success'].append(created_measure.json())
            else:
                resp['failed'].append(created_measure.json())
        return resp

    def delete_measure(self, measure_group_id: str, measure_id: str) -> bool:
        
        if (self.DEBUG):
            print(f"Deleting measure '{measure_id}' in measure group '{measure_group_id}'")
        resp = requests.delete(
            url=f"{self.sfm_url}/MeasureGroups/{measure_group_id}/Measures",
            params={'measureId': measure_id},
            headers=self.headers, 
            verify=False
        )
        
        if resp.status_code>=400:
            
            if (self.DEBUG):
                print(f"failed first time to delete measure '{measure_id}' in measure group '{measure_group_id}'. Trying to remove parents from current measure", resp.json())
            parents = requests.get(
                url=f"{self.sfm_url}/Measures/{measure_id}/Parents",
                headers=self.headers, 
                verify=False
            ).json()
            for parent in parents:
                # convert to function and add mutex?
                parent_resp = requests.get(
                    url=f"{self.sfm_url}/Measures/{parent['Id']}",
                    headers=self.headers, 
                    verify=False
                )
                if parent_resp.status_code == 500:
                    self.delete_measure(parent['MeasureGroupId'], parent['Id'])
                    parent_resp = requests.get(
                        url=f"{self.sfm_url}/Measures/{parent['Id']}",
                        headers=self.headers, 
                        verify=False
                    )
                
                m = parent_resp.json()
                
                if len(m['Dependents'])>1:
                    m['Dependents'] = [x['Id'] for x in m['Dependents'] if x['Id'] != measure_id]
                else:
                    m['ValueSource'] = 'External' if m['ValueSource']=='Aggregated' else m['ValueSource']
                    m['TargetSource'] = 'External' if m['TargetSource']=='Aggregated' else m['ValueSource']
                requests.put(
                    url=f"{self.sfm_url}/Measures/{parent['Id']}",
                    data=m,
                    headers=self.headers, 
                    verify=False
                ).json()
            resp = requests.delete(
                url=f"{self.sfm_url}/MeasureGroups/{measure_group_id}/Measures",
                params={'measureId': measure_id},
                headers=self.headers, 
                verify=False
            )
        return 200 <= resp.status_code < 300

    def clean_measure_group(self, measure_group_id: str, keep: list = [], keep_property: str = 'Id'):
        
        measures = requests.get(
            url=f"{self.sfm_url}/Measures",
            params={'measureGroupId': measure_group_id},
            headers=self.headers, 
            verify=False
        ).json()
        rerun = measures['IsResultsLimited']
        measures = [x for x in measures['Results'] if x[keep_property] not in keep]
        measures = sorted(measures, key = lambda x: x['ValueSource'])
        if (self.DEBUG):
            print(f"Deleting {len(measures)} measures in group '{measure_group_id}'")
        resp = {'success': 0, 'failed':0, 'errors': []}
        for measure in measures:
            delete_check = self.delete_measure(measure_group_id, measure['Id'])
            if delete_check:
                resp['success']+=1
            else:
                resp['failed']+=1
        if (rerun):
            sub_resp = self.clean_measure_group(measure_group_id, keep, keep_property)
            resp['success']+=sub_resp['success']
            resp['failed']+=sub_resp['failed']
            resp['errors']+=sub_resp['errors']
        return resp
    
    def delete_measures_in_group(self, measure_group_id: str, delete_list: list = []):
        pass
    
    def delete_measures(self, measures: list = []):
        
        resp = {'success': 0, 'failed': 0, 'errors': []}
        for measure in measures:
            check_delete = self.delete_measure(measure['kpi_group_id'],measure['measure_id'])
            if check_delete:
                resp["success"]+=1
            else:
                resp['failed']+=1
                