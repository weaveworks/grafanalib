from setuptools import setup, find_packages

setup(
    name='grafanalib',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.1.0',
    description='Library for building Grafana dashboards',
    long_description="",
    url='https://github.com/weaveworks/grafanalib',
    author='Weaveworks',
    author_email='help@weave.works',
    license='Apache',
    packages=find_packages(),
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'generate-dashboard=grafanalib._gen:generate_dashboard_script',
            'generate-dashboards=grafanalib._gen:generate_dashboards_script',
        ],
    },
)
