# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tagmanager']

package_data = \
{'': ['*']}

install_requires = \
['biplist>=1.0.0,<2.0.0', 'flake8>=4.0.1,<5.0.0', 'xattr>=0.9.9,<0.10.0']

setup_kwargs = {
    'name': 'tagmanager',
    'version': '1.0.0',
    'description': 'Applies tagging to organize files.',
    'long_description': '# tagmanager\n### A Python library for tagging files.\n#### Author: Grant Savage\n## Installation\n\n```zsh\npip install tagmanager\n```\n\n## Current Package Limitations\nThis package currently works on Mac OS X 10.9 and newer. It was developed on Mac OS X 12.2\nThere is currently no functionality for Linux or Windows.\n\n## Package Structure\n```\ntagmanager\n|   README.md\n|   LICENSE\n|   .gitignore\n|   poetry.lock\n|   pyproject.toml\n|───tagmanager\n|   |   __init__.py\n|   |   tagmanager.py\n|───tests\n|   |   test_tagmanager_macOS.py\n|───docs\n|   |   Functional_Specs.md\n|   |   Design_Specs.md\n|───sample_folder\n|   |   sample_file.txt\n```\n\n## Tutorial\n\nAdd tag to file:\n\n```python\nfrom tagmanager import tag_manager as tm\n\n>> > file_location = "sample_folder/sample_file.txt"\n\n# Add tag via Tag object\n>> > tag = tm.Tag(name="green_tag", color="green")\n\n>> > tm.add_tag(tag, file_location)\n\n# Add tag via string\n>> > tm.add_tag("blue_tag\\nblue", file_location)\n\n# Add colorless tag via string\n>> > tm.add_tag("no_color_tag", file_location)\n\n# Add tag via tuple\n>> > tm.add_tag(("purple_tag", \'purple\'), file_location)\n\n# Add multiple tags via list of tuples\n>> > red_list = [(\'first_red\', \'red\'), (\'second_red\', \'red\')]\n\n>> > tm.add_tag(red_list, file_location)\n```\n\nReturn tags by file:\n\n```python\n>>> tm.get_tags(file_location)\n[Tag("blue_tag", "BLUE"), Tag("green_tag", "GREEN"), Tag("no_color_tag", "NONE"), Tag("purple_tag", "PURPLE"), Tag("first_red", "RED"), Tag("second_red", "RED")]\n```\n\nRemove tags from file:\n\n```python\n# Remove tag via Tag object\n>>> blue_tag = tm.Tag("blue_tag", "blue")\n\n>>> tm.remove_tag(blue_tag, file_location)\n\n# Remove tag via string\n>>> tm.remove_tag("green_tag\\ngreen", file_location)\n\n# Remove colorless tag via string\n>>> tm.remove_tag("no_color_tag", file_location)\n\n# Remove tag via tuple\n>>> tm.remove_tag(("purple_tag", "purple"), file_location)\n\n# Remove multiple tags via list of tuples\n>>> red_list = [(\'first_red\', \'red\'), (\'second_red\', \'red\')]\n\n>>> tm.remove_tag(red_list, file_location)\n\n# Adding one tag back to show tags were removed\n>>> tm.add_tag("new_tag", file_location)\n\n>>> tm.get_tags(file_location)\n[Tag("new_tag", "NONE")]\n\n```\n',
    'author': 'Grant Savage',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/savageGrant/tagmanager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
