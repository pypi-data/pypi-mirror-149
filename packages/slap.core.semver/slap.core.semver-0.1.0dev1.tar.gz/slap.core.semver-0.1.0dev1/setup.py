# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['semver']

package_data = \
{'': ['*']}

install_requires = \
['packaging>=21.3,<22.0']

setup_kwargs = {
    'name': 'slap.core.semver',
    'version': '0.1.0dev1',
    'description': 'Provides a semver specifier to represent version constraints compatible with `packaging`.',
    'long_description': '# slap.core.semver\n\nA semver version constraint specifier compatible with [`packaging`][0].\n\n  [0]: https://packaging.pypa.io/\n  [1]: https://docs.npmjs.com/about-semantic-versioning#using-semantic-versioning-to-specify-update-types-your-package-can-accept\n\n## Usage\n\n```py\nfrom slap.core.semver.specifier import SemverSpecifier\n\nspec = SemverSpecifier(\'1.x\')\nassert str(spec.version_selector.canonical) == "^1.0.0"\nassert spec.contains("1.2.3")\nassert not spec.contains("0.3.0")\n```\n\nThe `SemverSpecifier` constructor will raise `packaging.specifier.InvalidSpecifier` if the\nspecifier string cannot be parsed.\n\n## Behaviour\n\nThe version ranges supported by `SemverSpecifier` are [inspired by NPM][1]. Below is a table to\nillustrate the behaviour:\n\n| Release | Example |\n| ------- | ------- |\n| Patch release | `1.0`, `1.0.x`, `~1.0.4` |\n| Minor release | `1.0`, `1.x`, `^1.0.4` |\n| Major release | `*` or `x` |\n| Other | `x.0.4` |\n\nIn addition to the NPM semver version ranges, Python version epochs, pre releases, post releases,\ndev releases and local versions are supported. To list some examples: `2!^1.0.4`, `~1.0.3.post1`,\n`^1.0.4.dev1+gdeadbeef`.\n\n> Note: The remainder fields are not supported in the `x` placeholder format.\n\n## Compatibility\n\nRequires Python 3.6 or higher.\n',
    'author': 'Niklas Rosenstein',
    'author_email': 'rosensteinniklas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
