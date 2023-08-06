"""
Type annotations for iotevents service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iotevents.client import IoTEventsClient

    session = get_session()
    async with session.create_client("iotevents") as client:
        client: IoTEventsClient
    ```
"""
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import EvaluationMethodType
from .type_defs import (
    AlarmCapabilitiesTypeDef,
    AlarmEventActionsTypeDef,
    AlarmNotificationTypeDef,
    AlarmRuleTypeDef,
    CreateAlarmModelResponseTypeDef,
    CreateDetectorModelResponseTypeDef,
    CreateInputResponseTypeDef,
    DescribeAlarmModelResponseTypeDef,
    DescribeDetectorModelAnalysisResponseTypeDef,
    DescribeDetectorModelResponseTypeDef,
    DescribeInputResponseTypeDef,
    DescribeLoggingOptionsResponseTypeDef,
    DetectorModelDefinitionTypeDef,
    GetDetectorModelAnalysisResultsResponseTypeDef,
    InputDefinitionTypeDef,
    InputIdentifierTypeDef,
    ListAlarmModelsResponseTypeDef,
    ListAlarmModelVersionsResponseTypeDef,
    ListDetectorModelsResponseTypeDef,
    ListDetectorModelVersionsResponseTypeDef,
    ListInputRoutingsResponseTypeDef,
    ListInputsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    LoggingOptionsTypeDef,
    StartDetectorModelAnalysisResponseTypeDef,
    TagTypeDef,
    UpdateAlarmModelResponseTypeDef,
    UpdateDetectorModelResponseTypeDef,
    UpdateInputResponseTypeDef,
)

__all__ = ("IoTEventsClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UnsupportedOperationException: Type[BotocoreClientError]


class IoTEventsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IoTEventsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/#can_paginate)
        """

    async def create_alarm_model(
        self,
        *,
        alarmModelName: str,
        roleArn: str,
        alarmRule: "AlarmRuleTypeDef",
        alarmModelDescription: str = ...,
        tags: Sequence["TagTypeDef"] = ...,
        key: str = ...,
        severity: int = ...,
        alarmNotification: "AlarmNotificationTypeDef" = ...,
        alarmEventActions: "AlarmEventActionsTypeDef" = ...,
        alarmCapabilities: "AlarmCapabilitiesTypeDef" = ...
    ) -> CreateAlarmModelResponseTypeDef:
        """
        Creates an alarm model to monitor an AWS IoT Events input attribute.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client.create_alarm_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/#create_alarm_model)
        """

    async def create_detector_model(
        self,
        *,
        detectorModelName: str,
        detectorModelDefinition: "DetectorModelDefinitionTypeDef",
        roleArn: str,
        detectorModelDescription: str = ...,
        key: str = ...,
        tags: Sequence["TagTypeDef"] = ...,
        evaluationMethod: EvaluationMethodType = ...
    ) -> CreateDetectorModelResponseTypeDef:
        """
        Creates a detector model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client.create_detector_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/#create_detector_model)
        """

    async def create_input(
        self,
        *,
        inputName: str,
        inputDefinition: "InputDefinitionTypeDef",
        inputDescription: str = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateInputResponseTypeDef:
        """
        Creates an input.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client.create_input)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/#create_input)
        """

    async def delete_alarm_model(self, *, alarmModelName: str) -> Dict[str, Any]:
        """
        Deletes an alarm model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client.delete_alarm_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/#delete_alarm_model)
        """

    async def delete_detector_model(self, *, detectorModelName: str) -> Dict[str, Any]:
        """
        Deletes a detector model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client.delete_detector_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/#delete_detector_model)
        """

    async def delete_input(self, *, inputName: str) -> Dict[str, Any]:
        """
        Deletes an input.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client.delete_input)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/#delete_input)
        """

    async def describe_alarm_model(
        self, *, alarmModelName: str, alarmModelVersion: str = ...
    ) -> DescribeAlarmModelResponseTypeDef:
        """
        Retrieves information about an alarm model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client.describe_alarm_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/#describe_alarm_model)
        """

    async def describe_detector_model(
        self, *, detectorModelName: str, detectorModelVersion: str = ...
    ) -> DescribeDetectorModelResponseTypeDef:
        """
        Describes a detector model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client.describe_detector_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/#describe_detector_model)
        """

    async def describe_detector_model_analysis(
        self, *, analysisId: str
    ) -> DescribeDetectorModelAnalysisResponseTypeDef:
        """
        Retrieves runtime information about a detector model analysis.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client.describe_detector_model_analysis)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/#describe_detector_model_analysis)
        """

    async def describe_input(self, *, inputName: str) -> DescribeInputResponseTypeDef:
        """
        Describes an input.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client.describe_input)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/#describe_input)
        """

    async def describe_logging_options(self) -> DescribeLoggingOptionsResponseTypeDef:
        """
        Retrieves the current settings of the AWS IoT Events logging options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client.describe_logging_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/#describe_logging_options)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/#generate_presigned_url)
        """

    async def get_detector_model_analysis_results(
        self, *, analysisId: str, nextToken: str = ..., maxResults: int = ...
    ) -> GetDetectorModelAnalysisResultsResponseTypeDef:
        """
        Retrieves one or more analysis results of the detector model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client.get_detector_model_analysis_results)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/#get_detector_model_analysis_results)
        """

    async def list_alarm_model_versions(
        self, *, alarmModelName: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListAlarmModelVersionsResponseTypeDef:
        """
        Lists all the versions of an alarm model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client.list_alarm_model_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/#list_alarm_model_versions)
        """

    async def list_alarm_models(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListAlarmModelsResponseTypeDef:
        """
        Lists the alarm models that you created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client.list_alarm_models)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/#list_alarm_models)
        """

    async def list_detector_model_versions(
        self, *, detectorModelName: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListDetectorModelVersionsResponseTypeDef:
        """
        Lists all the versions of a detector model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client.list_detector_model_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/#list_detector_model_versions)
        """

    async def list_detector_models(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListDetectorModelsResponseTypeDef:
        """
        Lists the detector models you have created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client.list_detector_models)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/#list_detector_models)
        """

    async def list_input_routings(
        self,
        *,
        inputIdentifier: "InputIdentifierTypeDef",
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListInputRoutingsResponseTypeDef:
        """
        Lists one or more input routings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client.list_input_routings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/#list_input_routings)
        """

    async def list_inputs(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListInputsResponseTypeDef:
        """
        Lists the inputs you have created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client.list_inputs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/#list_inputs)
        """

    async def list_tags_for_resource(
        self, *, resourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags (metadata) you have assigned to the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/#list_tags_for_resource)
        """

    async def put_logging_options(self, *, loggingOptions: "LoggingOptionsTypeDef") -> None:
        """
        Sets or updates the AWS IoT Events logging options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client.put_logging_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/#put_logging_options)
        """

    async def start_detector_model_analysis(
        self, *, detectorModelDefinition: "DetectorModelDefinitionTypeDef"
    ) -> StartDetectorModelAnalysisResponseTypeDef:
        """
        Performs an analysis of your detector model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client.start_detector_model_analysis)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/#start_detector_model_analysis)
        """

    async def tag_resource(
        self, *, resourceArn: str, tags: Sequence["TagTypeDef"]
    ) -> Dict[str, Any]:
        """
        Adds to or modifies the tags of the given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/#tag_resource)
        """

    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes the given tags (metadata) from the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/#untag_resource)
        """

    async def update_alarm_model(
        self,
        *,
        alarmModelName: str,
        roleArn: str,
        alarmRule: "AlarmRuleTypeDef",
        alarmModelDescription: str = ...,
        severity: int = ...,
        alarmNotification: "AlarmNotificationTypeDef" = ...,
        alarmEventActions: "AlarmEventActionsTypeDef" = ...,
        alarmCapabilities: "AlarmCapabilitiesTypeDef" = ...
    ) -> UpdateAlarmModelResponseTypeDef:
        """
        Updates an alarm model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client.update_alarm_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/#update_alarm_model)
        """

    async def update_detector_model(
        self,
        *,
        detectorModelName: str,
        detectorModelDefinition: "DetectorModelDefinitionTypeDef",
        roleArn: str,
        detectorModelDescription: str = ...,
        evaluationMethod: EvaluationMethodType = ...
    ) -> UpdateDetectorModelResponseTypeDef:
        """
        Updates a detector model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client.update_detector_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/#update_detector_model)
        """

    async def update_input(
        self,
        *,
        inputName: str,
        inputDefinition: "InputDefinitionTypeDef",
        inputDescription: str = ...
    ) -> UpdateInputResponseTypeDef:
        """
        Updates an input.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client.update_input)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/#update_input)
        """

    async def __aenter__(self) -> "IoTEventsClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotevents/client/)
        """
