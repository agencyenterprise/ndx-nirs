import os.path

from pynwb.spec import (
    NWBNamespaceBuilder,
    export_spec,
    NWBGroupSpec,
    NWBDatasetSpec,
    NWBAttributeSpec,
)


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        doc="""An NWB extension for storing Near-Infrared Spectroscopy (NIRS) data""",
        name="""ndx-nirs""",
        version="""0.2.0""",
        author=list(
            map(
                str.strip,
                """Sumner L Norman,Darin Erat Sleiter,José Ribeiro""".split(","),
            )
        ),
        contact=list(
            map(
                str.strip,
                """sumner@ae.studio,darin@ae.studio,jose@ae.studio""".split(","),
            )
        ),
    )

    # specify the neurodata_types that are used by the extension as well
    # as in which namespace they are found
    # this is similar to specifying the Python modules that need to be imported
    # to use your new data types
    # as of HDMF 1.6.1, the full ancestry of the neurodata_types that are used by
    # the extension should be included, i.e., the neurodata_type and its parent
    # type and its parent type and so on. this will be addressed in a future
    # release of HDMF.
    ns_builder.include_type("TimeSeries", namespace="core")
    ns_builder.include_type("NWBDataInterface", namespace="core")
    ns_builder.include_type("NWBContainer", namespace="core")
    ns_builder.include_type("Container", namespace="hdmf-common")
    ns_builder.include_type("DynamicTable", namespace="hdmf-common")
    ns_builder.include_type("DynamicTableRegion", namespace="hdmf-common")
    ns_builder.include_type("VectorData", namespace="hdmf-common")
    ns_builder.include_type("Data", namespace="hdmf-common")
    ns_builder.include_type("ElementIdentifiers", namespace="hdmf-common")
    ns_builder.include_type("Device", namespace="core")

    # define your new data types
    # see https://pynwb.readthedocs.io/en/latest/extensions.html#extending-nwb
    # for more information
    nirs_sources = NWBGroupSpec(
        neurodata_type_def="NIRSSourcesTable",
        neurodata_type_inc="DynamicTable",
        default_name="sources",
        doc="A table describing the optical sources of a NIRS device.",
        datasets=[
            NWBDatasetSpec(
                name="label",
                doc="The label of the source",
                dtype="text",
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="x",
                doc="The x coordinate in meters of the optical source",
                dtype="float",
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="y",
                doc="The y coordinate in meters of the optical source",
                dtype="float",
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="z",
                doc="The z coordinate in meters of the optical source",
                dtype="float",
                shape=(None,),
                neurodata_type_inc="VectorData",
                quantity="?",
            ),
        ],
        attributes=[
            NWBAttributeSpec(
                name="description",
                dtype="text",
                doc="description",
                default_value="A table describing the optical sources of a NIRS device.",
            )
        ],
    )

    nirs_detectors = NWBGroupSpec(
        neurodata_type_def="NIRSDetectorsTable",
        neurodata_type_inc="DynamicTable",
        default_name="detectors",
        doc="A table describing the optical detectors of a NIRS device.",
        datasets=[
            NWBDatasetSpec(
                name="label",
                doc="The label of the detector",
                dtype="text",
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="x",
                doc="The x coordinate in meters of the optical detector",
                dtype="float",
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="y",
                doc="The y coordinate in meters of the optical detector",
                dtype="float",
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="z",
                doc="The z coordinate in meters of the optical detector",
                dtype="float",
                shape=(None,),
                neurodata_type_inc="VectorData",
                quantity="?",
            ),
        ],
        attributes=[
            NWBAttributeSpec(
                name="description",
                dtype="text",
                doc="description",
                default_value="A table describing the optical detectors of a NIRS device.",
            )
        ],
    )

    nirs_channels = NWBGroupSpec(
        neurodata_type_def="NIRSChannelsTable",
        neurodata_type_inc="DynamicTable",
        default_name="channels",
        doc="A table describing the optical channels of a NIRS device.",
        datasets=[
            NWBDatasetSpec(
                name="label",
                doc="The label of the channel",
                dtype="text",
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="source",
                doc="A reference to the optical source for this channel in NIRSSourcesTable",
                shape=(None,),
                neurodata_type_inc="DynamicTableRegion",
            ),
            NWBDatasetSpec(
                name="detector",
                doc="A reference to the optical detector for this channel in NIRSDetectorsTable.",
                shape=(None,),
                neurodata_type_inc="DynamicTableRegion",
            ),
            NWBDatasetSpec(
                name="source_wavelength",
                doc="The wavelength of light in nm emitted by the source for this channel.",
                dtype="float",
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="emission_wavelength",
                doc=(
                    "The wavelength of light in nm emitted by the fluorophore under "
                    "fluorescent spectroscopy for this channel. Only used for fluorescent"
                    " spectroscopy"
                ),
                dtype="float",
                shape=(None,),
                neurodata_type_inc="VectorData",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="source_power",
                doc="The power of the source in mW used for this channel.",
                dtype="float",
                shape=(None,),
                neurodata_type_inc="VectorData",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="detector_gain",
                doc="The gain applied to the detector for this channel.",
                dtype="float",
                shape=(None,),
                neurodata_type_inc="VectorData",
                quantity="?",
            ),
        ],
        attributes=[
            NWBAttributeSpec(
                name="description",
                dtype="text",
                doc="description",
                default_value="A table describing the optical channels of a NIRS device.",
            )
        ],
    )

    nirs_device = NWBGroupSpec(
        neurodata_type_def="NIRSDevice",
        neurodata_type_inc="Device",
        doc="Metadata about a NIRS device.",
        attributes=[
            NWBAttributeSpec(
                name="nirs_mode",
                doc=(
                    "The mode of NIRS measurement performed with this device."
                    " Examples include (but are not limited to) continuous-wave,"
                    " frequency-domain, time-domain, time-domain-moments,"
                    " diffuse-correlation-spectroscopy, continuous-wave-fluorescence,"
                    " and diffuse-optical-tomography, as well as variants including"
                    " fluorescence."
                ),
                dtype="text",
            ),
            NWBAttributeSpec(
                name="frequency",
                doc=(
                    "The modulation frequency in Hz used for frequency domain NIRS."
                    " Only used if nirs_mode is a type of frequency domain spectroscopy."
                ),
                dtype="float",
                required=False,
            ),
            NWBAttributeSpec(
                name="time_delay",
                doc=(
                    "The time delay in ns used for gated time domain NIRS. Only used"
                    " if nirs_mode is a type of gated time domain spectroscopy."
                ),
                dtype="float",
                required=False,
            ),
            NWBAttributeSpec(
                name="time_delay_width",
                doc=(
                    "The time delay width in ns used for gated time domain NIRS. Only"
                    " used if nirs_mode is a type of gated time domain spectroscopy."
                ),
                dtype="float",
                required=False,
            ),
            NWBAttributeSpec(
                name="correlation_time_delay",
                doc=(
                    "The correlation time delay in ns for diffuse correlation"
                    " spectroscopy NIRS. Only used if nirs_mode is a type of diffuse"
                    " correlation spectroscopy."
                ),
                dtype="float",
                required=False,
            ),
            NWBAttributeSpec(
                name="correlation_time_delay_width",
                doc=(
                    "The correlation time delay width in ns for diffuse correlation"
                    " spectroscopy NIRS. Only used if nirs_mode is a type of diffuse"
                    " correlation spectroscopy."
                ),
                dtype="float",
                required=False,
            ),
            NWBAttributeSpec(
                name="additional_parameters",
                doc=(
                    "Any additional parameters corresponding to the NIRS device and"
                    " NIRS mode of operation that are useful for interpreting the"
                    " data."
                ),
                dtype="text",
                required=False,
            ),
        ],
        groups=[
            NWBGroupSpec(
                name="channels",
                doc="A table of the optical channels available on this device",
                neurodata_type_inc="NIRSChannelsTable",
            ),
            NWBGroupSpec(
                name="sources",
                doc="The optical sources of this device",
                neurodata_type_inc="NIRSSourcesTable",
            ),
            NWBGroupSpec(
                name="detectors",
                doc="The optical detectors of this device",
                neurodata_type_inc="NIRSDetectorsTable",
            ),
        ],
    )

    nirs_series = NWBGroupSpec(
        neurodata_type_def="NIRSSeries",
        neurodata_type_inc="TimeSeries",
        doc="A timeseries of recorded NIRS data.",
        datasets=[
            NWBDatasetSpec(
                name="channels",
                doc="DynamicTableRegion reference to the optical channels represented by this NIRSSeries",
                neurodata_type_inc="DynamicTableRegion",
            )
        ],
    )

    # all new data types defined in this module
    new_data_types = [
        nirs_sources,
        nirs_detectors,
        nirs_channels,
        nirs_device,
        nirs_series,
    ]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "spec")
    )
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
