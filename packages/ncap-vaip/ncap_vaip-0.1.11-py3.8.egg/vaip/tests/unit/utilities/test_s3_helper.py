import json
import os
import unittest

import boto3
import pytest
from moto import mock_s3
from vaip.update.updater import *
from vaip.utilities import s3_helper

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

        self.aip_full_key = "arbitrary/prefix/test.json"

    @mock_s3
    def test_write_new_vaip(self):
        self.client.create_bucket(Bucket=os.environ['AIP_BUCKET'])

        vaip_json = {'test-key': 'test-value'}
        return_value = s3_helper.write_new_vaip(
            self.client, vaip_json, self.aip_full_key)

        assert return_value['ResponseMetadata']['HTTPStatusCode'] == 200

    @mock_s3
    def test_check_for_vaip(self):
        # Show the response when the key is not found
        self.client.create_bucket(Bucket=os.environ['AIP_BUCKET'])
        result = check_for_vaip(self.client, self.aip_full_key)
        assert result is None

        # Show a successful match
        self.client.put_object(
            Bucket=os.environ['AIP_BUCKET'],
            Key="collections/C00844.json",
            Body=json.dumps(self.collection_vaip)
        )
        result = check_for_vaip(self.client, "collections/C00844.json")
        assert isinstance(result, dict)

    def test_get_filename(self):
        filename = s3_helper.get_filename("archive/oisst/oisst-avhrr-v02r01.173.nc")
        assert filename == "oisst-avhrr-v02r01.173.nc"