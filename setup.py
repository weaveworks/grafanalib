import os
from setuptools import setup, find_packages


def local_file(name):
    return os.path.relpath(os.path.join(os.path.dirname(__file__), name))


README = local_file('README.rst')


setup(
    name='grafanalib',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/guides/single-sourcing-package-version/
    version='0.7.0',
    description='Library for building Grafana dashboards',
    long_description=open(README).read(),
    url='https://github.com/weaveworks/grafanalib',
    project_urls={
        "Documentation": "https://grafanalib.readthedocs.io",
        "Source": "https://github.com/weaveworks/grafanalib",
    },
    author='Weaveworks',
    author_email='help+grafanalib@weave.works',
    license='Apache',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: System :: Monitoring',
    ],
    install_requires=[
        'attrs>=15.2.0',
    ],
    extras_require={
        'dev': [
            'flake8',
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'generate-dashboard=grafanalib._gen:generate_dashboard_script',
            'generate-dashboards=grafanalib._gen:generate_dashboards_script',
            'generate-alertgroup=grafanalib._gen:generate_alertgroup_script',
            'generate-alertgroups=grafanalib._gen:generate_alertgroups_script'
        ],
    },
)
