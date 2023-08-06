# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yte']

package_data = \
{'': ['*']}

install_requires = \
['plac>=1.3.4,<2.0.0', 'pyyaml>=6.0,<7.0']

entry_points = \
{'console_scripts': ['yte = yte:main']}

setup_kwargs = {
    'name': 'yte',
    'version': '1.2.3',
    'description': 'A YAML template engine with Python expressions',
    'long_description': '# YTE - A YAML template engine with Python expressions\n\n[![test coverage: 100%](https://img.shields.io/badge/test%20coverage-100%25-green)](https://github.com/koesterlab/yte/blob/main/pyproject.toml#L30)\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/koesterlab/yte/CI)\n![PyPI](https://img.shields.io/pypi/v/yte)\n[![Conda Recipe](https://img.shields.io/badge/recipe-yte-green.svg)](https://anaconda.org/conda-forge/yte)\n[![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/yte.svg)](https://anaconda.org/conda-forge/yte)\n[![Conda Version](https://img.shields.io/conda/vn/conda-forge/yte.svg)](https://github.com/conda-forge/yte-feedstock)\n\n\nYTE is a template engine for YAML format that utilizes the YAML structure in combination with Python expressions for enabling to dynamically build YAML documents.\n\n## Syntax\n\nThe key idea of YTE is to rely on the YAML structure to enable conditionals, loops and other arbitrary Python expressions to dynamically render YAML files.\nPython expressions are thereby declared by prepending them with a `?` anywhere in the YAML.\nAny such value will be automatically evaluated by YTE, yielding plain YAML as a result.\nImportantly, YTE templates are still valid YAML files (for YAML, the `?` expressions are just strings).\n\n### Examples\n\n#### Conditionals\n\n##### Template\n\n```yaml\n?if True:\n  foo: 1\n?elif False:\n  bar: 2\n?else:\n  bar: 1\n```\n\n##### Rendered\n\n```yaml\nfoo: 1\n```\n\n##### Template\n\n```yaml\n?if True:\n  - a\n  - b\n```\n\n##### Rendered\n\n```yaml\n- a\n- b\n```\n\n##### Template\n\n```yaml\n- foo\n- bar\n- ?if True:\n    baz\n  ?else:\n    bar\n```\n\n##### Rendered\n\n\n```yaml\n- foo\n- bar\n- baz\n```\n\n\n#### Loops\n\n##### Template\n\n```yaml\n?for i in range(2):\n  \'?f"key:{i}"\': 1  # When expressions in keys or values contain colons, they need to be additionally quoted.\n  ?if i == 1:\n      foo: true\n```\n\n##### Rendered\n\n```yaml\n"key:0": 1\n"key:1": 1\nfoo: true\n```\n\n#### Custom definitions\n\n##### Template\n\n```yaml\n  # The special keyword __definitions__ allows to define custom statements.\n  # It can be used anywhere in the YAML, also repeatedly and inside of ifs or loops\n  # with the restriction of not having duplicate __definitions__ keys on the same level.\n  __definitions__:\n    - from itertools import product\n    - someval = 2\n    - |\n      def squared(value):\n          return value ** 2\n\n  ?for item in product([1, 2], ["a", "b"]):\n    - ?f"{item}"\n\n  ?if True:\n    - ?squared(2) * someval\n    - someval: ?someval\n```\n\n##### Rendered\n\n```yaml\n- 1-a\n- 1-b\n- 2-a\n- 2-b\n- 4\n- someval: 2\n\n## Usage\n\n### Command line interface\n\nYTE comes with a command line interface.\nTo render any YTE template, just issue\n\n```bash\nyte < the-template.yaml > the-rendered-version.yaml\n```\n\n### Python API\n\nAlternatively, you can invoke YTE via its Python API:\n\n```python\nfrom yte import process_yaml\n\n# set some variables as a Python dictionary\nvariables = ...\n\n# render a string and obtain the result as a Python dict\nresult = process_yaml("""\n?for i in range(10):\n  - ?f"item-{i}"\n""", variables=variables)\n\n# render a file and obtain the result as a Python dict\nwith open("the-template.yaml", "r") as template:\n    result = process_yaml(template, variables=variables)\n\n# render a file and write the result as valid YAML\nwith open("the-template.yaml", "r") as template, open("the-rendered-version.yaml", "w") as outfile:\n    result = process_yaml(template, outfile=outfile, variables=variables)\n```\n\n## Comparison with other engines\n\nLots of template engines are available, for example the famous generic [jinja2](https://jinja.palletsprojects.com).\nThe reasons to generate a YAML specific engine are\n\n1. The YAML syntax can be exploited to simplify template expression syntax, and make it feel less foreign (i.e. fewer special characters for control flow needed) while increasing human readability.\n2. Whitespace handling (which is important with YAML since it has a semantic there) becomes unnecessary (e.g. with jinja2, some [tuning](https://radeksprta.eu/posts/control-whitespace-in-ansible-templates) is required to obtain proper YAML rendering).\n\nOf course, YTE is not the first YAML specific template engine.\nOthers include\n\n* [Yglu](https://yglu.io)\n* [Emrichen](https://github.com/con2/emrichen)\n\nThe main difference between YTE and these two is that YTE extends YAML with plain Python syntax instead of introducing another specialized language.\nOf course, the choice is also a matter of taste.\n',
    'author': 'Johannes Köster',
    'author_email': 'johannes.koester@tu-dortmund.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/koesterlab/yte',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
