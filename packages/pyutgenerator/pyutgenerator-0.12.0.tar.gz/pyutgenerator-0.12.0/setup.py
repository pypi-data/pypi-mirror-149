# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyutgenerator']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['pyutgen = pyutgenerator.run:main']}

setup_kwargs = {
    'name': 'pyutgenerator',
    'version': '0.12.0',
    'description': 'python ut test code generator.',
    'long_description': '#  Python UT generator\nThis tools generate automatically Python pytest Unit test code.  \nThis project uses ast module to generate.  \nEasy to make coverage test. And Easy to customize test code.\n\n### Feature\n\n* Generate unit test python file in tests package.\n* Generate pytest test function from each function.\n* Generate mock patch syntax code.\n* Generate argument syntax code to call.\n* If function has return value, create assert return.\n\n## Installation\n\n### Install pip\n\n```\npip install pyutgenerator\n```\nhttps://pypi.org/project/pyutgenerator/\n\n\n## Run tool.\n\n### Genarete test code\n\n\n```\npyutgen "Input File Name"\n```\n\nor\n\n```\npython -m pyutgenerator.run "Input File Name"\n```\n\n\n### Sample input file\n\n```\nimport os\n\n\ndef aaaaa():\n    """\n    call and return\n    """\n    return os.path.exists(\'\')\n\n```\n\n### Sample out put\n\n```\n\nimport pytest\nfrom unittest.mock import patch\nfrom unittest.mock import MagicMock\n\nfrom tests.pyutgenerator.data import pattern01\n\ndef test_aaaaa():\n    # plan\n\n    # do\n    with\\\n            patch(\'tests.pyutgenerator.data.pattern01.os.path\') as m1:\n        m1.return_value = None\n        m1.exists = MagicMock(return_value=None)\n        ret = pattern01.aaaaa()\n\n        # check\n        assert ret\n\n```\n### For the future\n\n* For Code\n    * Genarete various parameters for test.\n    * Write return check value.\n    * \'exception\' check.\n    * \'with\' description mock.\n    * Generate test data.\n    * Assertion for method call for count, parameter, throw.\n    * parameter type for str,list, obj ...\n    * Simple code analyst report. like no None check or Parameter \n    * For django\n* Customize parameter options or setting file.\n    * Exclude function mock.\n    * Source directory path. \n    * tab space num.\n* Get test data from debug. \n* able to run default generated code and pass test.\n* Full coverage.\n* web ui for test.\n\n### Prerequisites\n\nnot yet\n\n```\nnot yet\n```\n\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details\n\n## Acknowledgments\n\n* Hat tip to anyone whose code was used\n* Inspiration\n* etc\n',
    'author': 'shigeshige',
    'author_email': '5540474+shigeshige@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://py-ut-generator.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
