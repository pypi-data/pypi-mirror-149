"""
Schemas related to model unit tests
"""
import typing as t

from pydantic import UUID4, BaseModel

from taktile_types.enums.deployment.test import TestOutcomeColor, TestTypes


class TestResultSpecBase(BaseModel):
    """TestResultSpecBase.
    Base model of a test suite

    Attributes
    ----------
    test_suite_id : UUID4
        unique identifier
    outcome : str
        outcome of this test suite. TODO: This should be properly typed.

    """

    test_suite_id: UUID4
    outcome: str


class TestResultSpec(TestResultSpecBase):
    """TestResultSpec.
    Extended model of a test suite

    Attributes
    ----------
    section_name : str
        section name in which this test is
    message: str
        message of this test (either failure or success message)
    file_path: t.Optional[str]
        file path of the test file this is from
    test_name: t.Optional[str]
        name of of the test
    test_type: TestTypes
        type of test. TODO: Remove this, we don't use it.
    """

    section_name: str
    message: str
    file_path: t.Optional[str]
    test_name: t.Optional[str]
    test_type: TestTypes


class TestResultResponse(BaseModel):
    """TestResultResponse.
    Deployment-Api response model for tests

    Attributes
    ----------
    color : TestOutcomeColor
        a simplified color response: TODO: Remove this, we don't use it.
    git_hash : str
        git hash of this model
    results : t.List[TestResultSpec]
        list of test results
    """

    color: TestOutcomeColor
    git_hash: str
    results: t.List[TestResultSpec]
