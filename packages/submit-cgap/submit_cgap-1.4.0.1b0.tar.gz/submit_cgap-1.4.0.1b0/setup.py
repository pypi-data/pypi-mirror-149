# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['submit_cgap', 'submit_cgap.scripts', 'submit_cgap.tests']

package_data = \
{'': ['*'], 'submit_cgap.tests': ['data/*']}

install_requires = \
['awscli>=1.18.174',
 'boto3>=1.16.14,<2',
 'dcicutils>=3.9.0',
 'requests>=2.24.0,<3']

entry_points = \
{'console_scripts': ['make-sample-fastq-file = '
                     'submit_cgap.scripts.make_sample_fastq_file:main',
                     'resume-uploads = submit_cgap.scripts.resume_uploads:main',
                     'show-upload-info = '
                     'submit_cgap.scripts.show_upload_info:main',
                     'submit-genelist = '
                     'submit_cgap.scripts.submit_genelist:main',
                     'submit-metadata-bundle = '
                     'submit_cgap.scripts.submit_metadata_bundle:main',
                     'upload-item-data = '
                     'submit_cgap.scripts.upload_item_data:main']}

setup_kwargs = {
    'name': 'submit-cgap',
    'version': '1.4.0.1b0',
    'description': 'Support for uploading file submissions to the Clinical Genomics Analysis Platform (CGAP).',
    'long_description': '==========\nSubmitCGAP\n==========\n\n\nA file submission tool for CGAP\n===============================\n\n.. image:: https://travis-ci.org/dbmi-bgm/SubmitCGAP.svg\n   :target: https://travis-ci.org/dbmi-bgm/SubmitCGAP\n   :alt: Build Status\n\n.. image:: https://coveralls.io/repos/github/dbmi-bgm/SubmitCGAP/badge.svg\n   :target: https://coveralls.io/github/dbmi-bgm/SubmitCGAP\n   :alt: Coverage\n\n.. image:: https://readthedocs.org/projects/submitcgap/badge/?version=latest\n   :target: https://submitcgap.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n\nDescription\n===========\n\nThis is a tool for uploading certain kinds of files to CGAP.\n\nCurrent support is for submission of new cases, family histories, and gene lists.\n\n\nInstallation\n============\n\nInstalling this system involves these steps:\n\n1. Create, install, and activate a virtual environment.\n2. *Only if you are a developer*, install poetry and select the source repository.\n   Others will not have a source repository to select,\n   so should skip this step.\n3. If you are an end user, do "``pip install submit_cgap``".\n   Otherwise, do "``make build``".\n4. Set up a ``~/.cgap-keys.json`` credentials file.\n\nFor detailed information about these installation steps, see\n`Installing SubmitCGAP <https://submitcgap.readthedocs.io/en/latest/installation.html>`_.\n\n\nTesting\n=======\n\nTo run unit tests, do::\n\n   $ make test\n\nAdditional notes on testing these scripts for release can be found in\n`Testing SubmitCGAP <TESTING.rst>`__.\n\n\nGetting Started\n===============\n\nOnce you have finished installing this library into your virtual environment,\nyou should have access to the ``submit-metadata-bundle`` and the ``submit-genelist``\ncommands. For more information about how to format files for submission and how to\nuse these commands, see `Getting Started <https://submitcgap.readthedocs.io/en/latest/getting_started.html>`_.\n',
    'author': '4DN-DCIC Team',
    'author_email': 'support@4dnucleome.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dbmi-bgm/SubmitCGAP',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<3.10',
}


setup(**setup_kwargs)
