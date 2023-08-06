# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blint', 'blint.data', 'blint.data.annotations']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'defusedxml>=0.7.1,<0.8.0',
 'lief>=0.12.1,<0.13.0',
 'rich>=12.3.0,<13.0.0']

entry_points = \
{'console_scripts': ['blint = blint.cli:main']}

setup_kwargs = {
    'name': 'blint',
    'version': '1.0.18',
    'description': 'Linter for binary files powered by lief',
    'long_description': '# Introduction\n\n[![builds.sr.ht status](https://builds.sr.ht/~prabhu/blint.svg)](https://builds.sr.ht/~prabhu/blint?)\n\nBLint is a Binary Linter to check the security properties, and capabilities in your executables. It is powered by [lief](https://github.com/lief-project/LIEF)\n\n[![BLint Demo](https://asciinema.org/a/438138.png)](https://asciinema.org/a/438138)\n\nSupported binary formats:\n\n- ELF (GNU, musl)\n- PE (exe, dll)\n- Mach-O (x64, arm64)\n\nYou can run blint on Linux, Windows and Mac against any of these binary formats.\n\n## Motivation\n\nNowadays, vendors distribute statically linked binaries produced by golang or rust or dotnet tooling. Users are used to running antivirus and anti-malware scans while using these binaries in their local devices. Blint augments these scans by listing the technical capabilities of a binary. For example, whether the binary could use network connections, or can perform file system operations and so on.\n\nThe binary is first parsed using lief framework to identify the various properties such as functions, static, and dynamic symbols present. Thanks to YAML based [annotations](./blint/data/annotations) data, this information could be matched against capabilities and presented visually using a rich table.\n\nNOTE: The presence of capabilities doesn\'t imply that the operations are always performed by the binary. Use the output of this tool to get an idea about a binary. Also, this tool is not suitable to review malware and other heavily obfuscated binaries for obvious reasons.\n\n## Use cases\n\n- Add blint to CI/CD to inspect the final binaries to ensure code signing or authenticode is applied correctly\n- Identify interesting functions and symbols for fuzzing\n- Blint was used at [ShiftLeft](https://shiftleft.io) to review the statically linked packages and optimize the distributed cli binary\n- Quickly identify malicious binaries by looking at their capabilities (Ability to manipulate networks or drivers or kernels etc)\n\n## Installation\n\n- Install python 3.8 or 3.9\n\n```bash\npip3 install blint\n```\n\n### Single binary releases\n\nYou can download single binary builds from the [blint-bin releases](https://github.com/ngcloudsec/blint-bin/releases). These executables should work with requiring python to be installed. The macOS .pkg file is signed with a valid developer account.\n\n## Usage\n\n```bash\nusage: blint [-h] [-i SRC_DIR_IMAGE] [-o REPORTS_DIR] [--no-error] [--no-banner] [--no-reviews]\n\nLinting tool for binary files powered by lief.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -i SRC_DIR_IMAGE, --src SRC_DIR_IMAGE\n                        Source directory or container image or binary file\n  -o REPORTS_DIR, --reports REPORTS_DIR\n                        Reports directory\n  --no-error            Continue on error to prevent build from breaking\n  --no-banner           Do not display banner\n  --no-reviews          Do not perform method reviews\n  --suggest-fuzzable    Suggest functions and symbols for fuzzing based on a dictionary\n```\n\nTo test any binary including default commands\n\n```bash\nblint -i /bin/netstat -o /tmp/blint\n```\n\nUse -i to check any other binary. For eg: to check ngrok\n\n```bash\nblint -i ~/ngrok -o /tmp/blint\n```\n\nPass `--suggest-fuzzable` to get suggestions for fuzzing. A dictionary containing "common verbs" is used to identify these functions.\n\n```bash\nblint -i ~/ngrok -o /tmp/blint --suggest-fuzzable\n```\n\nPowerShell example\n\n![PowerShell](./docs/blint-powershell.jpg)\n\n## Reports\n\nBlint produces the following json artifacts in the reports directory:\n\n- blint-output.html - HTML output from the console logs\n- exename-metadata.json - Raw metadata about the parsed binary. Includes symbols, functions, and signature information\n- findings.json - Contains information from the security properties audit. Useful for CI/CD based integration\n- reviews.json - Contains information from the capability reviews. Useful for further analysis\n- fuzzables.json - Contains a suggested list of methods for fuzzing\n\n## References\n\n- [lief examples](https://github.com/lief-project/LIEF/tree/master/examples/python)\n- [checksec](https://github.com/Wenzel/checksec.py)\n',
    'author': 'Prabhu Subramanian',
    'author_email': 'prabhu@ngcloud.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.sr.ht/~prabhu/blint',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
