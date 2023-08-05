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


from ibm_aigov_facts_client.utils.utils import validate_type
from ibm_cloud_sdk_core import BaseService, DetailedResponse

from ibm_cloud_sdk_core.authenticators import BearerTokenAuthenticator, CloudPakForDataAuthenticator, IAMAuthenticator
from ibm_aigov_facts_client.base_classes.auth import FactsheetServiceClientManual
from ibm_aigov_facts_client.client import fact_trace, autolog, manual_log
from typing import Any, Dict

from ibm_aigov_facts_client.store.manual import bst_payload_manual, dl_payload_manual, spark_payload_manual, general_payload_manual
from ibm_aigov_facts_client.custom import custom_file_store, custom_exp

from ibm_aigov_facts_client.utils.utils import *
from ibm_aigov_facts_client.utils.manual_store_utils import *
from ibm_aigov_facts_client.utils.constants import *
from ibm_aigov_facts_client.utils.logging_utils import *

from datetime import datetime


_logger = logging.getLogger(__name__)


class ExportFactsManual(FactsheetServiceClientManual):

    def __init__(self, facts_service_client: 'fact_trace.FactsClientAdapter', **kwargs) -> None:
        validate_type(facts_service_client,
                      'facts_service_client', BaseService, True)
        self._factsheet_service_client = facts_service_client
        self.guid = None
        self.external=fact_trace.FactsClientAdapter._external
        self.authenticator = fact_trace.FactsClientAdapter._authenticator
        self.is_cp4d=fact_trace.FactsClientAdapter._is_cp4d
        self.final_payload = {}
        self.root_directory = None

        super().__init__(factsheet_auth_client=self._factsheet_service_client)


    def export_payload_manual(self, run_id: str, root_directory: str = None) -> DetailedResponse:
        """
        Export single run to factsheet when using manual logging option. Use this option when client is initiated with `enable_autolog=False and external_model=True`

        :param str run_id: Id of run to be exported
        :param str root_directory: (Optional) Absolute path for directory containing experiments and runs.
        :return: A `DetailedResponse` containing the factsheet response result
        :rtype: DetailedResponse

        A way you might use me is:

        >>> client.export_facts.export_payload_manual(<RUN_ID>)
        """
        _logger.debug("initiating export........")
        self.root_directory = local_file_uri_to_path(
            root_directory or default_root_dir())
        _logger.debug("root dir {}".format(self.root_directory))
        exp_id = check_exp(run_id)

        # if self.external_engine:
        #     self._set_framework_tag(run_id, self.external_engine)

        if check_if_auth_used(self.authenticator):
            if self.is_cp4d:
                self.token=self.authenticator.get_cp4d_auth_token()
            else:
                self.token = self.authenticator.token_manager.get_token() if isinstance(
                    self.authenticator, IAMAuthenticator) else self.authenticator.bearer_token

            if self.token:
                run_data, _ = get_run_data(run_id)
                _logger.debug("run_data tags {}".format(run_data.tags))

                payload = general_payload_manual.GetFinalPayloadGeneral().get_payload_and_publish(
                    self.root_directory, exp_id, run_id)

                self.final_payload["notebook_experiment"] = payload

                _logger.info(
                "logging results to factsheet for run_id {}".format(run_id))

                _logger.debug(
                    "Initiaing payload sending request for run {} and payload is {}".format(run_id, self.final_payload))

                super().add_payload(run_id=run_id,
                                    token=self.token,
                                    payload=self.final_payload,external=self.external,is_cp4d=self.is_cp4d)


            else:
                raise AuthorizationError(
                    "Could not authenticate, invalid token")

    