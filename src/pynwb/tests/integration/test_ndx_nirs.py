import datetime
import tempfile
from os import path

import numpy as np

from pynwb import NWBHDF5IO
from pynwb.file import NWBFile, Subject
from pynwb.testing import TestCase, remove_test_file
from hdmf.common import DynamicTableRegion

from ndx_nirs import (
    NIRSDevice,
    NIRSSeries,
    NIRSSourcesTable,
    NIRSDetectorsTable,
    NIRSChannelsTable,
)


def setup_nwbfile():
    nwbfile = NWBFile(
        session_description="A test NWB NIRS file",
        identifier="nirs_test",
        session_start_time=datetime.datetime(
            2021, 4, 1, 15, 0, 0, tzinfo=datetime.timezone.utc
        ),
        subject=Subject(subject_id="X"),
    )

    nirs_device = create_fake_nirs_device()
    nwbfile.add_device(nirs_device)
    nwbfile.add_acquisition(create_fake_nirs_series(nirs_device))
    return nwbfile


def create_fake_sources_table():
    table = NIRSSourcesTable()
    table.add_row({"label": "S1", "x": 0.0, "y": -1.0})
    table.add_row({"label": "S2", "x": 0.0, "y": 1.0})
    return table


def create_fake_detectors_table():
    table = NIRSDetectorsTable()
    table.add_row({"label": "D1", "x": 0.0, "y": -2.0})
    table.add_row({"label": "D2", "x": 0.0, "y": 0.0})
    table.add_row({"label": "D3", "x": 0.0, "y": 2.0})
    return table


def create_fake_channels_table():
    sources = create_fake_sources_table()
    detectors = create_fake_detectors_table()
    source_detector_pairs = [(0, 0), (0, 1), (1, 1), (1, 2)]
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


def create_fake_nirs_device():
    channels = create_fake_channels_table()

    return NIRSDevice(
        name="device",
        description="An fNIRS device",
        manufacturer="XYZ",
        nirs_mode="time-domain",
        channels=channels,
        sources=channels.source.table,
        detectors=channels.detector.table,
        time_delay=4.2,
        time_delay_width=0.5,
        additional_parameters="flux_capacitor_gain = 9000; speaker_volume = 11;",
    )


def create_fake_nirs_series(device):
    channels = device.channels
    fake_timeseries = np.arange(0, 100, 0.05)  # in seconds
    fake_data = np.random.rand(len(fake_timeseries), len(channels))

    return NIRSSeries(
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


class NIRSIntegrationTests(TestCase):
    """Integration tests for the ndx-nirs extension classes"""

    def setUp(self):
        self.nwb = setup_nwbfile()
        self.path = path.join(tempfile.gettempdir(), "test.nwb")

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        """Verify that an NWBFile with NIRS data saved to disk and read again is
        identical to the original NWBFile
        """

        with NWBHDF5IO(self.path, "w") as io:
            io.write(self.nwb)

        with NWBHDF5IO(self.path, "r") as io:
            read_nwb = io.read()
            self.assertContainerEqual(self.nwb, read_nwb)
            device = read_nwb.devices["device"]
            self.assertIs(device.channels.source.table, device.sources)
            self.assertIs(device.channels.detector.table, device.detectors)
