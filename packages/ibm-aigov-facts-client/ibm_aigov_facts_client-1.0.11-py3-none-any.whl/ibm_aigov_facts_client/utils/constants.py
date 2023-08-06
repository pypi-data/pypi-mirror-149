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

from .config import *

RESOURCES_URL_MAPPING = {
    dev_config["DEFAULT_DEV_SERVICE_URL"]: "https://resource-controller.test.cloud.ibm.com/v2/resource_instances",
    test_config["DEFAULT_TEST_SERVICE_URL"]: "https://resource-controller.cloud.ibm.com/v2/resource_instances",
    prod_config["DEFAULT_SERVICE_URL"]: "https://resource-controller.cloud.ibm.com/v2/resource_instances"
}

SPARK_FRAMEWORKS = ['pyspark', 'spark']
SPARK_ESTIMATOR_CLS = ['estimator_class']
DL_FRAMEWORKS = ['tensorflow', 'keras', 'pytorch']
BST_FRAMEWORKS = ['xgboost', 'lightgbm']


SPARK_JAR_PKG = "org.mlflow:mlflow-spark:1.11.0"
DL_EPOCHS_TAG = "epochs"
TF_EPOCHS_TAG = "steps"
BST_EPOCHS_TAG = "num_boost_round"
SPARK_HYP_TAG = "numFolds"


PRE_AUTOLOG_KEY = 'mlflow.autologging'
POST_AUTOLOG_KEY = 'facts.autologging'

SUPPORTED_FRAMEWORKS = ["sklearn", "pyspark",
                        "tensorflow", "keras", "xgboost", "lightgbm", "pytorch"]

MANUAL_SUPPORTED_FRAMEWORKS = ['sklearn']
MANUAL_FRAMEWORK_KEY = 'facts.manual'

AUTO_FRAMEWORK_KEYS = ['mlflow.autologging',
                       'facts.autologging', 'facts_manual']

TRASH_FOLDER = ".trash"
SUBFOLDER_DEFAULT = "metrics"

CONTAINER_PROJECT = "project_id"
CONTAINER_SPACE = "space_id"


METRICS_FOLDER_NAME = "metrics"
PARAMS_FOLDER_NAME = "params"
TAGS_FOLDER_NAME = "tags"
PUBLISH_TAG = "facts.publish"
