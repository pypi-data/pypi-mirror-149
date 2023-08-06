import json
from typing import BinaryIO, Dict, List, TextIO, Union

class ExternalModelSchemas:
    """
    External model schema

    :attr List[Dict] input: Model input data schema
    :attr List[Dict] output: (optional) Model output data schema

    """
    def __init__(self,input: List[Dict],
                output:List[Dict]=None) -> None:

        """
        Initialize a ExternalModelSchemas object.

        :param List[Dict] input: Model input data schema
        :param List[Dict] output: (optional) Model output data schema
        
        """

        self.input = input
        self.output = output

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ExternalModelSchemas':
        """Initialize a DeploymentDetails object from a json dictionary."""
        args = {}
        if 'input' in _dict:
            args['input'] = _dict.get('input')
        else:
            raise ValueError('Required property \'deployment_id\' not present in ExternalModelSchemas JSON')
        if 'output' in _dict:
            args['output'] = _dict.get('output') #[convert_model(x) for x in metrics]
        else:
            raise ValueError('Required property \'output\' not present in ExternalModelSchemas JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ExternalModelSchemas object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'input') and self.input is not None:
            _dict['input'] = self.input
        if hasattr(self, 'output') and self.output is not None:
            _dict['output'] = self.output
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ExternalModelSchemas object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ExternalModelSchemas') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ExternalModelSchemas') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class TrainingDataReference:
    """
    Training data schema definition

    :attr Dict schema: Model training data schema
    
    """
    def __init__(self,schema:Dict) -> None:
        """
        Initialize a TrainingDataReference object.

        :param Dict schema: Model training data schema
        
        """
        self.schema = schema

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'TrainingDataReference':
        """Initialize a TrainingDataReference object from a json dictionary."""
        args = {}
        if 'schema' in _dict:
            args['schema'] = _dict.get('schema')
        else:
            raise ValueError('Required property \'schema\' not present in TrainingDataReference JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a TrainingDataReference object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'schema') and self.schema is not None:
            _dict['schema'] = self.schema
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this TrainingDataReference object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'TrainingDataReference') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'TrainingDataReference') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class DeploymentDetails:
    """
    External model deployment details

    :attr str identifier: Deployment identifier specific to providers.
    :attr str name: Name of the deployment
    :attr str deployment_type: Deployment type (i.e., online)
    :attr str scoring_endpoint: Deployment scoring endpoint url.  
    
    """

    def __init__(self,identifier: str,
                 name: str,
                 deployment_type: str,
                 scoring_endpoint: str = None) -> None:
        
        """
        Initialize a DeploymentDetails object.

        :param str identifier: Deployment identifier specific to ML providers
        :param str name: Name of the deployment
        :param str deployment_type: Deployment type (i.e., online)
        :param str scoring_endpoint: Deployment scoring endpoint url.  

        """
        
        self.id = identifier
        self.name = name
        self.type = deployment_type
        self.scoring_endpoint = scoring_endpoint


    @classmethod
    def from_dict(cls, _dict: Dict) -> 'DeploymentDetails':
        """Initialize a DeploymentDetails object from a json dictionary."""
        args = {}
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        else:
            raise ValueError('Required property \'id\' not present in DeploymentDetails JSON')
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        else:
            raise ValueError('Required property \'name\' not present in DeploymentDetails JSON')
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        else:
            raise ValueError('Required property \'type\' not present in DeploymentDetails JSON')
        if 'scoring_endpoint' in _dict:
            args['scoring_endpoint'] = _dict.get('scoring_endpoint')
        else:
            raise ValueError('Required property \'scoring_endpoint\' not present in DeploymentDetails JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a DeploymentDetails object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'scoring_endpoint') and self.scoring_endpoint is not None:
            _dict['scoring_endpoint'] = self.scoring_endpoint
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this DeploymentDetails object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'DeploymentDetails') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'DeploymentDetails') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class ModelEntryProps:
    """
    Model Entry Properties

        
    :attr str model_entry_catalog_id: Catalog ID where model entry exist.
    :attr str asset_id: Published model/asset ID. It is optional for external models ONLY.
    :attr str model_catalog_id: (Optional) Catalog Id where model exist.
    :attr str model_entry_id: (Optional) Existing Model Entry to link with.
    :attr str model_entry_name: (Optional) New model entry name. Used only when creating new model entry. 
    :attr str model_entry_description: (Optional) New model entry description. Used only when creating new model entry. 
    :attr str project_id: (Optional) Project ID where the model exist.Not applicable for external models.
    :attr str space_id: (Optional) Space ID where model exist Not applicable for external models.
    :attr str grc_model_id: (Optional) Openpages model id. Only applicable for CPD environments.  
    
    """

    def __init__(self,
                 model_entry_catalog_id: str,
                 asset_id: str=None,
                 model_catalog_id: str=None,
                 model_entry_id: str=None,
                 model_entry_name: str=None,
                 model_entry_desc: str = None,
                 project_id: str=None,
                 space_id: str=None,
                 grc_model_id: str=None) -> None:
        
        """
        Initialize a ModelEntryProps object.

        
        :param str model_entry_catalog_id: Catalog ID where model entry exist.
        :param str asset_id: Published model/asset ID. Optional for external models.
        :param str model_catalog_id: (Optional) Catalog Id where model exist.
        :param str model_entry_id: (Optional) Existing Model Entry to link with.
        :param str model_entry_name: (Optional) New model entry name. Used only when creating new model entry. 
        :param str model_entry_description: (Optional) New model entry description. Used only when creating new model entry. 
        :param str project_id: (Optional) Project ID where the model exist. Not applicable for external models.
        :param str space_id: (Optional) Space ID where model exist. Not applicable for external models.
        :param str grc_model_id: (Optional) Openpages model id. Only applied for CPD environments.  

        """
        
        self.asset_id=asset_id
        self.model_entry_catalog_id = model_entry_catalog_id
        self.model_catalog_id=model_catalog_id
        self.model_entry_id = model_entry_id
        self.model_entry_name = model_entry_name
        self.model_entry_desc = model_entry_desc
        self.project_id=project_id
        self.space_id=space_id
        self.grc_model_id=grc_model_id


    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ModelEntryProps':
        """Initialize a ModelEntryProps object from a json dictionary."""
        args = {}
        if 'model_entry_catalog_id' in _dict:
            args['model_entry_catalog_id'] = _dict.get('model_entry_catalog_id')
        else:
            raise ValueError('Required property \'model_entry_catalog_id\' not present in ModelEntryProps JSON')
        if 'asset_id' in _dict:
            args['asset_id'] = _dict.get('asset_id')
        else:
            raise ValueError('Required property \'asset_id\' not present in ModelEntryProps JSON')
        if 'model_catalog_id' in _dict:
            args['model_catalog_id'] = _dict.get('model_catalog_id')
        else:
            raise ValueError('Required property \'model_catalog_id\' not present in ModelEntryProps JSON')
        if 'model_entry_id' in _dict:
            args['model_entry_id'] = _dict.get('model_entry_id')
        else:
            raise ValueError('Required property \'model_entry_id\' not present in ModelEntryProps JSON')
        if 'model_entry_name' in _dict:
            args['model_entry_name'] = _dict.get('model_entry_name')
        else:
            raise ValueError('Required property \'model_entry_name\' not present in ModelEntryProps JSON')
        if 'model_entry_desc' in _dict:
            args['model_entry_desc'] = _dict.get('model_entry_desc')
        else:
            raise ValueError('Required property \'model_entry_desc\' not present in ModelEntryProps JSON')
        if 'project_id' in _dict:
            args['project_id'] = _dict.get('project_id')
        else:
            raise ValueError('Required property \'project_id\' not present in ModelEntryProps JSON')
        if 'space_id' in _dict:
            args['space_id'] = _dict.get('space_id')
        else:
            raise ValueError('Required property \'space_id\' not present in ModelEntryProps JSON')
        if 'grc_model_id' in _dict:
            args['grc_model_id'] = _dict.get('grc_model_id')
        else:
            raise ValueError('Required property \'grc_model_id\' not present in ModelEntryProps JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ModelEntryProps object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'asset_id') and self.asset_id is not None:
            _dict['asset_id'] = self.asset_id
        if hasattr(self, 'model_entry_catalog_id') and self.model_entry_catalog_id is not None:
            _dict['model_entry_catalog_id'] = self.model_entry_catalog_id
        if hasattr(self, 'model_catalog_id') and self.model_catalog_id is not None:
            _dict['model_catalog_id'] = self.model_catalog_id
        if hasattr(self, 'model_entry_id') and self.model_entry_id is not None:
            _dict['model_entry_id'] = self.model_entry_id
        if hasattr(self, 'model_entry_name') and self.model_entry_name is not None:
            _dict['model_entry_name'] = self.model_entry_name
        if hasattr(self, 'model_entry_desc') and self.model_entry_desc is not None:
            _dict['model_entry_desc'] = self.model_entry_desc
        if hasattr(self, 'project_id') and self.project_id is not None:
            _dict['project_id'] = self.project_id
        if hasattr(self, 'space_id') and self.space_id is not None:
            _dict['space_id'] = self.space_id
        if hasattr(self, 'grc_model_id') and self.grc_model_id is not None:
            _dict['grc_model_id'] = self.grc_model_id
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this DeploymentDetails object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ModelEntryProps') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ModelEntryProps') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other