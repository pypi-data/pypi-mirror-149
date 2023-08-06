from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from ftw.testing import IS_PLONE_5
from ftw.testing.layer import ComponentRegistryLayer
from ftw.topics.behavior import ITopicSupportSchema
from ftw.topics.tests.utils import add_behaviors
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import ploneSite
from plone.testing import Layer
from plone.testing import z2
from plone.testing import zca
from plone.testing import zodb
from zope.configuration import xmlconfig
import ftw.topics.tests.builders #noqa


class ZCMLLayer(ComponentRegistryLayer):

    def setUp(self):
        super(ZCMLLayer, self).setUp()
        import ftw.topics
        self.load_zcml_file('tests.zcml', ftw.topics.tests)
        self.load_zcml_file('configure.zcml', ftw.topics)

ZCML_LAYER = ZCMLLayer()


class TopicsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        import z3c.autoinclude
        xmlconfig.file('meta.zcml', z3c.autoinclude,
                       context=configurationContext)
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <includePlugins package="plone" />'
            '</configure>',
            context=configurationContext)

        import ftw.topics
        xmlconfig.file('functional_tests.zcml', ftw.topics.tests,
                       context=configurationContext)

        z2.installProduct(app, 'ftw.simplelayout')
        z2.installProduct(app, 'Products.DateRecurringIndex')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftw.simplelayout.contenttypes:default')
        applyProfile(portal, 'ftw.topics:default')
        applyProfile(portal, 'plone.restapi:default')


TOPICS_FIXTURE = TopicsLayer()
TOPICS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(TOPICS_FIXTURE, ), name='ftw.topics:integration')
TOPICS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(TOPICS_FIXTURE, ), name='ftw.topics:functional')


class ExampleContentLayer(Layer):

    defaultBases = (TOPICS_FIXTURE, )

    def setUp(self):
        # Stack the component registry
        self['configurationContext'] = zca.stackConfigurationContext(
            self.get('configurationContext'))

        # Stack the database
        self['zodbDB'] = zodb.stackDemoStorage(
            self.get('zodbDB'), name='SimplelayoutTopicsLayer')

        with ploneSite() as portal:
            applyProfile(portal, 'plone.app.contenttypes:default')

            add_behaviors('Document', 'ftw.topics.behavior.ITopicSupportSchema')
            applyProfile(portal, 'ftw.topics.tests:example')


    def tearDown(self):
        # Zap the stacked ZODB
        self['zodbDB'].close()
        del self['zodbDB']
        # Zap the stacked component registry
        del self['configurationContext']


EXAMPLE_CONTENT_FIXTURE = ExampleContentLayer()
EXAMPLE_CONTENT_DEFAULT_FUNCTIONAL = FunctionalTesting(
    bases=(EXAMPLE_CONTENT_FIXTURE, ),
    name='ftw.topics.examplecontent:default:functional')
