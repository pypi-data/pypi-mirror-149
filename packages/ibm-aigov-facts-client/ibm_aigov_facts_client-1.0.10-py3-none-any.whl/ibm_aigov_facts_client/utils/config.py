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

import os 


def get_env():
    if os.environ.get("FACTS_CLIENT_ENV"):
        return os.environ["FACTS_CLIENT_ENV"]
    else:
        return "prod"


dev_config = {
    'DEFAULT_DEV_SERVICE_URL': 'https://api.dataplatform.dev.cloud.ibm.com',
    'IAM_URL': 'https://iam.stage1.ng.bluemix.net/identity/token'
}

test_config = {
    'DEFAULT_TEST_SERVICE_URL': 'https://api.dataplatform.test.cloud.ibm.com',
    'IAM_URL': 'https://iam.stage1.ng.bluemix.net/identity/token'
}

prod_config = {
    "DEFAULT_SERVICE_URL": "https://api.dataplatform.cloud.ibm.com"
}

WKC_MODEL_REGISTER = u"/v1/aigov/model_inventory/models/{}/model_entry"
WKC_MODEL_LIST_FROM_CATALOG = u"/v1/aigov/model_inventory/{}/model_entries"
WKC_MODEL_LIST_ALL = u"/v1/aigov/model_inventory/model_entries"
