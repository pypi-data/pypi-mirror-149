# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tickytacky']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.1.2,<3.0.0', 'Pillow>=9.1.0,<10.0.0', 'pyglet>=1.5.23,<2.0.0']

setup_kwargs = {
    'name': 'tickytacky',
    'version': '0.9.0',
    'description': 'Tickytacky pixel game maker',
    'long_description': '# Tickytacky\n\n[![tickytacky pypi shield](https://img.shields.io/pypi/v/tickytacky)](https://pypi.org/project/tickytacky/)\n\n## Description\n\nThis library aims to make it easy to make retro-style games with Pyglet.\n\n## Install from pypi\n\nCreate a virtualenvironment with python3 and install with pip:\n\n```\npip3 install tickytacky\n```\n\n## Installing with Poetry\n\nInstall poetry according to the [poetry docs](https://python-poetry.org/docs).\n\nThen, create a virtual environment with python3 and install with poetry.\n\n```\npoetry install\n```\n\n## Examples\n\nExamples can be found here, in the examples, repo:\n\n[Tickytacky Examples](https://github.com/numbertheory/tickytacky-examples)\n\n## Sprite Maker\n\nThe sprite library contains a small Flask app you can run to assist with making\nsprites.\n\nExample:\n```\npython3 tickytacky/sprite.py\n```\n\nThen open http://0.0.0.0:5000/ to start using the sprite maker.\n\n1. Select colors from the large color button. It\'s an HTML5 color selector, so it will\nuse your system\'s color picker to select any color.\n\n2. Click the "Create Color option" to add it to the palette.\n\n3. Choose that color from the palette options and draw with it. By default, the color name\nwill show as undefined, but you can change that in the text box.\n\n4. If you remove a color from the palette, all pixels with that color will also be removed.\n\n5. When done drawing, name the sprite and click the "Export" button. This will create a\nnew page which will show the JSON format for the sprite you drew.\n\n6. Copy that info into a JSON file in your game.\n',
    'author': 'JP Etcheber',
    'author_email': 'jetcheber@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
