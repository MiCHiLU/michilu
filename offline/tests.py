# -*- coding: utf-8 -*-
"""
"""

from django.test import TestCase
from django.test.client import Client
from django.utils import simplejson

class ResponseTest(TestCase):

    def test_response(self):
        response = self.client.get("/offline/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/static/offline/gears.js")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/static/offline/manifest.json")
        self.assertEqual(response.status_code, 200)
        json_parsed = simplejson.loads(response.content)
        self.assertEqual(json_parsed.keys(),
            [u'version', u'betaManifestVersion', u'entries'])

