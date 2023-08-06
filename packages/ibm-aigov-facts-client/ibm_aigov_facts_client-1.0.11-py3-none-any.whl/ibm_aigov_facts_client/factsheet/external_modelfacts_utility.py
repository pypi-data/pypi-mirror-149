# coding: utf-8

# Copyright 2020,2021 IBM All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import logging
from typing import Dict
from ibm_aigov_facts_client.utils import cp4d_utils
import jwt
import json
#import requests
import pandas as pd
import hashlib

import ibm_aigov_facts_client._wrappers.requests as requests

from ibm_cloud_sdk_core.authenticators.iam_authenticator import IAMAuthenticator
from ibm_aigov_facts_client.client import fact_trace, autolog, manual_log
from ibm_aigov_facts_client.utils.client_errors import *
from ibm_aigov_facts_client.utils.enums import FactsheetAssetType
from ibm_aigov_facts_client.utils.utils import validate_enum
from ibm_cloud_sdk_core.utils import convert_list, convert_model
from ibm_aigov_facts_client.utils.cp4d_utils import CloudPakforDataConfig
from ibm_aigov_facts_client.supporting_classes.cp4d_authenticator import CP4DAuthenticator
from ibm_aigov_facts_client.supporting_classes.factsheet_utils import ExternalModelSchemas,TrainingDataReference,DeploymentDetails,ModelEntryProps
from .factsheet_utility import FactSheetElements
from typing import BinaryIO, Dict, List, TextIO, Union

from ..utils.config import *

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

_logger = logging.getLogger(__name__)


class ExternalModelFactsElements:

    def __init__(self,api_key:str, experiment_name:str, is_cpd:bool=False,cp4d_configs:'CloudPakforDataConfig'=None):

        self.api_key = api_key
        self.experiment_name = experiment_name
        self.model_asset_id=None
        self.model_catalog_id=None
        self.is_cpd=is_cpd
        if self.is_cpd:
            self.cpd_configs=convert_model(cp4d_configs)
    
    def _get_token(self, api_key):

        if api_key:
            try:
                if get_env() is None or get_env() == 'prod':
                    _authenticator = IAMAuthenticator(
                        apikey=api_key)

                elif get_env() == 'dev' or get_env() == 'test':
                    _authenticator = IAMAuthenticator(
                        apikey=api_key, url=dev_config['IAM_URL'])
                else:
                    _authenticator = IAMAuthenticator(
                        apikey=api_key)
            except:
                raise AuthorizationError(
                    "Something went wrong when initiating Authentication")

        if isinstance(_authenticator, IAMAuthenticator):
            token = _authenticator.token_manager.get_token()
        else:
            token = _authenticator.bearer_token
        return token

    def _get_token_cpd(self, cp4d_configs):

            if cp4d_configs:
                try:
                    _auth_cpd=CP4DAuthenticator(url=cp4d_configs["url"],
                                                username=cp4d_configs["username"],
                                                password=cp4d_configs.get("password", None),
                                                apikey = cp4d_configs.get("apikey", None), 
                                                disable_ssl_verification=cp4d_configs["disable_ssl_verification"],
                                                bedrock_url = cp4d_configs.get("bedrock_url", None))
                except:
                    raise AuthorizationError(
                        "Something went wrong when initiating Authentication")

            if isinstance(_auth_cpd, CP4DAuthenticator):
                token = _auth_cpd.get_cp4d_auth_token()
            else:
                raise AuthorizationError(
                        "Something went wrong when getting token")
            return token

    def _encode_model_id(self,model_id):
        encoded_id=hashlib.md5(model_id.encode("utf-8")).hexdigest()
        return encoded_id

    def _encode_deployment_id(self,deployment_id):
        encoded_deployment_id=hashlib.md5(deployment_id.encode("utf-8")).hexdigest()
        return encoded_deployment_id

    def _validate_payload(self, payload):
        if not payload["model_id"] or not payload["name"]:
            raise ClientError("model_identifier or name is missing")
        else:
            payload["model_id"]= self._encode_model_id(payload["model_id"])
        if payload.get("deployment_details"):
            _logger.debug("details {}".format(json.dumps(payload,indent=4)))
            payload["deployment_details"]["id"]= self._encode_deployment_id(payload["deployment_details"]["id"])

        return payload


    def save_external_model_asset(self, model_identifier:str, name:str, description:str=None, schemas:'ExternalModelSchemas'=None, training_data_reference:'TrainingDataReference'=None,deployment_details:'DeploymentDetails'=None,model_entry_props:'ModelEntryProps'=None):
        
        """
        Save External model assets in catalog and (Optional) link to model entry

        :param str model_identifier: Identifier specific to ML providers (i.e., Azure ML service: `service_id`, AWS Sagemaker:`model_name`)
        :param str name: Name of the model
        :param str description: (Optional) description of the model
        :param ExternalModelSchemas schemas: (Optional) Input and Output schema of the model
        :param TrainingDataReference training_data_reference: (Optional) Training data schema
        :param DeploymentDetails deployment_details: (Optional) Model deployment details
        :param ModelEntryProps model_entry_props: (Optional) Properties about model asset and model entry catalog


        If using external models with manual log option, initiate client as:

        .. code-block:: python

            from ibm_aigov_facts_client import AIGovFactsClient
            client= AIGovFactsClient(api_key=API_KEY,experiment_name="external",enable_autolog=False,external_model=True)


        If using external models with Autolog, initiate client as:

        .. code-block:: python

            from ibm_aigov_facts_client import AIGovFactsClient
            client= AIGovFactsClient(api_key=API_KEY,experiment_name="external",external_model=True)

            
        If using Cloud pak for Data:

        .. code-block:: python

            creds=CloudPakforDataConfig(service_url="<HOST URL>",
                                        username="<username>",
                                        password="<password>")
            
            client = AIGovFactsClient(experiment_name=<experiment_name>,external_model=True,cloud_pak_for_data_configs=creds)
        
        Payload example by supported external providers:

        Azure ML Service:

        .. code-block:: python

            from ibm_aigov_facts_client.supporting_classes.factsheet_utils import DeploymentDetails,TrainingDataReference,ExternalModelSchemas

            external_schemas=ExternalModelSchemas(input=input_schema,output=output_schema)
            trainingdataref=TrainingDataReference(schema=training_ref)
            deployment=DeploymentDetails(identifier=<service_url in Azure>,name="deploymentname",deployment_type="online",scoring_endpoint="test/score")

            client.external_model_facts.save_external_model_asset(model_identifier=<service_id in Azure>
                                                                        ,name=<model_name>
                                                                        ,deployment_details=deployment
                                                                        ,schemas=external_schemas
                                                                        ,training_data_reference=tdataref)


        AWS Sagemaker:

        .. code-block:: python

            external_schemas=ExternalModelSchemas(input=input_schema,output=output_schema)
            trainingdataref=TrainingDataReference(schema=training_ref)
            deployment=DeploymentDetails(identifier=<endpoint_name in Sagemaker>,name="deploymentname",deployment_type="online",scoring_endpoint="test/score")

            client.external_model_facts.save_external_model_asset(model_identifier=<model_name in Sagemaker>
                                                                        ,name=<model_name>
                                                                        ,deployment_details=deployment
                                                                        ,schemas=external_schemas
                                                                        ,training_data_reference=tdataref)



        Model entry props example, IBM Cloud and CPD:

        >>> from ibm_aigov_facts_client.supporting_classes.factsheet_utils import ModelEntryProps,DeploymentDetails,TrainingDataReference,ExternalModelSchemas
        

        For new model entry:

        >>> props=ModelEntryProps(
                    model_entry_catalog_id=<catalog_id>,
                    model_entry_name=<name>,
                    model_entry_desc=<description>
                    )
        
        
        For linking to existing model entry:

        >>> props=ModelEntryProps(
                    model_entry_catalog_id=<catalog_id>,
                    model_entry_id=<model_entry_id to link>
                    )

        >>> client.external_model_facts.save_external_model_asset(model_identifier=<model_name in Sagemaker>
                                                                        ,name=<model_name>
                                                                        ,deployment_details=deployment
                                                                        ,schemas=external_schemas
                                                                        ,training_data_reference=tdataref
                                                                        ,model_entry_props= props)
        
        """
        
        if deployment_details:
            deployment_details=convert_model(deployment_details)
        if schemas:
            schemas=convert_model(schemas)
        if training_data_reference:
            training_data_reference=convert_model(training_data_reference)
        if model_entry_props:
            model_entry_props=convert_model(model_entry_props)
        # if self.cp4d_configs:
        #     self.is_cpd=True
        #     self.cp4d_configs=convert_model(self.cp4d_configs)
               
        data = {
            'model_id': model_identifier,
            'name': name,
            'description': description,
            'schemas': schemas,
            'training_data_references': training_data_reference,
            'deployment_details': deployment_details
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        _validated_payload= self._validate_payload(data) 
        _logger.debug("validated payload..{}".format(_validated_payload))
        self._publish(_validated_payload)

        if model_entry_props:
            if 'project_id' in model_entry_props or 'space_id' in model_entry_props:
                raise WrongProps("project or space is not expected for external models")

            if 'asset_id' not in model_entry_props:
                model_entry_props['asset_id']=self.model_asset_id
            
            model_entry_props['model_catalog_id']=self.model_catalog_id

            if self.is_cpd and self.cpd_configs:
                FactSheetElements(cp4d_details=self.cpd_configs).register_model_entry(model_entry_props=model_entry_props)
            else:
                FactSheetElements(api_key=self.api_key).register_model_entry(model_entry_props=model_entry_props)
        
        

    def _publish(self, data):

        headers = {}
        if self.is_cpd:
            headers["Authorization"] = "Bearer " + self._get_token_cpd(self.cpd_configs)
            url = self.cpd_configs["url"] + \
                '/v1/aigov/model_inventory/model_stub'
        else:
            headers["Authorization"] = "Bearer " + self._get_token(self.api_key)
            if get_env() == 'dev':
                url = dev_config["DEFAULT_DEV_SERVICE_URL"] + \
                '/v1/aigov/model_inventory/model_stub'
            elif get_env() == 'test':
                url = test_config["DEFAULT_TEST_SERVICE_URL"] + \
                    '/v1/aigov/model_inventory/model_stub'
            else:
                url = prod_config["DEFAULT_SERVICE_URL"] + \
                    '/v1/aigov/model_inventory/model_stub'

        headers["Accept"] = "application/json"
        headers["Content-Type"] = "application/json"

        params = {"experiment_name": self.experiment_name}


        _logger.debug("url...{}".format(url))
        response = requests.put(url=url,
                                headers=headers,
                                params=params,
                                data=json.dumps(data))

        if response.status_code == 401:
            _logger.exception("Expired token found.")
            
        elif response.status_code==403:
            _logger.exception("Access Forbidden")
            
        elif response.status_code == 200:
            if response.json()['metadata']['asset_id'] and response.json()['metadata']['catalog_id']:
                self.model_asset_id=response.json()['metadata']['asset_id']
                self.model_catalog_id=response.json()['metadata']['catalog_id']
            _logger.info("External model asset saved successfully under asset_id {} and catalog {}".format(self.model_asset_id,self.model_catalog_id))
            _logger.debug("External model asset saved successfully {}".format(response.json()))
        else:
            _logger.exception(
                "Error updating properties..{}".format(response.json()))



    def unregister_model_entry(self, asset_id, catalog_id):
        """
            Unregister WKC Model Entry

            :param str asset_id: WKC model entry id
            :param str catalog_id: Catalog ID where asset is stored


            Example for IBM Cloud or CPD:

            >>> client.external_model_facts.unregister_model_entry(asset_id=<model asset id>,catalog_id=<catalog_id>)

        """
        if self.is_cpd and self.cpd_configs:
            FactSheetElements(cp4d_details=self.cpd_configs).unregister_model_entry(asset_id=asset_id,catalog_id=catalog_id)
        else:
            FactSheetElements(api_key=self.api_key).unregister_model_entry(asset_id=asset_id,catalog_id=catalog_id)

    def list_model_entries(self, catalog_id=None)->Dict:
        """
        Returns all WKC Model Entry assets for a catalog

        :param str catalog_id: (Optional) Catalog ID where you want to register model, if None list from all catalogs
        
        :return: All WKC Model Entry assets for a catalog
        :rtype: dict

        Example:

        >>> client.external_model_facts.list_model_entries()
        >>> client.external_model_facts.list_model_entries(catalog_id=<catalog_id>)

        """

        if catalog_id:
            if self.is_cpd and self.cpd_configs:
                res=FactSheetElements(cp4d_details=self.cpd_configs).list_model_entries(catalog_id)
            else:
                res=FactSheetElements(api_key=self.api_key).list_model_entries(catalog_id)
        else:
            if self.is_cpd and self.cpd_configs:
                res=FactSheetElements(cp4d_details=self.cpd_configs).list_model_entries()
            else:
                res=FactSheetElements(api_key=self.api_key).list_model_entries()
        
        return res