import unittest
import pytest

from vaip.utilities.json_helper import *

class Handlertest(unittest.TestCase):
    # process_config.compute_membership_task_map
    aic_process_test_event = {
        "detail": {
            "environment": "brandon-dev-2",
            "processed_aiu": {
                "aiu_iri": "https://ncei.noaa.gov/ontologies/vaip/core/0.3.0/entities/RCnL53mixVunkaLjLmWKYgO",
            }
        },
        "process_config": {
            "compute_membership_task_map": {
                "arn": "arn:aws:states:us-east-1:633311497993:stateMachine:charlie-dev-retrieve-aic-process-template-aius",
                "input": {
                    "retrieve_aic_process_template_arn": "arn:aws:lambda:us-east-1:633311497993:function:charlie-dev-retrieve-aic-process-template",
                    "aiu_iri": "{{$.detail.processed_aiu.aiu_iri}}"
                }
            }
        }
    }

    granule_process_test_event = {
            "version": "0",
            "id": "10e68f45-0ca4-6e9d-ffb7-ac840cea0deb",
            "detail-type": "Ingest Event Processed",
            "source": "ncap-archive",
            "account": "633311497993",
            "time": "2022-01-05T17:28:50Z",
            "region": "us-east-1",
            "resources": [
                "arn:aws:states:us-east-1:633311497993:stateMachine:archive-brandon-dev-2-preprocessor",
                "arn:aws:states:us-east-1:633311497993:express:archive-brandon-dev-2-preprocessor:9c2188ad-23e6-61d4-425d-02574bc67344_b0bfad79-d6c3-fd37-3f02-611fcbc7868e:ca2e8d84-97a1-462f-9c5f-46e53012a689"
            ],
            "detail": {
                "environment": "brandon-dev-2",
                "processed_granule": {
                    "filename": "oisst-avhrr-v02r01.20200301.nc",
                    "prefix": "brandon-dev-2",
                    "key": "brandon-dev-2/oisst-avhrr-v02r01.20200301.nc",
                    "bucket": "ncap-archive-dev-nccf-ingest",
                    "granule": {
                        "arn": "arn:aws:s3:::ncap-archive-dev-nccf-ingest/brandon-dev-2/oisst-avhrr-v02r01.20200301.nc",
                        "size": 1661763,
                        "workflow_id": "AIU Archetype",
                        "process_template": "https://ncei.noaa.gov/ontologies/vaip/core/0.3.0/entities/RCnL53mixVunkaLjLmWKYgO"
                    }
                }
            },
            "aiu_workflow_config": {
                "archive_data_task_map": {
                    "arn": "arn:aws:states:us-east-1:633311497993:stateMachine:brandon-dev-satellite-archiver",
                    "input": {
                        "archive_file_arn": "arn:aws:lambda:us-east-1:633311497993:function:brandon-dev-satellite-archiver-ArchiveFileFunction-RnuwC2w6dbDk",
                        "create_uuid_arn": "arn:aws:lambda:us-east-1:633311497993:function:brandon-dev-satellite-archiver-CreateUUIDFunction-2fkfAfjJCKfm",
                        "source_key": "{{$.detail.processed_granule.key}}",
                        "source_bucket": "{{$.detail.processed_granule.bucket}}",
                        "uuid": "{{$.detail.processed_granule.granule.uuid}}",
                        "filename": "{{$.detail.processed_granule.filename}}",
                        "test": {
                            "sub_test": {
                                "source_bucket": "{{$.detail.processed_granule.bucket}}"
                            }
                        },
                        "destination_key": "OISST/",
                        "destination_bucket": "ncap-archive-dev",
                        "algorithm": "MD5",
                        "retention": 20,
                        "poc": {
                            "individual_email": "charles.burris@noaa.gov",
                            "org_email": "ncei.info@noaa.gov"
                        }
                    }
                }
            }
        }

    def test_aic_json_helper(self):
        """
        Show that the json_helper runs the same operation generically.
        :param test_event:
        :return:
        """

        # Show new implementation
        filled_process_template = merge_dicts(
            self.aic_process_test_event, '$.process_config.compute_membership_task_map.input')

        print(filled_process_template)
        self.aic_process_test_event['process_config']['compute_membership_task_map']['input'] = \
            filled_process_template

        # print(json.dumps(filled_process_template, indent=3))
        assert filled_process_template['aiu_iri'] == \
               self.aic_process_test_event['detail']['processed_aiu']['aiu_iri']

    def test_granule_json_helper(self):
        """
        Show that the json_helper runs the same operation generically.
        :param test_event:
        :return:
        """

        # Show new implementation
        filled_process_template = merge_dicts(
            self.granule_process_test_event, '$.aiu_workflow_config.archive_data_task_map.input')

        print(filled_process_template)
        self.granule_process_test_event['aiu_workflow_config']['archive_data_task_map']['input'] = \
            filled_process_template

        # print(json.dumps(filled_process_template, indent=3))
        assert filled_process_template['test'][
                   'sub_test']['source_bucket'] == \
               self.granule_process_test_event['detail']['processed_granule']['bucket']
