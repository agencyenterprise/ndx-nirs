import os.path

from pynwb.spec import (NWBNamespaceBuilder, export_spec, NWBGroupSpec,
                        NWBDatasetSpec, NWBAttributeSpec, NWBLinkSpec, NWBRefSpec)
# TODO: import the following spec classes as needed
# from pynwb.spec import NWBDatasetSpec, NWBLinkSpec, NWBDtypeSpec, NWBRefSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        doc="""An NWB extension for storing Near-Infrared Spectroscopy (NIRS) data""",
        name="""ndx-nirs""",
        version="""0.1.0""",
        author=list(map(str.strip, """Sumner Norman,Darin Erat Sleiter,José Ribeiro""".split(','))),
        contact=list(map(str.strip, """sumner@ae.studio,darin@ae.studio,jose@ae.studio""".split(',')))
    )

    # TODO: specify the neurodata_types that are used by the extension as well
    # as in which namespace they are found
    # this is similar to specifying the Python modules that need to be imported
    # to use your new data types
    # as of HDMF 1.6.1, the full ancestry of the neurodata_types that are used by
    # the extension should be included, i.e., the neurodata_type and its parent
    # type and its parent type and so on. this will be addressed in a future
    # release of HDMF.
    ns_builder.include_type('TimeSeries', namespace='core')
    ns_builder.include_type('NWBDataInterface', namespace='core')
    ns_builder.include_type('NWBContainer', namespace='core')
    ns_builder.include_type('Container', namespace='hdmf-common')
    ns_builder.include_type('DynamicTable', namespace='hdmf-common')
    ns_builder.include_type('DynamicTableRegion', namespace='hdmf-common')
    ns_builder.include_type('VectorData', namespace='hdmf-common')
    ns_builder.include_type('Data', namespace='hdmf-common')
    ns_builder.include_type('Device', namespace='core')
    
    # TODO: define your new data types
    # see https://pynwb.readthedocs.io/en/latest/extensions.html#extending-nwb
    # for more information
    
   
    OpticalSource = NWBGroupSpec(
        neurodata_type_def='OpticalSource',
        neurodata_type_inc='NWBDataInterface',
        doc='A NIRS Optical Source',
        datasets=[
            NWBDatasetSpec(
                name='x',
                doc='The x coordinate of the optical source',
                dtype='float',
            ),
            NWBDatasetSpec(
                name='y',
                doc='The y coordinate of the optical source',
                dtype='float',
            ),
            NWBDatasetSpec(
                name='z',
                doc='The z coordinate of the optical source',
                dtype='float',
                quantity='?'
            )
        ]
    )

    OpticalDetector = NWBGroupSpec(
        neurodata_type_def='OpticalDetector',
        neurodata_type_inc='NWBDataInterface',
        doc='A NIRS Optical Detector',
        datasets=[
            NWBDatasetSpec(
                name='x',
                doc='The x coordinate of the optical detector',
                dtype='float',
            ),
            NWBDatasetSpec(
                name='y',
                doc='The y coordinate of the optical detector',
                dtype='float',
            ),
            NWBDatasetSpec(
                name='z',
                doc='The z coordinate of the optical detector',
                dtype='float',
                quantity='?'
            )
        ]
    )


# instead of an Optode, let's just do a DynamicTable of channels. That will be easier.

#     Optode = NWBGroupSpec(
#         neurodata_type_def='Optode',
#         neurodata_type_inc='NWBDataInterface',
#         doc='A NIRS Optode comprised of a Source and Detector pair',
#         links=[
#             NWBLinkSpec(
#                 name='source',
#                 doc='A link to the optical source',
#                 target_type='OpticalSource',
#             ),
#             NWBLinkSpec(
#                 name='detector',
#                 doc='A link to the optical detector',
#                 target_type='OpticalDetector',
#             ),            
#         ],
#         datasets=[
#             NWBDatasetSpec(
#                 name='x',
#                 doc='The x coordinate of the optode',
#                 dtype='float',
#                 quantity='?'
#             ),
#             NWBDatasetSpec(
#                 name='y',
#                 doc='The y coordinate of the optode',
#                 dtype='float',
#                 quantity='?'
#             ),
#             NWBDatasetSpec(
#                 name='z',
#                 doc='The z coordinate of the optode',
#                 dtype='float',
#                 quantity='?'
#             ),
#             NWBDatasetSpec(
#                 name='wavelengths',
#                 doc='An array of wavelengths available for this source-detector pair',
#                 shape=(None,),
#                 dtype='float',
#                 attributes=[
#                     NWBAttributeSpec(
#                         name='unit',
#                         doc='The unit of measurement for the wavelengths',
#                         dtype='text',
#                         default_value='nm'
#                     )
#                 ]
#             )
#         ],
#     )
    
    
    NIRSDevice = NWBGroupSpec(
        neurodata_type_def='NIRSDevice',
        neurodata_type_inc='Device',
        doc='A NIRS Device',
        datasets=[
            NWBDatasetSpec(
                name='sources',
                doc='An array of the OpticalSources on this device',
                dtype=NWBRefSpec(target_type='OpticalSource', reftype='object'),
                shape=(None,)
            ),
            NWBDatasetSpec(
                name='detectors',
                doc='An array of the OpticalDetectors on this device',
                dtype=NWBRefSpec(target_type='OpticalDetector', reftype='object'),
                shape=(None,)
            ),
            NWBDatasetSpec(
                neurodata_type_inc='DynamicTable',
                name='channels',
                doc='A table of the optical channels available on this device'
            )
        ],
        attributes=[
            NWBAttributeSpec(
                name='wavelength_unit',
                doc='The unit of measurement for the wavelength channel column',
                dtype='text',
                default_value='nm'
            )
        ]
    )
    
    NIRSSeries = NWBGroupSpec(
        neurodata_type_def='NIRSSeries',
        neurodata_type_inc='NWBDataInterface',
        doc='A timeseries of NIRS data',
        datasets=[
            NWBDatasetSpec(
                neurodata_type_inc='DynamicTableRegion',
                name='channels',
                doc='DynamicTableRegion pointer to the optical channels represented by this NIRSSeries',
            )
        ]
    )

    # TODO: add all of your new data types to this list
    new_data_types = [
        OpticalSource,
        OpticalDetector,
#         Optode,
        NIRSDevice,
        NIRSSeries
    ]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
