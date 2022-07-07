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


def test_update_docval_cannot_use_both_keep_and_remove():
    """Verifies that an exception is raised if both keep and remove are used"""
    with pytest.raises(ValueError):
        _ = update_docval(
            fake_function,
            keep=["baz"],
            remove=["foo"],
        )


def test_update_docval_keep_should_filter_parameters():
    """Verify that use of 'keep' keeps only the specified parameters"""
    new_docval = update_docval(fake_function, keep=["foo", "baz"])
    assert len(new_docval) == 2
    assert new_docval[0]["name"] == "foo"
    assert new_docval[1]["name"] == "baz"


def test_update_docval_with_invalid_name_in_keep_list():
    """Verify than an exception is raised if the keep list contains the name of
    a non-existing docval item
    """
    with pytest.raises(ValueError):
        _ = update_docval(
            fake_function,
            keep=["nonexistant_item"],
        )


def test_update_docval_remove_should_filter_parameters():
    """Verify that use of 'remove' removes only the specified parameters"""
    new_docval = update_docval(fake_function, remove=["foo", "baz"])
    assert len(new_docval) == 1
    assert new_docval[0]["name"] == "bar"


def test_update_docval_with_invalid_name_in_remove_list():
    """Verify than an exception is raised if the remove list contains the name of
    a non-existing docval item
    """
    with pytest.raises(ValueError):
        _ = update_docval(
            fake_function,
            remove=["nonexistant_item"],
        )


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
