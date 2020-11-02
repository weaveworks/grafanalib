import os
from setuptools import setup, find_packages


def local_file(name):
    return os.path.relpath(os.path.join(os.path.dirname(__file__), name))


README = local_file('README.rst')


setup(
    name='grafanalib',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.5.8',
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
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: System :: Monitoring',
    ],
    install_requires=[
        'attrs==19.2',
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
        ],
    },
)
