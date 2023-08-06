"""
Type annotations for databrew service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_databrew.client import GlueDataBrewClient

    session = get_session()
    async with session.create_client("databrew") as client:
        client: GlueDataBrewClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import EncryptionModeType, InputFormatType, LogSubscriptionType
from .paginator import (
    ListDatasetsPaginator,
    ListJobRunsPaginator,
    ListJobsPaginator,
    ListProjectsPaginator,
    ListRecipesPaginator,
    ListRecipeVersionsPaginator,
    ListRulesetsPaginator,
    ListSchedulesPaginator,
)
from .type_defs import (
    BatchDeleteRecipeVersionResponseTypeDef,
    CreateDatasetResponseTypeDef,
    CreateProfileJobResponseTypeDef,
    CreateProjectResponseTypeDef,
    CreateRecipeJobResponseTypeDef,
    CreateRecipeResponseTypeDef,
    CreateRulesetResponseTypeDef,
    CreateScheduleResponseTypeDef,
    DatabaseOutputTypeDef,
    DataCatalogOutputTypeDef,
    DeleteDatasetResponseTypeDef,
    DeleteJobResponseTypeDef,
    DeleteProjectResponseTypeDef,
    DeleteRecipeVersionResponseTypeDef,
    DeleteRulesetResponseTypeDef,
    DeleteScheduleResponseTypeDef,
    DescribeDatasetResponseTypeDef,
    DescribeJobResponseTypeDef,
    DescribeJobRunResponseTypeDef,
    DescribeProjectResponseTypeDef,
    DescribeRecipeResponseTypeDef,
    DescribeRulesetResponseTypeDef,
    DescribeScheduleResponseTypeDef,
    FormatOptionsTypeDef,
    InputTypeDef,
    JobSampleTypeDef,
    ListDatasetsResponseTypeDef,
    ListJobRunsResponseTypeDef,
    ListJobsResponseTypeDef,
    ListProjectsResponseTypeDef,
    ListRecipesResponseTypeDef,
    ListRecipeVersionsResponseTypeDef,
    ListRulesetsResponseTypeDef,
    ListSchedulesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    OutputTypeDef,
    PathOptionsTypeDef,
    ProfileConfigurationTypeDef,
    PublishRecipeResponseTypeDef,
    RecipeReferenceTypeDef,
    RecipeStepTypeDef,
    RuleTypeDef,
    S3LocationTypeDef,
    SampleTypeDef,
    SendProjectSessionActionResponseTypeDef,
    StartJobRunResponseTypeDef,
    StartProjectSessionResponseTypeDef,
    StopJobRunResponseTypeDef,
    UpdateDatasetResponseTypeDef,
    UpdateProfileJobResponseTypeDef,
    UpdateProjectResponseTypeDef,
    UpdateRecipeJobResponseTypeDef,
    UpdateRecipeResponseTypeDef,
    UpdateRulesetResponseTypeDef,
    UpdateScheduleResponseTypeDef,
    ValidationConfigurationTypeDef,
    ViewFrameTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("GlueDataBrewClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class GlueDataBrewClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        GlueDataBrewClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#exceptions)
        """

    async def batch_delete_recipe_version(
        self, *, Name: str, RecipeVersions: Sequence[str]
    ) -> BatchDeleteRecipeVersionResponseTypeDef:
        """
        Deletes one or more versions of a recipe at a time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.batch_delete_recipe_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#batch_delete_recipe_version)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#can_paginate)
        """

    async def create_dataset(
        self,
        *,
        Name: str,
        Input: "InputTypeDef",
        Format: InputFormatType = ...,
        FormatOptions: "FormatOptionsTypeDef" = ...,
        PathOptions: "PathOptionsTypeDef" = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateDatasetResponseTypeDef:
        """
        Creates a new DataBrew dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.create_dataset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#create_dataset)
        """

    async def create_profile_job(
        self,
        *,
        DatasetName: str,
        Name: str,
        OutputLocation: "S3LocationTypeDef",
        RoleArn: str,
        EncryptionKeyArn: str = ...,
        EncryptionMode: EncryptionModeType = ...,
        LogSubscription: LogSubscriptionType = ...,
        MaxCapacity: int = ...,
        MaxRetries: int = ...,
        Configuration: "ProfileConfigurationTypeDef" = ...,
        ValidationConfigurations: Sequence["ValidationConfigurationTypeDef"] = ...,
        Tags: Mapping[str, str] = ...,
        Timeout: int = ...,
        JobSample: "JobSampleTypeDef" = ...
    ) -> CreateProfileJobResponseTypeDef:
        """
        Creates a new job to analyze a dataset and create its data profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.create_profile_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#create_profile_job)
        """

    async def create_project(
        self,
        *,
        DatasetName: str,
        Name: str,
        RecipeName: str,
        RoleArn: str,
        Sample: "SampleTypeDef" = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateProjectResponseTypeDef:
        """
        Creates a new DataBrew project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.create_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#create_project)
        """

    async def create_recipe(
        self,
        *,
        Name: str,
        Steps: Sequence["RecipeStepTypeDef"],
        Description: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateRecipeResponseTypeDef:
        """
        Creates a new DataBrew recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.create_recipe)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#create_recipe)
        """

    async def create_recipe_job(
        self,
        *,
        Name: str,
        RoleArn: str,
        DatasetName: str = ...,
        EncryptionKeyArn: str = ...,
        EncryptionMode: EncryptionModeType = ...,
        LogSubscription: LogSubscriptionType = ...,
        MaxCapacity: int = ...,
        MaxRetries: int = ...,
        Outputs: Sequence["OutputTypeDef"] = ...,
        DataCatalogOutputs: Sequence["DataCatalogOutputTypeDef"] = ...,
        DatabaseOutputs: Sequence["DatabaseOutputTypeDef"] = ...,
        ProjectName: str = ...,
        RecipeReference: "RecipeReferenceTypeDef" = ...,
        Tags: Mapping[str, str] = ...,
        Timeout: int = ...
    ) -> CreateRecipeJobResponseTypeDef:
        """
        Creates a new job to transform input data, using steps defined in an existing
        Glue DataBrew recipe See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/databrew-2017-07-25/CreateRecipeJob).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.create_recipe_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#create_recipe_job)
        """

    async def create_ruleset(
        self,
        *,
        Name: str,
        TargetArn: str,
        Rules: Sequence["RuleTypeDef"],
        Description: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateRulesetResponseTypeDef:
        """
        Creates a new ruleset that can be used in a profile job to validate the data
        quality of a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.create_ruleset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#create_ruleset)
        """

    async def create_schedule(
        self,
        *,
        CronExpression: str,
        Name: str,
        JobNames: Sequence[str] = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateScheduleResponseTypeDef:
        """
        Creates a new schedule for one or more DataBrew jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.create_schedule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#create_schedule)
        """

    async def delete_dataset(self, *, Name: str) -> DeleteDatasetResponseTypeDef:
        """
        Deletes a dataset from DataBrew.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.delete_dataset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#delete_dataset)
        """

    async def delete_job(self, *, Name: str) -> DeleteJobResponseTypeDef:
        """
        Deletes the specified DataBrew job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.delete_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#delete_job)
        """

    async def delete_project(self, *, Name: str) -> DeleteProjectResponseTypeDef:
        """
        Deletes an existing DataBrew project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.delete_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#delete_project)
        """

    async def delete_recipe_version(
        self, *, Name: str, RecipeVersion: str
    ) -> DeleteRecipeVersionResponseTypeDef:
        """
        Deletes a single version of a DataBrew recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.delete_recipe_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#delete_recipe_version)
        """

    async def delete_ruleset(self, *, Name: str) -> DeleteRulesetResponseTypeDef:
        """
        Deletes a ruleset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.delete_ruleset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#delete_ruleset)
        """

    async def delete_schedule(self, *, Name: str) -> DeleteScheduleResponseTypeDef:
        """
        Deletes the specified DataBrew schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.delete_schedule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#delete_schedule)
        """

    async def describe_dataset(self, *, Name: str) -> DescribeDatasetResponseTypeDef:
        """
        Returns the definition of a specific DataBrew dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.describe_dataset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#describe_dataset)
        """

    async def describe_job(self, *, Name: str) -> DescribeJobResponseTypeDef:
        """
        Returns the definition of a specific DataBrew job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.describe_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#describe_job)
        """

    async def describe_job_run(self, *, Name: str, RunId: str) -> DescribeJobRunResponseTypeDef:
        """
        Represents one run of a DataBrew job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.describe_job_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#describe_job_run)
        """

    async def describe_project(self, *, Name: str) -> DescribeProjectResponseTypeDef:
        """
        Returns the definition of a specific DataBrew project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.describe_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#describe_project)
        """

    async def describe_recipe(
        self, *, Name: str, RecipeVersion: str = ...
    ) -> DescribeRecipeResponseTypeDef:
        """
        Returns the definition of a specific DataBrew recipe corresponding to a
        particular version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.describe_recipe)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#describe_recipe)
        """

    async def describe_ruleset(self, *, Name: str) -> DescribeRulesetResponseTypeDef:
        """
        Retrieves detailed information about the ruleset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.describe_ruleset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#describe_ruleset)
        """

    async def describe_schedule(self, *, Name: str) -> DescribeScheduleResponseTypeDef:
        """
        Returns the definition of a specific DataBrew schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.describe_schedule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#describe_schedule)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#generate_presigned_url)
        """

    async def list_datasets(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListDatasetsResponseTypeDef:
        """
        Lists all of the DataBrew datasets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.list_datasets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#list_datasets)
        """

    async def list_job_runs(
        self, *, Name: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListJobRunsResponseTypeDef:
        """
        Lists all of the previous runs of a particular DataBrew job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.list_job_runs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#list_job_runs)
        """

    async def list_jobs(
        self,
        *,
        DatasetName: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        ProjectName: str = ...
    ) -> ListJobsResponseTypeDef:
        """
        Lists all of the DataBrew jobs that are defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.list_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#list_jobs)
        """

    async def list_projects(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListProjectsResponseTypeDef:
        """
        Lists all of the DataBrew projects that are defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.list_projects)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#list_projects)
        """

    async def list_recipe_versions(
        self, *, Name: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListRecipeVersionsResponseTypeDef:
        """
        Lists the versions of a particular DataBrew recipe, except for `LATEST_WORKING`
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.list_recipe_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#list_recipe_versions)
        """

    async def list_recipes(
        self, *, MaxResults: int = ..., NextToken: str = ..., RecipeVersion: str = ...
    ) -> ListRecipesResponseTypeDef:
        """
        Lists all of the DataBrew recipes that are defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.list_recipes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#list_recipes)
        """

    async def list_rulesets(
        self, *, TargetArn: str = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> ListRulesetsResponseTypeDef:
        """
        List all rulesets available in the current account or rulesets associated with a
        specific resource (dataset).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.list_rulesets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#list_rulesets)
        """

    async def list_schedules(
        self, *, JobName: str = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> ListSchedulesResponseTypeDef:
        """
        Lists the DataBrew schedules that are defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.list_schedules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#list_schedules)
        """

    async def list_tags_for_resource(
        self, *, ResourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all the tags for a DataBrew resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#list_tags_for_resource)
        """

    async def publish_recipe(
        self, *, Name: str, Description: str = ...
    ) -> PublishRecipeResponseTypeDef:
        """
        Publishes a new version of a DataBrew recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.publish_recipe)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#publish_recipe)
        """

    async def send_project_session_action(
        self,
        *,
        Name: str,
        Preview: bool = ...,
        RecipeStep: "RecipeStepTypeDef" = ...,
        StepIndex: int = ...,
        ClientSessionId: str = ...,
        ViewFrame: "ViewFrameTypeDef" = ...
    ) -> SendProjectSessionActionResponseTypeDef:
        """
        Performs a recipe step within an interactive DataBrew session that's currently
        open.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.send_project_session_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#send_project_session_action)
        """

    async def start_job_run(self, *, Name: str) -> StartJobRunResponseTypeDef:
        """
        Runs a DataBrew job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.start_job_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#start_job_run)
        """

    async def start_project_session(
        self, *, Name: str, AssumeControl: bool = ...
    ) -> StartProjectSessionResponseTypeDef:
        """
        Creates an interactive session, enabling you to manipulate data in a DataBrew
        project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.start_project_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#start_project_session)
        """

    async def stop_job_run(self, *, Name: str, RunId: str) -> StopJobRunResponseTypeDef:
        """
        Stops a particular run of a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.stop_job_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#stop_job_run)
        """

    async def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds metadata tags to a DataBrew resource, such as a dataset, project, recipe,
        job, or schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#tag_resource)
        """

    async def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes metadata tags from a DataBrew resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#untag_resource)
        """

    async def update_dataset(
        self,
        *,
        Name: str,
        Input: "InputTypeDef",
        Format: InputFormatType = ...,
        FormatOptions: "FormatOptionsTypeDef" = ...,
        PathOptions: "PathOptionsTypeDef" = ...
    ) -> UpdateDatasetResponseTypeDef:
        """
        Modifies the definition of an existing DataBrew dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.update_dataset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#update_dataset)
        """

    async def update_profile_job(
        self,
        *,
        Name: str,
        OutputLocation: "S3LocationTypeDef",
        RoleArn: str,
        Configuration: "ProfileConfigurationTypeDef" = ...,
        EncryptionKeyArn: str = ...,
        EncryptionMode: EncryptionModeType = ...,
        LogSubscription: LogSubscriptionType = ...,
        MaxCapacity: int = ...,
        MaxRetries: int = ...,
        ValidationConfigurations: Sequence["ValidationConfigurationTypeDef"] = ...,
        Timeout: int = ...,
        JobSample: "JobSampleTypeDef" = ...
    ) -> UpdateProfileJobResponseTypeDef:
        """
        Modifies the definition of an existing profile job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.update_profile_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#update_profile_job)
        """

    async def update_project(
        self, *, RoleArn: str, Name: str, Sample: "SampleTypeDef" = ...
    ) -> UpdateProjectResponseTypeDef:
        """
        Modifies the definition of an existing DataBrew project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.update_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#update_project)
        """

    async def update_recipe(
        self, *, Name: str, Description: str = ..., Steps: Sequence["RecipeStepTypeDef"] = ...
    ) -> UpdateRecipeResponseTypeDef:
        """
        Modifies the definition of the `LATEST_WORKING` version of a DataBrew recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.update_recipe)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#update_recipe)
        """

    async def update_recipe_job(
        self,
        *,
        Name: str,
        RoleArn: str,
        EncryptionKeyArn: str = ...,
        EncryptionMode: EncryptionModeType = ...,
        LogSubscription: LogSubscriptionType = ...,
        MaxCapacity: int = ...,
        MaxRetries: int = ...,
        Outputs: Sequence["OutputTypeDef"] = ...,
        DataCatalogOutputs: Sequence["DataCatalogOutputTypeDef"] = ...,
        DatabaseOutputs: Sequence["DatabaseOutputTypeDef"] = ...,
        Timeout: int = ...
    ) -> UpdateRecipeJobResponseTypeDef:
        """
        Modifies the definition of an existing DataBrew recipe job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.update_recipe_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#update_recipe_job)
        """

    async def update_ruleset(
        self, *, Name: str, Rules: Sequence["RuleTypeDef"], Description: str = ...
    ) -> UpdateRulesetResponseTypeDef:
        """
        Updates specified ruleset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.update_ruleset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#update_ruleset)
        """

    async def update_schedule(
        self, *, CronExpression: str, Name: str, JobNames: Sequence[str] = ...
    ) -> UpdateScheduleResponseTypeDef:
        """
        Modifies the definition of an existing DataBrew schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.update_schedule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#update_schedule)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_datasets"]) -> ListDatasetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_job_runs"]) -> ListJobRunsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_jobs"]) -> ListJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_projects"]) -> ListProjectsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_recipe_versions"]
    ) -> ListRecipeVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_recipes"]) -> ListRecipesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_rulesets"]) -> ListRulesetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_schedules"]) -> ListSchedulesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#get_paginator)
        """

    async def __aenter__(self) -> "GlueDataBrewClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/)
        """
