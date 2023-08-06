import unittest
import pytest
from vaip.json.build.build_aic import *

@pytest.mark.usefixtures('fixtures')
class BuildAICTest(unittest.TestCase):

    def setUp(self):
        self.data_obj_type = 'digital_object'
        self.arn = 'arn.123456789'
        self.IRI = 'IRI_TO_ORIGINAL'
        self.uuid = 'test2dfc-7c04-418d-8edf-f908ea4657f2'
        self.key = "arbitrary/prefix/test.nc"
        self.aip_key = self.key.replace('.nc', '.json')
        self.aip_bucket = "test-aip-bucket"
        self.archive_bucket = "test-archive-bucket"
        s3_base = "https://s3.console.aws.amazon.com/s3/object/" \
                  "{0}?region=us-east-1&prefix={1}"
        self.uri = s3_base.format(self.archive_bucket, self.key)
        self.vaip_uri = s3_base.format(self.aip_bucket, self.aip_key)
        self.shortname = 'gov.noaa.ncdc:C00844'
        self.version = 'Version 2'
        self.updated = '2021-09-10T14:25:00Z'
        self.poc = 'test@noaa.gov'
        self.aic_class = 'archival_information_package'
        self.aic_type = 'archival_information_collection'

    def test_build_data_object(self):

        data_obj = build_data_object(self.data_obj_type, self.arn, self.IRI)

        assert isinstance(data_obj, DataObject)

    def test_build_content_data_object(self):

        data_obj = build_data_object(self.data_obj_type, self.arn, self.IRI)
        content_data_obj = build_content_data_object(data_obj)

        assert isinstance(content_data_obj, ContentDataObject)

    def test_build_content_information(self):

        data_obj = build_data_object(self.data_obj_type, self.arn, self.IRI)
        content_data_obj = build_content_data_object(data_obj)
        content_information = build_content_information(content_data_obj)

        assert isinstance(content_information, ContentInformation)

    def test_build_granule(self):

        granule = build_granule(self.uuid, self.uri, self.vaip_uri)

        assert isinstance(granule, Granule)

    def test_build_provenance(self):

        granule = build_granule(self.uuid, self.uri, self.vaip_uri)
        provenance = build_provenance([granule])

        assert isinstance(provenance, Provenance)

    def test_build_reference_information(self):

        reference_information = build_reference_information(self.shortname, self.version, self.updated)

        assert isinstance(reference_information, ReferenceInformation)

    def test_build_preservation_description_information(self):

        granule = build_granule(self.uuid, self.uri, self.vaip_uri)
        provenance = build_provenance([granule])
        reference_information = build_reference_information(self.shortname, self.version, self.updated)
        preservation_description_information = build_preservation_description_information(reference_information,provenance)

        assert isinstance(preservation_description_information, PreservationDescriptionInformation)

    def test_build_aic(self):

        aic = build_aic(self.aic_class, self.aic_type, self.poc, self.data_obj_type, self.arn, self.IRI, self.uuid,
                        self.uri, self.vaip_uri, self.shortname, self.version, self.updated)

        assert isinstance(aic, Aic)

        aic_dict = aic.to_dict()
        assert aic_dict == {
            "class": "archival_information_package",
            "type": "archival_information_collection",
            "preservation_description_information": {
                "reference_information": {
                    "shortname": "gov.noaa.ncdc:C00844",
                    "version": "Version 2",
                    "updated": "2021-09-10T14:25:00+00:00"
                },
                "provenance": {
                    "granules": [
                        {
                            "uuid": "test2dfc-7c04-418d-8edf-f908ea4657f2",
                            "uri": 'https://s3.console.aws.amazon.com/s3/object/'
                           'test-archive-bucket?region=us-east-1&prefix='
                           'arbitrary/prefix/test.nc',
                            "vaip_uri": 'https://s3.console.aws.amazon.com/s3/object/'
                                'test-aip-bucket?region=us-east-1&prefix='
                                'arbitrary/prefix/test.json'
                        }
                    ]
                }
            },
            "content_information": {
                "content_data_object": {
                    "data_object": {
                        "type": "digital_object",
                        "arn": "arn.123456789",
                        "IRI": "IRI_TO_ORIGINAL"
                    }
                }
            },
            "poc": "test@noaa.gov"
        }

    def test_build_aic_empty_granule(self):

        aic_empty_granule = build_aic_empty_granule(self.aic_class, self.aic_type, self.data_obj_type,
                                self.arn, self.IRI, self.shortname, self.version, self.updated)

        assert isinstance(aic_empty_granule, Aic)

        aic_dict = aic_empty_granule.to_dict()
        assert aic_dict == {
            "class": "archival_information_package",
            "type": "archival_information_collection",
            "preservation_description_information": {
                "reference_information": {
                    "shortname": "gov.noaa.ncdc:C00844",
                    "version": "Version 2",
                    "updated": "2021-09-10T14:25:00+00:00"
                },
                "provenance": {
                    "granules": []
                }
            },
            "content_information": {
                "content_data_object": {
                    "data_object": {
                        "type": "digital_object",
                        "arn": "arn.123456789",
                        "IRI": "IRI_TO_ORIGINAL"
                    }
                }
            },
            "poc": None
        }