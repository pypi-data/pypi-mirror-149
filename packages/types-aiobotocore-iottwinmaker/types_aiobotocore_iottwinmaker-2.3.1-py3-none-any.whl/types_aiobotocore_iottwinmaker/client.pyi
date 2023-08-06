"""
Type annotations for iottwinmaker service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iottwinmaker.client import IoTTwinMakerClient

    session = get_session()
    async with session.create_client("iottwinmaker") as client:
        client: IoTTwinMakerClient
    ```
"""
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import OrderByTimeType
from .type_defs import (
    BatchPutPropertyValuesResponseTypeDef,
    ComponentRequestTypeDef,
    ComponentUpdateRequestTypeDef,
    CreateComponentTypeResponseTypeDef,
    CreateEntityResponseTypeDef,
    CreateSceneResponseTypeDef,
    CreateWorkspaceResponseTypeDef,
    DeleteComponentTypeResponseTypeDef,
    DeleteEntityResponseTypeDef,
    FunctionRequestTypeDef,
    GetComponentTypeResponseTypeDef,
    GetEntityResponseTypeDef,
    GetPropertyValueHistoryResponseTypeDef,
    GetPropertyValueResponseTypeDef,
    GetSceneResponseTypeDef,
    GetWorkspaceResponseTypeDef,
    InterpolationParametersTypeDef,
    ListComponentTypesFilterTypeDef,
    ListComponentTypesResponseTypeDef,
    ListEntitiesFilterTypeDef,
    ListEntitiesResponseTypeDef,
    ListScenesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWorkspacesResponseTypeDef,
    ParentEntityUpdateRequestTypeDef,
    PropertyDefinitionRequestTypeDef,
    PropertyFilterTypeDef,
    PropertyValueEntryTypeDef,
    UpdateComponentTypeResponseTypeDef,
    UpdateEntityResponseTypeDef,
    UpdateSceneResponseTypeDef,
    UpdateWorkspaceResponseTypeDef,
)

__all__ = ("IoTTwinMakerClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ConnectorFailureException: Type[BotocoreClientError]
    ConnectorTimeoutException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class IoTTwinMakerClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IoTTwinMakerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#exceptions)
        """
    async def batch_put_property_values(
        self, *, entries: Sequence["PropertyValueEntryTypeDef"], workspaceId: str
    ) -> BatchPutPropertyValuesResponseTypeDef:
        """
        Sets values for multiple time series properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.batch_put_property_values)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#batch_put_property_values)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#can_paginate)
        """
    async def create_component_type(
        self,
        *,
        componentTypeId: str,
        workspaceId: str,
        description: str = ...,
        extendsFrom: Sequence[str] = ...,
        functions: Mapping[str, "FunctionRequestTypeDef"] = ...,
        isSingleton: bool = ...,
        propertyDefinitions: Mapping[str, "PropertyDefinitionRequestTypeDef"] = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateComponentTypeResponseTypeDef:
        """
        Creates a component type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.create_component_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#create_component_type)
        """
    async def create_entity(
        self,
        *,
        entityName: str,
        workspaceId: str,
        components: Mapping[str, "ComponentRequestTypeDef"] = ...,
        description: str = ...,
        entityId: str = ...,
        parentEntityId: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateEntityResponseTypeDef:
        """
        Creates an entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.create_entity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#create_entity)
        """
    async def create_scene(
        self,
        *,
        contentLocation: str,
        sceneId: str,
        workspaceId: str,
        capabilities: Sequence[str] = ...,
        description: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateSceneResponseTypeDef:
        """
        Creates a scene.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.create_scene)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#create_scene)
        """
    async def create_workspace(
        self,
        *,
        role: str,
        s3Location: str,
        workspaceId: str,
        description: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateWorkspaceResponseTypeDef:
        """
        Creates a workplace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.create_workspace)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#create_workspace)
        """
    async def delete_component_type(
        self, *, componentTypeId: str, workspaceId: str
    ) -> DeleteComponentTypeResponseTypeDef:
        """
        Deletes a component type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.delete_component_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#delete_component_type)
        """
    async def delete_entity(
        self, *, entityId: str, workspaceId: str, isRecursive: bool = ...
    ) -> DeleteEntityResponseTypeDef:
        """
        Deletes an entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.delete_entity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#delete_entity)
        """
    async def delete_scene(self, *, sceneId: str, workspaceId: str) -> Dict[str, Any]:
        """
        Deletes a scene.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.delete_scene)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#delete_scene)
        """
    async def delete_workspace(self, *, workspaceId: str) -> Dict[str, Any]:
        """
        Deletes a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.delete_workspace)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#delete_workspace)
        """
    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#generate_presigned_url)
        """
    async def get_component_type(
        self, *, componentTypeId: str, workspaceId: str
    ) -> GetComponentTypeResponseTypeDef:
        """
        Retrieves information about a component type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.get_component_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#get_component_type)
        """
    async def get_entity(self, *, entityId: str, workspaceId: str) -> GetEntityResponseTypeDef:
        """
        Retrieves information about an entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.get_entity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#get_entity)
        """
    async def get_property_value(
        self,
        *,
        selectedProperties: Sequence[str],
        workspaceId: str,
        componentName: str = ...,
        componentTypeId: str = ...,
        entityId: str = ...
    ) -> GetPropertyValueResponseTypeDef:
        """
        Gets the property values for a component, component type, entity, or workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.get_property_value)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#get_property_value)
        """
    async def get_property_value_history(
        self,
        *,
        endDateTime: Union[datetime, str],
        selectedProperties: Sequence[str],
        startDateTime: Union[datetime, str],
        workspaceId: str,
        componentName: str = ...,
        componentTypeId: str = ...,
        entityId: str = ...,
        interpolation: "InterpolationParametersTypeDef" = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        orderByTime: OrderByTimeType = ...,
        propertyFilters: Sequence["PropertyFilterTypeDef"] = ...
    ) -> GetPropertyValueHistoryResponseTypeDef:
        """
        Retrieves information about the history of a time series property value for a
        component, component type, entity, or workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.get_property_value_history)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#get_property_value_history)
        """
    async def get_scene(self, *, sceneId: str, workspaceId: str) -> GetSceneResponseTypeDef:
        """
        Retrieves information about a scene.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.get_scene)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#get_scene)
        """
    async def get_workspace(self, *, workspaceId: str) -> GetWorkspaceResponseTypeDef:
        """
        Retrieves information about a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.get_workspace)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#get_workspace)
        """
    async def list_component_types(
        self,
        *,
        workspaceId: str,
        filters: Sequence["ListComponentTypesFilterTypeDef"] = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListComponentTypesResponseTypeDef:
        """
        Lists all component types in a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.list_component_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#list_component_types)
        """
    async def list_entities(
        self,
        *,
        workspaceId: str,
        filters: Sequence["ListEntitiesFilterTypeDef"] = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListEntitiesResponseTypeDef:
        """
        Lists all entities in a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.list_entities)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#list_entities)
        """
    async def list_scenes(
        self, *, workspaceId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListScenesResponseTypeDef:
        """
        Lists all scenes in a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.list_scenes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#list_scenes)
        """
    async def list_tags_for_resource(
        self, *, resourceARN: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all tags associated with a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#list_tags_for_resource)
        """
    async def list_workspaces(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListWorkspacesResponseTypeDef:
        """
        Retrieves information about workspaces in the current account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.list_workspaces)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#list_workspaces)
        """
    async def tag_resource(self, *, resourceARN: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds tags to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#tag_resource)
        """
    async def untag_resource(self, *, resourceARN: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#untag_resource)
        """
    async def update_component_type(
        self,
        *,
        componentTypeId: str,
        workspaceId: str,
        description: str = ...,
        extendsFrom: Sequence[str] = ...,
        functions: Mapping[str, "FunctionRequestTypeDef"] = ...,
        isSingleton: bool = ...,
        propertyDefinitions: Mapping[str, "PropertyDefinitionRequestTypeDef"] = ...
    ) -> UpdateComponentTypeResponseTypeDef:
        """
        Updates information in a component type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.update_component_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#update_component_type)
        """
    async def update_entity(
        self,
        *,
        entityId: str,
        workspaceId: str,
        componentUpdates: Mapping[str, "ComponentUpdateRequestTypeDef"] = ...,
        description: str = ...,
        entityName: str = ...,
        parentEntityUpdate: "ParentEntityUpdateRequestTypeDef" = ...
    ) -> UpdateEntityResponseTypeDef:
        """
        Updates an entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.update_entity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#update_entity)
        """
    async def update_scene(
        self,
        *,
        sceneId: str,
        workspaceId: str,
        capabilities: Sequence[str] = ...,
        contentLocation: str = ...,
        description: str = ...
    ) -> UpdateSceneResponseTypeDef:
        """
        Updates a scene.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.update_scene)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#update_scene)
        """
    async def update_workspace(
        self, *, workspaceId: str, description: str = ..., role: str = ...
    ) -> UpdateWorkspaceResponseTypeDef:
        """
        Updates a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client.update_workspace)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/#update_workspace)
        """
    async def __aenter__(self) -> "IoTTwinMakerClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iottwinmaker.html#IoTTwinMaker.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/client/)
        """
