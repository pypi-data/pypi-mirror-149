from sys import platform
import pandas as pd
import os
from simple_salesforce import Salesforce
from simple_salesforce import SalesforceLogin
from salesforce_bulk import SalesforceBulk
from sfdclib import SfdcSession
from sfdclib import SfdcMetadataApi
from sfdclib import SfdcToolingApi
import re
import time
import json
from salesforce_bulk.util import IteratorBytesIO
import pandas as pd
import requests
import base64
from typing import List, Tuple, Optional

class Sf:
    def __init__(self) -> None:
        self.filename: str = None
        self.os_platform: str = platform
        self.credentials: pd.DataFrame = pd.DataFrame()
        self.sfUsername: str = None
        self.sfPassword: str = None
        self.sfOrgId: str = None
        self.isSandbox: bool = None
        self.session_id: str = None
        self.instance: str = None
        self.domain: str = None
        self.security_token: str = ''
        self.sf: Salesforce = None
        self.bulk: SalesforceBulk = None
        self.sfMeta: SfdcMetadataApi = None
        self.tooling: SfdcToolingApi = None
        self.api_version: str = 'v52.0'
        self.record_count: dict = {}
        self.record_count_caseinsensitive: dict = {}
        self.debug: bool = False
        
    def query(self, query: str, excludedFields: Optional[List] = []) -> pd.DataFrame:
        """
        Using SFDC SOQL Syntax, and allowing for Relationships and group bys. 
        
        Arguments:
            query (str): A Standard SFDC SOQL Query allowing for relationships (Owner.Name)
                Asterisks(*) represents all queryable fields and can be used in conjunction
                with other relationship fields. 
                i.e. (Select *, Owner.Profile.Name, Owner.Name From Account)
        
        Returns:
            Pandas Dataframe Object.
        
        Raises:
            KeyError: Typically raised when 0 records exist for the object
                
            badfield: A self-correcting error that is raised when a field is unqueriable, i.e. Address Fields
            
            Exception: When relationship query contains more than 4 layers, an Exception is raised.
            i.e. Parent_Account_vod__r.Owner.Profile.LastModifiedBy.Name (<- a 5 layer deep relationship is not supported)
        
        Example of Usage:
            sf.query("Select *, Owner.Profile.Name From Account ORDER BY CreatedDate DESC LIMIT 100")
            
            return:
            A Pandas Dataframe of the last created 100 account records, with all queriable fields included in the query and a relationship field.
            
        """
        objectName = re.search('(?<=from )\w*', query.lower()).group(0)
        successful = False
        
        extracted_object = pd.DataFrame()
        # replaces "*" in query with all fields on object
        sfSchema = getattr(self.sf, objectName).describe().get('fields')

        schemaDict = {}
        for x in sfSchema:
            schemaDict[x['name']] = x

        while not successful:
            try:
                results = []
                for field in schemaDict:
                    if (schemaDict[field]['type'] != 'location' and 
                        schemaDict[field]['type'] != 'address' and 
                        schemaDict[field]['name'] not in excludedFields):
                        results.append(field)
                final_query = query.replace("*", ", ".join(results))                
#                 # if the object has 0 records in Salesforce, return empty dataframe
#                 if objectName not in self.record_count_caseinsensitive.keys():
#                     return pd.DataFrame(columns=results)
                query_response = self.sf.query_all(final_query)
                result = pd.DataFrame(query_response)['records']
                for _ in result:
                    del _['attributes']
                successful = True
            except KeyError:
                if self.debug:
                    print(objectName + ' skipped. (Potentially due to no records found.)')
                    
                return pd.DataFrame(columns=results)
            except Exception as badfield:
                field_exclusion = badfield.state_message[badfield.state_message.find("No such column '")+\
                    16:badfield.state_message.find("No such column '")+16+\
                        badfield.state_message[badfield.state_message.find("No such column '")+16:].find("'")]
                excludedFields.append(field_exclusion)
                print("Excluded unqueriable field: " + field_exclusion)
                if query.find("*") == -1:
                    raise Exception(f"Unqueriable field {field_exclusion} found in query.")
                else:
                    continue
            
            result = result.apply(lambda x: pd.Series(x)).copy()

            relationship_fields_preparsed = re.search('(?<=select )(.*?)(?= from)', query,  re.IGNORECASE).group(0).split(",")
            # relationship_fields_prepared Example:
            # ['*',
            #  ' Parent_Account_vod__r.Owner.Profile.Name',
            #  ' Child_Account_vod__r.Owner.Profile.Name',
            #  'Parent_Account_vod__r.Owner.Profile.Id ']

            relational_fields = [{x.strip(): x.strip().split(".")} for x in relationship_fields_preparsed if "." in x]
            # relationship_fields Example:
            # [{'Parent_Account_vod__r.Owner.Profile.Name': ['Parent_Account_vod__r',
            #    'Owner',
            #    'Profile',
            #    'Name']},
            #  {'Child_Account_vod__r.Owner.Profile.Name': ['Child_Account_vod__r',
            #    'Owner',
            #    'Profile',
            #    'Name']},
            #  {'Parent_Account_vod__r.Owner.Profile.Id': ['Parent_Account_vod__r',
            #    'Owner',
            #    'Profile',
            #    'Id']}]

            columns_to_remove = set()
            for x in relational_fields:
                if len(list(x.values())[0]) > 4:
                    raise Exception("Too Many Relationship Levels. The Query you have entered contains more than 4 levels deep and is not supported.")
                elif len(list(x.values())[0]) == 4:
                    result[list(x.keys())[0]] = result[list(x.keys())[0].split(".")[0]].\
                        apply(lambda z: z[list(x.values())[0][1]][list(x.values())[0][2]][list(x.values())[0][3]])
                    columns_to_remove.add(list(x.values())[0][0])
                elif len(list(x.values())[0]) == 3:
                    result[list(x.keys())[0]] = result[list(x.keys())[0].split(".")[0]].\
                        apply(lambda z: z[list(x.values())[0][1]][list(x.values())[0][2]])
                    columns_to_remove.add(list(x.values())[0][0])
                elif len(list(x.values())[0]) == 2:
                    result[list(x.keys())[0]] = result[list(x.keys())[0].split(".")[0]].\
                        apply(lambda z: z[list(x.values())[0][1]])
                    columns_to_remove.add(list(x.values())[0][0])
            result.drop(columns_to_remove, axis=1, inplace=True)        

                
        return result
    
    def retrieve_credentials(self,
                                os_platform: Optional[str] = None, 
                                filename: Optional[str] = None, 
                                *args, **kwargs) -> Tuple[dict, pd.DataFrame]:
        """
        Retrieves the credential file from the current working directory 
        and returns the credentials file dataframe.
        Arguments:
            os_platform (str - Optional): String value of the plaform for which
            this script is ran on. i.e. "linux", "win32", "darwin"

            filename (str - Optional): The name of the credentials.xlsx file in the current
            working directory folder.


        Example:
            retrieve_credentials(platform, 'credentials.xlsx')

        Return Example:
            ({'sfUsername': 'michael.pay@verteo.biopharma.com',
              'sfPassword': 'aq539z12315123423TRP9',
              'sfOrgId': '00T3T000000FZCq',
              'isSandbox': True,
              'networkURL': 'https://verteodev.veevanetwork.com',
              'networkUserName': 'michael.pay@verteo.veevanetwork.com',
              'networkPassword': 'ipiJi2315fasdrwqetX6zp1',
              'networkCountry': 'AU;HK;NZ;TJ;TT;TN;TR;TM;UA;AE;UY;UZ;VE;YE;BM;CA;US'},
              ## credentials.xlsx pandas dataframe ##
            )

        Dependencies:
            from sys import platform
            import pandas as pd
            import os
        """
        self.os_platform = self.os_platform if os_platform is None else os_platform
        self.filename = self.filename if filename is None else filename
        
        assert filename is not None, \
            "Please provide a file name to the credentials file (i.e. Sf.retrieve_credentials(filename='credentials.xlsx'))"
        
        if os_platform =="darwin" or os_platform == "linux" or os_platform == "linux2":
            credentials = pd.read_excel(os.getcwd() + "/" + filename)
        elif platform == "win32":
            credentials = pd.read_excel(os.getcwd() + "\\" + filename)
        else:
            credentials = pd.DataFrame()
        sfUsername = self.sfUsername = credentials['Salesforce Username'][0]
        sfPassword = self.sfPassword = credentials['Salesforce Password'][0]
        sfOrgId = self.sfOrgId = credentials['Salesforce Org Id'][0]
        isSandbox = self.isSandbox = True if credentials['Sandbox Org?'][0]=="Yes" else False
        networkURL = self.networkURL = credentials['Salesforce Username'][3]
        networkUserName = self.networkUserName = credentials['Salesforce Password'][3]
        networkPassword = self.networkPassword = credentials['Salesforce Org Id'][3]
        networkCountry = self.networkCountry = credentials['Sandbox Org?'][3]

        return {'sfUsername':sfUsername, 
                'sfPassword':sfPassword, 
                'sfOrgId':sfOrgId, 
                'isSandbox':isSandbox, 
                'networkURL':networkURL, 
                'networkUserName':networkUserName,
                'networkPassword':networkPassword,
                'networkCountry':networkCountry}, credentials
    
    def authenticate_salesforce(self, sfUsername: Optional[str]=None, 
                                sfPassword: Optional[str]=None, 
                                sfOrgId: Optional[str]=None, 
                                isSandbox: Optional[str]=None, 
                                session_id: Optional[str]=None, 
                                instance: Optional[str]=None, 
                                security_token: Optional[str] = None,
                                domain: Optional[str] = None,
                                if_return: Optional[bool] = False,
                                *args, **kwargs) -> Optional[dict]:
        """
        Authenticates Salesforce and retrieves the auth token.

        Example:
        authenticate using unpacked kwargs from the retrieve_credentials function
            authenticate_salesforce(**retrieve_credentials(platform, 'credentials.xlsx')[0])

        Return Example:
            {'sf': <simple_salesforce.api.Salesforce at 0x24a045c7b50>,
             'bulk': <salesforce_bulk.salesforce_bulk.SalesforceBulk at 0x24a045c7e20>,
             'sfMeta': <sfdclib.session.SfdcSession at 0x24a044b3400>,
             'tooling': <sfdclib.tooling.SfdcToolingApi at 0x24a045d17f0>,
             'session_id': '00D3F000000FZCq!AQYAQHYfSLYGI9cTyjD...PuuzNnZNb3461sUGeUZ57ttE.GBawbt5h',
             'instance': 'cslbehring-core--devr01.my.salesforce.com',
             'sfMeta_is_connected': True,
             'bulk_api_sessionId': '00D3F000000FZCq!AQYAQHYfSLYGI9cTyjD...PuuzNnZNb3461sUGeUZ57ttE.GBawbt5h'}

        Dependencies:
            from simple_salesforce import Salesforce
            from simple_salesforce import SalesforceLogin
            from salesforce_bulk import SalesforceBulk
            from sfdclib import SfdcSession
            from sfdclib import SfdcMetadataApi
            from sfdclib import SfdcToolingApi
        """
        
        sfUsername = self.sfUsername if sfUsername is None else sfUsername
        sfPassword = self.sfPassword if sfPassword is None else sfPassword
        sfOrgId = self.sfOrgId if sfOrgId is None else sfOrgId
        isSandbox = self.isSandbox if isSandbox is None else isSandbox
        session_id = self.session_id if session_id is None else session_id
        instance = self.instance if instance is None else instance
        security_token = self.security_token if security_token is None else security_token
        domain = self.domain if domain is None else domain
        
        if session_id is not None and instance is not None:
            sf = Salesforce(session_id = session_id, instance_url = instance)
            self.sf = sf

        elif sfUsername is not None and sfPassword is not None and sfOrgId is not None and isSandbox is not None:
            if isSandbox:
                self.domain = 'test'
                sf = Salesforce(password=sfPassword, 
                                username=sfUsername, 
                                organizationId=sfOrgId, 
                                security_token = self.security_token,domain='test')
                session_id, instance = SalesforceLogin(
                username=sfUsername,
                password=sfPassword,
                security_token=self.security_token,
                domain= self.domain)
                self.session_id = session_id
                self.instance = instance
                self.sf = sf
            else:
                sf = Salesforce(password=sfPassword, 
                                username=sfUsername, 
                                organizationId=sfOrgId, 
                                security_token=self.security_token)
                session_id, instance = SalesforceLogin(
                username=sfUsername,
                password=sfPassword,
                security_token=self.security_token)
                self.session_id = session_id
                self.instance = instance
                self.sf = sf
        else:
            raise Exception('Either sfUsername, sfPassword, sfOrgId and isSandbox must be populated, OR session_id and instance must be populated.')

        # bulk = SalesforceBulk(username=sfUsername, password=sfPassword, security_token='')
        bulk = SalesforceBulk(sessionId = session_id, host = instance)
        self.bulk = bulk
        
        sfMeta = SfdcSession(session_id=session_id, instance=instance)
        self.sfMeta = sfMeta
    #     sfMeta = SfdcSession(username=sfUsername,password=sfPassword,token='',is_sandbox=isSandbox)
        sfMeta._api_version = "51.0"

        tooling = SfdcToolingApi(sfMeta)
        self.tooling = tooling
        
        self.api_version = 'v' + self.sf_api_call('/services/data')[-1]['version']
        
        for x in self.sf_api_call('/services/data/'+self.api_version+'/limits/recordCount')['sObjects']:
            self.record_count[x['name']] = x['count']
            self.record_count_caseinsensitive[x['name'].lower()] = x['count']
        
        if if_return:
            return {'sf':sf, 
                    'bulk':bulk, 
                    'sfMeta': sfMeta, 
                    'tooling':tooling, 
                    'session_id':session_id, 
                    'instance':instance, 
                    'sfMeta_is_connected':sfMeta.is_connected(), 
                    'bulk_api_sessionId':bulk.sessionId}

    def extract_bulk(self, og_query: str, 
                        excludedFields: Optional[List] = []) -> pd.DataFrame:
        """
        Uses a standard SOQL query to extract Salesforce Data and outputs a pandas dataframe
        
        Dependencies:
            import re
            import time
            import json
            from salesforce_bulk.util import IteratorBytesIO
            import pandas as pd
        
        """
        objectName = re.search('(?<=from )\w*', og_query.lower()).group(0)
        successful = False
        
        extracted_object = pd.DataFrame()
        # replaces "*" in query with all fields on object
        sfSchema = getattr(self.sf, objectName).describe().get('fields')

        schemaDict = {}
        for x in sfSchema:
            schemaDict[x['name']] = x

        while not successful:
            try:
                results = []
                for field in schemaDict:
                    if (schemaDict[field]['type'] != 'location' and 
                        schemaDict[field]['type'] != 'address' and 
                        schemaDict[field]['name'] not in excludedFields):
                        results.append(field)
                query = og_query.replace("*", ", ".join(results))
                
#                 # if the object has 0 records in Salesforce, return empty dataframe
#                 if objectName not in self.record_count_caseinsensitive.keys():
#                     return pd.DataFrame(columns=results)
                    
                job = self.bulk.create_query_job(objectName, contentType='JSON')
                batch = self.bulk.query(job, query)
                while not self.bulk.is_batch_done(batch):
                    time.sleep(1)
                sfdf = pd.DataFrame()
                for result in self.bulk.get_all_results_for_query_batch(batch):
                    result = json.load(IteratorBytesIO(result))
                    sfdf = sfdf.append(pd.DataFrame(result))

                # drops attributes column in dataframe
                sfdf.drop(columns="attributes", inplace = True)

                # formats all datetime to the proper formatting
                for column in sfdf:
                    if schemaDict[column]['type'] == 'datetime':
                        sfdf[column] = pd.to_datetime(sfdf[column], unit='ms')
                    # if the column has a 'scale' or salesforce's decimal places, then turn the column into an int
                    elif schemaDict[column]['type'] == 'double' and schemaDict[column]['scale'] == 0:
                        sfdf[column] = pd.to_numeric(sfdf[column], downcast='integer')

            #                         pd.to_datetime(sfdf[column], unit = 's')
            #                         sfdf[column].apply(lambda x : datetime.fromtimestamp(int(x), tz).isoformat())
            #                 sfdf.convert_dtypes()
                # converts the output of the bulk query to text so that the unix timestamp displays property, and fills and empty values with the '' string.
                sfdf = sfdf.fillna('').astype(str)
                successful = True
            except KeyError:
                if self.debug:
                    print(objectName + ' skipped. (Potentially due to no records found.)')
                    
                return pd.DataFrame(columns=results)
            except Exception as badfield:
                field_exclusion = badfield.state_message[badfield.state_message.find("No such column '")+\
                    16:badfield.state_message.find("No such column '")+16+\
                        badfield.state_message[badfield.state_message.find("No such column '")+16:].find("'")]
                excludedFields.append(field_exclusion)
                print("Excluded unqueriable field: " + field_exclusion)
                if og_query.find("*") == -1:
                    raise Exception(f"Unqueriable field {field_exclusion} found in query.")
                else:
                    continue
        if self.debug:
            print("Extracted " + objectName + " successfully!")
        return sfdf
    
    def join(self, 
                dataframe, 
                rt_dataframe, 
                left_on="", 
                right_on="", 
                new_columns=[], 
                suffix = "_new"):
        """
        Joins and appends the Name and DeveloperName columns of record type to the dataframe.
        The dataframe must contain a column named "RecordTypeId" with the 18 digit SFID of the record type.
        """
        df_columns = dataframe.columns.to_list()
        if right_on not in new_columns:
            new_columns.insert(0,right_on)
        dataframe = pd.merge(dataframe, rt_dataframe[new_columns], how = 'inner', 
                                left_on = left_on,right_on = right_on, suffixes=('', suffix))
#         dataframe.drop([col for col in dataframe.columns if 'drop' in col], axis=1, inplace=True)
        return dataframe


    
    def object_describe(self, sobject_api_name):
        """
        TODO:
        
        Description of what it does
        
        Description of arguments and data types
        
        Description of return values and data types
        
        Description of Errors raised
        
        Extra Notes and Examples of Usage
        """
        return getattr(self.sf, sobject_api_name).describe()
    
    
    def field_describe(self, objects = ['Account','Address_vod__c','Child_Account_vod__c'], attributes = ['name','type','length']):
        """
        TODO:
        
        Description of what it does
        
        Description of arguments and data types
        
        Description of return values and data types
        
        Description of Errors raised
        
        Extra Notes and Examples of Usage
        """
        outputList = []
        columnNames = []
        for sObjectAPIName in objects:
            for attribute in attributes:
                outputList.append([field[attribute] for field in getattr(self.sf, sObjectAPIName).describe()['fields']])
                if attribute == "name":
                    columnNames.append(sObjectAPIName)
                else:
                    columnNames.append(attribute.title())
        field_describe = pd.DataFrame(outputList).transpose()
        field_describe.columns = columnNames
        return field_describe
    
    def picklist_dataframe_stacked(self,objects=['Account','Address_vod__c','Child_Account_vod__c']):
        """
        TODO:
        
        Description of what it does
        
        Description of arguments and data types
        
        Description of return values and data types
        
        Description of Errors raised
        
        Extra Notes and Examples of Usage
        """
        output_df = pd.DataFrame()
        for object in objects:
            objectDescribe = getattr(self.sf, object).describe()
            processing_df = pd.DataFrame(pd.DataFrame([pd.Series(data = [picklist['value'] for picklist in field['picklistValues']], 
                                                                   name = object + "." + field["name"]) for field in objectDescribe['fields'] if field['type'] == 'picklist']).stack())
            processing_df.columns = ['Picklist API Value']
            processing_df['CRM Object and Field API'] = processing_df.index.get_level_values(0)
            processing_df[['CRM Object API','CRM Field API']] = processing_df['CRM Object and Field API'].str.split(".", expand = True)
            processing_df.reset_index(drop=True, inplace=True)
            output_df = output_df.append(processing_df)
        return output_df

    def picklist_dataframe(self,objects = ['Account','Address_vod__c','Child_Account_vod__c']):
        """
        TODO:
        
        Description of what it does
        
        Description of arguments and data types
        
        Description of return values and data types
        
        Description of Errors raised
        
        Extra Notes and Examples of Usage
        """
        referenceList = []
        for object in objects:
            objectDescribe = getattr(self.sf, object).describe()
            objectPicklistValues = pd.DataFrame(index=range(0,max(len(field["picklistValues"]) for field in objectDescribe['fields'] if field['type'] == 'picklist')))
            for x in [pd.Series(data = [picklist['value'] for picklist in field['picklistValues']], name = object + "." + field["name"]) for field in objectDescribe['fields'] if field['type'] == 'picklist']:
                objectPicklistValues.insert(0, str(x.name), x)
            referenceList.append(objectPicklistValues)
        return referenceList
    
    def record_type_retrieval(self, objectAPIName, fieldAPINames = ["Id","Name",'SobjectType']):
        """
        TODO:
        
        Description of what it does
        
        Description of arguments and data types
        
        Description of return values and data types
        
        Description of Errors raised
        
        Extra Notes and Examples of Usage
        """
        sfRTDF = pd.DataFrame(self.sf.query("SELECT "+ ",".join(fieldAPINames) + " from RecordType WHERE SobjectType = '" + objectAPIName + "'")['records'])
        sfRTDF.drop(columns="attributes", inplace = True)
        return sfRTDF
    
    def sf_api_call(self, action, parameters = {}, method = 'get', data = {}):
        """
        Helper function to make calls to Salesforce REST API.
        Parameters: action (the URL), URL params, method (get, post or patch), data for POST/PATCH.
        """
        headers = {
            'Content-type': 'application/json',
            'Accept-Encoding': 'gzip',
            'Authorization': 'Bearer %s' % self.session_id
        }
        if method == 'get':
            r = requests.request(method, 'https://'+self.instance+action, headers=headers, params=parameters, timeout=30)
        elif method in ['post', 'patch']:
            r = requests.request(method, 'https://'+self.instance+action, headers=headers, json=data, params=parameters, timeout=10)
        else:
            # other methods not implemented in this example
            raise ValueError('Method should be get or post or patch.')
#         print('Debug: API %s call: %s' % (method, r.url) )
        if r.status_code < 300:
            if method=='patch':
                return None
            else:
                return r.json()
        else:
            raise Exception('API error when calling %s : %s' % (r.url, r.content))