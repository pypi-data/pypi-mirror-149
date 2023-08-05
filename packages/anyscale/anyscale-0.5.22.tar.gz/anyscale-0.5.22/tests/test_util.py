from typing import Any, Dict
from unittest.mock import patch

import pytest

from anyscale.util import (
    _update_external_ids_for_policy,
    number_of_external_ids_in_policy,
    updating_printer,
)


def test_updating_printer() -> None:
    out = ""

    def mock_print(
        string: str, *args: Any, end: str = "\n", flush: bool = False, **kwargs: Any
    ) -> None:
        nonlocal out
        out += string
        out += end

    with patch("anyscale.util.print", new=mock_print), patch(
        "shutil.get_terminal_size"
    ) as get_terminal_size_mock:
        get_terminal_size_mock.return_value = (10, 24)
        with updating_printer() as print_status:
            print_status("Step 1")
            print_status("Step 2")
            print_status("Step 3")

    assert out == (
        "\r          \r"
        "Step 1"
        "\r          \r"
        "Step 2"
        "\r          \r"
        "Step 3"
        "\r          \r"
    )


def test_updating_printer_multiline() -> None:
    out = ""

    def mock_print(
        string: str, *args: Any, end: str = "\n", flush: bool = False, **kwargs: Any
    ) -> None:
        nonlocal out
        out += string
        out += end

    with patch("anyscale.util.print", new=mock_print), patch(
        "shutil.get_terminal_size"
    ) as get_terminal_size_mock:
        get_terminal_size_mock.return_value = (10, 24)
        with updating_printer() as print_status:
            print_status("Step 1\nExtra stuff")
            print_status("ExtraLongLine12345")
            print_status("ExtraLongLine12345\nExtra stuff")
            print_status("Step 3")

    assert out == (
        "\r          \r"
        "Step 1..."
        "\r          \r"
        "ExtraLo..."
        "\r          \r"
        "ExtraLo..."
        "\r          \r"
        "Step 3"
        "\r          \r"
    )


STATEMENT_TEMPLATE = {
    "Action": "sts:AssumeRole",
    "Effect": "Allow",
    "Principal": {"AWS": "arn:aws:iam::ACCT_ID:root"},
}


@pytest.mark.parametrize(
    "statement_policy,expected_conditions",
    [
        pytest.param(
            [STATEMENT_TEMPLATE],
            [{"StringEquals": {"sts:ExternalId": ["new_id"]}}],
            id="OneStatement,NoPrior",
        ),
        pytest.param(
            [STATEMENT_TEMPLATE, STATEMENT_TEMPLATE],
            [{"StringEquals": {"sts:ExternalId": ["new_id"]}}] * 2,
            id="TwoStatements,NoPrior",
        ),
        pytest.param(
            [
                {
                    "Condition": {"StringEquals": {"sts:ExternalId": "old_id"}},
                    **STATEMENT_TEMPLATE,  # type: ignore
                }
            ],
            [{"StringEquals": {"sts:ExternalId": ["old_id", "new_id"]}}],
            id="OneStatement,OnePriorExternal",
        ),
        pytest.param(
            [
                {
                    "Condition": {"StringEquals": {"sts:ExternalId": "old_id"}},
                    **STATEMENT_TEMPLATE,  # type: ignore
                },
                STATEMENT_TEMPLATE,
            ],
            [
                {"StringEquals": {"sts:ExternalId": ["old_id", "new_id"]}},
                {"StringEquals": {"sts:ExternalId": ["new_id"]}},
            ],
            id="TwoStatements,OnePriorExternal",
        ),
        pytest.param(
            [
                {
                    "Condition": {"StringNotEquals": {"sts:ExternalId": "old_id"}},
                    **STATEMENT_TEMPLATE,  # type: ignore
                },
                STATEMENT_TEMPLATE,
            ],
            [
                {
                    "StringEquals": {"sts:ExternalId": ["new_id"]},
                    "StringNotEquals": {"sts:ExternalId": "old_id"},
                },
            ],
            id="OneStatemnt,OtherCondition",
        ),
    ],
)
def test_update_external_ids_for_policy(statement_policy, expected_conditions):
    policy_document = {
        "Statement": statement_policy,
        "Version": "2012-10-17",
    }
    new_policy = _update_external_ids_for_policy(policy_document, "new_id")

    for new, expected in zip(new_policy["Statement"], expected_conditions):
        assert new["Condition"] == expected


@pytest.mark.parametrize(
    "statement,num_ext_ids",
    [
        pytest.param(
            [STATEMENT_TEMPLATE, STATEMENT_TEMPLATE],
            0,
            id="MultipleStatements,NoExtID",
        ),
        pytest.param(
            [
                {
                    "Condition": {"StringEquals": {"sts:ExternalId": "old_id"}},
                    **STATEMENT_TEMPLATE,  # type: ignore
                },
                STATEMENT_TEMPLATE,
            ],
            1,
            id="OneExternalID,MultipleStatements",
        ),
        pytest.param(
            [
                {
                    "Condition": {
                        "StringEquals": {"sts:ExternalId": ["id_one", "id_two"]}
                    },
                    **STATEMENT_TEMPLATE,  # type: ignore
                }
            ],
            2,
            id="ExternalIdList",
        ),
    ],
)
def test_number_of_external_ids_in_policy(statement: Dict[str, Any], num_ext_ids: int):
    policy = {
        "Statement": statement,
        "Version": "2012-10-17",
    }
    assert number_of_external_ids_in_policy(policy) == num_ext_ids
