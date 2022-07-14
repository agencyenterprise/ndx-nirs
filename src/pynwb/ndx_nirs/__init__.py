import os
from pynwb import load_namespaces, get_class, register_class

from hdmf.common import DynamicTable
from hdmf.utils import docval, getargs, popargs, AllowPositional

from ndx_nirs.utils import update_docval


# Set path of the namespace.yaml file to the expected install location
ndx_nirs_specpath = os.path.join(
    os.path.dirname(__file__), "spec", "ndx-nirs.namespace.yaml"
)

# If the extension has not been installed yet but we are running directly from
# the git repo
if not os.path.exists(ndx_nirs_specpath):
    ndx_nirs_specpath = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "spec",
            "ndx-nirs.namespace.yaml",
        )
    )

# Load the namespace
load_namespaces(ndx_nirs_specpath)


_sources_docval = update_docval(
    DynamicTable.__init__,
    updates=dict(
        name={"default": "sources"},
        description={
            "default": "A table describing the optical sources of a NIRS device."
        },
    ),
)


@register_class("NIRSSourcesTable", "ndx-nirs")
class NIRSSourcesTable(DynamicTable):
    """A table describing the optical sources of a NIRS device."""

    __columns__ = (
        dict(name="label", description="The label of the optical source."),
        dict(name="x", description="The x coordinate of the optical source."),
        dict(name="y", description="The y coordinate of the optical source."),
        dict(
            name="z",
            description="The z coordinate of the optical source.",
            required=False,
        ),
    )

    @docval(*_sources_docval, allow_positional=AllowPositional.ERROR)
    def __init__(self, **kwargs):
        """Initializes a NIRSSourcesTable instance.

        Users should only use the following parameters:
            (name, description)
        The following should only be the build backend for constructing containers
        when loading an nwb file from disk:
            (id, columns, colnames)
        """
        super().__init__(**kwargs)


_detectors_docval = update_docval(
    DynamicTable.__init__,
    updates=dict(
        name={"default": "detectors"},
        description={
            "default": "A table describing the optical detectors of a NIRS device."
        },
    ),
)


@register_class("NIRSDetectorsTable", "ndx-nirs")
class NIRSDetectorsTable(DynamicTable):
    """A table describing the optical detectors of a NIRS device."""

    __columns__ = (
        dict(name="label", description="The label of the optical detector."),
        dict(name="x", description="The x coordinate of the optical detector."),
        dict(name="y", description="The y coordinate of the optical detector."),
        dict(
            name="z",
            description="The z coordinate of the optical detector.",
            required=False,
        ),
    )

    @docval(*_detectors_docval, allow_positional=AllowPositional.ERROR)
    def __init__(self, **kwargs):
        """Initializes a NIRSDetectorsTable instance.

        Users should only use the following parameters:
            (name, description)
        The following should only be the build backend for constructing containers
        when loading an nwb file from disk:
            (id, columns, colnames)
        """
        super().__init__(**kwargs)


_channels_docval = [
    {
        "name": "sources",
        "type": NIRSSourcesTable,
        "doc": "The table that is referenced by the source column.",
        "default": None,
    },
    {
        "name": "detectors",
        "type": NIRSDetectorsTable,
        "doc": "The table that is referenced by the detector column.",
        "default": None,
    },
    *update_docval(
        DynamicTable.__init__,
        updates=dict(
            name={"default": "channels"},
            description={
                "default": "A table describing the optical channels of a NIRS device."
            },
        ),
    ),
]


@register_class("NIRSChannelsTable", "ndx-nirs")
class NIRSChannelsTable(DynamicTable):
    """A table describing the optical channels of a NIRS device.

    Before adding channels to the table, the sources and detectors for the
    device need to be defined in a NIRSSourcesTable and a NIRSDetectorsTable,
    respectively. These can be passed in either during class initializing or
    afterwards.

    Examples:
    ```python
    sources = NIRSSourcesTable()
    detectors = NIRSDetectorsTable()

    # during initialization:
    channels = NIRSChannelsTable(sources=sources, detectors=detectors)

    # after initialization:
    channels = NIRSChannelsTable()
    channels.set_sources_table(sources)
    channels.set_detectors_table(detectors)
    ```
    """

    __columns__ = (
        dict(name="label", description="The label of the channel", required=True),
        dict(
            name="source",
            description="A reference to the optical source for this channel in NIRSSourcesTable.",
            required=True,
            table=True,
        ),
        dict(
            name="detector",
            description="A reference to the optical detector for this channel in NIRSDetectorsTable.",
            required=True,
            table=True,
        ),
        dict(
            name="source_wavelength",
            description="The wavelength of light in nm emitted by the source for this channel.",
            required=True,
        ),
        dict(
            name="emission_wavelength",
            description=(
                "The wavelength of light in nm emitted by the fluorophore under "
                "fluorescent spectroscopy for this channel. Only used for fluorescent"
                " spectroscopy."
            ),
            required=False,
        ),
        dict(
            name="source_power",
            description="The power of the source in mW used for this channel.",
            required=False,
        ),
        dict(
            name="detector_gain",
            description="The gain applied to the detector for this channel.",
            required=False,
        ),
    )

    @docval(*_channels_docval, allow_positional=AllowPositional.ERROR)
    def __init__(self, **kwargs):
        """Initializes a NIRSChannelsTable instance.

        Users should only use the following parameters:
            (name, description, sources, detectors)
        The following should only be the build backend for constructing containers
        when loading an nwb file from disk:
            (id, columns, colnames)
        """
        sources = popargs("sources", kwargs)
        detectors = popargs("detectors", kwargs)
        super().__init__(**kwargs)
        if sources is not None:
            self.set_sources_table(sources)
        if detectors is not None:
            self.set_detectors_table(detectors)

    @docval(
        {
            "name": "sources",
            "type": NIRSSourcesTable,
            "doc": "The table that is referenced by the source column.",
        }
    )
    def set_sources_table(self, **kwargs):
        """Assigns the NIRSourcesTable which should be referenced by the source column."""
        sources = getargs("sources", kwargs)
        self.source.table = sources

    @docval(
        {
            "name": "detectors",
            "type": NIRSDetectorsTable,
            "doc": "The table that is referenced by the detector column.",
        }
    )
    def set_detectors_table(self, **kwargs):
        """Assigns the NIRDetectorsTable which should be referenced by the detector column."""
        detectors = getargs("detectors", kwargs)
        self.detector.table = detectors


NIRSDevice = get_class("NIRSDevice", "ndx-nirs")
NIRSDevice.__doc__ = "Metadata about a NIRS device."

NIRSSeries = get_class("NIRSSeries", "ndx-nirs")
NIRSSeries.__doc__ = "A timeseries of recorded NIRS data."
