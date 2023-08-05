"""
Schemas related to the /models endpoint
"""
import typing as t
from datetime import datetime

from pydantic import UUID4, BaseModel

from taktile_types.enums.endpoint import EndpointKinds
from taktile_types.enums.repository.access import AccessKind
from taktile_types.schemas.deployment.endpoint import EndpointDeploymentApi
from taktile_types.schemas.deployment.test import TestResultResponse
from taktile_types.schemas.repository.pull_request import PullRequest


class ModelEndpoint(EndpointDeploymentApi):
    """ModelEndpoint.
    Extended endpoint model

    Attributes
    ----------
    kind : t.Optional[EndpointKinds]
        The kind of this endpoint
    position : int
        Its position relative to the other endpoints
    tags : t.List[str]
        A list of tags of this endpoint
    """

    kind: t.Optional[EndpointKinds]
    position: int
    tags: t.List[str]


class ModelDeployment(BaseModel):
    """ModelDeployment.
    A deployed model

    Attributes
    ----------
    id : UUID4
        unique identifier
    created_at : datetime
        when was this created
    status : t.Optional[str]
       status of this deployment
    public_docs_url : t.Optional[str]
       url to the public documentation
    rest_cpu_request : t.Optional[str]
       cpu requested
    rest_memory_request : t.Optional[str]
       memory requested
    rest_gpu_request : t.Optional[str]
        gpu requested
    arrow_cpu_request : t.Optional[str]
       cpu requested
    arrow_memory_request : t.Optional[str]
       memory requested
    arrow_gpu_request : t.Optional[str]
       gru requested
    rest_replicas : t.Optional[int]
       rest default replicas requested
    max_rest_replicas : t.Optional[int]
       rest max replicas
    arrow_replicas : t.Optional[int]
       arrow replicas
    git_ref : str
       git ref of this deployment
    check_run_reference_id : t.Optional[int]
       GH id of latest check run
    commit_hash : str
       commit hash of this deployment
    endpoints : t.List[ModelEndpoint]
       endpoints of this deployment
    tests : t.Optional[TestResultResponse]
       tests of this deployment
    running_commit : t.Optional[str]
       currently running commit
    rest_runtime_logs_link : t.Optional[str]
       link to rest runtime logs on Grafana
    grpc_runtime_logs_link : t.Optional[str]
       link to arrow runtime logs on Grafana
    build_logs_link : t.Optional[str]
       link to build logs on Grafana
    rest_runtime_dashboard_link : t.Optional[str]
       link to rest dashboard on grafana
    grpc_runtime_dashboard_link : t.Optional[str]
       link to grpc dashboard on grafana
    """

    id: UUID4
    created_at: datetime
    status: t.Optional[str]
    public_docs_url: t.Optional[str]
    rest_cpu_request: t.Optional[str]
    rest_memory_request: t.Optional[str]
    rest_gpu_request: t.Optional[str]
    arrow_cpu_request: t.Optional[str]
    arrow_memory_request: t.Optional[str]
    arrow_gpu_request: t.Optional[str]
    rest_replicas: t.Optional[int]
    max_rest_replicas: t.Optional[int]
    arrow_replicas: t.Optional[int]
    git_ref: str
    check_run_reference_id: t.Optional[int]
    commit_hash: str
    endpoints: t.List[ModelEndpoint]
    tests: t.Optional[TestResultResponse]
    running_commit: t.Optional[str]

    rest_runtime_logs_link: t.Optional[str]
    grpc_runtime_logs_link: t.Optional[str]
    build_logs_link: t.Optional[str]
    rest_runtime_dashboard_link: t.Optional[str]
    grpc_runtime_dashboard_link: t.Optional[str]


class Model(BaseModel):
    """Model.
    Response of the model endpoint

    Attributes
    ----------
    id : UUID4
       unique identifier
    ref_id : int
       GH identifier of model
    repository_name : str
       name of repository
    repository_owner : str
        repository owner of model
    repository_default_branch : t.Optional[str] = None
        default branch of model
    repository_description : t.Optional[str] = None
        GH description of repository
    access : AccessKind
        Access type the requesting user has to this model
    pull_requests : t.List[PullRequest]
        A list of pull requests of this model
    deployments: t.List[ModelDeployment]
        A list of deployments of this model
    """

    id: UUID4
    ref_id: int
    repository_name: str
    repository_owner: str
    repository_default_branch: t.Optional[str] = None
    repository_description: t.Optional[str] = None
    access: AccessKind
    pull_requests: t.List[PullRequest]
    deployments: t.List[ModelDeployment]
