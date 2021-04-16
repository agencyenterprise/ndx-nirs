import os
from pynwb import load_namespaces, get_class


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

NIRSSourcesTable, NIRSDetectorsTable, NIRSChannelsTable, NIRSDevice, NIRSSeries = [
    get_class(x, "ndx-nirs")
    for x in (
        "NIRSSourcesTable",
        "NIRSDetectorsTable",
        "NIRSChannelsTable",
        "NIRSDevice",
        "NIRSSeries",
    )
]
