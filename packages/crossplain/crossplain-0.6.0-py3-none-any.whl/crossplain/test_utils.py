from crossplain.utils import split_expression
from ward import test


@test("splits a quote-less expression correctly")
def _():
    assert split_expression("foo bar baz") == ["foo", "bar", "baz"]

@test("splits an expression with a quoted part correctly")
def _():
    assert split_expression("$http_authentication == 'Bearer hunter2'") == [
        "$http_authentication",
        "==",
        "Bearer hunter2",
    ]
