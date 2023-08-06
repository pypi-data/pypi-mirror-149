import pytest

from great_expectations.rule_based_profiler.helpers.util import (
    integer_semantic_domain_type,
)
from great_expectations.rule_based_profiler.types import (
    INFERRED_SEMANTIC_TYPE_KEY,
    Domain,
    SemanticDomainTypes,
)


def test_semantic_domain_serialization():
    domain: Domain

    domain = Domain(
        rule_name="my_rule",
        domain_type="column",
        domain_kwargs={"column": "passenger_count"},
        details={
            "estimator": "categorical",
            "cardinality": "low",
        },
    )

    assert domain.to_json_dict() == {
        "rule_name": "my_rule",
        "domain_type": "column",
        "domain_kwargs": {"column": "passenger_count"},
        "details": {
            "estimator": "categorical",
            "cardinality": "low",
        },
    }

    domain = Domain(
        rule_name="my_rule",
        domain_type="column",
        domain_kwargs={"column": "passenger_count"},
        details={
            "estimator": "categorical",
            "cardinality": "low",
            INFERRED_SEMANTIC_TYPE_KEY: {
                "passenger_count": SemanticDomainTypes.NUMERIC,
            },
        },
    )

    assert domain.to_json_dict() == {
        "rule_name": "my_rule",
        "domain_type": "column",
        "domain_kwargs": {
            "column": "passenger_count",
        },
        "details": {
            "estimator": "categorical",
            "cardinality": "low",
            INFERRED_SEMANTIC_TYPE_KEY: {
                "passenger_count": SemanticDomainTypes.NUMERIC.value,
            },
        },
    }

    domain = Domain(
        rule_name="my_rule",
        domain_type="column",
        domain_kwargs={"column": "passenger_count"},
        details={
            "estimator": "categorical",
            "cardinality": "low",
            INFERRED_SEMANTIC_TYPE_KEY: {
                "passenger_count": SemanticDomainTypes.NUMERIC,
            },
        },
    )

    assert domain.to_json_dict() == {
        "rule_name": "my_rule",
        "domain_type": "column",
        "domain_kwargs": {
            "column": "passenger_count",
        },
        "details": {
            "estimator": "categorical",
            "cardinality": "low",
            INFERRED_SEMANTIC_TYPE_KEY: {
                "passenger_count": SemanticDomainTypes.NUMERIC.value,
            },
        },
    }


def test_semantic_domain_comparisons():
    domain_a: Domain
    domain_b: Domain
    domain_c: Domain

    domain_a = Domain(
        rule_name="my_rule",
        domain_type="column",
        domain_kwargs={"column": "VendorID"},
        details={
            INFERRED_SEMANTIC_TYPE_KEY: {
                "VendorID": SemanticDomainTypes.NUMERIC,
            },
        },
    )
    domain_b = Domain(
        rule_name="my_rule",
        domain_type="column",
        domain_kwargs={"column": "passenger_count"},
        details={
            INFERRED_SEMANTIC_TYPE_KEY: {
                "passenger_count": SemanticDomainTypes.NUMERIC,
            },
        },
    )
    domain_c = Domain(
        rule_name="my_rule",
        domain_type="column",
        domain_kwargs={"column": "passenger_count"},
        details={
            INFERRED_SEMANTIC_TYPE_KEY: {
                "passenger_count": SemanticDomainTypes.NUMERIC,
            },
        },
    )

    assert not (domain_a == domain_b)
    assert domain_b == domain_c

    domain_a = Domain(
        rule_name="my_rule",
        domain_type="column",
        domain_kwargs={"column": "VendorID"},
        details={
            INFERRED_SEMANTIC_TYPE_KEY: {
                "VendorID": SemanticDomainTypes.NUMERIC,
            },
        },
    )
    domain_b = Domain(
        rule_name="my_rule",
        domain_type="column",
        domain_kwargs={"column": "passenger_count"},
        details={
            INFERRED_SEMANTIC_TYPE_KEY: {
                "passenger_count": SemanticDomainTypes.NUMERIC,
            },
        },
    )
    domain_c = Domain(
        rule_name="my_rule",
        domain_type="column",
        domain_kwargs={"column": "passenger_count"},
        details={
            INFERRED_SEMANTIC_TYPE_KEY: {
                "passenger_count": SemanticDomainTypes.NUMERIC,
            },
        },
    )

    assert not (domain_a == domain_b)
    assert domain_b == domain_c

    domain_d: Domain = Domain(
        rule_name="my_rule",
        domain_type="column",
        domain_kwargs={"column": "passenger_count"},
        details={
            INFERRED_SEMANTIC_TYPE_KEY: {
                "passenger_count": "unknown_semantic_type_as_string",
            },
        },
    )

    with pytest.raises(ValueError) as excinfo:
        # noinspection PyUnusedLocal
        domain_as_dict: dict = domain_d.to_json_dict()

    assert (
        "'unknown_semantic_type_as_string' is not a valid SemanticDomainTypes"
        in str(excinfo.value)
    )

    domain_e: Domain = Domain(
        rule_name="my_rule",
        domain_type="column",
        domain_kwargs={"column": "passenger_count"},
        details={
            "estimator": "categorical",
            "cardinality": "low",
            INFERRED_SEMANTIC_TYPE_KEY: {
                "passenger_count": "unknown_semantic_type_as_string",
            },
        },
    )

    with pytest.raises(ValueError) as excinfo:
        # noinspection PyUnusedLocal
        domain_as_dict: dict = domain_e.to_json_dict()

    assert (
        "'unknown_semantic_type_as_string' is not a valid SemanticDomainTypes"
        in str(excinfo.value)
    )


def test_integer_semantic_domain_type():
    domain: Domain

    domain = Domain(
        rule_name="my_rule",
        domain_type="column",
        domain_kwargs={
            "column": "passenger_count",
        },
        details={
            INFERRED_SEMANTIC_TYPE_KEY: {
                "VendorID": SemanticDomainTypes.NUMERIC,
            },
        },
    )
    assert not integer_semantic_domain_type(domain=domain)

    domain = Domain(
        rule_name="my_rule",
        domain_type="column",
        domain_kwargs={
            "column": "VendorID",
        },
        details={
            INFERRED_SEMANTIC_TYPE_KEY: {
                "VendorID": SemanticDomainTypes.IDENTIFIER,
            },
        },
    )
    assert integer_semantic_domain_type(domain=domain)

    domain = Domain(
        rule_name="my_rule",
        domain_type="column",
        domain_kwargs={
            "column": "is_night_time",
        },
        details={
            INFERRED_SEMANTIC_TYPE_KEY: {
                "is_night_time": SemanticDomainTypes.LOGIC,
            },
        },
    )
    assert integer_semantic_domain_type(domain=domain)

    domain = Domain(
        rule_name="my_rule",
        domain_type="column",
        domain_kwargs={
            "column_A": "passenger_count",
            "column_B": "fare_amount",
        },
        details={
            INFERRED_SEMANTIC_TYPE_KEY: {
                "passenger_count": SemanticDomainTypes.NUMERIC,
                "fare_amount": SemanticDomainTypes.NUMERIC,
            },
        },
    )
    assert not integer_semantic_domain_type(domain=domain)

    domain = Domain(
        rule_name="my_rule",
        domain_type="column",
        domain_kwargs={
            "column_A": "passenger_count",
            "column_B": "VendorID",
        },
        details={
            INFERRED_SEMANTIC_TYPE_KEY: {
                "passenger_count": SemanticDomainTypes.NUMERIC,
                "VendorID": SemanticDomainTypes.IDENTIFIER,
            },
        },
    )
    assert not integer_semantic_domain_type(domain=domain)

    domain = Domain(
        rule_name="my_rule",
        domain_type="column",
        domain_kwargs={
            "column_A": "is_night_time",
            "column_B": "VendorID",
        },
        details={
            INFERRED_SEMANTIC_TYPE_KEY: {
                "is_night_time": SemanticDomainTypes.LOGIC,
                "VendorID": SemanticDomainTypes.IDENTIFIER,
            },
        },
    )
    assert integer_semantic_domain_type(domain=domain)

    domain = Domain(
        rule_name="my_rule",
        domain_type="column",
        domain_kwargs={
            "column_list": [
                "passenger_count",
                "fare_amount",
                "is_night_time",
            ],
        },
        details={
            INFERRED_SEMANTIC_TYPE_KEY: {
                "passenger_count": SemanticDomainTypes.NUMERIC,
                "fare_amount": SemanticDomainTypes.NUMERIC,
                "is_night_time": SemanticDomainTypes.LOGIC,
            },
        },
    )
    assert not integer_semantic_domain_type(domain=domain)

    domain = Domain(
        rule_name="my_rule",
        domain_type="column",
        domain_kwargs={
            "column_list": [
                "VendorID",
                "fare_amount",
                "is_night_time",
            ],
        },
        details={
            INFERRED_SEMANTIC_TYPE_KEY: {
                "VendorID": SemanticDomainTypes.IDENTIFIER,
                "RatecodeID": SemanticDomainTypes.IDENTIFIER,
                "is_night_time": SemanticDomainTypes.LOGIC,
            },
        },
    )
    assert integer_semantic_domain_type(domain=domain)
