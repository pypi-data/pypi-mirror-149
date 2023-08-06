import unittest

import pytest

from vaip.json.build.build_aiu import *


@pytest.mark.usefixtures("fixtures")
class BuildAIUTest(unittest.TestCase):

    def setUp(self):
        self.key = "arbitrary/prefix/test.nc"
        self.aip_key = self.key.replace('.nc', '.json')
        self.ingest_bucket = "test-ingest-bucket"
        self.aip_bucket = "test-aip-bucket"
        self.archive_bucket = "test-archive-bucket"
        s3_base = "https://s3.console.aws.amazon.com/s3/object/" \
                  "{0}?region=us-east-1&prefix={1}"
        self.granule_uri = s3_base.format(self.archive_bucket, self.key)
        self.aip_uri = s3_base.format(self.aip_bucket, self.aip_key)
        self.aip_type = "unit description"
        self.aiu_class = "archive_information_package"
        self.uuid = "test2dfc-7c04-418d-8edf-f908ea4657f2"
        self.package_description_type = "unit description"
        self.folder = "version-0"
        self.checksum = "test23a6498ef444dcde36efb400a3a1"
        self.algorithm = "SHA-256"
        self.size = 1337
        self.date = "2021-04-01T00:00:00"
        self.retention = 10
        self.version = 0
        self.versionid = "testJ2R.F5Em7sImrRvnLuaE_FUaVFT0"

    def test_build_associated_description(self):
        associated_desc = \
            build_associated_description(self.key, self.aip_bucket,
                                         self.granule_uri, self.aip_uri)
        assert isinstance(associated_desc, AssociatedDescription)

    def test_build_content_data_object(self):
        data_obj = build_data_object(self.granule_uri, self.uuid)
        content_data_object = build_content_data_object([data_obj])

        assert isinstance(content_data_object, ContentDataObject)

    def test_build_content_information(self):
        data_obj = build_data_object(self.granule_uri, self.uuid)
        content_data_object = build_content_data_object([data_obj])
        content_information = \
            build_content_information(content_data_object,
                                      build_representation_information())

        assert isinstance(content_information, ContentInformation)

    def test_build_data_object(self):
        data_object = build_data_object(self.granule_uri, self.uuid)

        assert isinstance(data_object, DataObject)

    def test_build_object(self):
        object = build_object(
            self.uuid, self.checksum, self.algorithm, self.size, self.date)

        assert isinstance(object, Object)

    def test_build_data_objects(self):
        obj = build_object(self.uuid, self.checksum,
                           self.algorithm, self.size, self.date)
        data_objects = build_data_objects(obj)

        assert isinstance(data_objects, DataObjects)

    def test_build_fixity(self):
        obj = build_object(self.uuid, self.checksum,
                           self.algorithm, self.size, self.date)
        data_objects = build_data_objects(obj)

        fixity = build_fixity(data_objects)

        assert isinstance(fixity, Fixity)

    def test_build_package_description(self):
        associated_description = \
            build_associated_description(self.key, self.aip_bucket,
                                         self.granule_uri, self.aip_uri)
        package_description = \
            build_package_description(self.aip_type, associated_description)

        assert isinstance(package_description, PackageDescription)

    def test_build_version(self):
        version = build_version(
            self.versionid, self.checksum, self.algorithm,
            self.size, self.date, self.retention, self.version
        )

        assert isinstance(version, Version)

    def test_build_provenance(self):
        version_obj = \
            build_version(
                self.versionid, self.checksum, self.algorithm,
                self.size, self.date, self.retention, self.version
            )
        provenance = build_provenance([version_obj])

        assert isinstance(provenance, Provenance)

    def test_build_preservation_description_information(self):
        version_obj = \
            build_version(
                self.versionid, self.checksum, self.algorithm,
                self.size, self.date, self.retention, self.version
            )
        provenance = build_provenance([version_obj])

        obj = build_object(self.uuid, self.checksum,
                           self.algorithm, self.size, self.date)
        data_objects = build_data_objects(obj)
        fixity = build_fixity(data_objects)

        preservation_description_information = \
            build_preservation_description_information(provenance, fixity)

        assert isinstance(preservation_description_information,
                          PreservationDescriptionInformation)

    def test_build_aiu(self):
        aiu = build_aiu(
            self.aiu_class, self.aip_type, self.uuid,
            self.package_description_type, self.key, self.ingest_bucket,
            self.granule_uri, self.aip_uri, self.checksum,
            self.algorithm, self.size, self.date,
            self.retention, self.version, self.versionid
        )

        assert isinstance(aiu, Aiu)

        # Show some values are correct
        aiu_dict = aiu.to_dict()
        assert aiu_dict == {
            'class': 'archive_information_package',
            'type': 'unit description',
            'package_description': {
                'type': 'unit description',
                'associated_description': {
                    'key': 'arbitrary/prefix/test.nc',
                    'bucket': 'test-ingest-bucket',
                    'uri': 'https://s3.console.aws.amazon.com/s3/object/'
                           'test-archive-bucket?region=us-east-1&prefix='
                           'arbitrary/prefix/test.nc',
                    'vaip_uri': 'https://s3.console.aws.amazon.com/s3/object/'
                                'test-aip-bucket?region=us-east-1&prefix='
                                'arbitrary/prefix/test.json'
                }
            },
            'packaging_information': {},
            'content_information': {
                'content_data_object': {
                    'data_object': [
                        {
                            'URI': 'https://s3.console.aws.amazon.com/s3/'
                                   'object/test-archive-bucket?region='
                                   'us-east-1&prefix=arbitrary/prefix/test.nc',
                            'UUID': 'test2dfc-7c04-418d-8edf-f908ea4657f2'
                        }
                    ]
                },
                'representation_information': {
                    'structure_information': {},
                    'semantic_information': {},
                    'other_information': {}
                }
            },
            'preservation_description_information': {
                'reference_information': {},
                'provenance': {
                    'versions': [
                        {
                            'id': 'testJ2R.F5Em7sImrRvnLuaE_FUaVFT0',
                            'folder': 'version-0',
                            'checksum': 'test23a6498ef444dcde36efb400a3a1',
                            'algorithm': 'SHA-256',
                            'size': 1337,
                            'date': '2021-04-01T00:00:00',
                            'retention': 10,
                            'version': 0
                        }
                    ]
                },
                'context_information': {},
                'fixity': {
                    'data_objects': {
                        'object': {
                            'UUID': 'test2dfc-7c04-418d-8edf-f908ea4657f2',
                            'checksum': 'test23a6498ef444dcde36efb400a3a1',
                            'algorithm': 'SHA-256',
                            'size': 1337,
                            'date': '2021-04-01T00:00:00'
                        }
                    }
                },
                'access_rights_information': {}
            }
        }