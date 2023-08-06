from setuptools import setup

setup(
    name = 'python-timeout',
    packages = ['timeout'],
    version='3.3',
    description = 'Random timeout between minimum and maximum values',
    url = 'https://github.com/xjxckk/python-timeout/',
    download_url = 'https://github.com/xjxckk/python-timeout/archive/refs/tags/v1.tar.gz',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
    )