# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['teselagen',
 'teselagen.api',
 'teselagen.api.tests',
 'teselagen.examples',
 'teselagen.utils',
 'teselagen.utils.tests']

package_data = \
{'': ['*'],
 'teselagen.api.tests': ['test_multiomics/*'],
 'teselagen.examples': ['pytested/*']}

install_requires = \
['SecretColors>=1.2.4,<2.0.0',
 'dna_features_viewer>=3.0.3,<4.0.0',
 'openpyxl>=3.0.7,<4.0.0',
 'pytest-cov>=3.0.0,<4.0.0',
 'pytest-datadir>=1.3.1,<2.0.0',
 'pytest-notebook>=0.7.0,<0.8.0',
 'pytest-timeout>=2.0.2,<3.0.0',
 'pytest-xdist>=2.4.0,<3.0.0',
 'pytest>=6.2.5,<7.0.0',
 'requests-mock>=1.9.3,<2.0.0',
 'requests>=2.26.0,<3.0.0',
 'setuptools==58.1.0',
 'single_version>=1.5.1,<2.0.0',
 'tenacity>=8.0.0,<9.0.0']

extras_require = \
{':extra == "examples"': ['fastaparser>=1.1,<2.0',
                          'pandas>=1.1.5,<2.0.0',
                          'tqdm>=4.62.3,<5.0.0'],
 'examples': ['seaborn>=0.11.2,<0.12.0',
              'jupyter>=1.0.0,<2.0.0',
              'jupyter-console>=6.4.0,<7.0.0',
              'jupyter-contrib-nbextensions>=0.5.1,<0.6.0']}

setup_kwargs = {
    'name': 'teselagen',
    'version': '0.4.5',
    'description': 'Teselagen Biotechnology API client',
    'long_description': '# TeselaGen Python API Client\n\nThe _TeselaGen Python API Client_ runs on Python 3.\n\n**NOTE :** All the following commands are supposed to be run on the _base_ directory, unless specified.\n\n## Library Installation\n\nThis library contains the TeselaGen Python API Client.\n\nTo install it locally,\n\n1. Install it with pip\n\n    ```bash\n    pip3 install teselagen\n    ```\n\n## Examples\n\nTo be able to run the `examples`, you need to (after installing the library)\n\n1. Clone or download `teselagen/examples`\n\n1. Open any notebook in the `examples` folder with Jupyter Notebook\n\n## Use the provided environment\n\nYou can use the provided docker environment that contains a ready to use installation of all required packages to run\nthe notebooks. Here are the instructions according to your OS\n\n### Linux/MacOS\n\n1. After clone/download, run the build script with `bash build.sh`\n\n1. Run the container with `bash run.sh`\n\n1. Open your browser and set the address: `http://localhost:8888`. From there you can explore all example notebooks\n\n## Development (Linux/MacOS)\n\n### Docker environment\n\n1. Build the docker environment with command `bash build.sh`\n\n1. Run the container as a developer with the command `bash run_dev.sh`.\n  With this command the `teselagen` library will be installed in\n  [editable](https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs) mode.\n\n### Dependencies\n\n#### Install dependencies\n\nIf lock file exists (the lock file contains fixed versions of dependencies), the `poetry install` command will install\nall dependencies according to the lock file (lock file **must** be added to the repo). If the file does not exist, it\nwill generate the lock file again.\n\n#### Update dependencies\n\nUse this command if you made changes on the dependencies at the `pyproject.toml` file:\n\n```bash\npoetry update\n```\n\nIt is the equivalent to make an install after deleting the `lock` file.\n\n### Tests\n\n1. Add your credentials\n\n    To run the tests, you must create a `.credentials` file containing the test _username_ and _password_, in the\n    _root_ folder.\n\n    The content of `.credentials` file should look similar to the following:\n\n    ```JSON\n        {\n            "username" : "ReplaceWithYourUsername",\n            "password" : "ReplaceWithYourPassword"\n        }\n    ````\n\n    - **NOTE**: It should be a valid `JSON`  file. `JSON with Comments` (`JSONC` ) format is not supported.\n\n    ```diff\n    - DO NOT COMMIT THIS FILE : .credentials\n    ```\n\n1. Modify configuration\n\n    You may modify some test configuration parameters by creating a `.test_configuration` file.\n    This is a `JSON` formatted file, where you can edit the server name used for tests.\n    This file must be stored next to `.credentials` file. Here is an example\n\n    ```JSON\n    {\n      "host_url" : "https://platform.teselagen.com"\n    }\n    ```\n\n    - **NOTE**: It should be a valid `JSON`  file. `JSON with Comments` (`JSONC` ) format is not supported.\n\n1. Run the tests\n\n    ```bash\n    cd /home && python3 setup.py test\n    ```\n\n    You may use the docker environment for testing. For that, first build the environment with `bash build.sh`.\n    Then just run the container with `bash run_dev.sh`.\n    Once inside (`docker exec -ti tgclient bash`), go to `home/` and you are ready to run the test command shown above.\n\n### Publishing\n\nPublishing is limited to administrators. PyPi publishing is made by using [poetry](https://python-poetry.org/docs/).\n\nTo publish:\n\n1. Run `poetry build` from the project\'s root folder (same directory as `pyproject.toml`)\n\n1. Be sure you have set the credentials with the api token:\n\n```bash\npoetry config pypi-token.pypi <TOKEN>\n```\n\nAsk for a token to administrators if needed\n\n1. Publish (check you have set a new version tag in `pyproject.toml`):\n\n```bash\npoetry publish\n```\n\n### Notes\n\nDefault shell in `Ubuntu` is `dash`, to which `/bin/sh` is symlinked. But `dash` doesn\'t have the `pipefail` option.\nThat\'s why some of our shell scripts have the following line:\n\n```bash\n# pipefail is necessary to propagate exit codes (but it may not be supported by your shell)\nbash | set -o pipefail > /dev/null 2>&1\n```\n\nFor example, the following commands will list all options supported by `set` in each of the respective shells:\n\n```bash\nsh -c \'set -o\'\ndash -c \'set -o\'\nbash -c \'set -o\'\nzsh -c \'set -o\'\n```\n\nSo, in `Ubuntu` it may be recommended to use `bash` instead of `sh`.\n\n```bash\nbash some_shell_script.sh\n```\n\nOr, as follows:\n\n```bash\n. some_shell_script.sh\n```\n\n---\n\n<!--\n\n# apply end-of-line normalization\ngit add --renormalize .\n\n# attach to the container\ndocker exec --tty --interactive tgclient bash\n\n# go to the lib folder\ncd /home\n\n# validates the structure of the pyproject.toml file\npoetry check\n\n# list all available packages in the container\npoetry show\n# poetry show --tree\n# poetry show --outdated\n# poetry show --latest\n\n# run docstrings formatter\npython3 -m docformatter --recursive --wrap-summaries 119 --wrap-descriptions 119 --in-place .\n\n# remove unused imports\npython3 -m autoflake --verbose --remove-all-unused-imports --ignore-init-module-imports --recursive --in-place .\n\n# fix exceptions\n# python3 -m tryceratops --experimental --autofix .\n\n# autopep8\npython3 -m autopep8 \\\n         --jobs=$(nproc) \\\n         --diff \\\n         --aggressive \\\n         --aggressive \\\n         --aggressive \\\n         --aggressive \\\n         --aggressive \\\n         --experimental \\\n         --max-line-length=119 \\\n         --select=E26,E265,E266,E731,E711 \\\n         --recursive \\\n         .\n\npython3 -m autopep8 \\\n         --jobs=$(nproc) \\\n         --in-place \\\n         --aggressive \\\n         --aggressive \\\n         --aggressive \\\n         --aggressive \\\n         --aggressive \\\n         --experimental \\\n         --max-line-length=119 \\\n         --select=E26,E265,E266,E731,E711 \\\n         --recursive \\\n         .\n\n# fixit\npython3 -m fixit.cli.run_rules \\\n       --rules CollapseIsinstanceChecksRule \\\n               NoInheritFromObjectRule \\\n               NoRedundantLambdaRule \\\n               NoRedundantListComprehensionRule \\\n               ReplaceUnionWithOptionalRule \\\n               RewriteToComprehensionRule \\\n               UseIsNoneOnOptionalRule \\\n               RewriteToLiteralRule \\\n               NoRedundantArgumentsSuperRule \\\n               NoRedundantFStringRule \\\n               UseClsInClassmethodRule \\\n               UseFstringRule\n\npython3 -m fixit.cli.apply_fix \\\n       --skip-autoformatter \\\n       --rules CollapseIsinstanceChecksRule \\\n               NoInheritFromObjectRule \\\n               NoRedundantLambdaRule \\\n               NoRedundantListComprehensionRule \\\n               ReplaceUnionWithOptionalRule \\\n               RewriteToComprehensionRule \\\n               UseIsNoneOnOptionalRule \\\n               RewriteToLiteralRule \\\n               NoRedundantArgumentsSuperRule \\\n               NoRedundantFStringRule \\\n               UseClsInClassmethodRule \\\n               UseFstringRule\n\n# sort imports\npython3 -m isort --jobs=8 --color .\n\n# run code formatter\npython3 -m yapf --in-place --recursive --parallel .\n\n# run flake8\nflake8\n\n# run mypy\nmypy -p teselagen\n\n# run radon\nradon cc teselagen\n\n# run tests\npython3 setup.py test\n\n# run coverage\npytest --cov="teselagen" --cov-report term:skip-covered\n\n# run pyclean\ncd /home\npython3 -m pyclean --verbose --dry-run .\ncd /home\n\ncd /home\npython3 -m pyclean --verbose .\ncd /home\n\n# run cleanpy\ncd /home\npython3 -m cleanpy --include-builds --include-envs --include-testing --include-metadata --verbose --dry-run .\ncd /home\n\ncd /home\npython3 -m cleanpy --include-builds --include-envs --include-testing --include-metadata --verbose .\ncd /home\n\n-->\n',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TeselaGen/api-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9.6,<4.0.0',
}


setup(**setup_kwargs)
