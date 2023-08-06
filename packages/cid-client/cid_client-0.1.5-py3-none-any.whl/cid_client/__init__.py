import json
from dataclasses import is_dataclass, asdict
import textwrap
import requests
import os
from .mapping import *
from enum import Enum

__all__ = ['CIDClient']


class CIDClient:
    """
    Main class for CID manipulation methods
    """
    __access_token = None
    __environment = None

    __graphql_env_endpoints = {
        'dev': 'https://pkynkv5pck.execute-api.us-east-2.amazonaws.com/dev/graphql',
        'prod': 'https://o56dder9y3.execute-api.us-east-2.amazonaws.com/prod/graphql',
        'sandbox': 'http://0.0.0.0:5000/graphql',
    }

    __cose_endpoints = {
        'dev': 'http://cose-ms-dev.coherentdigital.net:8000',
        'prod': 'http://cose-ms-prod.coherentdigital.net:8000',
        'sandbox': 'http://0.0.0.0:8080',
    }

    __graphql_endpoint = None

    def __init__(self, environment='prod', access_token=None):
        """
        Create instance of CIDClient.
        :param environment: PROD or DEV. If DEV specified - CIDs will be created in test database
        """
        if not environment or environment.lower() not in ['prod', 'dev', 'sandbox']:
            raise ValueError('Parameter environment must be set to "prod" or "dev" only')

        self.__graphql_endpoint = self.__graphql_env_endpoints[environment.lower()]
        self.__cose_endpoint = self.__cose_endpoints[environment.lower()]
        self.__environment = environment
        self.__access_token = access_token

    def __check_auth(self):
        if not self.__access_token:
            raise Exception('Authentication required. Call cid_client.authenticate_basic(login, password)')

    def __indent(self, s):
        return textwrap.indent(s, '    ')

    def __graphql_authenticate(self, login, password):
        """
        Produces GQL query for basic auth
        """
        return f"""
           query {{
              authenticate(login: "{login}", password: "{password}") {{
                status
                errorMessage
                accessToken
              }}
            }}
        """

    def __graphql_find_by_artifact(self, artifact):
        """
        Produces GQL query for getting CID by artifact
        """
        return f"""
           query {{
              findByArtifact(artifact: {json.dumps(artifact)}) {{
                total
                results
              }}
            }}
        """

    def __graphql_get_by_id(self, cid, text_fields=None):
        """
        Produces GQL query for getting CID by ID
        """
        return f"""
            query {{
                  getCID(cid: "{cid}") {{
                    ...cidFields
                  }}
                }}
        {get_fragments(text_fields)}
        """

    def __graphql_get_cid_children(self, cid, size=10):
        """
        Produces GQL query for getting the children of a CID
        """
        return f"""
           query {{
              searchCIDChildren(cid: "{cid}", size: {size}) {{
                total
                results
              }}
            }}
        """

    def __graphql_get_cid_siblings(self, cid, size=10):
        """
        Produces GQL query for getting the siblings of a CID
        """
        return f"""
           query {{
              searchCIDSiblings(cid: "{cid}", size: {size}) {{
                total
                results
              }}
            }}
        """

    def __graphql_mutation(self, mutation_name, input_name, input, output=None):
        """
        Produces GQL Mutation for updating CID
        """

        fragments = ''
        if not output:
            output = """
                cid {
                    ...cidFields
                }
            """
            fragments = get_fragments()

        query = f"""
            mutation {{
              {mutation_name} (
                {input_name}: {{
                    {self.__generate_gql_input(input)}
                }}
              ) 
              {{
                {output}
              }}
        }}
        {fragments}
        """
        return query

    def __run_gql_query(self, query, attachments=None):
        """
        Runs query and return results.
        If attachments are specified, they are sent as binaries.
        """
        headers = {'Authorization': self.__access_token} if self.__access_token else None
        if attachments:
            files_map = {}
            for i, path in enumerate(attachments):
                filename, file_ext = os.path.splitext(path)
                files_map[f'attachment_{i}{file_ext}'] = open(path, 'rb')
            resp = requests.post(self.__graphql_endpoint, data={'query': query},
                                 files=files_map, headers=headers)
        else:
            resp = requests.post(self.__graphql_endpoint, data={'query': query},
                                 headers=headers)

        if resp.status_code != 200:
            raise Exception(f'Query failed with status code {resp.status_code}. Error: {resp.text}')

        data = json.loads(resp.text)

        if 'errors' in data:
            raise Exception(f"Query returned errors {data['errors']}.")

        return data

    def __generate_gql_input(self, input_val):
        output = ''

        for key, val in input_val.__dict__.items():
            if val:
                output += '\n'

                output += f'{key}: '
                if is_dataclass(val):
                    output += f'{{ {self.__generate_gql_input(val)} }}'
                elif isinstance(val, list):
                    output += '['
                    for i in val:
                        if is_dataclass(i):
                            output += f'{{ {self.__generate_gql_input(i)} }}'
                        else:
                            output += json.dumps(i)
                    output += ']'
                elif isinstance(val, Enum):
                    output += val.name
                else:
                    output += json.dumps(val)

        return self.__indent(output)

    def authenticate_basic(self, login, password):
        """
        Authenticates user by login and password. Returns object: {status, accessToken, errorMessage}
        """
        if not login or not password:
            raise Exception('Login and password required')

        query = self.__graphql_authenticate(login, password)
        data = self.__run_gql_query(query)

        if data['data']['authenticate'].get('accessToken'):
            self.__access_token = data['data']['authenticate']['accessToken']
            return True
        else:
            raise Exception(data['data']['authenticate']['errorMessage'])

    def custom_asdict_factory(self, data):
        def convert_value(obj):
            if isinstance(obj, Enum):
                return obj.value
            return obj
        return dict((k, convert_value(v)) for k, v in data)

    def assign_identifier(self, assign_id_input):
        """
        Assign a related CID, DOI, ARK or MARC identifier.
        Data is pulled from corresponding sources and saved as CID event.
        :param assign_id_input: AssignIdentifierInput object (see mapping_inputs.py)
        :return: updated CID record
        """
        errors = assign_id_input.validate()
        if errors:
            raise Exception('Error in Assign ID input: {0}'.format(', '.join(errors)))

        self.__check_auth()

        query = self.__graphql_mutation('assignIdentifier', 'assignIdInput', assign_id_input)

        data = self.__run_gql_query(query)
        return data['data']['assignIdentifier']['cid']

    def create_cid(self, cid_input):
        """
        Create new CID record
        :param cid_input: CreateCIDInput input object (see mapping_inputs.py)
        :return: newly created record
        """
        errors = cid_input.validate()
        if errors:
            raise Exception('Error in CID input: {0}'.format(', '.join(errors)))

        self.__check_auth()

        query = self.__graphql_mutation('createCID', 'cidInput', cid_input)
        data = self.__run_gql_query(query)
        return data['data']['createCID']['cid']

    def find_by_artifact(self, artifact: str):
        """
        Returns cids by artifact link
        :param artifact: link to artifact
        """
        data = self.__run_gql_query(self.__graphql_find_by_artifact(artifact))
        return data['data']['findByArtifact']

    def get_by_id(self, cid: str, text_fields: list = None):
        """
        Returns all fields of CID.
        """
        data = self.__run_gql_query(self.__graphql_get_by_id(cid, text_fields))
        return data['data']['getCID']

    def get_cid_children(self, cid: str, size: int = 10):
        """
        Returns cids which have the provided CID as a PARENT.
        :param cid: CID to obtain child list for
        :param size: Max number of CIDs to return.  Defaults to 10
        """
        data = self.__run_gql_query(self.__graphql_get_cid_children(cid, size))
        return data['data']['searchCIDChildren']

    def get_cid_siblings(self, cid: str, size: int = 10):
        """
        Returns cids which have the same PARENT or WHERE.url of the provided CID.
        :param cid: CID to obtain sibling list for
        :param size: Max number of CIDs to return. Defaults to 10
        """
        data = self.__run_gql_query(self.__graphql_get_cid_siblings(cid, size))
        return data['data']['searchCIDSiblings']

    def remove_identifier(self, remove_id_input):
        """
        Remove a related CID, DOI, ARK or MARC identifier.
        :param remove_id_input: RemoveIdentifierInput object (see mapping_inputs.py)
        :return: updated CID record
        """
        errors = remove_id_input.validate()
        if errors:
            raise Exception('Error in Remove ID input: {0}'.format(', '.join(errors)))

        self.__check_auth()

        query = self.__graphql_mutation('removeIdentifier', 'removeIdInput', remove_id_input)

        data = self.__run_gql_query(query)
        return data['data']['removeIdentifier']['cid']

    def update_cid(self, cid_input):
        """
        Update CID record
        :param cid_input: UpdateCIDInput object (see mapping_inputs.py)
        :return: updated CID record
        """
        errors = cid_input.validate()
        if errors:
            raise Exception('Error in CID input: {0}'.format(', '.join(errors)))

        self.__check_auth()

        query = self.__graphql_mutation('updateCID', 'cidInput', cid_input)
        data = self.__run_gql_query(query)
        return data['data']['updateCID']['cid']

    def extract_fulltext(self, extract_ft_input):
        """
        Extract FullText for CID artifact
        :param extract_ft_input: ExtractFullTextInput object (see mapping_inputs.py)
        :return: status (SUCCESS/ERROR) and errorMessage in case of failure
        """
        errors = extract_ft_input.validate()
        if errors:
            raise Exception('Error in CID input: {0}'.format(', '.join(errors)))

        self.__check_auth()

        query = self.__graphql_mutation('extractFullText',
                                        'extractFullTextInput',
                                        extract_ft_input,
                                        'result { status errorMessage }')
        data = self.__run_gql_query(query)
        return data['data']['extractFullText']

    def set_archival_copy_url(self, archival_copy_url_input):
        """
        Sets archival copy URL for CID.
        :param extract_ft_input: SetArchivalCopyUrlInput object (see mapping_inputs.py)
        :return: status (SUCCESS/ERROR) and errorMessage in case of failure
        """
        errors = archival_copy_url_input.validate()
        if errors:
            raise Exception('Error in CID input: {0}'.format(', '.join(errors)))

        self.__check_auth()

        query = self.__graphql_mutation('setArchivalCopyUrl',
                                        'setArchivalCopyUrlInput',
                                        archival_copy_url_input,
                                        'result { status errorMessage }')
        data = self.__run_gql_query(query)
        return data['data']['setArchivalCopyUrl']

    def extract_fragments(self, extract_artifacts_input):
        """
        Extract fragments(images, tables, etc) from CID artifact
        :param extract_artifacts_input: ExtractFragmentsInput object (see mapping_inputs.py)
        :return: run information
        """
        errors = extract_artifacts_input.validate()

        if errors:
            raise Exception('Error in CID input: {0}'.format(', '.join(errors)))

        data = {
            "cids": [
                {
                    "cid": extract_artifacts_input.cid,
                },
            ],
            "features": extract_artifacts_input.features,
            "callback": asdict(extract_artifacts_input.callback, dict_factory=self.custom_asdict_factory)
        }

        response = requests.post(
            f"{self.__cose_endpoint}/extract",
            headers={
                'Content-Type': 'application/json; charset=utf-8',
                'accept': 'application/json'
            },
            json=data
        )

        response.raise_for_status()

        return response.json()

    def serialize(self):
        return {'environment': self.__environment, 'access_token': self.__access_token}

    @staticmethod
    def deserialize(serialized):
        return CIDClient(environment=serialized.get('environment'), access_token=serialized.get('access_token'))
