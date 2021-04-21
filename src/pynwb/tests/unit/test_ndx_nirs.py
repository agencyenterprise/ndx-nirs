import pytest
import pandas as pd
import numpy as np

from pynwb.testing import TestCase
from hdmf.utils import get_docval
from hdmf.common import DynamicTable, DynamicTableRegion

from ndx_nirs import (
    NIRSSourcesTable,
    NIRSDetectorsTable,
    NIRSChannelsTable,
    NIRSDevice,
    NIRSSeries,
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

        self.assertEqual(table.name, "sources")
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


class TestNIRSDetectorsTable(TestCase):
    """Unit tests for NIRSDetectorsTable"""

    def test_empty_constructor(self):
        """Verify that the table can be instantiated with default name and description"""
        table = NIRSDetectorsTable()

        self.assertEqual(table.name, "detectors")
        self.assertIsInstance(table.description, str)

    def test_add_row_without_optional_z(self):
        """Verify that add_row correctly adds a row when z is omitted"""
        table = NIRSDetectorsTable()
        table.add_row(label="foo", x=1.0, y=2.0)

        self.assertEqual(len(table), 1)
        self.assertEqual(table.label[0], "foo")
        self.assertEqual(table.x[0], 1.0)
        self.assertEqual(table.y[0], 2.0)
        self.assertIsNone(table.z)

    def test_add_row_with_optional_z(self):
        """Verify that add_row correctly adds a row when z is included"""
        table = NIRSDetectorsTable()
        table.add_row(label="foo", x=1.0, y=2.0, z=3.0)

        self.assertEqual(len(table), 1)
        self.assertEqual(table.label[0], "foo")
        self.assertEqual(table.x[0], 1.0)
        self.assertEqual(table.y[0], 2.0)
        self.assertEqual(table.z[0], 3.0)


def create_fake_sources_table():
    """Returns a NIRSSourcesTable which can be used for testing"""
    table = NIRSSourcesTable()
    for n in range(7):
        table.add_row({"label": f"S{n+1}", "x": (n % 4) - 1.5, "y": (n % 3) - 1.0})
    return table


def create_fake_detectors_table():
    """Returns a NIRSDetectorsTable which can be used for testing"""
    table = NIRSDetectorsTable()
    for n in range(4):
        table.add_row({"label": f"D{n+1}", "x": (n % 2) + 0.5, "y": n - 3.5})
    return table


def create_fake_channels_table():
    """Returns a NIRSChannelsTable which can be used for testing"""
    sources = create_fake_sources_table()
    detectors = create_fake_detectors_table()
    source_detector_pairs = [(n, n % 5) for n in range(7)]
    table = NIRSChannelsTable(sources, detectors)
    ch_id = 0
    for source_idx, detector_idx in source_detector_pairs:
        for wavelength in [690.0, 830.0]:
            table.add_row(
                label=f"CH{ch_id}",
                source=source_idx,
                detector=detector_idx,
                source_wavelength=wavelength,
            )
            ch_id += 1
    return table


class TestNIRSChannelsTable(TestCase):
    """Unit tests for NIRSChannelsTable"""

    def test_constructor_assigns_tables(self):
        """Verify that the table can be instantiated and assigns source and detector tables"""
        sources = create_fake_sources_table()
        detectors = create_fake_detectors_table()
        table = NIRSChannelsTable(sources, detectors)

        self.assertEqual(table.name, "channels")
        self.assertIsInstance(table.description, str)
        self.assertIs(table.source.table, sources)
        self.assertIs(table.detector.table, detectors)

    def test_set_sources_table(self):
        """Verify that the sources table can be set after instantiation"""
        table = NIRSChannelsTable()
        sources = create_fake_sources_table()
        table.set_sources_table(sources)
        self.assertIs(table.source.table, sources)

    def test_set_detectors_table(self):
        """Verify that the sources table can be set after instantiation"""
        table = NIRSChannelsTable()
        detectors = create_fake_detectors_table()
        table.set_detectors_table(detectors)
        self.assertIs(table.detector.table, detectors)

    def test_add_row_with_the_correct_columns_provided(self):
        """Verify that add_row correctly adds a row when the correct columns are provided"""
        table = NIRSChannelsTable(
            create_fake_sources_table(), create_fake_detectors_table()
        )
        table.add_row(label="foo", source=6, detector=1, source_wavelength=123.5)

        self.assertEqual(len(table), 1)
        self.assertEqual(table.label[0], "foo")
        expected_source = pd.DataFrame(
            dict(label="S7", x=0.5, y=-1.0), index=pd.Index([6], name="id")
        )
        pd.testing.assert_frame_equal(table.source[0], expected_source)
        expected_detector = pd.DataFrame(
            dict(label="D2", x=1.5, y=-2.5), index=pd.Index([1], name="id")
        )
        pd.testing.assert_frame_equal(table.detector[0], expected_detector)
        self.assertEqual(table.source_wavelength[0], 123.5)

    def test_add_row_with_optional_columns(self):
        """Verify that optional columns can be specified"""
        table = NIRSChannelsTable(
            create_fake_sources_table(), create_fake_detectors_table()
        )
        table.add_row(
            label="foo",
            source=6,
            detector=1,
            source_wavelength=123.5,
            emission_wavelength=234.6,
            source_power=11.0,
            detector_gain=5.1,
        )

        self.assertEqual(table.emission_wavelength[0], 234.6)
        self.assertEqual(table.source_power[0], 11.0)
        self.assertEqual(table.detector_gain[0], 5.1)


class TestNIRSDevice(TestCase):
    """Unit tests for NIRSDevice"""

    def test_initialization(self):
        """Verify that fields are correctly defined after initialization"""
        channels = create_fake_channels_table()
        device = NIRSDevice(
            name="test_device",
            description="Foo",
            nirs_mode="time-domain",
            channels=channels,
            sources=channels.source.table,
            detectors=channels.detector.table,
        )
        self.assertEqual(device.name, "test_device")
        self.assertIs(device.channels, channels)
        self.assertIs(device.sources, channels.source.table)
        self.assertIs(device.detectors, channels.detector.table)

    def create_test_device_with_params(self, **kwargs):
        """Returns an initialized NIRSDevice giving it additional kwargs"""
        channels = create_fake_channels_table()
        return NIRSDevice(
            name="test_device",
            description="Foo",
            nirs_mode="time-domain",
            channels=channels,
            sources=channels.source.table,
            detectors=channels.detector.table,
            **kwargs,
        )

    def test_optional_attributes(self):
        """Verify that all expected optional attributes can be provided to a NIRSDevice"""
        test_attributes = {
            "frequency": 30.5,
            "time_delay": 25.0,
            "time_delay_width": 13.0,
            "correlation_time_delay": 0.013,
            "correlation_time_delay_width": 0.008,
            "additional_parameters": "some additional text",
        }
        for name, value in test_attributes.items():
            with self.subTest(attr_name=name, attr_value=value):
                device = self.create_test_device_with_params(**{name: value})
                self.assertEqual(
                    getattr(device, name),
                    value,
                    f"failed for '{name}' attribute subtest",
                )


class TestNIRSSeries(TestCase):
    """Unit tests for NIRSSeries"""

    def test_initialization(self):
        """Verify that fields are correctly defined after initialization"""
        channels = create_fake_channels_table()
        fake_timeseries = np.arange(0, 100, 0.05)  # in seconds
        fake_data = np.random.rand(len(fake_timeseries), len(channels))
        series = NIRSSeries(
            name="nirs_data",
            description="The raw NIRS channel data",
            timestamps=fake_timeseries,
            channels=DynamicTableRegion(
                name="channels",
                description="an ordered map to the channels in this NIRS series",
                table=channels,
                data=channels.id[:],
            ),
            data=fake_data,
            unit="V",
        )

        self.assertEqual(series.name, "nirs_data")
        np.testing.assert_array_equal(series.timestamps[:], fake_timeseries)
        np.testing.assert_array_equal(series.data[:], fake_data)
        self.assertIs(series.channels.table, channels)
        self.assertEqual(series.unit, "V")
