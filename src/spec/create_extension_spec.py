import os.path

from pynwb.spec import (
    NWBNamespaceBuilder,
    export_spec,
    NWBGroupSpec,
    NWBDatasetSpec,
    NWBAttributeSpec,
)

# TODO: import the following spec classes as needed
# from pynwb.spec import NWBDatasetSpec, NWBLinkSpec, NWBDtypeSpec, NWBRefSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        doc="""An NWB extension for storing Near-Infrared Spectroscopy (NIRS) data""",
        name="""ndx-nirs""",
        version="""0.1.0""",
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

    # TODO: specify the neurodata_types that are used by the extension as well
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

    # TODO: define your new data types
    # see https://pynwb.readthedocs.io/en/latest/extensions.html#extending-nwb
    # for more information

    nirs_sources = NWBGroupSpec(
        neurodata_type_def="NIRSSourcesTable",
        neurodata_type_inc="DynamicTable",
        name="sources",
        doc="A table describing optical sources of a NIRS device",
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
                doc="The x coordinate of the optical source",
                dtype="float",
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="y",
                doc="The y coordinate of the optical source",
                dtype="float",
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="z",
                doc="The z coordinate of the optical source",
                dtype="float",
                shape=(None,),
                neurodata_type_inc="VectorData",
                quantity="?",
            ),
        ],
    )

    nirs_detectors = NWBGroupSpec(
        neurodata_type_def="NIRSDetectorsTable",
        neurodata_type_inc="DynamicTable",
        name="detectors",
        doc="A table describing optical detectors of a NIRS device",
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
                doc="The x coordinate of the optical detector",
                dtype="float",
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="y",
                doc="The y coordinate of the optical detector",
                dtype="float",
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="z",
                doc="The z coordinate of the optical detector",
                dtype="float",
                shape=(None,),
                neurodata_type_inc="VectorData",
                quantity="?",
            ),
        ],
    )

    nirs_channels = NWBGroupSpec(
        neurodata_type_def="NIRSChannelsTable",
        neurodata_type_inc="DynamicTable",
        name="channels",
        doc="A table describing optical channels of a NIRS device",
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
                doc="A reference to the optical detector for this channel in NIRSDetectorsTable",
                shape=(None,),
                neurodata_type_inc="DynamicTableRegion",
            ),
            NWBDatasetSpec(
                name="wavelength",
                doc="The wavelength of light for this channel in nm",
                dtype="float",
                shape=(None,),
                neurodata_type_inc="VectorData",
                attributes=[
                    NWBAttributeSpec(
                        name="unit",
                        doc="The unit of measurement for the wavelength",
                        dtype="text",
                        value="nm",
                    )
                ],
            ),
        ],
    )

    nirs_device = NWBGroupSpec(
        neurodata_type_def="NIRSDevice",
        neurodata_type_inc="Device",
        doc="A NIRS Device",
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
        doc="A timeseries of NIRS data",
        datasets=[
            NWBDatasetSpec(
                name="channels",
                doc="DynamicTableRegion reference to the optical channels represented by this NIRSSeries",
                neurodata_type_inc="DynamicTableRegion",
            )
        ],
    )

    # TODO: add all of your new data types to this list
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
