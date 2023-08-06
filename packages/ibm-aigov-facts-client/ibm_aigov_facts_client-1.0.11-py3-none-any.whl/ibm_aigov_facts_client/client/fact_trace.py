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

import mlflow

from typing import Optional

from ibm_aigov_facts_client.base_classes.auth import FactsAuthClient
from ibm_cloud_sdk_core.authenticators import BearerTokenAuthenticator, CloudPakForDataAuthenticator, IAMAuthenticator, NoAuthAuthenticator
from ibm_cloud_sdk_core.utils import  convert_model

from ibm_aigov_facts_client.export.export_facts import *
from ibm_aigov_facts_client.export.export_facts_manual import *
from ibm_aigov_facts_client.utils.enums import ContainerType
from ibm_aigov_facts_client.utils.experiments.experiments_utils import Experiments
from ibm_aigov_facts_client.utils.runs.runs_utils import Runs
from ibm_aigov_facts_client.utils.support_scope_meta import FrameworkSupportOptions
from ibm_aigov_facts_client.factsheet.factsheet_utility import FactSheetElements
from ibm_aigov_facts_client.factsheet.external_modelfacts_utility import ExternalModelFactsElements
from .autolog import AutoLog
from .manual_log import ManualLog


from ibm_aigov_facts_client.utils.utils import validate_enum, validate_external_connection_props, version, validate_type, get_instance_guid
from ibm_aigov_facts_client.utils.client_errors import *
from ibm_aigov_facts_client.utils.logging_utils import *
from ibm_aigov_facts_client.store.autolog.autolog_utils import *
from ibm_aigov_facts_client.utils.constants import SPARK_JAR_PKG
from ibm_aigov_facts_client.utils.config import *
from ibm_aigov_facts_client.utils.cp4d_utils import CloudPakforDataConfig
from ibm_aigov_facts_client.supporting_classes.cp4d_authenticator import CP4DAuthenticator



class FactsClientAdapter(FactsAuthClient):

    """
    AI GOVERNANCE FACTS CLIENT

    :var version: Returns version of the python library.
    :vartype version: str

    :param str experiment_name: Name of the Experiment.
    :param str container_type: (Optional) Name of the container where model would be saved. Currently supported options are `SPACE` or `PROJECT`.  It is (Required) when using IBM Cloud.
    :param str container_id: (Optional) container id specific to container type.It is (Required) when using IBM Cloud.
    :param bool set_as_current_experiment: (Optional) if `True` new experiment will not be created if experiment already exists with same experiment name.By default set to False.
    :param bool enable_autolog: (Optional) if False, manual log option will be available. By default set to True.
    :param bool external_model: (Optional) if True, external models tracing would be enabled. By default set to False. 
    :param CloudPakforDataConfig cloud_pak_for_data_configs: (Optional) Cloud pak for data cluster details.


    A way you might use me is:

    For IBM Cloud:

    >>> from ibm_aigov_facts_client import AIGovFactsClient
    >>> client = AIGovFactsClient(api_key=<API_KEY>, experiment_name="test",container_type="space",container_id=<space_id>)
    >>> client = AIGovFactsClient(api_key=<API_KEY>,experiment_name="test",container_type="project",container_id=<project_id>)


    If using existing experiment as current:

    >>> client = AIGovFactsClient(api_key=<API_KEY>, experiment_name="test",container_type="space",container_id=<space_id>,set_as_current_experiment=True)


    If using external models with manual log:

    >>> client= AIGovFactsClient(api_key=API_KEY,experiment_name="external",enable_autolog=False,external_model=True)

    If using external models with Autolog:

    >>> client= AIGovFactsClient(api_key=API_KEY,experiment_name="external",external_model=True)


    For Cloud Pak for Data:

    >>> from ibm_aigov_facts_client import AIGovFactsClient,CloudPakforDataConfig
    >>> cpd_creds=CloudPakforDataConfig(service_url="<hosturl>",username="<username>",password="<password>")
    >>> client = AIGovFactsClient(experiment_name="<name of experiment>",container_type="<space or project>",container_id="<space_id or project_id>",cloud_pak_for_data_configs=cpd_creds)

    if Cloud Pak for Data platform has IAM enabled:

    >>> from ibm_aigov_facts_client import AIGovFactsClient,CloudPakforDataConfig
    >>> cpd_creds=CloudPakforDataConfig(service_url="<hosturl>",username="<username>",password="<password>",bedrock_url="<cluster bedrock url>")
    >>> client = AIGovFactsClient(experiment_name="<name of experiment>",container_type="<space or project>",container_id="<space_id or project_id>",cloud_pak_for_data_configs=cpd_creds )

    For Standalone use in localhost without factsheet functionality:

    >>> from ibm_aigov_facts_client import AIGovFactsClient
    >>> client = AIGovFactsClient(experiment_name="test")
    """

    _authenticator = None
    _container_type = None
    _container_id = None
    _autolog = None
    _external = None
    _is_cp4d=None
    _trace_obj=None


    def __init__(self,
                 experiment_name: str,
                 container_type: Optional[str] = None,
                 container_id: Optional[str] = None,
                 api_key: Optional[str] = None,
                 set_as_current_experiment: Optional[bool] = False,
                 enable_autolog: Optional[bool] = True,
                 external_model: Optional[bool]=False,
                 cloud_pak_for_data_configs:'CloudPakforDataConfig'=None,
                 ) -> None:
        self.experiment_name = experiment_name
        FactsClientAdapter._container_type = container_type
        FactsClientAdapter._container_id = container_id
        self.set_as_current_exp = set_as_current_experiment
        FactsClientAdapter._is_cp4d = False
        #self.ORG_FACTS_SPARK = SPARK_JAR_PKG
        FactsClientAdapter._autolog = enable_autolog
        FactsClientAdapter._external= external_model
        self.cp4d_configs=None

        if self.experiment_name is None or self.experiment_name == "":
            raise MissingValue("experiment_name", "Experiment name is missing")

        if cloud_pak_for_data_configs:
            FactsClientAdapter._is_cp4d=True
            super().set_disable_ssl_verification(self._is_cp4d)
            self.cp4d_configs=convert_model(cloud_pak_for_data_configs)

        _ENV = get_env()

        if api_key is not None and not FactsClientAdapter._is_cp4d:
            try:
                if _ENV == 'dev' or _ENV == 'test':
                    FactsClientAdapter._authenticator = IAMAuthenticator(
                        apikey=api_key, url=dev_config['IAM_URL'])

                elif _ENV == 'prod' or _ENV is None:
                    FactsClientAdapter._authenticator = IAMAuthenticator(
                        apikey=api_key)
                else:
                    FactsClientAdapter._authenticator = IAMAuthenticator(
                        apikey=api_key)
            except:
                raise AuthorizationError(
                    "Something went wrong when initiating client with provided API_KEY")
        
        elif FactsClientAdapter._is_cp4d:
            FactsClientAdapter._authenticator=CloudPakForDataAuthenticator(url=self.cp4d_configs['url'],
                                                                            username=self.cp4d_configs['username'],
                                                                            password=self.cp4d_configs['password'],
                                                                            disable_ssl_verification=self.cp4d_configs['disable_ssl_verification']
                                                                            )
        elif not self.cp4d_configs['password'] and self.cp4d_configs["api_key"]:
            FactsClientAdapter._authenticator=CloudPakForDataAuthenticator(url=self.cp4d_configs['url'],
                                                                            username=self.cp4d_configs['username'],
                                                                            apikey=self.cp4d_configs["api_key"],
                                                                            disable_ssl_verification=self.cp4d_configs['disable_ssl_verification']
                                                                            )

        else:
            FactsClientAdapter._authenticator = NoAuthAuthenticator()


        super().__init__(authenticator=FactsClientAdapter._authenticator)


        
        if type(FactsClientAdapter._authenticator) in [NoAuthAuthenticator]:
            if FactsClientAdapter._autolog:
                AutoLog(experiment_name=self.experiment_name,
                        set_as_current_exp=self.set_as_current_exp)
            else:
                self.manual_log = ManualLog(experiment_name=self.experiment_name,
                                            set_as_current_exp=self.set_as_current_exp)

        elif type(FactsClientAdapter._authenticator) in [CloudPakForDataAuthenticator, IAMAuthenticator, BearerTokenAuthenticator]:
            validate_type(FactsClientAdapter._authenticator, "authenticator", [
                BearerTokenAuthenticator, CloudPakForDataAuthenticator, IAMAuthenticator
            ], True)

            if isinstance(FactsClientAdapter._authenticator, CloudPakForDataAuthenticator):
                url = FactsClientAdapter._authenticator.token_manager.url[0:FactsClientAdapter._authenticator.token_manager.url.index("/",9)]
                username = FactsClientAdapter._authenticator.token_manager.username
                password = FactsClientAdapter._authenticator.token_manager.password
                apikey = FactsClientAdapter._authenticator.token_manager.apikey
                disable_ssl_verification=FactsClientAdapter._authenticator.token_manager.disable_ssl_verification
                FactsClientAdapter._authenticator = CP4DAuthenticator(url=url,
                                            username=username,
                                            password=password,
                                            apikey = apikey,
                                            disable_ssl_verification=disable_ssl_verification,
                                            bedrock_url = self.cp4d_configs.get("bedrock_url", None))

            if not FactsClientAdapter._external:
                if not FactsClientAdapter._autolog:
                   raise ClientError("Manual logging is supported for external models, set `external_model=True` when initiating client") 

                if not FactsClientAdapter._container_type  or not FactsClientAdapter._container_id:
                    raise MissingValue("container_type/container_id",
                                    "container_type or container_id is missing")

                elif(FactsClientAdapter._container_type is not None):
                    validate_enum(FactsClientAdapter._container_type,
                                "container_type", ContainerType, False)

                self.valid_service_instance = get_instance_guid(
                    FactsClientAdapter._authenticator, _ENV, FactsClientAdapter._container_type,is_cp4d=FactsClientAdapter._is_cp4d)
            else:

                if FactsClientAdapter._container_type or FactsClientAdapter._container_id:
                    raise ClientError("Container type and id is specific to IBM Cloud or CP4D only")

                self.valid_service_instance = get_instance_guid(
                    FactsClientAdapter._authenticator, _ENV,is_cp4d=FactsClientAdapter._is_cp4d)

            if not self.valid_service_instance:
                raise ClientError("Valid service instance/s not found")
            else:
                if FactsClientAdapter._autolog:
                    AutoLog(experiment_name=self.experiment_name,
                            set_as_current_exp=self.set_as_current_exp)
                    self.export_facts = ExportFacts(self)

                    if external_model:
                        self.external_model_facts = ExternalModelFactsElements(api_key,self.experiment_name,self._is_cp4d,self.cp4d_configs)
                else:
                    if FactsClientAdapter._container_type or FactsClientAdapter._container_id:
                        raise ClientError("Manual logging is supported for external models which does not require container type or id") 
                    
                    self.manual_log = ManualLog(experiment_name=self.experiment_name,
                                                set_as_current_exp=self.set_as_current_exp)
                    self.export_facts = ExportFactsManual(self)

                    self.external_model_facts = ExternalModelFactsElements(api_key,self.experiment_name,self._is_cp4d,self.cp4d_configs)

        else:
            raise AuthorizationError("Could not initiate client")

        self.version = version()
        self.experiments = Experiments()
        self.runs = Runs()
        self.FrameworkSupportNames = FrameworkSupportOptions()


