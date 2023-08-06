ftw.topics
==========

This package integrates a subject tree into Plone.

Features
--------

- Dexterity based content types "Topic Tree" and "Topic" for
  creating a topic tree (subject tree).

- The topic-view lists all content referenced the topic.


Usage
-----

- Add ``ftw.topics`` to your buildout configuration:

.. code:: ini

    [instance]
    eggs +=
        ftw.topics

- Install the default generic import profile.


ITopicSupport for Dexterity
---------------------------

If you would like to have the topics field on dexterity based types, use
the `ITopicSupportSchema` behavior:

.. code:: xml

    <?xml version="1.0"?>
    <object name="example.conference.presenter" meta_type="Dexterity FTI"
       xmlns:i18n="http://xml.zope.org/namespaces/i18n"
       i18n:domain="example.conference">

         <!-- enabled behaviors -->
         <property name="behaviors">
             <element value="ftw.topics.behavior.ITopicSupportSchema" />
         </property>

    </object>


plone.restapi support
---------------------

If necessary install the [restapi] extra.

.. code:: ini

    [instance]
    eggs +=
        ftw.topics [restapi]



List all backreferences on a topic.

.. code:: http

    GET /plone/topictree/topic?expand=backreferences HTTP/1.1
    Accept: application/json


Response - check the expanded section under "backreferences"

.. code:: http

    HTTP/1.1 200 OK
    Content-Type: application/json

    {
        "@components": {
            "actions": {
                "@id": "http://localhost:55001/plone/topictree/topic/@actions"
            },
            "backreferences": {
                "@id": "http://localhost:55001/plone/topictree/topic/@backreferences",
                "items": [
                    {
                        "@id": "http://localhost:55001/plone/front-page",
                        "title": "Welcome to Plone"
                        ...
                    }
                ],
                ...
            }
        }
    }



Customizing reference representations
-------------------------------------

The ``ITopicReferencePresentation`` adapters are responsible for rendering the
references on the topic view. The adapters consume all items they know and
render them in a section of the view.

`ftw.topics` includes an `ITopicReferencePresentation` for rendering content pages
and a default adapter for all contents which are not consumed by another adapter.

Adding a custom representation adapter is easy:

.. code:: python

    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
    from ftw.topics.browser.representation import DefaultRepresentation
    from my.package.interfaces import IMyType
    from my.package import _

    class MyRepresentation(DefaultRepresentation):
        template = ViewPageTemplateFile('my_representation.pt')

        def consume(self, objects):
            for obj in objects:
                if IMyType.providedBy(obj):
                    self.objects.append(obj)
                else:
                    yield obj

        def title(self):
            return _(u'label_my_objects', default=u'My objects')

        def position(self):
            return 50


consume()
    Be sure that you yield all objects which you do not handle in your adapter.
    They will be passed up the pipeline until another adapter handles them.
    The last adapter is usually the default representation adapter, which consumes
    all left over objects.

title()
    Return the title for your section.

position()
    The adapters are ordered by position. The default adapter has the position 1000,
    the `ftw.contentpage` adapter has the position 100.

Register your adapter with ZCML:

.. code:: xml

    <configure xmlns="http://namespaces.zope.org/zope">

        <adapter
            factory=".representation.MyRepresentation"
            name="my_representation"
            />

    </configure>

Be sure you give the adapter a name, so that it does not conflict with other adapters.


Links
-----

- Github: https://github.com/4teamwork/ftw.topics
- Issues: https://github.com/4teamwork/ftw.topics/issues
- Pypi: http://pypi.python.org/pypi/ftw.topics
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.topics


Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.topics`` is licensed under GNU General Public License, version 2.
