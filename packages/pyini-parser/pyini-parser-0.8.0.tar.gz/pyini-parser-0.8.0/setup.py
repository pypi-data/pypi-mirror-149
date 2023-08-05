# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyini_parser', 'pyini_parser.configure', 'pyini_parser.errors']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.1.2,<8.0.0']

setup_kwargs = {
    'name': 'pyini-parser',
    'version': '0.8.0',
    'description': '',
    'long_description': '## ini-configuration-parser\n\n## description\n<p>\n    An INI file is a configuration file for computer software that consists of a text-based content with a structure and syntax comprising key–value pairs for properties, and sections that organize the properties.[1] The name of these configuration files comes from the filename extension INI, for initialization, used in the MS-DOS operating system which popularized this method of software configuration. The format has become an informal standard in many contexts of configuration, but many applications on other operating systems use different file name extensions, such as conf and cfg.\n</p>\n\n## Getting started\n<p>Install the package</p>\n\n```bash\n$ pip install pyini-parser\n```\n\n```python\n\nfrom pyini_parser.configure.parser import ConfigParser\n\nconfig = ConfigParser()\n\nconfig["deployment"] = {\n    "domain_name": "www.example.com",\n    "secret_key": "!@#$#$#@!!",\n}\n\nconfig["database"] = {\n    "host": "localhost",\n    "port": "3306",\n    "user": "root",\n}\nconfig["email"] = {\n    "host": "smtp.gmail.com",\n    "port": "587",\n}\nconfig["devolvement"] = {\n    "api_key": "!@#$%^&*()_+",\n}\nstring_content = """\n    [deployment]\n    domain_name=www.example.com\n    secret_key=!@#$#$#@!!\n    [devolvement]\n    api_key=!@#$%^&*()_+\n"""\n\nwith open("example.ini", "w") as f:\n    config.write(f) # Check example.ini file contents\n    config.sections() # Return a list of sections\n    config.get("deployment", "domain_name") # Get the value of a key in a section\n    config.append(\'devolvement\', {\'password\':\'#%$%80@#$36415\'}) # Append a new key/value pair to section \'devolvement\'\n    config.read_from_string(string_content) # you can use this method to check if everything working well\n\n\n# Uncomment the following lines to test the read method if you have a file\n# config.read(f) # Read example.ini file contents | you must have file example.ini in the same directory\n\n```\n\n* Then you can test you\'r file with pytest test library.\n\n```bash\n    $ pytest\n```\nYou should see something like this\n`======= 11 passed in 0.08s =======`\n',
    'author': 'Mahmoud Emad',
    'author_email': 'mahmmoud.hassanein@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Mahmoud-Emad/ini-configuration-parser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
