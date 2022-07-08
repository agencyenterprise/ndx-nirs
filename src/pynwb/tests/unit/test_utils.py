import pytest

from hdmf.utils import docval, get_docval

from ndx_nirs import update_docval


@docval(
    {"name": "foo", "type": str, "doc": "a parameter named foo"},
    {"name": "bar", "type": int, "doc": "a parameter named bar", "default": None},
    {"name": "baz", "type": str, "doc": "a parameter named baz", "default": "BAZ"},
)
def fake_function(*args, **kwargs):
    """A function declared just to test the functionality of update_docval"""
    pass


def test_update_docval_does_not_modify_original_docval():
    """Verify that update_docval does not modify the docval of the original fn"""
    original_docval = get_docval(fake_function)
    _ = update_docval(fake_function, updates=dict(foo={"default": "FOO"}))
    assert "default" not in original_docval[0]


def test_update_docval_correctly_updates_fields():
    """Verify that update_docval correctly updates the new docval"""
    new_docval = update_docval(
        fake_function,
        updates=dict(
            foo={"default": "FOO", "miscfield": "xyz"},
            bar={"default": None},
        ),
    )
    assert new_docval[0]["default"] == "FOO"
    assert new_docval[0]["miscfield"] == "xyz"
    assert new_docval[1]["default"] is None


def test_update_docval_raises_error_if_parameter_does_not_exist():
    """Verify that update_docval raises a ValueError if the parameter doesn't exist"""
    with pytest.raises(ValueError):
        _ = update_docval(
            fake_function,
            updates=dict(badparam={"doc": "this parameter doesn't exist"}),
        )
