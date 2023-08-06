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

from enum import Enum


class ContainerType:
    """
    Describes possible container types.
    Contains: [PROJECT,SPACE]
    """
    PROJECT = 'project'
    SPACE = 'space'


class FactsheetAssetType:
    """
    Describes possible Factsheet custom asset types.
    Contains: [MODEL_FACTS_USER,MODEL_ENTRY_USER]

    - The modelfacts user AssetType to capture the user defined attributes of a model
    - The model entry user asset type to capture user defined attributes of a model entry

    """
    MODEL_FACTS_USER = 'modelfacts_user'
    MODEL_ENTRY_USER = 'model_entry_user'


class OnErrorTypes:
    """
    expected behaviour on error.
    """
    STOP = 'stop'
    CONTINUE = 'continue'


class ContentTypes:
    """
    The type of the input. A character encoding can be specified by including a
    `charset` parameter. For example, 'text/csv;charset=utf-8'.
    """
    APPLICATION_JSON = 'application/json'
    TEXT_CSV = 'text/csv'
