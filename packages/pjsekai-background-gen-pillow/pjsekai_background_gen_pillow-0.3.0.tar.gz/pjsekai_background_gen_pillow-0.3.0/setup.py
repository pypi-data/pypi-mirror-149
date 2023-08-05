# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pjsekai_background_gen_pillow']

package_data = \
{'': ['*'], 'pjsekai_background_gen_pillow': ['assets/*']}

install_requires = \
['Pillow>=9.0.1,<10.0.0']

entry_points = \
{'console_scripts': ['pjbg = pjsekai_background_gen_pillow.__main__:main',
                     'pjsekai_background_gen_pillow = '
                     'pjsekai_background_gen_pillow.__main__:main']}

setup_kwargs = {
    'name': 'pjsekai-background-gen-pillow',
    'version': '0.3.0',
    'description': 'Generates PJSekai backgrounds with Pillow',
    'long_description': '# pjsekai_background_gen_pillow\n[![Python Versions](https://img.shields.io/pypi/v/pjsekai_background_gen_pillow.svg)](https://pypi.org/project/pjsekai_background_gen_pillow/)\n\nGenerates PJSekai background image from Image.\n\n## Installation\n\n```\npip install pjsekai_background_gen_pillow\n```\n\n## Example\n\n```python\nfrom PIL import Image\nimport pjsekai_background_gen_pillow as pjbg\n\ngenerator = pjbg.Generator()\ngenerator.generate(Image.open("path/to/image.png")).save("path/to/output.png")\n```\n\n## CLI\n\nYou can run `pjsekai_background_gen_pillow`, `pjbg` or `python -m pjsekai_background_gen_pillow` from command line.\n\n```\nusage: pjsekai_background_gen_pillow [-h] [-b BACKGROUND] [-f FORMAT] base output\n\nGenerates PJSekai background image from Image.\n\npositional arguments:\n  base                  Base image file path, or "-" for stdin.\n  output                Output image file path, or "-" for stdout.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -b BACKGROUND, --background BACKGROUND\n                        Background image file path.\n  -f FORMAT, --format FORMAT\n                        Output image format.\n```\n\n## API\n\n### `Generator`\n\nGenerater for background images.\n\n##### Parameters\n\nbase : PIL.Image\n\n> Base background image.\n> Defaults to Built-in background image.\n\n#### `.generate(image)`\n\nGenerate background image from source image.\n\n##### Parameters\n\nsource : PIL.Image\n\n> Source image.\n\n##### Returns\n\nPIL.Image\n\n## License\n\nThis library is licensed under GPLv3. `test.png` is licensed under CC-BY-SA 4.0.',
    'author': 'sevenc-nanashi',
    'author_email': 'sevenc-nanashi@sevenbot.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sevenc-nanashi/pjsekai_background_gen_pillow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
