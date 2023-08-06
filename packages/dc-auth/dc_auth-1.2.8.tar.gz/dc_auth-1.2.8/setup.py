import os
from setuptools import find_packages, setup
import versioneer

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='dc_auth',
    version=versioneer.get_version(),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    license='BSD',
    description='The Data Central authentication django app',
    long_description=README,
    url='https://datacentral.org',
    author='Liz Mannering',
    author_email='elizabeth.mannering@mq.edu.au',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        "Framework :: Pytest",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'Django>=2.1.2',
        'django-settings-export>=1.2.1',
        'django-cas-ng>=3.6.0',
        'django-cookie-law>=2.0.3',
        'django-extensions>=2.2.8',
        # for testing support
        "pytest",
        "pytest-django",
        "hypothesis[django]",
        "Faker>=0.9.2",
        "factory-boy>=2.11.1",
        "pytz",
    ],
    entry_points={"pytest11": ["dcauth = dc_auth.testing_support"]},
    cmdclass=versioneer.get_cmdclass(),
)
