# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['wranglertools']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.4',
 'awscli>=1.22.88,<2.0.0',
 'dcicutils>=3.11.0',
 'openpyxl>=3.0.9,<4.0.0',
 'python-magic>=0.4.12']

entry_points = \
{'console_scripts': ['get_field_info = wranglertools.get_field_info:main',
                     'import_data = wranglertools.import_data:main']}

setup_kwargs = {
    'name': 'submit4dn',
    'version': '2.2.0',
    'description': 'Utility package for submitting data to the 4DN Data Portal',
    'long_description': '\n# Submit 4DN - Data Submitter Tools\n\n[![Build Status](https://travis-ci.org/4dn-dcic/Submit4DN.svg?branch=master)](https://travis-ci.org/4dn-dcic/Submit4DN)\n[![Coverage Status](https://coveralls.io/repos/github/4dn-dcic/Submit4DN/badge.svg?branch=master)](https://coveralls.io/github/4dn-dcic/Submit4DN?branch=master)\n[![Code Quality](https://api.codacy.com/project/badge/Grade/a4d521b4dd9c49058304606714528538)](https://www.codacy.com/app/jeremy_7/Submit4DN)\n[![PyPI version](https://badge.fury.io/py/Submit4DN.svg)](https://badge.fury.io/py/Submit4DN)\n\nThe Submit4DN package is written by the [4DN Data Coordination and Integration Center](http://dcic.4dnucleome.org/) for data submitters from the 4DN Network. Please [contact us](mailto:support@4dnucleome.org) to get access to the system, or if you have any questions or suggestions.  Detailed documentation on data submission can be found [at this link](https://data.4dnucleome.org/help/submitter-guide/getting-started-with-submissions)\n\n## Installing the package\n\n```\npip install submit4dn\n```\n\nTo upgrade to the latest version\n\n```\npip install submit4dn --upgrade\n```\n\n### Troubleshooting\n\nThis package is not supported on older Python versions and is supported and tested for versions 3.6 - 3.9.  It may work with other python versions but your mileage may vary.\n\nIt is recommended to install this package in a virtual environment to avoid dependency clashes.\n\nProblems have been reported on recent MacOS X versions having to do with the inablity to find `libmagic`,\na C library to check file types that is used by the `python-magic` library.\n\neg. `ImportError: failed to find libmagic.  Check your installation`\n\nFirst thing to try is:\n\n```\npip uninstall python-magic\npip install python-magic\n```\n\nIf that doesn\'t work one solution that has worked for some from [here](https://github.com/Yelp/elastalert/issues/1927):\n\n```\npip uninstall python-magic\npip install python-magic-bin==0.4.14\n```\n\nOthers have had success using homebrew to install `libmagic`:\n\n```\nbrew install libmagic\nbrew link libmagic  (if the link is already created is going to fail, don\'t worry about that)\n```\n\n## Connecting to the Data Portal\nTo be able to use the provided tools, you need to generate an AccessKey on the [data portal](https://data.4dnucleome.org/).\nIf you do not yet have access, please contact [4DN Data Wranglers](mailto:support@4dnucleome.org)\nto get an account and [learn how to generate and save a key](https://data.4dnucleome.org/help/submitter-guide/getting-started-with-submissions#getting-connection-keys-for-the-4dn-dcic-servers).\n\n## Generating data submission forms\nTo create the data submission excel workbook, you can use `get_field_info`.\n\nIt will accept the following parameters:\n~~~~\n    --keyfile        the path to the file where you have stored your access key info (default ~/keypairs.json)\n    --key            the name of the key identifier for the access key and secret in your keys file (default=default)\n    --type           use for each sheet that you want to add to the excel workbook\n    --nodesc         do not add the descriptions in the second line (by default they are added)\n    --noenums        do not add the list of options for a field if they are specified (by default they are added)\n    --comments       adds any (usually internal) comments together with enums (by default False)\n    --outfile        change the default file name "fields.xlsx" to a specified one\n    --debug          to add more debugging output\n    --noadmin        if you have admin access to 4DN this option lets you generate the sheet as a non-admin user\n~~~~\n\nExamples generating a single sheet:\n~~~~\nget_field_info --type Biosample\nget_field_info --type Biosample --comments\nget_field_info --type Biosample --comments --outfile biosample.xlsx\n~~~~\n\nExample Workbook with all sheets:\n~~~~\nget_field_info --outfile MetadataSheets.xlsx\n~~~~\n\nExamples for Workbooks using a preset option:\n~~~~\nget_field_info --type HiC --comments --outfile exp_hic_generic.xlsx\nget_field_info --type ChIP-seq --comments --outfile exp_chipseq_generic.xlsx\nget_field_info --type FISH --comments --outfile exp_fish_generic.xlsx\n~~~~\n\nCurrent presets include: `Hi-C, ChIP-seq, Repli-seq, ATAC-seq, DamID, ChIA-PET, Capture-C, FISH, SPT`\n\n## Data submission\n\nPlease refer to the [submission guidelines](https://data.4dnucleome.org/help/submitter-guide) and become familiar with the metadata structure prior to submission.\n\nAfter you fill out the data submission forms, you can use `import_data` to submit the metadata. The method can be used both to create new metadata items and to patch fields of existing items.\n~~~~\n\timport_data filename.xlsx\n~~~~\n\n#### Uploading vs Patching\n\nRunnning `import_data` without one of the flags described below will perform a dry run submission that will include several validation checks.\nIt is strongly recommended to do a dry run prior to actual submission and if necessary work with a Data Wrangler to correct any errors.\n\nIf there are uuid, alias, @id, or accession fields in the excel form that match existing entries in the database, you will be asked if you want to PATCH each object.\nYou can use the `--patchall` flag, if you want to patch ALL objects in your document and ignore that message.\n\nIf no object identifiers are found in the document, you need to use `--update` for POSTing to occur.\n\n**Other Helpful Advanced parameters**\n\nNormally you are asked to verify the **Lab** and **Award** that you are submitting for.  In some cases it may be desirable to skip this prompt so a submission\ncan be run by a scheduler or in the background:\n\n`--remote` is an option that will skip any prompt before submission\n\n**However** if you submit for more than one Lab or there is more than one Award associated with your lab you will need to specify these values\nas parameters using `--lab` and/or `--award` followed by the uuids for the appropriate items.\n\n<img src="https://media.giphy.com/media/l0HlN5Y28D9MzzcRy/giphy.gif" width="200" height="200" />\n\n\n# Development\nNote if you are attempting to run the scripts in the wranglertools directory without installing the package then in order to get the correct sys.path you need to run the scripts from the parent directory using the following command format:\n\n```\n  python -m wranglertools.get_field_info —-type Biosource\n\tpython -m wranglertools.import_data filename.xlsx\n```\n\npypi page is - https://pypi.python.org/pypi/Submit4DN\n\nSubmit4DN is packaged with poetry.  New versions can be released and submitted to pypi using `poetry publish`\n\n# Pytest\nEvery function is tested by pytest implementation. It can be run in terminal in submit4dn folder by:\n\n    py.test\n\nSome tests need internet access, and labeled with "webtest" mark.\n\nSome tests have file operations, and labeled with "file_operation" mark.\n\nTo run the mark tests, or exclude them from the tests you can use the following commands:\n\n    # Run all tests\n    py.test\n\n    # Run only webtest\n    py.test -m webtest\n\n    # Run only tests with file_operation\n    py.test -m file_operation\n\n    # skip tests that use ftp (do this when testing locally)\n    py.test -m "not ftp"\n',
    'author': '4DN-DCIC Team',
    'author_email': 'support@4dnucleome.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/4dn-dcic/Submit4DN',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<3.10',
}


setup(**setup_kwargs)
