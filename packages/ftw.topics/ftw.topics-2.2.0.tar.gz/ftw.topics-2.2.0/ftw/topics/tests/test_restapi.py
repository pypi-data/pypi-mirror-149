from ftw.testbrowser import browsing
from ftw.topics.testing import EXAMPLE_CONTENT_DEFAULT_FUNCTIONAL
from unittest import TestCase
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME


class TestTopicRestapi(TestCase):

    layer = EXAMPLE_CONTENT_DEFAULT_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        self.tree = self.portal.get('topics')

    @browsing
    def test_backreferences_expandable(self, browser):
        browser.login()
        topic = self.tree.get('manufacturing')
        document = self.portal.get('manufacturing-processes')

        browser.open(document.absolute_url(), method='GET',
                     headers={'Accept': 'application/json'})
        self.assertNotIn('backreferences', browser.json['@components'])

        browser.open(topic.absolute_url(), method='GET',
                     headers={'Accept': 'application/json'})
        self.assertIn('backreferences', browser.json['@components'])

    @browsing
    def test_node_json_representation(self, browser):
        browser.login()
        topic = self.tree.get('manufacturing')
        document = self.portal.get('manufacturing-processes')

        browser.open(topic.absolute_url() + '?expand=backreferences', method='GET',
                     headers={'Accept': 'application/json'})

        self.assertEqual(
            browser.json['@components']['backreferences']['@id'],
            topic.absolute_url() + '/@backreferences',
        )

        self.assertEqual(
            len(browser.json['@components']['backreferences']['items']),
            1,
        )

        document_json = browser.json['@components']['backreferences']['items'][0]

        browser.open(document.absolute_url(), method='GET',
                     headers={'Accept': 'application/json'})

        self.assertEqual(browser.json, document_json)
