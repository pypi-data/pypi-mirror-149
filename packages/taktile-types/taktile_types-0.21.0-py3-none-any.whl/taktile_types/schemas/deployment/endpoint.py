"""
Schemas related to model endpoints
"""
import typing as t

from pydantic import UUID4, BaseModel

from taktile_types.enums.endpoint import (
    ArrowFormatKinds,
    EndpointKinds,
    ProfileKinds,
)


class EndpointInfoSchema(BaseModel):
    """EndpointInfoSchema.
    Endpoint type of /info endpoint

    Attributes
    ----------

    name : str
        name of endpoint
    position : t.Optional[int]
        position of endpoint relative to others
    path : str
        path of endpoint
    kind : EndpointKinds
       kind of endpoint
    profile_kind : t.Optional[ProfileKinds]
       profile type of this endpoint
    explain_path : t.Optional[str]
        where is the explainer endpoint
    response_kind: t.Optional[ArrowFormatKinds]
        what type of arrow response does this endpoint return
    input_names: t.List[str] = []
        list of input names
    output_names: t.Optional[str] = None
        output name
    profile_columns : t.Optional[t.List[str]] = None
        columns that have been profiled
    input_example : t.Optional[t.List[t.Dict[str, t.Any]]] = None
        json input example for this endpoint
    output_example : t.Optional[t.List[t.Any]] = None
        example output of endpoint
    explainer_example : t.Optional[t.List[t.Any]] = None
        example input for explainer
    tags : t.Optional[t.List[str]]
        list of tags of this endpoint
    """

    name: str
    position: t.Optional[int]
    path: str
    kind: EndpointKinds
    profile_kind: t.Optional[ProfileKinds]
    explain_path: t.Optional[str]
    response_kind: t.Optional[ArrowFormatKinds]
    input_names: t.List[str] = []
    output_names: t.Optional[str] = None
    profile_columns: t.Optional[t.List[str]] = None
    input_example: t.Optional[t.List[t.Dict[str, t.Any]]] = None
    output_example: t.Optional[t.List[t.Any]] = None
    explainer_example: t.Optional[t.List[t.Any]] = None
    tags: t.Optional[t.List[str]]


class InfoEndpointResponseModelBase(BaseModel):
    """InfoEndpointResponseModel.
    Return type of info endpoint for REST and GRPC
    Attributes
    ----------
    schema_version:: str
        response version of this response
    taktile_cli : str
        taktile_cli version installed
    profiling : str
        profiling version installed
    git_sha : str
        commit sha of model
    git_ref : str
        git branch name of model
    """

    schema_version: str
    taktile_cli: str
    profiling: str
    git_sha: t.Optional[str] = "unknown"
    git_ref: t.Optional[str] = "unknown"


class InfoEndpointResponseModelFlight(InfoEndpointResponseModelBase):
    """InfoEndpointResponseModel.
    Return type of /info GRPC endpoint

    Attributes
    ----------
    schema_version:: str
        response version of this response
    taktile_cli : str
        taktile_cli version installed
    profiling : str
        profiling version installed
    git_sha : str
        commit sha of model
    git_ref : str
        git branch name of model
    """


class InfoEndpointResponseModel(InfoEndpointResponseModelBase):
    """InfoEndpointResponseModel.
    Return type of /info REST endpoint

    Attributes
    ----------
    schema_version:: str
        response version of this response
    taktile_cli : str
        taktile_cli version installed
    profiling : str
        profiling version installed
    git_sha : str
        commit sha of model
    git_ref : str
        git branch name of model
    endpoints : t.List[EndpointInfoSchema]
        list of endpoints on this model
    """

    endpoints: t.List[EndpointInfoSchema]


class EndpointDeploymentApi(BaseModel):
    """EndpointDeploymentApi.
    Endpoint type in deployment-api

    Attributes
    ----------
    id : UUID4
        unique identifier of endpoint
    name : str
        name of endpoint
    git_hash : str
        sha of git commit of this endpoint
    """

    id: UUID4
    name: str
    git_hash: str


class ModelEndpoint(BaseModel):
    """ModelEndpoint.
    Extended endpoint type on deployment-api

    Attributes
    ----------
    kind : t.Optional[EndpointKinds]
        endpoint kind
    position : int
        order of endpoints
    tags : t.List[str]
        tags of an endpoint (see OAS)
    """

    kind: t.Optional[EndpointKinds]
    position: int
    tags: t.List[str]
