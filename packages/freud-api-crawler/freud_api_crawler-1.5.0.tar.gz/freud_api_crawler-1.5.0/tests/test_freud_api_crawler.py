#!/usr/bin/env python

"""Tests for `freud_api_crawler` package."""

import unittest
import types

import lxml.etree as ET

from freud_api_crawler import freud_api_crawler as frd
from freud_api_crawler import string_utils
from freud_api_crawler import tei_utils


WERK_ID = "9d035a03-28d7-4013-adaf-63337d78ece4"
MANIFESTATION_ID = "a10e8c78-adad-4ca2-bfcb-b51bedcd7b58"
MANIFESTATION_PAGE_ID = "5126755a-eeae-4f53-82f9-aaa3a6fd81a9"
MANIFESTATION_PAGE_URL = "https://www.freud-edition.net/jsonapi/node/manifestation_\
seite/5126755a-eeae-4f53-82f9-aaa3a6fd81a9"

FRD_WERK = frd.FrdWerk(auth_items=frd.AUTH_ITEMS, werk_id=WERK_ID)
FRD_MANIFESTATION = frd.FrdManifestation(
    auth_items=frd.AUTH_ITEMS,
    manifestation_id=MANIFESTATION_ID
)


class TestFrdWerk(unittest.TestCase):
    """Tests for `freud_api_crawler` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test001_init_frdwerk(self):
        werk = FRD_WERK
        self.assertEqual(werk.werk_id, WERK_ID)

    def test002_init_frdwerk(self):
        werk = FRD_WERK
        self.assertEqual(
            werk.md__title,
            'Freud, Sigmund  (1905-004; 1905d): Drei Abhandlungen zur Sexualtheorie'
        )


class TestFreud_api_crawler(unittest.TestCase):
    """Tests for `freud_api_crawler` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_002_endpoints_with_auth(self):
        """Test of endpoints-method"""
        frd_obj = frd.FrdClient(auth_items=frd.AUTH_ITEMS)
        endpoints = frd_obj.list_endpoints()
        self.assertTrue(endpoints)
        self.assertTrue('node' in endpoints.keys())

    def test_004_FrdManifestation_init_test(self):
        """check for correct id"""
        frd_obj = FRD_MANIFESTATION
        self.assertEqual(frd_obj.manifestation_id, MANIFESTATION_ID)

    def test_005_FrdManifestation_init_test(self):
        """test if correct manifestation endpoint is returned"""
        frd_obj = FRD_MANIFESTATION
        self.assertEqual(
            frd_obj.manifestation_endpoint,
            f'https://www.freud-edition.net/jsonapi/node/manifestation/{MANIFESTATION_ID}'
        )

    def test_006_FrdManifestation_return_manifestation(self):
        """check if correct manifestation is returned"""
        frd_obj = FRD_MANIFESTATION
        fetch_man_id = frd_obj.manifestation['data']['id']
        self.assertEqual(fetch_man_id, MANIFESTATION_ID)

    def test_007_FrdManifestation_page_count(self):
        """count related pages"""
        frd_obj = FRD_MANIFESTATION
        pages = frd_obj.page_count
        self.assertEqual(pages, 22)

    def test_008_FrdManifestation_number_of_metaattributes(self):
        """Count meta_attributes"""
        frd_obj = FRD_MANIFESTATION
        test_item = frd_obj.meta_attributes
        self.assertEqual(len(test_item), 68)

    def test_009_FrdManifestation_title(self):
        """Check title"""
        frd_obj = FRD_MANIFESTATION
        test_item = frd_obj.md__title
        self.assertEqual(test_item, 'II. Die infantile Sexualität')

    def test_010_FrdManifestation_page(self):
        """Check loading of manifestation_seite"""
        frd_obj = FRD_MANIFESTATION
        for x in [MANIFESTATION_PAGE_ID, MANIFESTATION_PAGE_URL]:
            page = frd_obj.get_page(page_id=x)
            test_item = page['data']['id']
            self.assertEqual(test_item, MANIFESTATION_PAGE_ID)

    def test_011_str_cleaning(self):
        """test clean_markup function"""
        frd_obj = FRD_MANIFESTATION
        page = frd_obj.get_page(page_id=MANIFESTATION_PAGE_ID)
        body = page['data']['attributes']['body']['processed']
        test_pattern = string_utils.CLEAN_UP_PATTERNS[1][0]
        cleaned_body = string_utils.clean_markup(body)
        self.assertTrue(test_pattern not in cleaned_body)

    def test_011a_str_cleaning(self):
        some_string = "safljk ı sdfdsf ‚"
        cleaned_string = string_utils.clean_markup(some_string)
        self.assertTrue = ('ı' not in cleaned_string)
        self.assertTrue = ('‚' not in cleaned_string)

    def test_012_str_cleaning(self):
        """test clean_markup function"""
        frd_obj = FRD_MANIFESTATION
        page = frd_obj.get_page(page_id=MANIFESTATION_PAGE_ID)
        result = frd_obj.process_page(page)
        self.assertEqual(result['id'], MANIFESTATION_PAGE_ID)
        self.assertTrue('body' in result.keys())

    def test_013_check_dummy_tei(self):
        """test for dummy tei"""
        frd_obj = FRD_MANIFESTATION
        doc = frd_obj.tei_dummy
        root_el = doc.xpath('//tei:TEI', namespaces=frd_obj.nsmap)[0]
        self.assertEqual(root_el.tag, '{http://www.tei-c.org/ns/1.0}TEI')

    def test_014_check_tei_serialiazer(self):
        """test tei serialisation"""
        frd_obj = FRD_MANIFESTATION
        xml = frd_obj.make_xml()
        xml_str = ET.tostring(xml).decode('utf-8')
        print(type(xml), type(xml_str))
        self.assertTrue(frd_obj.manifestation_id in xml_str)

    def test_015_yield_works(self):
        yielder = frd.yield_works(frd.FRD_WORK_LIST)
        self.assertIsInstance(yielder, types.GeneratorType)

    def test_016_filter_man_by_type(self):
        werk = FRD_WERK
        all_man = werk.get_manifestations()
        full_man = werk.get_manifestations(filters=frd.MANIFEST_DEFAULT_FILTER)
        self.assertTrue(len(all_man) > len(full_man))


class TestStringUtils(unittest.TestCase):
    """Tests for `freud_api_crawler` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_001_extract_page_nr(self):
        """ Test if page number is recogniced"""
        samples = [
            ('Seite 21', '21'),
            ('Seite keine Zahl', 'Seite keine Zahl'),
            ('Seite21-22', '21-22')
        ]
        for x in samples:
            page_nr = string_utils.extract_page_nr(x[0])
            self.assertEqual(page_nr, x[1])

    def test_002_always_https(self):
        samples = [
            ('no_url', 'no_url'),
            ('http://whatever.com', 'https://whatever.com'),
            ('https://whatever.com', 'https://whatever.com')
        ]
        for x in samples:
            new_url = string_utils.always_https(x[0])
            self.assertEqual(new_url, x[1])


class TestTeiUtils(unittest.TestCase):
    """Tests for `freud_api_crawler.tei_utils` module."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_001_make_pg(self):
        """ Test make_pb"""
        pb_el = tei_utils.make_pb(
            1, 'https://whatever.com', "1234sieben"
        )
        pb_str = ET.tostring(pb_el).decode('utf-8')
        self.assertEqual(
            pb_str,
            '<ns0:pb xmlns:ns0="http://www.tei-c.org/ns/1.0" n="1" facs="https://whatever.com" xml:id="faks__1234sieben"/>'  # noqa: E501
        )
