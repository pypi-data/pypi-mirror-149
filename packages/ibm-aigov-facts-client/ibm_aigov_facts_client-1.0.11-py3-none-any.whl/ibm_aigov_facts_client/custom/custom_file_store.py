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

from ibm_aigov_facts_client.store.autolog import general_payload_store, dl_payload_store, bst_payload_store, spark_payload_store
from mlflow.store.tracking.file_store import FileStore
from ibm_aigov_facts_client.client import fact_trace
from ibm_aigov_facts_client.custom import custom_exp
from ibm_aigov_facts_client.utils.logging_utils import *

from ..utils.utils import *
from ..utils.store_utils import *
from ..utils.constants import *

_logger = logging.getLogger(__name__)


class FactSheetStore(FileStore):
    """FileStore provided through entrypoints system"""
    _cur_runid=None
    def __init__(self, root_directory=None, artifact_uri=None, **kwargs):
        if root_directory is None:
            self.root_directory = local_file_uri_to_path(
                root_directory or default_root_dir())
        self.is_plugin = True
        self.exp_guid = None
        self.parent_run_id = None
        self.autolog = fact_trace.FactsClientAdapter._autolog
        super().__init__(self.root_directory, artifact_uri)

    def set_tag(self, run_id, custom_tag):
        super().set_tag(run_id, custom_tag)

    def clean_tags(self, tags, run_id):
        for k, val in tags.items():
            updated_key = k.replace("mlflow", "facts")
            updated_tag = custom_exp.GenerateExpId().gen_tag(
                {updated_key: val})
            super().set_tag(run_id, updated_tag)
            super().delete_tag(run_id, k)

    def get_path_metric(self, run_id):
        parent_path, metric_files = super()._get_run_files(
            super()._get_run_info(run_id), "metric")

        return parent_path, metric_files


    def log_batch(self, run_id, metrics, params, tags):
        
        if self.autolog:

            super().log_batch(run_id, metrics, params, tags)
            currentRun = super().get_run(run_id)
            FactSheetStore._cur_runid=run_id
            currentData = currentRun.data

            check_spark_tag = check_tags_exist(
                currentData.tags, SPARK_FRAMEWORKS)
            check_tensorflow_tag = check_tags_exist(
                currentData.tags, DL_FRAMEWORKS)
            check_estimator_cls_tag = check_if_keys_exist(
                currentData.tags, SPARK_ESTIMATOR_CLS)
            check_hyp_tag = currentData.params.get(SPARK_HYP_TAG)
            check_bst_tag = check_tags_exist(
                currentData.tags, BST_FRAMEWORKS)

            check_valid_framework = check_framework_support(
                currentData.tags, SUPPORTED_FRAMEWORKS)
            _logger.debug("current framework..{}".format(
                check_valid_framework))
            _logger.debug("tags are {}".format(currentData.tags))

            if (check_valid_framework):

                check_if_published = check_if_autolog_published(
                    currentData.tags, PUBLISH_TAG)

                _logger.debug("already published in autolog {}".format(
                    check_if_published))
               # _logger.debug("Current data...{}".format(currentData))

                if check_spark_tag and currentData.params and currentData.tags and check_estimator_cls_tag and check_hyp_tag:
                    self.parent_run_id = run_id
                    if self.parent_run_id is not None:
                        get_run_data = super().get_run(self.parent_run_id).data
                        check_param_tag = {
                            k: v for k, v in get_run_data.params.items() if k.startswith("best_")}
                        if check_param_tag:
                            _logger.debug(
                                "found best params {}".format(check_param_tag))
                            _logger.debug(
                                "exporting parent run now....{}".format(self.parent_run_id))
                            return spark_payload_store.GetFinalPayloadSpark(self.parent_run_id, get_run_data, self.root_directory).get_final_payload_and_publish()

                if check_spark_tag and currentData.params and currentData.tags and check_estimator_cls_tag and not check_hyp_tag:

                    return spark_payload_store.GetFinalPayloadSpark(run_id, currentData, self.root_directory).get_final_payload_and_publish()

                if currentData.tags and currentData.params and currentData.metrics and not check_spark_tag and not check_if_published:

                    if check_tensorflow_tag or check_bst_tag:
                        if check_valid_framework == "pytorch":
                            clear_up_handler()

                        parent_path, metric_files = self.get_path_metric(
                            run_id)
                        _logger.debug(
                            "metric files.......{}".format(metric_files))

                        if check_tensorflow_tag:
                            return dl_payload_store.GetFinalPayloadDl(run_id, currentData, self.root_directory).get_final_payload_and_publish(parent_path, metric_files)

                        else:
                            return bst_payload_store.GetFinalPayloadBST(run_id, currentData, self.root_directory).get_final_payload_and_publish(parent_path, metric_files)

                    else:
                        return general_payload_store.GetFinalPayloadGeneral(run_id, currentData, self.root_directory).get_final_payload_and_publish()
                
                

            else:
                raise ClientError("Framework not supported for autologging, current supported ones are {}".format(
                    SUPPORTED_FRAMEWORKS))
        else:
            pass
