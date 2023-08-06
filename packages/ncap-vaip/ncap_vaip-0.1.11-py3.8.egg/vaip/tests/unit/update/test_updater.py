import json
import os
import unittest

import boto3
import pytest
from moto import mock_s3
from vaip.update.updater import *

os.environ['AIP_BUCKET'] = 'test-vaip-bucket'
os.environ['ARCHIVE_BUCKET'] = 'test-archive-bucket'


@pytest.mark.usefixtures("fixtures")
class Handlertest(unittest.TestCase):

    @mock_s3
    def setUp(self):
        self.client = boto3.client('s3', region_name='us-east-1')

        # We expect an AIC to be present for these granule-level updates
        fixture_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "fixtures", "C00844.json"
        )
        with open(fixture_path, 'rb') as f:
            self.collection_vaip = json.loads(f.read())

        self.uuid = "test2dfc-7c04-418d-8edf-f908ea4657f2"
        self.data_key = "arbitrary/prefix/test.nc"
        self.aip_full_key = self.data_key.replace('.nc', '.json')

        self.event = {
            "key": self.data_key,
            "granule": {
                "vaip": {
                    "algorithm": "MD5",
                    "retention": 1337,
                    "poc": "test"
                },
                "size": 1337,
                "checksum": "test23a6498ef444dcde36efb400a3a1",
                "uuid": "test0b4-06f1-4bb9-b7e5-99266f33d639",
                "shortname": "gov.noaa.ncdc:C00844",
                "poc": {
                    "email": "test@noaa.gov"
                }
            },
            "archive_result": {
                "ResponseMetadata": {
                    "HTTPHeaders": {
                        "x-amz-version-id": "561VLdshfnvo9tui4amhzhlPHGz3s5dj"
                    },
                    "RetryAttempts": 0
                },
                "CopyObjectResult": {
                    "LastModified": "2021-03-01"
                },
                "VersionId": "LHEnMpUI1rRPVuAC9RxmHCIbyhTDD_ut"
            }
        }

    def test_generate_granule_vaip(self):
        # Simulate a new GVAIP
        latest_aip = None
        update_or_instantiate_granule_vaip(
            self.event, latest_aip, self.data_key, self.aip_full_key)

        # Simulate an updated GVAIP
        latest_aip = {
            "preservation_description_information" : {
                "provenance": {
                    "versions": [
                        {
                            "version": 0
                        }
                    ]
                }
            }
        }
        update_or_instantiate_granule_vaip(self.event, latest_aip,
                                           self.data_key, self.aip_full_key)

    def test_generate_collection_vaip(self):
        update_collection_vaip(
            self.collection_vaip, self.data_key, self.aip_full_key,
            self.uuid, {"POC": "tester@noaa.gov"}
        )

    @mock_s3
    def test_handle_granule_vaip(self):
        # Instantiate the AIU
        self.client.create_bucket(Bucket=os.environ['AIP_BUCKET'])
        initial_aiu = handle_granule_vaip(
            self.event, self.client, self.aip_full_key)
        assert len(initial_aiu['preservation_description_information'][
                       'provenance']['versions']) == 1

        # Update the AIU
        updated_aiu = handle_granule_vaip(
            self.event, self.client, self.aip_full_key)
        assert len(updated_aiu['preservation_description_information'][
                       'provenance']['versions']) == 2

    @mock_s3
    def test_handle_collection_vaip(self):
        # We assume the AIC was instantiated in the collection state machine
        self.client.create_bucket(Bucket=os.environ['AIP_BUCKET'])
        self.client.put_object(
            Bucket=os.environ['AIP_BUCKET'],
            Key="collections/C00844.json",
            Body=json.dumps(self.collection_vaip)
        )
        latest_granule_vaip = handle_granule_vaip(
            self.event, self.client, self.aip_full_key)
        aic = handle_collection_vaip(
            self.event, self.client, latest_granule_vaip
        )
        assert len(aic['preservation_description_information'][
                       'provenance']['granules']) == 2

    @mock_s3
    def test_update_collection_vaip(self):
        # We assume the AIC was instantiated in the collection state machine
        self.client.create_bucket(Bucket=os.environ['AIP_BUCKET'])
        self.client.put_object(
            Bucket=os.environ['AIP_BUCKET'],
            Key="collections/C00844.json",
            Body=json.dumps(self.collection_vaip)
        )
        collection_vaip = update_collection_vaip(
            self.collection_vaip,
            self.data_key,
            self.aip_full_key,
            self.uuid,
            None
        )

        assert collection_vaip