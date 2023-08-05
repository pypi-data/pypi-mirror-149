#!python
VERSION = '2.0.5'

# Major Version 2 Release - python 3, primarily, cython

# from op.subsystem.project.distribution import structured

CMRWebsite = ''

# todo: keywords, classifiers, fix author email, update version,
# get other attributes straight from the core.  determine license.

# fix using .pyc

#@structured('STUPHOS') # .run
def setup(api):
    '''
    Westmetal Configuration::
        project = common.subsystem.project.distribution

    # todo: somehow tag this release as a 'cmr'
    MN(project$distribution):
        description: &description 'Application software.'
        summary: *description

        copyright: 2011-2020 All rights reserved.

        version: 1.0.0
        url: ''

        license: none
        classifiers: []
        keywords: []

        author: pypiContributor
        author-email: none

        include-package-data: true

        # todo: put this all under description structure.
        ignore-packages: true
        ignore-description: true

        document:
            indent($expression): indent
            report::

                by {project[author]}, {environment[copyright]}

                This package contains a Composition Milestone Report (CMR) for:
                    Name: {project[name]}
                    Version: {project[version]}

                For information about a CMR, see:
                    {description.website}

                {description.indented}

                About this project:

                    {long_description}


        customization($method):
            parameters: [appl, client, config] # , +args, ++kwd]
            code::
                try: appl.deleteConfiguration('packages')
                except KeyError: pass

                report = container.document.report.format

                with appl.distributionApi as api:
                    kwd = dict(appl.meta,
                               description = client(api),
                               long_description = appl['description'],
                               application = appl,
                               client = client,
                               project = appl.settings,
                               environment = appl.environment)

                    appl.modifyConfiguration \
                        ('long_description',
                         report(**kwd))

                         '''

    # XXX Don't want to be using io.here, want to be using another
    # folder target, especially because the script will end up using
    # this exported (distribution) package.
    #
    # This is bad because it generates .pyc, thereby polluting our
    # checksum.  I suppose this is ok for _any other project_, but
    # alas, bootstrap.
    #
    # Because this is NOT a distutils command, just try to find landmark.
    from op.subsystem.project.cmr import ProjectHash

    # folder = io.path(__file__).folder

    def findNewest():
        MONTHS = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                  'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

        from op.runtime.layer.etc import _daily_time_pattern_base as timestamp

        import re
        pattern = re.compile(r'wrlc-%s-r(\d+)' % timestamp)

        newest = None

        for folder in io.here.baseFilter('stuphos-*-r*'):
            a = folder.basename
            m = pattern.match(a)

            if m is not None:
                (month, day, year, revision) = m.groups()
                month = MONTHS.index(month.lower())
                day = int(day)
                year = int(year)
                revision = int(revision)

                encoded = '%04d%02d%02d%08d' % (month, day, year, revision)
                if newest and encoded < newest[0]:
                    continue

                newest = [encoded, folder]

        if newest is None:
            return io.here

        return newest[1]

    # Are there other ways to pass parameters to setup distributions?
    folder = system.module.os.environ.get('CMRTARGET') or findNewest()
    folder = io.path(folder)
    hash = ProjectHash.GenerateFromProjectFolder(folder)

    return synthetic(text = hash, website = CMRWebsite,
                     indented = indent(hash)) # XXX indenting signature line...


if __name__ == '__main__':
    import sys
    # import pdb; pdb.set_trace()
    if len(sys.argv) >= 2 and sys.argv[1] == '--dist':
        # Invoke traditional setuptools.
        del sys.argv[0]

        try: from setuptools import setup, find_packages
        except ImportError: from distutils.core import setup, find_packages

        SETUP_CONF = \
        dict (name = "stuphos",
              description = "Containerization middleware.",
              download_url = "",

              license = "None",
              platforms = ['OS-independent', 'Many'],

              include_package_data = True,

              keywords = [],

              classifiers = ['Development Status :: 4 - Beta',
                             'Environment :: Console',
                             'Environment :: No Input/Output (Daemon)',
                             'Environment :: Other Environment',
                             'Environment :: Web Environment',
                             'Framework :: Django :: 1.10',
                             'Framework :: Django',
                             'Intended Audience :: Developers',
                             'Intended Audience :: Information Technology',
                             'Intended Audience :: System Administrators',
                             'License :: Other/Proprietary License',
                             'Natural Language :: English',
                             'Operating System :: POSIX',
                             'Operating System :: POSIX :: Other',
                             'Programming Language :: Other',
                             'Programming Language :: Other Scripting Engines',
                             'Programming Language :: Python',
                             'Programming Language :: Python :: 3',
                             'Programming Language :: Python :: Implementation :: Stackless',
                             'Topic :: Communications :: Chat',
                             'Topic :: Database :: Database Engines/Servers',
                             'Topic :: Games/Entertainment :: Multi-User Dungeons (MUD)',
                             'Topic :: Games/Entertainment :: Real Time Strategy',
                             'Topic :: Games/Entertainment :: Simulation',
                             'Topic :: Internet',
                             'Topic :: Internet :: WWW/HTTP',
                             'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
                             'Topic :: Internet :: WWW/HTTP :: Session',
                             'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
                             'Topic :: Scientific/Engineering :: Physics',
                             'Topic :: Software Development :: Compilers',
                             'Topic :: Software Development :: Embedded Systems',
                             'Topic :: Software Development :: Interpreters',
                             'Topic :: Software Development :: Libraries :: Application Frameworks',
                             'Topic :: System :: Distributed Computing',
                             'Topic :: System :: Emulators',
                             'Topic :: System :: Networking',
                             'Topic :: System :: Operating System Kernels',
                             'Topic :: System :: Operating System',
                             'Topic :: System :: Systems Administration',
                             'Topic :: Terminals :: Telnet',
                             'Topic :: Text Processing :: Markup :: HTML',
                             'Topic :: Text Processing :: Markup :: XML'])


        SETUP_CONF['version'] = VERSION
        SETUP_CONF['url'] = 'http://runphase.com' # 'https://github.com/matrixApi'

        SETUP_CONF['author'] = ''
        SETUP_CONF['author_email'] = ''

        SETUP_CONF['long_description_content_type'] = 'text/plain'
        SETUP_CONF['long_description'] = open('README').read()

        packages  = ['stuphos.'  + p for p in find_packages('stuphos')]
        packages += ['stuphmud.' + p for p in find_packages('stuphmud')]
        packages += ['stuphos', 'stuphmud']
        SETUP_CONF['packages'] = packages

        setup(**SETUP_CONF)

    else:
        # WMC Release.
        setup.main()
