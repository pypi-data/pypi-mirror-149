from ftw.testbrowser import browsing
from ftw.testing import MockTestCase
from ftw.topics.browser import tree
from ftw.topics.testing import TOPICS_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.dexterity.utils import createContentInContainer
from unittest import TestCase
import transaction


class TestHelperFunctions(MockTestCase):

    def setUp(self):
        super(TestHelperFunctions, self).setUp()

        self.brain_mocks = [
            self.create_dummy(Title='Foo',
                              getPath=lambda: '/plone/foo',
                              getURL=lambda: 'http://nohost/plone/foo'),

            self.create_dummy(Title='Bar',
                              getPath=lambda: '/plone/foo/bar',
                              getURL=lambda: 'http://nohost/plone/foo/bar'),

            self.create_dummy(Title='Baz',
                              getPath=lambda: '/plone/foo/baz',
                              getURL=lambda: 'http://nohost/plone/foo/baz')]

    def test_get_brain_data(self):
        self.assertEqual(map(tree.get_brain_data, self.brain_mocks),

                         [{'title': 'Foo',
                           'path': '/plone/foo',
                           'url': 'http://nohost/plone/foo',
                           'children': []},

                          {'title': 'Bar',
                           'path': '/plone/foo/bar',
                           'url': 'http://nohost/plone/foo/bar',
                           'children': []},

                          {'title': 'Baz',
                           'path': '/plone/foo/baz',
                           'url': 'http://nohost/plone/foo/baz',
                           'children': []}])

    def test_make_treeish(self):
        data = map(tree.get_brain_data, self.brain_mocks)

        self.maxDiff = None
        self.assertEqual(
            tree.make_treeish(data),

            [{'title': 'Foo',
              'path': '/plone/foo',
              'url': 'http://nohost/plone/foo',

              'children': [

                        {'title': 'Bar',
                         'path': '/plone/foo/bar',
                         'url': 'http://nohost/plone/foo/bar',
                         'children': []},

                        {'title': 'Baz',
                         'path': '/plone/foo/baz',
                         'url': 'http://nohost/plone/foo/baz',
                         'children': []},

                        ]},
             ])


class TestTreeView(TestCase):

    layer = TOPICS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    @browsing
    def test_visible_topic_levels_on_tree_view(self, browser):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        tree = self.create_tree(self.portal)
        first = self.create_topic(tree, u'First Level')
        second = self.create_topic(first, u'Second Level')
        self.create_topic(second, u'Third Level')
        transaction.commit()

        browser.login()
        browser.visit(tree)

        self.assertNotIn(
            'Third Level', self.get_content_links_labels(browser),
            'The tree view should only display the first and the second'
            ' level of the tree, not the third.')

        self.assertEquals(
            ['First Level', 'Second Level'],
            self.get_content_links_labels(browser),
            'The tree view should display the first two tree levels.')

    @browsing
    def test_tree_view_has_two_columns(self, browser):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        tree = self.create_tree(self.portal)
        self.create_topic(tree, u'Topic 1')
        self.create_topic(tree, u'Topic 2')
        transaction.commit()

        browser.login()
        browser.visit(tree)

        self.assertEquals(
            [['Topic 1'], ['Topic 2']],
            self.get_content_links_per_column(browser),

            'The tree view should have two columns and arrange the first'
            ' level topics in those two columns.')

    @browsing
    def test_first_level_topics_are_sorted_by_title(self, browser):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        tree = self.create_tree(self.portal)
        self.create_topic(tree, u'Topic 3')
        self.create_topic(tree, u'Topic 1')
        self.create_topic(tree, u'Topic 2')
        transaction.commit()

        browser.login()
        browser.visit(tree)

        self.assertEquals(
            ['Topic 1', 'Topic 2', 'Topic 3'],
            self.get_content_links_labels(browser),
            'First level topics should be sorted by title.')

    @browsing
    def test_second_level_topics_are_sorted_by_title(self, browser):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        tree = self.create_tree(self.portal)
        parent = self.create_topic(tree, u'Parent')
        self.create_topic(parent, u'Topic 3')
        self.create_topic(parent, u'Topic 1')
        self.create_topic(parent, u'Topic 2')
        transaction.commit()

        browser.login()
        browser.visit(tree)

        self.assertEquals(
            ['Parent', 'Topic 1', 'Topic 2', 'Topic 3'],
            self.get_content_links_labels(browser),
            'Second level topics should be sorted by title.')


    def create_tree(self, parent, title=u'Topics'):
        return createContentInContainer(
            parent, 'ftw.topics.TopicTree', title=title)

    def create_topic(self, parent, title='Topic'):
        return createContentInContainer(parent, 'ftw.topics.Topic',
                                        title=title)

    def get_content_links_labels(self, browser):
        links = browser.css('#content-core a')
        return map(lambda item: item.text, links)

    def get_content_links_per_column(self, browser):
        columns = browser.css('#content-core div.listing-column')
        result = []

        for column in columns:
            links = column.css('a')
            result.append(map(lambda item: item.text, links))

        return result
