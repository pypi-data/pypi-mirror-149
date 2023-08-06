# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['buildingsync_asset_extractor']

package_data = \
{'': ['*'], 'buildingsync_asset_extractor': ['config/*', 'schemas/*']}

install_requires = \
['importlib-resources>=5.7.0,<6.0.0', 'lxml==4.7.1']

setup_kwargs = {
    'name': 'buildingsync-asset-extractor',
    'version': '0.1.7',
    'description': 'BuildingSync Asset Extractor (BAE)',
    'long_description': '# BuildingSync Asset Extractor (BAE)\n\nThis package processes a BuildingSync file to extract asset information that can then be imported into SEED\n\n## Installation\n\n### Install from PyPI\n\n```bash\npip install buildingsync-asset-extractor\n```\n### Install from source\n[Poetry](https://python-poetry.org/) is required to install buildingsync-asset-extractor.\n```bash\n# Copy repo\ngit clone https://github.com/BuildingSync/BuildingSync-asset-extractor.git\n\n# install the package\ncd BuildingSync-asset-extractor\npoetry install\n\n# Test that it works, you should see a message describing the usage\npoetry run buildingsync_asset_extractor\n```\n\n## Usage\n\nBuildingSync version 2.4.0.\n\nThe pre-importer will identify assets defined in the `asset_definitions.json` file stored in the `config` directory.  There are various methods of calculating assets:\n\n1. `sqft`.  The sqft method will calculate a \'primary\' and \'secondary\' value for the asset based on the area it serves. This is calculated from the floor areas defined in each `Section` element.  `Conditioned` floor area values will be used if present; `Gross` otherwise.\n\n1. `num`. The num method will sum up all assets of the specified type and return a single overall number.\n\n1. `avg`. The avg method will return an average value for all assets of the specified type found.\n\n1. `avg_sqft`. The avg_sqft method will return a weighted average value for all assets of the specified type found based on the area they serve.\n\n1. `age_oldest` and `age_newest`. The age method will retrieve the \'YearInstalled\' element of a specified equipment type and return either the oldest or newest, as specified.\n\nTo test usage:\n\n```bash\n\tpython buildingsync_asset_extractor/main.py\n```\n\nThis will extract assets from `tests/files/testfile.xml` and save the results to `assets_output.json`\n\nThere are 2 methods of initializing the Processor: with either a filename or data\n\n```bash\nbp = BSyncProcessor(filename=filename)\n```\n\n```bash\nbp = BSyncProcessor(data=file_data)\n```\n\n## Assumptions\n1. Assuming 1 building per file\n1. Assuming sqft method uses "Conditioned" floor area for calculations. If not present, uses "Gross"\n\n## TODO\n1. thermal zones: when spaces are listed within them with spaces (or multiple thermal zones), this would change the average setpoint calculations. Is this an exception or a normal case to handle?\n\n## Assets Definitions File\n\nThis file is used to specify what assets to extract from a BuildingSync XML file. By default, the file found in `config/asset_definitions.json` is used, but a custom file can be specified with the `set_asset_defs_file` method in the `BSyncProcessor` class.\n\nThere are currently 5 types of assets that can be extracted:\n\n1. sqft: Sqft assets take into account the floor area served by a specific asset and returns \'Primary\' and \'Secondary\' values.  For example: Primary HVAC System and Secondary HVAC System.\n\n1. avg_sqft: Avg_sqft assets compute a weighted average to get the an average asset value.  For example:  Average Heating Setpoint.\n\n1. num: Num assets count the total number of the specified asset found.  For example, Total number of lighting systems.\n\n1. age_oldest and age_newest: These types return the oldest or newest asset of a specific type.  For example: Oldest Boiler.\n\nThe schema for the assets definition JSON file is in `schemas/asset_definitions_schema.json`.\n\n## Extracted Assets File\n\nThe schema for the extracted assets JSON file is in `schemas/extracted_assets_schema.json`.\n\nThis file lists the extracted assets information in name, value, units triples.  Names will match the `export_name` listed in the asset_definitions JSON file, except for assets of type \'sqft\', which will be prepended by \'Primary\' and \'Secondary\'.\n\n## Developing\n\n### Pre-commit\n\nThis project uses `pre-commit <https://pre-commit.com/>`_ to ensure code consistency.\nTo enable pre-commit on every commit run the following from the command line from within the git checkout of the\nGMT:\n\n```bash\n  pre-commit install\n```\n\nTo run pre-commit against the files without calling git commit, then run the following. This is useful when cleaning up the repo before committing.\n\n```bash\n  pre-commit run --all-files\n```\n### Testing\n\n\tpoetry run pytest\n\n## Releasing\n\n```bash\npoetry build\n\n# config and push to testpypi\npoetry config repositories.testpypi https://test.pypi.org/legacy/\npoetry publish -r testpypi\n\n# install from testpypi\npip install --index-url https://test.pypi.org/simple/ buildingsync-asset-extractor\n```\nIf everything looks good, publish to pypi:\n```bash\npoetry publish\n```\n\nIf you have environment variables setup for PYPI token username and password:\n\n```bash\npoetry publish --build --username $PYPI_USERNAME --password $PYPI_PASSWORD\n```\n',
    'author': 'Katherine Fleming',
    'author_email': 'katherine.fleming@nrel.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://buildingsync.net',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
