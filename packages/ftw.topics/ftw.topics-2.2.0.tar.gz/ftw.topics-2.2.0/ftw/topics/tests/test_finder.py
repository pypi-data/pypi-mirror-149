from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from ftw.testing import MockTestCase
from ftw.topics.finder import DefaultTopicTreeFinder
from ftw.topics.interfaces import ITopicRootFinder
from ftw.topics.interfaces import ITopicTree
from ftw.topics.testing import ZCML_LAYER
from plone.app.layout.navigation.interfaces import INavigationRoot
from zope.component import getMultiAdapter
from zope.component import getSiteManager
from zope.component import queryMultiAdapter
from zope.component.hooks import setSite
from zope.interface.verify import verifyClass


class TestDefaultTopicTreeFinder(MockTestCase):

    layer = ZCML_LAYER

    def setUp(self):
        super(TestDefaultTopicTreeFinder, self).setUp()
        self.request = self.stub_request()

    def tearDown(self):
        super(TestDefaultTopicTreeFinder, self).tearDown()
        setSite(None)

    def create_tree(self, with_trees=True):
        objs = {}

        objs['site'] = self.providing_stub(IPloneSiteRoot, INavigationRoot)
        objs['site'].getPhysicalPath.return_value = ['', 'site']
        objs['site'].getSiteManager.side_effect = getSiteManager

        if with_trees:
            objs['root'] = self.providing_stub(ITopicRootFinder)
            objs['site'].contentValues.return_value = [objs['root']]
        else:
            objs['site'].contentValues.return_value = []

        objs['foo'] = self.stub()
        objs['foo'].getPhysicalPath.return_value = ['', 'site', 'foo']
        self.set_parent(objs['foo'], objs['site'])

        objs['subsite'] = self.providing_stub(INavigationRoot)
        objs['subsite'].getPhysicalPath.return_value = ['', 'site', 'subsite']
        self.set_parent(objs['subsite'], objs['site'])

        objs['bar'] = self.stub()
        objs['bar'].getPhysicalPath.return_value = [
            '', 'site', 'subsite', 'bar']
        self.set_parent(objs['bar'], objs['subsite'])

        if with_trees:
            objs['subtree'] = self.providing_stub(ITopicTree)
            objs['subsite'].contentValues.return_value = [objs['subtree']]
        else:
            objs['subsite'].contentValues.return_value = []

        return objs

    def test_adapter_implements_interface(self):
        self.assertTrue(
            ITopicRootFinder.implementedBy(DefaultTopicTreeFinder))
        verifyClass(ITopicRootFinder, DefaultTopicTreeFinder)

    def test_adapter_registered(self):
        context = self.create_dummy()

        self.assertTrue(
            queryMultiAdapter((context, self.request), ITopicRootFinder),
            'ZugTopicTreeFinder adapter is not registered')

    def test_finds_next_navigation_root(self):
        objs = self.create_tree(with_trees=True)

        obj = objs['foo']
        finder = getMultiAdapter((obj, self.request), ITopicRootFinder)

        self.assertEqual(finder.get_topic_root_path(), '/site')

    def test_subsite_obj_finds_subsite_with_trees(self):
        objs = self.create_tree(with_trees=True)

        obj = objs['bar']
        finder = getMultiAdapter((obj, self.request), ITopicRootFinder)

        self.assertEqual(finder.get_topic_root_path(), '/site/subsite')

    def test_subsite_obj_finds_site_without_trees(self):
        objs = self.create_tree(with_trees=False)

        obj = objs['bar']
        finder = getMultiAdapter((obj, self.request), ITopicRootFinder)

        self.assertEqual(finder.get_topic_root_path(), '/site')

    def test_finds_site_on_site(self):
        objs = self.create_tree(with_trees=True)

        obj = objs['site']
        finder = getMultiAdapter((obj, self.request), ITopicRootFinder)

        self.assertEqual(finder.get_topic_root_path(), '/site')

    def test_fall_back_to_plone_site_root(self):
        site = self.create_dummy(getSiteManager=getSiteManager,
                                 getPhysicalPath=lambda: ('', 'site'))
        setSite(site)

        finder = getMultiAdapter((self.create_dummy(), self.request),
                                 ITopicRootFinder)

        self.assertEqual(finder.get_topic_root_path(), '/site')
