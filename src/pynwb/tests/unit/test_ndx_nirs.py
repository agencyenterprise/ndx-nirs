import pytest

from pynwb.testing import TestCase
from hdmf.utils import get_docval
from hdmf.common import DynamicTable

from ndx_nirs import (
    NIRSSourcesTable,
    NIRSDetectorsTable,
    NIRSChannelsTable,
    NIRSDevice,
    update_docval,
)


def test_update_docval_does_not_modify_original_docval():
    """Verify that update_docval does not modify the original fn docval"""
    original_docval = get_docval(DynamicTable.__init__)
    _ = update_docval(DynamicTable.__init__, name={"default": "FOO"})
    assert "default" not in original_docval[0]


def test_update_docval_correctly_updates_fields():
    """Verify that update_docval correctly updates the new docval"""
    new_docval = update_docval(
        DynamicTable.__init__,
        name={"default": "FOO", "miscfield": "xyz"},
        description={"required": False},
    )
    assert new_docval[0]["default"] == "FOO"
    assert new_docval[0]["miscfield"] == "xyz"
    assert not new_docval[1]["required"]


def test_update_docval_raises_error_if_parameter_does_not_exist():
    """Verify that update_docval raises a ValueError if the parameter doesn't exist"""
    with pytest.raises(ValueError):
        _ = update_docval(
            DynamicTable.__init__,
            foo={"default": "bar"},
        )


class TestNIRSSourcesTable(TestCase):
    """Unit tests for NIRSSourcesTable"""

    def test_empty_constructor(self):
        """Verify that the table can be instantiated with default name and description"""
        table = NIRSSourcesTable()

        self.assertEqual(table.name, "NIRSSourcesTable")
        self.assertIsInstance(table.description, str)

    def test_add_row_without_optional_z(self):
        """Verify that add_row correctly adds a row when z is omitted"""
        table = NIRSSourcesTable()
        table.add_row(label="foo", x=1.0, y=2.0)

        self.assertEqual(len(table), 1)
        self.assertEqual(table.label[0], "foo")
        self.assertEqual(table.x[0], 1.0)
        self.assertEqual(table.y[0], 2.0)
        self.assertIsNone(table.z)

    def test_add_row_with_optional_z(self):
        """Verify that add_row correctly adds a row when z is included"""
        table = NIRSSourcesTable()
        table.add_row(label="foo", x=1.0, y=2.0, z=3.0)

        self.assertEqual(len(table), 1)
        self.assertEqual(table.label[0], "foo")
        self.assertEqual(table.x[0], 1.0)
        self.assertEqual(table.y[0], 2.0)
        self.assertEqual(table.z[0], 3.0)
