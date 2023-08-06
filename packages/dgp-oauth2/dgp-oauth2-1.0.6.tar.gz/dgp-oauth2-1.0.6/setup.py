import os
import io
from setuptools import setup, find_packages


# Helpers
def read(*paths):
    """Read a text file."""
    basedir = os.path.dirname(__file__)
    fullpath = os.path.join(basedir, *paths)
    contents = io.open(fullpath, encoding='utf-8').read().strip()
    return contents
    
    
# Prepare
PACKAGE = 'dgp_oauth2'
NAME = 'dgp-oauth2'
INSTALL_REQUIRES = [
    'flask',
    'flask-cors',
    'flask-jsonpify',
    'flask-session',
    'flask-oauthlib',
    'pyjwt',
    'sqlalchemy',
    'cryptography',
    'psycopg2-binary',
    'requests',
]
TESTS_REQUIRE = [
    'pylama',
    'tox',
    'coverage',
    'coveralls',
    'pytest',
    'pytest-cov',
    'requests-mock==1.3.0'
]
README = read('README.md')
VERSION = read(PACKAGE, 'VERSION')
PACKAGES = find_packages(exclude=['examples', 'tests', 'tools'])


# Run
setup(
    name=NAME,
    version=VERSION,
    packages=PACKAGES,
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    extras_require={'develop': TESTS_REQUIRE},
    zip_safe=False,
    long_description=README,
    long_description_content_type='text/markdown',
    description='{{ DESCRIPTION }}',
    author='Adam Kariv, Open Knowledge (International), Datopian',
    url='https://github.com/dataspot/dgp-oauth2',
    license='MIT',
    keywords=[
        'data',
        'authentication',
        'oauth2'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
