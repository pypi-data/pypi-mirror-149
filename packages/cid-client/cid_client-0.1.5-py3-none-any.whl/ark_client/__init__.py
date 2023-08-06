import json
from dataclasses import is_dataclass
import textwrap
import requests
import os
from .mapping import *
from enum import Enum
from .mapping_inputs import ARK_NAAN

__all__ = ['ARKClient']


class ARKClient:
    """
        Main class for CID manipulation methods
        """
    __access_token = None

    __graphql_env_endpoints = {
        'dev': 'https://m752xzraej.execute-api.us-east-2.amazonaws.com/dev/graphql',
        'prod': 'https://o56dder9y3.execute-api.us-east-2.amazonaws.com/prod/graphql',
        'sandbox': 'http://0.0.0.0:5000/graphql',
    }

    __graphql_endpoint = None

    def __init__(self, environment='dev'):
        """
        Create instance of ARKClient.
        :param environment: PROD or DEV. If DEV specified - ARKs will be created in test database
        """
        if not environment or environment.lower() not in ['prod', 'dev', 'sandbox']:
            raise ValueError('Parameter environment must be set to "prod" or "dev" only')

        self.__graphql_endpoint = self.__graphql_env_endpoints[environment.lower()]

    def __check_auth(self):
        if not self.__access_token:
            raise Exception('Authentication required. Call cid_client.authenticate_basic(login, password)')

    def __indent(self, s):
        return textwrap.indent(s, '    ')

    def __graphql_get_by_id(self, ark):
        """
        Produces GQL query for getting ARK by ID
        """
        return f"""
            query {{
                  getARK(ark: "{ark}") {{
                    ...arkFields
                  }}
                }}
        {get_fragments()}
        """

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

    def __graphql_mutation(self, mutation_name, input_name, input):
        """
        Produces GQL Mutation for updating ARK
        """
        query = f"""
            mutation {{
              {mutation_name} (
                {input_name}: {{
                    {self.__generate_gql_input(input)}
                }}
              ) 
              {{ 
                ark {{
                    ...arkFields
                }}
              }}
        }}
        {get_fragments()}
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
            raise Exception(f'Query failed with status code {resp.status_code}.')

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

    def create_ark(self, ark_input):
        """
        Create new ARK record
        :param ark_input: CreateARKInput input object (see mapping_inputs.py)
        :return: newly created record
        """

        errors = ark_input.validate()
        if errors:
            raise Exception('Error in ARK input: {0}'.format(', '.join(errors)))

        self.__check_auth()

        query = self.__graphql_mutation('createARK', 'arkInput', ark_input)
        data = self.__run_gql_query(query)
        return data['data']['createARK']['ark']

    def update_ark(self, ark_input):
        """
        Update ARK record
        :param ark_input: UpdateARKInput object (see mapping_inputs.py)
        :return: updated ARK record
        """

        errors = ark_input.validate()
        if errors:
            raise Exception('Error in ARK input: {0}'.format(', '.join(errors)))

        # Remove prefix before generating query
        ark_input.ark = ark_input.ark.replace('ark:', '')

        self.__check_auth()

        query = self.__graphql_mutation('updateARK', 'arkInput', ark_input)
        data = self.__run_gql_query(query)
        return data['data']['updateARK']['ark']

    def get_by_id(self, ark: str):
        """
        Returns all fields of ARK.
        """
        prefix = 'ark:' + ARK_NAAN + '/'
        if not ark.startswith(prefix) or not ark.replace(prefix, '').isalnum():
            raise Exception('Invalid ark format. Must be ark:45488/abcdef')

        # Remove prefix before generating query
        ark = ark.replace('ark:', '')

        data = self.__run_gql_query(self.__graphql_get_by_id(ark))
        return data['data']['getARK']

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
