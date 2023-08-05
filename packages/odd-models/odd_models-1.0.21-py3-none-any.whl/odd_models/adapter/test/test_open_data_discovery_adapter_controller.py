# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from odd_models.adapter.models.data_entity_list import DataEntityList  # noqa: E501
from odd_models.adapter.test import BaseTestCase


class TestOpenDataDiscoveryAdapterController(BaseTestCase):
    """OpenDataDiscoveryAdapterController integration test stubs"""

    def test_get_data_entities(self):
        """Test case for get_data_entities

        
        """
        query_string = [('changed_since', '2013-10-20T19:20:30+01:00')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/entities',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
