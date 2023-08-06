"""
Type annotations for robomaker service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_robomaker.client import RoboMakerClient

    session = get_session()
    async with session.create_client("robomaker") as client:
        client: RoboMakerClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import ArchitectureType, FailureBehaviorType
from .paginator import (
    ListDeploymentJobsPaginator,
    ListFleetsPaginator,
    ListRobotApplicationsPaginator,
    ListRobotsPaginator,
    ListSimulationApplicationsPaginator,
    ListSimulationJobBatchesPaginator,
    ListSimulationJobsPaginator,
    ListWorldExportJobsPaginator,
    ListWorldGenerationJobsPaginator,
    ListWorldsPaginator,
    ListWorldTemplatesPaginator,
)
from .type_defs import (
    BatchDeleteWorldsResponseTypeDef,
    BatchDescribeSimulationJobResponseTypeDef,
    BatchPolicyTypeDef,
    ComputeTypeDef,
    CreateDeploymentJobResponseTypeDef,
    CreateFleetResponseTypeDef,
    CreateRobotApplicationResponseTypeDef,
    CreateRobotApplicationVersionResponseTypeDef,
    CreateRobotResponseTypeDef,
    CreateSimulationApplicationResponseTypeDef,
    CreateSimulationApplicationVersionResponseTypeDef,
    CreateSimulationJobResponseTypeDef,
    CreateWorldExportJobResponseTypeDef,
    CreateWorldGenerationJobResponseTypeDef,
    CreateWorldTemplateResponseTypeDef,
    DataSourceConfigTypeDef,
    DeploymentApplicationConfigTypeDef,
    DeploymentConfigTypeDef,
    DeregisterRobotResponseTypeDef,
    DescribeDeploymentJobResponseTypeDef,
    DescribeFleetResponseTypeDef,
    DescribeRobotApplicationResponseTypeDef,
    DescribeRobotResponseTypeDef,
    DescribeSimulationApplicationResponseTypeDef,
    DescribeSimulationJobBatchResponseTypeDef,
    DescribeSimulationJobResponseTypeDef,
    DescribeWorldExportJobResponseTypeDef,
    DescribeWorldGenerationJobResponseTypeDef,
    DescribeWorldResponseTypeDef,
    DescribeWorldTemplateResponseTypeDef,
    EnvironmentTypeDef,
    FilterTypeDef,
    GetWorldTemplateBodyResponseTypeDef,
    ListDeploymentJobsResponseTypeDef,
    ListFleetsResponseTypeDef,
    ListRobotApplicationsResponseTypeDef,
    ListRobotsResponseTypeDef,
    ListSimulationApplicationsResponseTypeDef,
    ListSimulationJobBatchesResponseTypeDef,
    ListSimulationJobsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWorldExportJobsResponseTypeDef,
    ListWorldGenerationJobsResponseTypeDef,
    ListWorldsResponseTypeDef,
    ListWorldTemplatesResponseTypeDef,
    LoggingConfigTypeDef,
    OutputLocationTypeDef,
    RegisterRobotResponseTypeDef,
    RenderingEngineTypeDef,
    RobotApplicationConfigTypeDef,
    RobotSoftwareSuiteTypeDef,
    SimulationApplicationConfigTypeDef,
    SimulationJobRequestTypeDef,
    SimulationSoftwareSuiteTypeDef,
    SourceConfigTypeDef,
    StartSimulationJobBatchResponseTypeDef,
    SyncDeploymentJobResponseTypeDef,
    TemplateLocationTypeDef,
    UpdateRobotApplicationResponseTypeDef,
    UpdateSimulationApplicationResponseTypeDef,
    UpdateWorldTemplateResponseTypeDef,
    VPCConfigTypeDef,
    WorldCountTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("RoboMakerClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentDeploymentException: Type[BotocoreClientError]
    IdempotentParameterMismatchException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]


class RoboMakerClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        RoboMakerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#exceptions)
        """

    async def batch_delete_worlds(
        self, *, worlds: Sequence[str]
    ) -> BatchDeleteWorldsResponseTypeDef:
        """
        Deletes one or more worlds in a batch operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.batch_delete_worlds)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#batch_delete_worlds)
        """

    async def batch_describe_simulation_job(
        self, *, jobs: Sequence[str]
    ) -> BatchDescribeSimulationJobResponseTypeDef:
        """
        Describes one or more simulation jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.batch_describe_simulation_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#batch_describe_simulation_job)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#can_paginate)
        """

    async def cancel_deployment_job(self, *, job: str) -> Dict[str, Any]:
        """
        Cancels the specified deployment job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.cancel_deployment_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#cancel_deployment_job)
        """

    async def cancel_simulation_job(self, *, job: str) -> Dict[str, Any]:
        """
        Cancels the specified simulation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.cancel_simulation_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#cancel_simulation_job)
        """

    async def cancel_simulation_job_batch(self, *, batch: str) -> Dict[str, Any]:
        """
        Cancels a simulation job batch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.cancel_simulation_job_batch)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#cancel_simulation_job_batch)
        """

    async def cancel_world_export_job(self, *, job: str) -> Dict[str, Any]:
        """
        Cancels the specified export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.cancel_world_export_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#cancel_world_export_job)
        """

    async def cancel_world_generation_job(self, *, job: str) -> Dict[str, Any]:
        """
        Cancels the specified world generator job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.cancel_world_generation_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#cancel_world_generation_job)
        """

    async def create_deployment_job(
        self,
        *,
        clientRequestToken: str,
        fleet: str,
        deploymentApplicationConfigs: Sequence["DeploymentApplicationConfigTypeDef"],
        deploymentConfig: "DeploymentConfigTypeDef" = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateDeploymentJobResponseTypeDef:
        """
        Deploys a specific version of a robot application to robots in a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.create_deployment_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#create_deployment_job)
        """

    async def create_fleet(
        self, *, name: str, tags: Mapping[str, str] = ...
    ) -> CreateFleetResponseTypeDef:
        """
        Creates a fleet, a logical group of robots running the same robot application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.create_fleet)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#create_fleet)
        """

    async def create_robot(
        self,
        *,
        name: str,
        architecture: ArchitectureType,
        greengrassGroupId: str,
        tags: Mapping[str, str] = ...
    ) -> CreateRobotResponseTypeDef:
        """
        Creates a robot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.create_robot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#create_robot)
        """

    async def create_robot_application(
        self,
        *,
        name: str,
        robotSoftwareSuite: "RobotSoftwareSuiteTypeDef",
        sources: Sequence["SourceConfigTypeDef"] = ...,
        tags: Mapping[str, str] = ...,
        environment: "EnvironmentTypeDef" = ...
    ) -> CreateRobotApplicationResponseTypeDef:
        """
        Creates a robot application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.create_robot_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#create_robot_application)
        """

    async def create_robot_application_version(
        self,
        *,
        application: str,
        currentRevisionId: str = ...,
        s3Etags: Sequence[str] = ...,
        imageDigest: str = ...
    ) -> CreateRobotApplicationVersionResponseTypeDef:
        """
        Creates a version of a robot application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.create_robot_application_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#create_robot_application_version)
        """

    async def create_simulation_application(
        self,
        *,
        name: str,
        simulationSoftwareSuite: "SimulationSoftwareSuiteTypeDef",
        robotSoftwareSuite: "RobotSoftwareSuiteTypeDef",
        sources: Sequence["SourceConfigTypeDef"] = ...,
        renderingEngine: "RenderingEngineTypeDef" = ...,
        tags: Mapping[str, str] = ...,
        environment: "EnvironmentTypeDef" = ...
    ) -> CreateSimulationApplicationResponseTypeDef:
        """
        Creates a simulation application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.create_simulation_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#create_simulation_application)
        """

    async def create_simulation_application_version(
        self,
        *,
        application: str,
        currentRevisionId: str = ...,
        s3Etags: Sequence[str] = ...,
        imageDigest: str = ...
    ) -> CreateSimulationApplicationVersionResponseTypeDef:
        """
        Creates a simulation application with a specific revision id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.create_simulation_application_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#create_simulation_application_version)
        """

    async def create_simulation_job(
        self,
        *,
        maxJobDurationInSeconds: int,
        iamRole: str,
        clientRequestToken: str = ...,
        outputLocation: "OutputLocationTypeDef" = ...,
        loggingConfig: "LoggingConfigTypeDef" = ...,
        failureBehavior: FailureBehaviorType = ...,
        robotApplications: Sequence["RobotApplicationConfigTypeDef"] = ...,
        simulationApplications: Sequence["SimulationApplicationConfigTypeDef"] = ...,
        dataSources: Sequence["DataSourceConfigTypeDef"] = ...,
        tags: Mapping[str, str] = ...,
        vpcConfig: "VPCConfigTypeDef" = ...,
        compute: "ComputeTypeDef" = ...
    ) -> CreateSimulationJobResponseTypeDef:
        """
        Creates a simulation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.create_simulation_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#create_simulation_job)
        """

    async def create_world_export_job(
        self,
        *,
        worlds: Sequence[str],
        outputLocation: "OutputLocationTypeDef",
        iamRole: str,
        clientRequestToken: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateWorldExportJobResponseTypeDef:
        """
        Creates a world export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.create_world_export_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#create_world_export_job)
        """

    async def create_world_generation_job(
        self,
        *,
        template: str,
        worldCount: "WorldCountTypeDef",
        clientRequestToken: str = ...,
        tags: Mapping[str, str] = ...,
        worldTags: Mapping[str, str] = ...
    ) -> CreateWorldGenerationJobResponseTypeDef:
        """
        Creates worlds using the specified template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.create_world_generation_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#create_world_generation_job)
        """

    async def create_world_template(
        self,
        *,
        clientRequestToken: str = ...,
        name: str = ...,
        templateBody: str = ...,
        templateLocation: "TemplateLocationTypeDef" = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateWorldTemplateResponseTypeDef:
        """
        Creates a world template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.create_world_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#create_world_template)
        """

    async def delete_fleet(self, *, fleet: str) -> Dict[str, Any]:
        """
        Deletes a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.delete_fleet)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#delete_fleet)
        """

    async def delete_robot(self, *, robot: str) -> Dict[str, Any]:
        """
        Deletes a robot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.delete_robot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#delete_robot)
        """

    async def delete_robot_application(
        self, *, application: str, applicationVersion: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes a robot application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.delete_robot_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#delete_robot_application)
        """

    async def delete_simulation_application(
        self, *, application: str, applicationVersion: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes a simulation application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.delete_simulation_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#delete_simulation_application)
        """

    async def delete_world_template(self, *, template: str) -> Dict[str, Any]:
        """
        Deletes a world template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.delete_world_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#delete_world_template)
        """

    async def deregister_robot(self, *, fleet: str, robot: str) -> DeregisterRobotResponseTypeDef:
        """
        Deregisters a robot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.deregister_robot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#deregister_robot)
        """

    async def describe_deployment_job(self, *, job: str) -> DescribeDeploymentJobResponseTypeDef:
        """
        Describes a deployment job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.describe_deployment_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#describe_deployment_job)
        """

    async def describe_fleet(self, *, fleet: str) -> DescribeFleetResponseTypeDef:
        """
        Describes a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.describe_fleet)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#describe_fleet)
        """

    async def describe_robot(self, *, robot: str) -> DescribeRobotResponseTypeDef:
        """
        Describes a robot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.describe_robot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#describe_robot)
        """

    async def describe_robot_application(
        self, *, application: str, applicationVersion: str = ...
    ) -> DescribeRobotApplicationResponseTypeDef:
        """
        Describes a robot application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.describe_robot_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#describe_robot_application)
        """

    async def describe_simulation_application(
        self, *, application: str, applicationVersion: str = ...
    ) -> DescribeSimulationApplicationResponseTypeDef:
        """
        Describes a simulation application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.describe_simulation_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#describe_simulation_application)
        """

    async def describe_simulation_job(self, *, job: str) -> DescribeSimulationJobResponseTypeDef:
        """
        Describes a simulation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.describe_simulation_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#describe_simulation_job)
        """

    async def describe_simulation_job_batch(
        self, *, batch: str
    ) -> DescribeSimulationJobBatchResponseTypeDef:
        """
        Describes a simulation job batch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.describe_simulation_job_batch)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#describe_simulation_job_batch)
        """

    async def describe_world(self, *, world: str) -> DescribeWorldResponseTypeDef:
        """
        Describes a world.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.describe_world)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#describe_world)
        """

    async def describe_world_export_job(self, *, job: str) -> DescribeWorldExportJobResponseTypeDef:
        """
        Describes a world export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.describe_world_export_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#describe_world_export_job)
        """

    async def describe_world_generation_job(
        self, *, job: str
    ) -> DescribeWorldGenerationJobResponseTypeDef:
        """
        Describes a world generation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.describe_world_generation_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#describe_world_generation_job)
        """

    async def describe_world_template(
        self, *, template: str
    ) -> DescribeWorldTemplateResponseTypeDef:
        """
        Describes a world template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.describe_world_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#describe_world_template)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#generate_presigned_url)
        """

    async def get_world_template_body(
        self, *, template: str = ..., generationJob: str = ...
    ) -> GetWorldTemplateBodyResponseTypeDef:
        """
        Gets the world template body.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.get_world_template_body)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#get_world_template_body)
        """

    async def list_deployment_jobs(
        self,
        *,
        filters: Sequence["FilterTypeDef"] = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListDeploymentJobsResponseTypeDef:
        """
        Returns a list of deployment jobs for a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.list_deployment_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#list_deployment_jobs)
        """

    async def list_fleets(
        self,
        *,
        nextToken: str = ...,
        maxResults: int = ...,
        filters: Sequence["FilterTypeDef"] = ...
    ) -> ListFleetsResponseTypeDef:
        """
        Returns a list of fleets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.list_fleets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#list_fleets)
        """

    async def list_robot_applications(
        self,
        *,
        versionQualifier: str = ...,
        nextToken: str = ...,
        maxResults: int = ...,
        filters: Sequence["FilterTypeDef"] = ...
    ) -> ListRobotApplicationsResponseTypeDef:
        """
        Returns a list of robot application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.list_robot_applications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#list_robot_applications)
        """

    async def list_robots(
        self,
        *,
        nextToken: str = ...,
        maxResults: int = ...,
        filters: Sequence["FilterTypeDef"] = ...
    ) -> ListRobotsResponseTypeDef:
        """
        Returns a list of robots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.list_robots)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#list_robots)
        """

    async def list_simulation_applications(
        self,
        *,
        versionQualifier: str = ...,
        nextToken: str = ...,
        maxResults: int = ...,
        filters: Sequence["FilterTypeDef"] = ...
    ) -> ListSimulationApplicationsResponseTypeDef:
        """
        Returns a list of simulation applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.list_simulation_applications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#list_simulation_applications)
        """

    async def list_simulation_job_batches(
        self,
        *,
        nextToken: str = ...,
        maxResults: int = ...,
        filters: Sequence["FilterTypeDef"] = ...
    ) -> ListSimulationJobBatchesResponseTypeDef:
        """
        Returns a list simulation job batches.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.list_simulation_job_batches)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#list_simulation_job_batches)
        """

    async def list_simulation_jobs(
        self,
        *,
        nextToken: str = ...,
        maxResults: int = ...,
        filters: Sequence["FilterTypeDef"] = ...
    ) -> ListSimulationJobsResponseTypeDef:
        """
        Returns a list of simulation jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.list_simulation_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#list_simulation_jobs)
        """

    async def list_tags_for_resource(
        self, *, resourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all tags on a AWS RoboMaker resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#list_tags_for_resource)
        """

    async def list_world_export_jobs(
        self,
        *,
        nextToken: str = ...,
        maxResults: int = ...,
        filters: Sequence["FilterTypeDef"] = ...
    ) -> ListWorldExportJobsResponseTypeDef:
        """
        Lists world export jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.list_world_export_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#list_world_export_jobs)
        """

    async def list_world_generation_jobs(
        self,
        *,
        nextToken: str = ...,
        maxResults: int = ...,
        filters: Sequence["FilterTypeDef"] = ...
    ) -> ListWorldGenerationJobsResponseTypeDef:
        """
        Lists world generator jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.list_world_generation_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#list_world_generation_jobs)
        """

    async def list_world_templates(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListWorldTemplatesResponseTypeDef:
        """
        Lists world templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.list_world_templates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#list_world_templates)
        """

    async def list_worlds(
        self,
        *,
        nextToken: str = ...,
        maxResults: int = ...,
        filters: Sequence["FilterTypeDef"] = ...
    ) -> ListWorldsResponseTypeDef:
        """
        Lists worlds.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.list_worlds)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#list_worlds)
        """

    async def register_robot(self, *, fleet: str, robot: str) -> RegisterRobotResponseTypeDef:
        """
        Registers a robot with a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.register_robot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#register_robot)
        """

    async def restart_simulation_job(self, *, job: str) -> Dict[str, Any]:
        """
        Restarts a running simulation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.restart_simulation_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#restart_simulation_job)
        """

    async def start_simulation_job_batch(
        self,
        *,
        createSimulationJobRequests: Sequence["SimulationJobRequestTypeDef"],
        clientRequestToken: str = ...,
        batchPolicy: "BatchPolicyTypeDef" = ...,
        tags: Mapping[str, str] = ...
    ) -> StartSimulationJobBatchResponseTypeDef:
        """
        Starts a new simulation job batch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.start_simulation_job_batch)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#start_simulation_job_batch)
        """

    async def sync_deployment_job(
        self, *, clientRequestToken: str, fleet: str
    ) -> SyncDeploymentJobResponseTypeDef:
        """
        Syncrhonizes robots in a fleet to the latest deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.sync_deployment_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#sync_deployment_job)
        """

    async def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds or edits tags for a AWS RoboMaker resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#tag_resource)
        """

    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#untag_resource)
        """

    async def update_robot_application(
        self,
        *,
        application: str,
        robotSoftwareSuite: "RobotSoftwareSuiteTypeDef",
        sources: Sequence["SourceConfigTypeDef"] = ...,
        currentRevisionId: str = ...,
        environment: "EnvironmentTypeDef" = ...
    ) -> UpdateRobotApplicationResponseTypeDef:
        """
        Updates a robot application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.update_robot_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#update_robot_application)
        """

    async def update_simulation_application(
        self,
        *,
        application: str,
        simulationSoftwareSuite: "SimulationSoftwareSuiteTypeDef",
        robotSoftwareSuite: "RobotSoftwareSuiteTypeDef",
        sources: Sequence["SourceConfigTypeDef"] = ...,
        renderingEngine: "RenderingEngineTypeDef" = ...,
        currentRevisionId: str = ...,
        environment: "EnvironmentTypeDef" = ...
    ) -> UpdateSimulationApplicationResponseTypeDef:
        """
        Updates a simulation application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.update_simulation_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#update_simulation_application)
        """

    async def update_world_template(
        self,
        *,
        template: str,
        name: str = ...,
        templateBody: str = ...,
        templateLocation: "TemplateLocationTypeDef" = ...
    ) -> UpdateWorldTemplateResponseTypeDef:
        """
        Updates a world template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.update_world_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#update_world_template)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_deployment_jobs"]
    ) -> ListDeploymentJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_fleets"]) -> ListFleetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_robot_applications"]
    ) -> ListRobotApplicationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_robots"]) -> ListRobotsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_simulation_applications"]
    ) -> ListSimulationApplicationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_simulation_job_batches"]
    ) -> ListSimulationJobBatchesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_simulation_jobs"]
    ) -> ListSimulationJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_world_export_jobs"]
    ) -> ListWorldExportJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_world_generation_jobs"]
    ) -> ListWorldGenerationJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_world_templates"]
    ) -> ListWorldTemplatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_worlds"]) -> ListWorldsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/#get_paginator)
        """

    async def __aenter__(self) -> "RoboMakerClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker.html#RoboMaker.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/client/)
        """
