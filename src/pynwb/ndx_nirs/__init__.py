import os
from copy import deepcopy
from pynwb import load_namespaces, get_class, register_class


from hdmf.common import DynamicTable
from hdmf.utils import docval, call_docval_func, get_docval, getargs, popargs


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

# TODO: import your classes here or define your class using get_class to make
# them accessible at the package level


def update_docval(overridden_fn, **kwargs):
    """Copy the docval from an existing function and update specified parameters"""
    original_docval = get_docval(overridden_fn)
    new_docval = deepcopy(original_docval)
    for name, update_vals in kwargs.items():
        for item in new_docval:
            if item["name"] == name:
                item.update(update_vals)
                break
        else:
            msg = "docval item named {} does not exist for function {}".format(
                name, overridden_fn.__name__
            )
            raise ValueError(msg)
    return new_docval


sources_docval = update_docval(
    DynamicTable.__init__,
    name={"default": "sources"},
    description={"default": "A table describing optical sources of a NIRS device"},
)


@register_class("NIRSSourcesTable", "ndx-nirs")
class NIRSSourcesTable(DynamicTable):
    """A DynamicTable representing the optical sources of this NIRS device"""

    __columns__ = (
        dict(name="label", description="The label of the optical source"),
        dict(name="x", description="The x coordinate of the optical source"),
        dict(name="y", description="The y coordinate of the optical source"),
        dict(
            name="z",
            description="The z coordinate of the optical source",
            required=False,
        ),
    )

    @docval(*sources_docval)
    def __init__(self, **kwargs):
        call_docval_func(super().__init__, kwargs)


detectors_docval = update_docval(
    DynamicTable.__init__,
    name={"default": "detectors"},
    description={"default": "A table describing optical detectors of a NIRS device"},
)


@register_class("NIRSDetectorsTable", "ndx-nirs")
class NIRSDetectorsTable(DynamicTable):
    """A DynamicTable representing the optical detectors of this NIRS device"""

    __columns__ = (
        dict(name="label", description="The label of the optical detector"),
        dict(name="x", description="The x coordinate of the optical detector"),
        dict(name="y", description="The y coordinate of the optical detector"),
        dict(
            name="z",
            description="The z coordinate of the optical detector",
            required=False,
        ),
    )

    @docval(*detectors_docval)
    def __init__(self, **kwargs):
        call_docval_func(super().__init__, kwargs)


channels_docval = [
    {
        "name": "sources",
        "type": NIRSSourcesTable,
        "doc": "The table that is referenced by the source column",
        "default": None,
    },
    {
        "name": "detectors",
        "type": NIRSDetectorsTable,
        "doc": "The table that is referenced by the detector column",
        "default": None,
    },
    *update_docval(
        DynamicTable.__init__,
        name={"default": "channels"},
        description={"default": "A table describing optical channels of a NIRS device"},
    ),
]


@register_class("NIRSChannelsTable", "ndx-nirs")
class NIRSChannelsTable(DynamicTable):
    """A DynamicTable representing the optical channels of this NIRS device"""

    __columns__ = (
        dict(name="label", description="The label of the channel", required=True),
        dict(
            name="source",
            description="A reference to the optical source for this channel in NIRSSourcesTable",
            required=True,
            table=True,
        ),
        dict(
            name="detector",
            description="A reference to the optical detector for this channel in NIRSDetectorsTable",
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
                " spectroscopy"
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

    @docval(*channels_docval)
    def __init__(self, **kwargs):
        sources = popargs("sources", kwargs)
        detectors = popargs("detectors", kwargs)
        call_docval_func(super().__init__, kwargs)
        self.source.table = sources
        self.detector.table = detectors

    @docval(
        {
            "name": "sources",
            "type": NIRSSourcesTable,
            "doc": "The table that is referenced by the source column",
        }
    )
    def set_sources_table(self, **kwargs):
        """Assigns the NIRSourcesTable which should be referenced by the source column"""
        sources = getargs("sources", kwargs)
        self.source.table = sources

    @docval(
        {
            "name": "detectors",
            "type": NIRSDetectorsTable,
            "doc": "The table that is referenced by the detector column",
        }
    )
    def set_detectors_table(self, **kwargs):
        """Assigns the NIRDetectorsTable which should be referenced by the detector column"""
        detectors = getargs("detectors", kwargs)
        self.detector.table = detectors


NIRSDevice = get_class("NIRSDevice", "ndx-nirs")
NIRSSeries = get_class("NIRSSeries", "ndx-nirs")
