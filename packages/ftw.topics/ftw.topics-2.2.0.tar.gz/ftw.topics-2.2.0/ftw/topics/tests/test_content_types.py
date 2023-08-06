from ftw.testbrowser import browsing
from ftw.topics.interfaces import ITopic
from ftw.topics.interfaces import ITopicTree
from ftw.topics.testing import TOPICS_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from unittest import TestCase
import transaction


class TestContentTypeCreation(TestCase):

    layer = TOPICS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        transaction.commit()

    @browsing
    def test_create_topic_tree(self, browser):
        browser.login()
        browser.open(self.portal)
        browser.css('#ftw-topics-topictree').first.click()

        self.assertTrue(
            browser.url.endswith('++add++ftw.topics.TopicTree'),
            'Should be on the topic tree add view, but url is: %s' % (
                browser.url))

        browser.fill({'Title': 'Topical'}).submit()

        self.assertTrue(
            browser.url.endswith('topical/view'),
            'Should be on "topical" view, but url is: %s' % (
                browser.url))
        self.assertIn('Topical', browser.contents)

        tree = self.portal.get('topical')
        self.assertTrue(ITopicTree.providedBy(tree))

    @browsing
    def test_create_topic(self, browser):
        # first create a tree
        browser.login()
        browser.open('http://nohost/plone/++add++ftw.topics.TopicTree')
        browser.fill({'Title': 'Topical'}).submit()

        self.assertEqual(browser.url,
                         'http://nohost/plone/topical/view')

        factory_link = browser.css('#ftw-topics-topic').first
        self.assertTrue(
            factory_link,
            'There is no "Topic" factory link on the topic tree view.')
        factory_link.click()

        self.assertEqual(
            browser.url,
            'http://nohost/plone/topical/++add++ftw.topics.Topic')

        browser.fill({'Title': 'Manufacturing'}).submit()

        self.assertEqual(browser.url,
                         'http://nohost/plone/topical/manufacturing/view')
        self.assertIn('Manufacturing', browser.contents)

        topic = self.portal.get('topical').get('manufacturing')
        self.assertTrue(ITopic.providedBy(topic))
