from setuptools import setup
from setuptools import find_namespace_packages, find_packages

# Load the README file
with open(file="README.md", mode="r") as readme_handle:
    long_description = readme_handle.read()


setup(
    

    name='rss-parser-celine-trial1',

    author='Celine Hovanessian Far',

    author_email='celien.hovanessian@gmail.com',

    version='5.1.0',

    description='RSS-parser is a command line interface RSS feed reader',

    long_description=long_description,

    long_description_content_type="text/markdown",

    install_requires=[
		"sphinx-rtd-theme",
        "beautifulsoup4==4.11.1",
        "python_dateutil==2.8.2",
        "reportlab==3.6.9",
        "requests==2.27.1"

    ],

    keywords='rss, rss parser, rss feed, news',

    # here are the packages I want "build."
    packages=["RSSparser"],

    include_package_data=True,

    python_requires='>=3.7',

    # py_modules=['source', 'source.rss_version_11'],

    entry_points={
        'console_scripts': [
            'rss_reader=RSSparser.rss_parser:main'
        ]
    },
    

    classifiers=[

        'License :: OSI Approved :: MIT License',

        'Natural Language :: English',

        'Operating System :: OS Independent',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',

        'Topic :: Education',
    ]
)