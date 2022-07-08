# ndx-nirs Extension for NWB

This is an [NWB](https://www.nwb.org/) extension for storing and sharing near-infrared spectroscopy (NIRS) data.

If you're new to NWB: "Neurodata Without Borders (NWB) is a data standard for neurophysiology, providing neuroscientists with a common standard to share, archive, use, and build common analysis tools for neurophysiology data." ([source](https://www.nwb.org/nwb-neurophysiology/))

This extension defines the data specification for NIRS data in addition to providing a python API for reading and writing .nwb files containing data that follows this specification. The python package can be used with [pyNWB](https://github.com/NeurodataWithoutBorders/pynwb).

This extension has been officially accepted into the [Neurodata Extensions Catalog](https://nwb-extensions.github.io/) and can be found there along with other accepted extensions.

## Introduction to NIRS

NIRS uses near-infrared sources (from 780 nm to 2500 nm) to assess brain function by detecting changes in blood hemoglobin (Hb) concentrations. 

As neural activity changes, blood volume and the concentration of hemoglobin in the local area changes through the neurovascular coupling phenomenon. NIRS techniques requires optical sources with two or more wavelengths in the near-infrared spectrum. One must have a wavelength above and one below the isosbestic point of 810 nm - the point at which deoxygenated hemoglobin (deoxy-Hb) and oxygenated hemoglobin (oxy-Hb) have identical absorption coefficients. Using the modified Beer-Lambert law (mBLL), NIRS techniques reveal  changes in hemoglobin concentration. NIRS monitors hemoglobin levels through these optical absorption coefficients as a proxy for localized brain activity.

## Purpose of the extension

The user-base of NIRS techniques continues to grow. In addition, NIRS techniques are often used in conjunction with other brain recording techniques (e.g. EEG) and/or use common stimuli or behavioral paradigms. The NWB NIRS extension provides a data standard for neuroscientist to share, archive, use, and build analysis tools for NIRS data. 

Integration of NIRS into the NWB data standard affords all NIRS users interoperability with many of the data storage, processing, analysis, and visualization tools already integrated within NWB. 

## Modes of NIRS currently supported

This extension currently explicitly supports: 

1. Continuous Wave
    - see `NIRSDevice.nirs_mode` 
2. Frequency-Domain
    - see `NIRSDevice.nirs_mode` and `NIRSDevice.frequency`
3. Time-Domain 
    - see `NIRSDevice.nirs_mode`, `NIRSDevice.time_delay`, and `NIRSDevice.time_delay_width`
4. Diffuse Correlation Spectroscopy
    - see `NIRSDevice.nirs_mode`, `NIRSDevice.correlation_time_delay`, and `NIRSDevice.correlation_time_delay_width`

In addition, it includes support for fluorescent versions of each of these techniques.
  - see `NIRSChannelsTable.emssion_wavelength`

Other NIRS modalities are supported implicitly. We acknowledge that NIRS is a fast-growing recording method with new modalities constantly under development. For this reason, it is possible to define other useful parameters using the `NIRSDevice.additional_parameters` field. Future version of NWB NIRS will add native support for new NIRS modalities.

## Related data standards 

The NWB NIRS neurodata type was inspired by the [SNIRF](https://fnirs.org/resources/software/snirf/) data specification ([Github](https://github.com/fNIRS/snirf)). Many of the data fields can be directly mapped from SNIRF to NWB and vice-versa. We expect to release a SNIRF<->NWB conversion tool in the near future to improve compatibility between data standards and ease the burden of conversion on NIRS researchers.

## NWB NIRS data architecture

The two principal neurodata types of this extension are ``NIRSDevice``, which extends the `Device` data type and holds information about the NIRS hardware and software configuration, and ``NIRSSeries``, which contains the timeseries data collected by the NIRS device.

``NIRSSourcesTable``, ``NIRSDetectorsTable``, and ``NIRSChannelsTable`` are children of ``NIRSDevice`` which describe the source and detector layout as well as the wavelength-specific optical channels that are measured.

Each row of ``NIRSChannelsTable`` represents a specific source and detector pair along with the source illumination wavelength (and optionally, in the case of fluorescent spectroscopy, the emission/detection wavelength). The channels in this table correspond have a 1-to-1 correspondence with the data columns in ``NIRSSeries``.

![ndx-nirs UML](https://github.com/agencyenterprise/ndx-nirs/raw/main/docs/source/images/ndx-nirs-uml.png)

### Defined neurodata types

1. ``NIRSSourcesTable`` stores rows for each optical source of a NIRS device. ``NIRSSourcesTable`` columns includes:
    - ``label`` - the label of the source.
    - ``x``, ``y``, and ``z`` - the coordinates in meters of the optical source (``z`` is optional).

2. ``NIRSDetectorsTable`` stores rows for each of the optical detectors of a NIRS device. ``NIRSDetectorsTable`` columns includes:
    - ``label`` - the label of the detector.
    - ``x``, ``y``, and ``z`` - the coordinates in meters of the optical detector (``z`` is optional).

3. ``NIRSChannelsTable`` stores rows for each physiological channel, which is defined by source-detector pairs, where sources & detectors are referenced via ``NIRSSourcesTable`` and ``NIRSDetectorsTable``. ``NIRSChannelsTable`` columns includes:
    - ``label`` - the label of the channel.
    - ``source`` - a reference to the optical source in ``NIRSSourcesTable``.
    - ``detector`` - a reference to the optical detector in ``NIRSDetectorsTable``.
    - ``source_wavelength`` - the wavelength of light in nm emitted by the source for this channel.
    - ``emission_wavelength`` - the wavelength of light in nm emitted by the fluorophone (optional; only used for fluorescent spectroscopy).
    - ``source_power`` - the power of the source in mW used for this channel (optional).
    - ``detector_gain`` - the gain applied to the detector for this channel (optional).
    
4. ``NIRSDevice`` defines the NIRS device itself and includes the following required fields:
    - ``name`` - a unique name for the device.
    - ``description`` - a free-form text description of the device.
    - ``manufacturer`` - the name of the manufacturer of the device.
    - ``channels`` - a table of the optical channels available on this device (references ``NIRSChannelsTable``).
    - ``sources`` - the optical sources of this device (references ``NIRSSourcesTable``).
    - ``detectors`` - the optical detectors of this device (references ``NIRSDetectorsTable``).
    - ``nirs_mode`` - the mode of NIRS measurement performed with this device (e.g., 'continuous-wave', 'frequency-domain', etc.).
        
   ``NIRSDevice`` also includes several optional attributes to be used in parallel with specific ``nirs_mode`` values:
    - ``frequency`` - the modulation frequency in Hz for frequency domain NIRS (optional).
    - ``time_delay`` - the time delay in ns used for gated time domain NIRS (TD-NIRS) (optional).
    - ``time_delay_width`` - the time delay width in ns used for gated time domain NIRS (optional).
    - ``correlation_time_delay`` - the correlation time delay in ns for diffuse correlation spectroscopy NIRS (optional).
    - ``correlation_time_delay_width`` - the correlation time delay width in ns for diffuse correlation spectroscopy NIRS (optional).
    - ``additional_parameters`` - any additional parameters corresponding to the NIRS device/mode that are useful for interpreting the data (optional).

5. ``NIRSSeries`` stores the actual timeseries data collected by the NIRS device and includes:
    - ``name`` - a unique name for the NIRS timeseries.
    - ``description`` - a description of the NIRS timeseries.
    - ``timestamps`` - the timestamps for each row of ``data`` in seconds.
    - ``channels`` - a ``DynamicTableRegion`` mapping to the appropriate channels in a ``NIRSChannelsTable``.
    - ``data`` - the actual numeric raw data measured by the NIRS system. It is a 2D array where the columns correspond to ``channels`` and the rows correspond to ``timestamps``.

## Installation

To install from PyPI use pip:

```
$ pip install ndx-nirs
```

To install after cloning the extension repo from github, execute the following from the root of the repo:

```
$ pip install .
```

For development purposes, it might be useful to install in editable mode:

```
$ pip install -e .
```

## Usage

```python
from datetime import datetime

import numpy as np

from hdmf.common import DynamicTableRegion
from pynwb import NWBHDF5IO
from pynwb.file import NWBFile, Subject

from ndx_nirs import NIRSSourcesTable, NIRSDetectorsTable, NIRSChannelsTable, NIRSDevice, NIRSSeries


##### create some example data to add to the NWB file #####

# create NIRS source & detector labels
source_labels = ["S1", "S2"]
detector_labels = ["D1", "D2"]

# create NIRS source & detector positions as a numpy array
# with dims: [num sources/detectors rows x 2 columns (for x, y)]
source_pos = np.array([[-2.0, 0.0], [-4.0, 5.6]])
detector_pos = np.array([[0.0, 0.0], [-4.0, 1.0]])

# create a list of source detector pairs (pairs of indices)
source_detector_pairs = [(0, 0), (0, 1), (1, 0), (1, 1)]


##### create NWB file using the example data above #####

# create a basic NWB file
nwb = NWBFile(
    session_description="A NIRS test session",
    identifier="nirs_test_001",
    session_start_time=datetime.now().astimezone(),
    subject=Subject(subject_id="nirs_subj_01"),
)


# create and populate a NIRSSourcesTable containing the
# label and location of optical sources for the device
sources = NIRSSourcesTable()
# add source labels & positions row-by-row
for i_source in range(0, len(source_labels)):
    sources.add_row(
        label=source_labels[i_source],
        x=source_pos[i_source, 0],
        y=source_pos[i_source, 1],
    )


# create and populate a NIRSDetectorsTable containing the
# label and location of optical sources for the device
detectors = NIRSDetectorsTable()
# add a row for each detector
for i_detector in range(0, len(detector_labels)):
    detectors.add_row(
        label=detector_labels[i_detector],
        x=detector_pos[i_detector, 0],
        y=detector_pos[i_detector, 1],
    )  # z-coordinate is optional


# create a NIRSChannelsTable which defines the channels
# between the provided sources and detectors
channels = NIRSChannelsTable(sources=sources, detectors=detectors)
# each channel is composed of a single source, a single detector, and the wavelength
# most source-detector pairs will use two separate wavelengths, and have two channels
for i_source, i_detector in source_detector_pairs:
    for wavelength in [690.0, 830.0]:
        # for the source and detector parameters, pass in the index of
        # the desired source (detector) in the sources (detectors) table
        channels.add_row(
            label=f"{source_labels[i_source]}.{detector_labels[i_detector]}.{wavelength:0.0f}nm",
            source=i_source,
            detector=i_detector,
            source_wavelength=wavelength,
        )


# create a NIRSDevice which contains all of the information
# about the device configuration and arrangement
device = NIRSDevice(
    name="nirs_device",
    description="world's best fNIRS device",
    manufacturer="skynet",
    nirs_mode="time-domain",
    channels=channels,
    sources=sources,
    detectors=detectors,
    # depending on which nirs_mode is selected, additional parameter values should be
    # included. these two parameters are included because we are using time-domain NIRS
    time_delay=1.5,  # in ns
    time_delay_width=0.1,  # in ns
    # specialized NIRS hardware may require additional parameters that can be defined
    # using the `additional_parameters` field:
    additional_parameters="flux_capacitor_gain = 9000; speaker_volume = 11;",
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
with NWBHDF5IO(filename, "w") as io:
    io.write(nwb)

# Read the data back in
with NWBHDF5IO(filename, "r", load_namespaces=True) as io:
    nwb = io.read()
    print(nwb)
    print(nwb.devices["nirs_device"])
    print(nwb.acquisition["nirs_data"])
```

This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).
