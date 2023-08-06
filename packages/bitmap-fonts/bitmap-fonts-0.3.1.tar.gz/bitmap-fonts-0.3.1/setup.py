# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bitmap_fonts']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0.0,<9.0.0', 'pillow>=9.1.0,<10.0.0']

entry_points = \
{'console_scripts': ['create-font-texture = '
                     'bitmap_fonts.create_font_texture:main']}

setup_kwargs = {
    'name': 'bitmap-fonts',
    'version': '0.3.1',
    'description': 'Creation of bitmap fonts useful in OpenGL context.',
    'long_description': '## Bitmap fonts\nBitmap fonts are useful in generating text messages in OpenGL contexts. This utility allows to \nconvert a TTF font file into a bitmap font.\n\n\n## Description\nThe script `create-font-texture` should be self-explanatory.\n\n\n## Installation\n\n    pip install bitmap-fonts\n\n\n## Usage\n\n    create-font-texture UbuntuMono-Regular.ttf\n\n    font_file_name: UbuntuMono-Regular.ttf\n    size: 512\n    char_size: 32\n    ubuntumono-regular-iso-8859-1.png\n\n![](https://gitlab.com/simune/components/bitmap-fonts/-/blob/1-substitute-template-keywords/ubuntumono-regular-iso-8859-1.png "Generated png file.")\n\n## Authors and acknowledgment\nPeter Koval <koval.peter@gmail.com>\n\n## License\nMIT,\n\nthe font UbuntuMono-Regular.ttf has an Ubuntu font license 1.0\n\n## Project status\nAlready useful\n\n',
    'author': 'Simune Team',
    'author_email': 'devops@simuneatomistics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.simuneatomistics.com/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
