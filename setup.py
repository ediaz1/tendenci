import os
import sys
import subprocess

from fnmatch import fnmatchcase
from distutils.util import convert_path
from setuptools import setup, find_packages

from tendenci import __version__ as version


def read(*path):
    return open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                *path)).read()

# Provided as an attribute, so you can append to these instead
# of replicating them:
standard_exclude = ["*.pyc", "*~", "*.bak", ".DS_Store"]
standard_exclude_directories = [
    ".*", "CVS", "_darcs", "./build",
    "./dist", "EGG-INFO", "*.egg-info"
]


# Copied from paste/util/finddata.py
def find_package_data(where=".", package="", exclude=standard_exclude,
        exclude_directories=standard_exclude_directories,
        only_in_packages=True, show_ignored=False):
    """
    Return a dictionary suitable for use in ``package_data``
    in a distutils ``setup.py`` file.

    The dictionary looks like::

        {"package": [files]}

    Where ``files`` is a list of all the files in that package that
    don't match anything in ``exclude``.

    If ``only_in_packages`` is true, then top-level directories that
    are not packages won't be included (but directories under packages
    will).

    Directories matching any pattern in ``exclude_directories`` will
    be ignored; by default directories with leading ``.``, ``CVS``,
    and ``_darcs`` will be ignored.

    If ``show_ignored`` is true, then all the files that aren't
    included in package data are shown on stderr (for debugging
    purposes).

    Note patterns use wildcards, or can be exact paths (including
    leading ``./``), and all searching is case-insensitive.
    """

    out = {}
    stack = [(convert_path(where), "", package, only_in_packages)]
    while stack:
        where, prefix, package, only_in_packages = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        if show_ignored:
                            print >> sys.stderr, (
                                "Directory %s ignored by pattern %s"
                                % (fn, pattern))
                        break
                if bad_name:
                    continue
                if (os.path.isfile(os.path.join(fn, "__init__.py"))
                    and not prefix):
                    if not package:
                        new_package = name
                    else:
                        new_package = package + "." + name
                    stack.append((fn, "", new_package, False))
                else:
                    stack.append((fn, prefix + name + "/", package,
                                    only_in_packages))
            elif package or not only_in_packages:
                # is a file
                bad_name = False
                for pattern in exclude:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        if show_ignored:
                            print >> sys.stderr, (
                                "File %s ignored by pattern %s"
                                % (fn, pattern))
                        break
                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix + name)
    return out


excluded_directories = standard_exclude_directories + ["example", "tests"]
package_data = find_package_data(exclude_directories=excluded_directories, only_in_packages=False)

DESCRIPTION = "Tendenci - A CMS for Nonprofits"

LONG_DESCRIPTION = None
try:
    LONG_DESCRIPTION = subprocess.check_output(['pandoc', '-f', 'markdown', '-t', 'rst', 'README.md'])
except:
    LONG_DESCRIPTION = open('README.md').read()

setup(
    name='tendenci',
    version=version,
    packages=find_packages(),
    package_data=package_data,
    include_package_data=True,
    author='Schipul',
    author_email='programmers@schipul.com',
    url='http://github.com/tendenci/tendenci/',
    license='GPL3',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    platforms=['any'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    entry_points="""
            [console_scripts]
            create-tendenci-project=tendenci.bin.create_tendenci_project:create_project
            update-tendenci-project=tendenci.bin.update_tendenci_project:update_project
        """,
    install_requires=[
        "Django>=1.8,<1.9",
        "django-formtools>=1.0",
        "pisa",
        "Reportlab==2.5",
        "html5lib",
        "Pillow==2.8.2",
        "anyjson>=0.2.4",
        "django-authority>=0.4",
        #"django-avatar>=2.1",  # the one on pypi 2.0 - is not compatible
        "django-countries==3.3",
        "django-form-utils>=0.1.8",
        "django-localflavor==1.1",
        "django-pagination>=1.0.7",
        "django-picklefield>=0.1.6",
        "django-simple-captcha==0.4.5",
        "django-tagging==0.3.6",
        "django-tinymce==1.5.2",
        "django-haystack==2.4.0",
        "feedparser>=4.1",
        "httplib2>=0.4.0",
        "pytz==2015.4",
        "simplejson>=2.0.9",
        "webcolors>=1.3.1",
        "xlrd==0.9.3",
        "xlwt>=0.7.2",
        "BeautifulSoup==3.2.1",
        "beautifulsoup4==4.3.2",
        "oauth2>=1.5.167",
        "python_openid>=2.2",
        "ordereddict==1.1",
        "createsend==3.3.0",
        "celery==3.1.18",
        "django-celery==3.1.16",
        "django-kombu>=0.9.4",
        "mimeparse>=0.1.3",
        "python-dateutil==2.4.2",
        "pdfminer==20110515",
        "stripe==1.22.3",
        "pycrypto==2.6.1",
        "boto==2.38.0",
        "django-timezones==0.2",
        "django-ses==0.7.0",
        "Geraldo==0.4.16",
        "django-tastypie==0.12.2",
        "johnny-cache==1.6.1a",
        "docutils==0.12",
        'chardet==2.3.0',
        "psycopg2==2.6.1",
        "gunicorn==19.3.0",
        "django-storages==1.1.8",
        "python-memcached==1.54",
        "Whoosh==2.7.0",
        "simple-salesforce==0.67.2",
        "selenium==2.46.0",
        "raven==5.1.1",
        "django-admin-bootstrapped==2.5.2",
        "django-bootstrap3==5.4.0",
        "django-app-namespace-template-loader==0.3",
        'django-annoying',
        'unidecode',
        'Markdown',
        'unicodecsv',
    ],
)
