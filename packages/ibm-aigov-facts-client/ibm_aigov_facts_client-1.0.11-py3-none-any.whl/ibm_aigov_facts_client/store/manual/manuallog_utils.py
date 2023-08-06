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
import mlflow
from ibm_aigov_facts_client.utils.client_errors import *
from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING

from ibm_aigov_facts_client.store.autolog.autolog_utils import *
from ibm_aigov_facts_client.custom import custom_file_store
from ibm_aigov_facts_client.utils.manual_store_utils import *

_logger = logging.getLogger(__name__)


def get_experiment(experiment_name):
    exp_exist = mlflow.get_experiment_by_name(experiment_name)
    return exp_exist


def create_experiment(experiment_name:str=None):
    client = mlflow.tracking.MlflowClient()
    if experiment_name is None:
        exp_id = client.create_experiment("Default")
    else: 
        exp_id = client.create_experiment(experiment_name)
    return exp_id


def set_experiment(experiment_name):
    mlflow.set_experiment(experiment_name)


def get_experiment_by_name(experiment_name):
    exp = mlflow.get_experiment_by_name(experiment_name)
    return exp


def clean_default_exp():
    client = mlflow.tracking.MlflowClient()
    default_experiment = get_experiment_by_name("Default")
    if (default_experiment is not None) and (default_experiment.lifecycle_stage != "deleted"):
        client.delete_experiment("0")


def start_trace(experiment_id: str = None):

    check_if_active_run_exist = mlflow.active_run()
    if check_if_active_run_exist is not None:
        mlflow.end_run()

    try:
        if experiment_id:
            mlflow.start_run(experiment_id=experiment_id)
        else:
            mlflow.start_run()
    except:
        raise ClientError("Can not initiate tracing....")


def end_trace():
    try:
        check_if_active_run_exist = mlflow.active_run()
        if check_if_active_run_exist is None:
            return("No active run found")
        else:
            mlflow.end_run()
    except:
        raise ClientError("Can not end tracing....")


def log_metric_data(key: str, value: float, step: Optional[int] = None) -> None:
    mlflow.log_metric(key, value, step)


def log_metrics_data(metrics: Dict[str, float], step: Optional[int] = None) -> None:
    #mlflow.log_metrics(metrics, step)
    for key, value in metrics.items():
        mlflow.log_metric(key,value,step or 0)


def log_param_data(key: str, value: Any) -> None:
    mlflow.log_param(key, value)


def log_params_data(params: Dict[str, Any]) -> None:
    #mlflow.log_params(params)
    for key, value in params.items():
        mlflow.log_param(key,value)


def log_tag_data(key: str, value: Any) -> None:
    mlflow.set_tag(key, value)


def log_tags_data(tags: Dict[str, Any]) -> None:
    #mlflow.set_tags(tags)
    for key, value in tags.items():
        mlflow.set_tag(key,value)


# def set_guid_tag(run_id):
#     custom_tag, _ = gen_new_tag()
#     _logger.debug("setting up GUID for {} and tag is {}".format(
#         run_id, custom_tag))
#     custom_file_store.FactSheetStore().set_tag(run_id, custom_tag)


def clean_tags(run_id):
    data, _ = get_run_data(run_id)
    get_sys_tags = {k: v for k, v in data.tags.items() if k.startswith(
        "mlflow.")}
    _logger.debug("Updating tags for given run...")
    custom_file_store.FactSheetStore().clean_tags(get_sys_tags, run_id)


def get_active_run():
    run = mlflow.active_run()
    return run
