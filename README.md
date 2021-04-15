# ndx-nirs Extension for NWB

**WIP**

_ideas to include_:
* purpose of the extension
  * bring NIRS into nwb
  * interoperability with tools, etc
* modes of nirs that it is compatible with
* based off of SNIRF
  * expect to release conversion tool
* main architecture


## Installation

To install after cloning the extension repo from github, execute the following from the root of the repo:

```
$ pip install .
```

For development purposes, it might be useful to install in editable mode:

```
$ pip install -e .
```

Note: a version of the ndx-nirs package will be released on PyPI before the extension is submitted to the NDX Catalog.


## Usage

```python
from datetime import datetime

import numpy as np

from pynwb import NWBHDF5IO
from pynwb.file import NWBFile, Subject
from hdmf.common import DynamicTableRegion

from ndx_nirs import NIRSSourcesTable, NIRSDetectorsTable, NIRSChannelsTable, NIRSDevice, NIRSSeries


# create a basic NWB file
nwb = NWBFile(
    session_description="A NIRS test session",
    identifier="nirs_test_001",
    session_start_time=datetime.now().astimezone(),
    subject=Subject(subject_id="nirs_subj_01")
)


# create and populate a NIRSSourcesTable containing the
# label and location of optical sources for the device
sources = NIRSSourcesTable()
# add a row for each source
sources.add_row(label="S1", x=-1.0, y=0.0, z=0.0)
sources.add_row(label="S2", x=1.0, y=0.0, z=0.0)


# create and populate a NIRSDetectorsTable containing the
# label and location of optical sources for the device
detectors = NIRSDetectorsTable()
# add a row for each detector
detectors.add_row(label="D1", x=0.0, y=-1.0) # the z-coordinate is optional
detectors.add_row(label="D2", x=0.0, y=1.0)


# create a NIRSChannelsTable which defines the channels
# between the provided sources and detectors
channels = NIRSChannelsTable(sources, detectors)
# each channel is composed of a single source, a single detector, and the wavelength
# most source-detector pairs will use two separate wavelengths, and have two channels
for wavelength in [690.0, 830.0]:
    # for the source and detector parameters, pass in the index of
    # the desired source (detector) in the sources (detectors) table
    channels.add_row(label=f"S1.D1.{wavelength:.0f}nm", source=0,
                     detector=0, source_wavelength=wavelength)
    channels.add_row(label=f"S1.D2.{wavelength:.0f}nm", source=0,
                     detector=1, source_wavelength=wavelength)
    channels.add_row(label=f"S2.D1.{wavelength:.0f}nm", source=1,
                     detector=0, source_wavelength=wavelength)
    channels.add_row(label=f"S2.D2.{wavelength:.0f}nm", source=1,
                     detector=1, source_wavelength=wavelength)


# create a NIRSDevice which contains all of the information
# about the device configuration and arrangement
device = NIRSDevice(
    name="nirs_device",
    description="An fNIRS device",
    manufacturer="XYZ",
    nirs_mode="time-domain",
    channels=channels,
    sources=sources,
    detectors=detectors,
    # depending on which nirs_mode is selected, additional parameter values should be
    # included. these two parameters are included because we are using time-domain NIRS
    time_delay=1.5, # in ns
    time_delay_width=0.1, # in ns
)
# add the device to the NWB file
nwb.add_device(device)


# create a NIRSSeries timeseries containing raw NIRS data
nirs_series = NIRSSeries(
    name="nirs_data",
    description="The raw NIRS channel data",
    timestamps=np.arange(0, 10, 0.01),  # in seconds
    # reference only the channels associated with this series
    channels=DynamicTableRegion(  
        name="channels",
        description="an ordered map to the channels in this NIRS series",
        table=channels,
        data=channels.id[:],
    ),
    data=np.random.rand(1000, 8),  # shape: (num timesteps, num channels)
    unit="V",
)
# add the series to the NWB file
nwb.add_acquisition(nirs_series)


# Write our test file
filename = "test_nirs_file.nwb"
with NWBHDF5IO(filename, 'w') as io:
    io.write(nwb)

# Read the data back in
with NWBHDF5IO(filename, 'r', load_namespaces=True) as io:
    nwb = io.read()
    print(nwb)
    print(nwb.devices["nirs_device"])
    print(nwb.acquisition["nirs_data"])
```

This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).
