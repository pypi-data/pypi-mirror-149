# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['usernado', 'usernado.torntriplets']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.1.2,<3.0.0', 'tornado-debugger>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'usernado',
    'version': '0.2.4',
    'description': 'Usernado is a Tornado Extension to Make Life Easier.',
    'long_description': '<a id="top"></a>\n<br />\n\n<div align="center">\n  <h1>Usernado</h1>\n  <p align="center">\n    A Tornado Extension to Make Life Easier.\n    <br />\n    <a href="#"><strong>Explore the docs »</strong></a>\n    <br />\n    <br />\n    <a href="https://github.com/reganto/Usernado/tree/master/example">View Demo</a>\n    ·\n    <a href="https://github.com/reganto/Usernado/issues">Report Bug</a>\n    ·\n    <a href="https://github.com/reganto/Usernado/issues">Request Feature</a>\n  </p>\n</div>\n\n<!-- TABLE OF CONTENTS -->\n\n<details>\n  <summary>Table of Contents</summary>\n  <ol>\n    <li><a href="#why-usernado">Why Usernado</a></li>\n    <li><a href="#features">Features</a></li>\n    <li><a href="#installation">Installation</a></li>\n    <li>\n      <a href="#usage">Usage</a>\n      <ul>\n        <li><a href="#example">Example</a></li>\n        <li><a href="#resources">Resources</a></li>\n      </ul>\n    </li>\n    <li><a href="#roadmap">Roadmap</a></li>\n    <li><a href="#license">License</a></li>\n    <li><a href="#contact">Contact</a></li>\n  </ol>\n</details>\n\n<!-- Why Userndo  -->\n\n## Why Usernado\n\nI\'m using Tornado every day. I really like it. Besides of all advantages of Tornado, it\'s not a full-stack framework, and I had to put all the pieces of the puzzle together every day! So this is my attempt to follow DRY(Don\'t Repeat Yourself) principle. this is how the Usernado was born.\n\n<!-- Features -->\n\n## Features\n\n- REST support\n\n- Websocket easier than ever\n\n- ORM agnostic authentication\n\n- Humanize datetime in templates\n\n- Better exception printer thanks to [tornado-debugger](https://github.com/bhch/tornado-debugger)\n\n<!-- Getting Started -->\n\n## Installation\n\nInstall either with pip or poetry.\n\n```bash\npip install usernado\nor\npoetry add usernado\n```\n\nOr optionally you can install from github using `pip install git+https://github.com/reganto/usernado`\n\n<!-- USAGE EXAMPLES -->\n\n## Usage\n\n### Example\n\n```python\nfrom usernado import Usernado\n\n\nclass HelloHandler(Usernado.Web):\n    def get(self):\n        self.write("Hello, World!")\n```\n\nFor more examples please Check out [examples](https://github.com/reganto/Usernado/tree/master/example).\n\n### Resources\n\n- [Documentation](#)\n\n- [PyPI](https://pypi.org/project/usernado/)\n\n- [Change Log](https://github.com/reganto/Usernado/blob/master/CHANGES.md)\n\n<!-- ROADMAP -->\n\n## Roadmap\n\n- [x] Send and broadcast for websockets\n- [x] Abstracted authentication methods\n- [x] Authenticaion methods should return True/False\n- [x] Add diff_for_human (humanize) decorator\n- [x] Add api_route for API handlers\n- [x] Add username & password to test login \n- [x] Add pluralize (str_plural) uimodule\n- [ ] Add third party authentication abstract methods\n- [ ] Add pagination\n\nSee the [open issues](https://github.com/reganto/Usernado/issues) for a full list of proposed features (and known issues).\n\n<!-- LICENSE -->\n\n## License\n\nDistributed under the Apache License. See `LICENSE.txt` for more information.\n\n<!-- CONTACT -->\n\n## Contact\n\nEmail: tell.reganto[at]gmail[dotcom]\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n',
    'author': 'Reganto',
    'author_email': 'tell.reganto@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/reganto/usernado',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
