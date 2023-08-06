# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coveo_systools']

package_data = \
{'': ['*']}

install_requires = \
['coveo-functools>=2.0.0,<3.0.0', 'typing_extensions']

setup_kwargs = {
    'name': 'coveo-systools',
    'version': '2.0.5',
    'description': 'Filesystem, language and OS related tools.',
    'long_description': '# coveo-systools\n\nLanguage and OS related utilities.\n\n\nContent in a nutshell:\n\n- enhanced subprocess calls\n- file and app finding made easy\n- safe text write and replace-if-different\n- git-repo-root locator\n- bool platforms `if WINDOWS or LINUX or MAC or WSL:`\n\n\n# searching the filesystem\n\n```python\nimport os\nfrom coveo_systools.filesystem import find_paths, find_application, find_repo_root\n\nos.getcwd()\n# \'/code/coveo-python-oss/coveo-systools\'\n\nfind_application(\'git\')\n# WindowsPath(\'C:/Program Files/Git/cmd/git.EXE\')  # windows example for completeness\n\nfind_repo_root()\n# Path(\'/code/coveo-python-oss\')\n\nlist(find_paths(\'pyproject.toml\', search_from=find_repo_root(), in_root=True, in_children=True))\n# [Path(\'/code/coveo-python-oss/pyproject.toml\'), ...]\n```\n\n# enhanced subprocess calls\n\nAn opinionated version of `subprocess.check_call` and `subprocess.check_output`.\n\nAdds the following features:\n- command line is a variable args (instead of a list)\n- automatic conversion of output to a stripped string (instead of raw bytes)\n- automatic conversion of Path, bytes and number variables in command line\n- automatic filtering of ansi codes from the output\n- enhanced DetailedCalledProcessError on error (a subclass of the typical CalledProcessError)\n\n```python\nfrom pathlib import Path\nfrom coveo_systools.subprocess import check_call\n\ncheck_call(\'mypy\', \'--config-file\', Path(\'configs/mypy.ini\'), verbose=True)\n```\n\n\n# safe I/O, if changed\n\nGood programming practices requires files to be saved using a temporary filename and then renamed.\nThis helper takes it a step further by skipping the write operation if the content did not change: \n\n```python\nimport json\nfrom pathlib import Path\nfrom coveo_systools.filesystem import safe_text_write\n\nsafe_text_write(Path(\'./path/to/file.txt\'), json.dumps(...), only_if_changed=True)\n```\n\n\n# conditional platforms syntactic sugar\n\nReadability is important, not repeating yourself is important.\nForget about `platform.platform()` and use bools directly:\n\n```python\nfrom coveo_systools.platforms import WINDOWS, LINUX, IOS, WSL\n\nif WINDOWS or WSL:\n    print("Hello Windows!")\nelif LINUX or IOS:\n    print("Hello Unix!")\n```\n',
    'author': 'Jonathan Piché',
    'author_email': 'tools@coveo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/coveooss/coveo-python-oss/tree/main/coveo-systools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
