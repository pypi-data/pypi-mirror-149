from ftw.testbrowser import browsing
from ftw.testing.testcase import Dummy
from ftw.topics.testing import EXAMPLE_CONTENT_DEFAULT_FUNCTIONAL
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.browserlayer.layer import mark_layer
from Products.CMFCore.utils import getToolByName
from unittest import TestCase
import transaction


class TestDefaultTopicView(TestCase):

    layer = EXAMPLE_CONTENT_DEFAULT_FUNCTIONAL
    viewname = 'topic_view'

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.subsite = self.portal.get('foo').get('subsite')

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        self.tree = self.portal.get('topics')
        self.node = self.tree.get('manufacturing')
        self.subnode = self.node.get('agile-manufacturing')
        self.topic_technology = self.tree.get('technology')

        self.subsite_tree = self.subsite.get('topics')
        self.subsite_node = self.subsite_tree.get('manufacturing')

        transaction.commit()

        mark_layer(None, Dummy(request=self.request))

    def test_default_topic_view(self):
        portal_types = getToolByName(self.portal, 'portal_types')
        fti = portal_types.get('ftw.topics.Topic')
        self.assertEqual(
            fti.default_view, self.viewname,
            'Expected default view to be %s on "ftw.topics.Topic"'
            ' since only the default GS profile was installed' % (
                self.viewname))

    @browsing
    def test_subnode_listed(self, browser):
        browser.open(self.node, view=self.viewname)
        doc = browser.css('h2.subelements-heading').first.text

        self.assertEqual(doc, 'Topics', 'Expected a "Topics" heading')

        # on node (Manufacturing) should be subnode (Agile Manufacturing)
        link_nodes = browser.css('.subelements-listing a')
        self.assertEqual(len(link_nodes), 2,
                         'Found more or less links than expected')

        self.assertEqual(' '.join(link_nodes.text), 'Agile Manufacturing Quality')

    @browsing
    def test_subnode_has_no_children(self, browser):
        browser.open(self.subnode, view=self.viewname)

        self.assertFalse(browser.css('h2.subelements-heading'),
                         'Expected no "Topics" heading')

    @browsing
    def test_default_section_filter_selection(self, browser):
        browser.login().open(self.node, view=self.viewname)

        self.assertEquals(browser.css('.topic-filter li b').first.text,
                          'Plone site',
                          'Expected section "Plone site" to be ' +
                          'selected by default.')

        filter_links = browser.css('.topic-filter li a').first.text
        self.assertIn('Sub Site', filter_links,
                      'Missing awailable section filter "Sub Site"')

        reference_links = browser.css('.topic-reference-listings a').text
        self.assertIn(
            'Manufacturing processes', reference_links,
            'Link "Manufacturing processes" should be shown')

        self.assertNotIn(
            'Theories', reference_links,
            'Link "Theories" should not be shown, it is in'
            ' the section "Sub Site", not "Plone site"')

    @browsing
    def test_other_section_filter(self, browser):
        browser.login().open(self.node, view=self.viewname)
        browser.find('Sub Site').click()

        self.assertEquals(browser.css('.topic-filter li b').first.text,
                          'Sub Site',
                          'Expected section "Sub Site" to be ' +
                          'selected by default.')

        filter_links = browser.css('.topic-filter li a').first.text
        self.assertIn('Plone site', filter_links,
                      'Missing awailable section filter "Plone site"')

        reference_links = browser.css('.topic-reference-listings a').text
        self.assertNotIn(
            'Manufacturing processes', reference_links,
            'Link "Manufacturing processes" should not be shown, it is in'
            ' the section "Sub Site", not "Plone site"')

        self.assertIn(
            'Theories', reference_links,
            'Link "Theories" should be shown')

    @browsing
    def test_SUBSITE_default_section_filter_selection(self, browser):
        browser.open(self.subsite_node, view=self.viewname)

        self.assertEquals(browser.css('.topic-filter li b').first.text,
                          'Sub Site',
                          'Expected section "Sub Site" to be ' +
                          'selected by default.')

        filter_links = browser.css('.topic-filter li a').first.text
        self.assertIn('Plone site', filter_links,
                      'Missing awailable section filter "Plone site"')

        reference_links = browser.css('.topic-reference-listings a').text
        self.assertNotIn(
            'Manufacturing processes', reference_links,
            'Link "Manufacturing processes" should not be shown, it is in'
            ' the section "Sub Site", not "Plone site"')

        self.assertIn(
            'Theories', reference_links,
            'Link "Theories" should be shown')

    @browsing
    def test_sections_are_always_shown_when_there_are_subsites_and_brefs(self, browser):
        browser.open(self.topic_technology, view=self.viewname)

        self.assertEquals(
            browser.css('.topic-filter li').first.text, 'Plone site',
            'Only Plone site should be shown as section, because there'
            ' are other sections (subsites) - even when there is only one'
            ' section shown.')

    @browsing
    def test_sections_are_not_shown_when_there_are_subsites_but_no_brefs(self, browser):
        self.topic_quality = self.node.get('quality')
        browser.open(self.topic_quality, view=self.viewname)

        self.assertEquals(browser.css('.topic-filter li'), [],
                          'Expect no section, because there is no content')

    @browsing
    def test_sections_are_shown_when_other_sections_have_brefs(self, browser):
        obj = self.subsite_tree.get('technology')
        browser.open(obj, view=self.viewname)

        self.assertEquals(
            ['Plone site', 'Sub Site'],
            browser.css('.topic-filter li').text,
            'Section filter should be visible because other sections have'
            ' backreferences.')

    @browsing
    def test_no_section_are_shown_when_there_are_no_subsites(self, browser):
        # delete all "subsites", so that we have only one "section",
        # which is the site.
        self.portal.manage_delObjects(['foo', 'empty-subsite'])
        transaction.commit()

        browser.open(self.topic_technology, view=self.viewname)

        self.assertEquals(
            0, len(browser.css('.topic-filter')),
            'Sections should not be shown in a non-subsite setup.')

    @browsing
    def test_backreferences_without_view_permissions_are_not_visible(self, browser):
        # setup content and relation
        folder = self.portal.get('foo')
        browser.login().open(folder, view='edit')
        browser.fill({'Related Items': self.subnode})
        browser.find('form.buttons.save').click()

        browser.open(self.subnode, view='topic_view')
        foo_logged_in = browser.css(
                '.topic-reference-listings li a').first.text

        self.assertEquals('Foo', foo_logged_in)

        # remove permissions
        folder.manage_permission('View', roles=[], acquire=False)
        transaction.commit()

        browser.open(self.subnode, view='topic_view')
        foo_logged_out = browser.css('.topic-reference-listings li a')

        self.assertEquals([], foo_logged_out)

    @browsing
    def test_settings_can_hide_backreferences(self, browser):
        browser.login()

        browser.visit(self.topic_technology)
        self.assertTrue(browser.css('.referenceRepresentationListing'))

        browser.visit(self.topic_technology, view='edit')
        browser.fill({'Show backreferences': False}).submit()

        self.assertFalse(browser.css('.referenceRepresentationListing'))
