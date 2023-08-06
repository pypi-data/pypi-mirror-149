import os
from setuptools import setup, find_packages


version = '2.2.0'


extras_require = {
    'restapi': [
        'plone.restapi',
    ]
}


tests_require = [
    'ftw.simplelayout [contenttypes]',
    'ftw.testing',
    'ftw.testbrowser',
    'ftw.builder',

    'zope.i18n',
    'z3c.autoinclude',
    'transaction',
    'zope.traversing',
    'AccessControl',
    'zope.configuration',

    'plone.uuid',
    'plone.testing',
    'plone.app.testing',
    'plone.app.contenttypes',

    'ftw.inflator [dexterity]',
    'Products.DateRecurringIndex',
    ]

extras_require['tests'] = tests_require + extras_require['restapi']


setup(name='ftw.topics',
      version=version,
      description='Create subject trees in Plone',

      long_description=open('README.rst').read() + '\n' + \
          open(os.path.join('docs', 'HISTORY.txt')).read(),

      classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Framework :: Plone :: 5.1',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

      keywords='ftw topics',
      author='4teamwork AG',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/ftw.topics',

      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw', ],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'setuptools',

        'zope.schema',
        'zope.interface',
        'zope.component',
        'zope.i18nmessageid',
        'Acquisition',
        'Zope2',
        'zc.relation',

        'Plone',
        'plone.app.layout',
        'plone.browserlayer',
        'plone.memoize',
        'Products.GenericSetup',
        'Products.CMFCore',
        'Products.CMFPlone',

        'plone.autoform',
        'plone.behavior',
        'plone.dexterity',
        'plone.app.dexterity',
        'plone.app.relationfield',
        'collective.dexteritytextindexer',
        'plone.app.referenceablebehavior',
        'plone.directives.form',

        'ftw.upgrade',
        'ftw.referencewidget',
        ],

      tests_require=tests_require,
      extras_require=extras_require,

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
