# Automatically created by: scrapyd-deploy

from setuptools import setup, find_packages

setup(
    name='cambridge crawler',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = dictionary_crawler.settings']},
)
