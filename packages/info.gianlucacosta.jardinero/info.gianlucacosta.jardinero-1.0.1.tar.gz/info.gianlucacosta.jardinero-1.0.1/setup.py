# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['info',
 'info.gianlucacosta.jardinero',
 'info.gianlucacosta.jardinero.dictionary',
 'info.gianlucacosta.jardinero.dictionary.sqlite',
 'info.gianlucacosta.jardinero.utils',
 'info.gianlucacosta.jardinero.websockets']

package_data = \
{'': ['*'], 'info.gianlucacosta.jardinero': ['static/*']}

install_requires = \
['Flask-SocketIO>=5.1.1,<6.0.0',
 'Flask>=2.0.3,<3.0.0',
 'eventlet>=0.33.0,<0.34.0',
 'info.gianlucacosta.wikiprism>=1.0.0,<2.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'info.gianlucacosta.jardinero',
    'version': '1.0.1',
    'description': 'Extensible web application for exploring natural languages',
    'long_description': "# Jardinero\n\n_Extensible web application for exploring natural languages_\n\n![(main page screenshot)](screenshots/main.png)\n\n## Introduction\n\n_Natural languages_ are as _sublime_ as exquisite flowers in a garden - and from such a naturalistic simile stems the name of this web application: **Jardinero**, meaning _gardener_.\n\nI definitely needed a tool to perform morphological analysis over the Spanish language - that is, I wanted to find an answer to questions like:\n\n> Why some Spanish words end with -tad, whereas others end with -dad? What are the differences between them, in terms of both morphology and cardinality?\n\nTo solve this mystery - and several more - I decided to create Jardinero, a web application extracting my compact SQLite Spanish dictionary from **Wikcionario**, ready for custom SQL queries.\n\nWhile developing the project, I felt it would be nice to extend the approach to any language, thus creating the whole open source architecture consisting of:\n\n- [Eos-core](https://github.com/giancosta86/Eos-core) - type-checked, dependency-free utility library for modern Python\n\n- [WikiPrism](https://github.com/giancosta86/WikiPrism) - library for parsing wiki pages and creating dictionaries\n\n- [Cervantes](https://github.com/giancosta86/Cervantes) - WikiPrism-based library extracting a compact Spanish dictionary from Wikcionario\n\n- **Jardinero**: hybrid Python/TypeScript web application, with a Flask backend and a React frontend communicating via websockets\n\nAs a core aspect, the architecture can be easily _extended_ by creating Python modules and packages named _linguistic modules_.\n\n## Main features\n\nJardinero's user interface enables users to:\n\n- **create a SQLite dictionary from a wiki file** - whose URL depends on the current linguistic module\n\n- **perform queries** - in SQL or even in a custom DSL - upon the internal dictionary\n\n- **re-create the dictionary**, especially when the data source gets frequent updates\n\n![(Pipeline screenshot)](screenshots/pipeline.png)\n\n## Presentation on SpeakerDeck\n\nTo explore in detail how the overall architecture works, as well as the purpose and the creation process of its components, please consult **my presentation on SpeakerDeck**: [The making of Jardinero](https://speakerdeck.com/giancosta86/the-making-of-jardinero).\n\n[![(Presentation preview)](slides/preview.png)](https://speakerdeck.com/giancosta86/the-making-of-jardinero)\n\n## Requirements\n\nJardinero requires at least **Python 3.10** - available at [Python's official website](https://www.python.org/) or via your operating system's package manager.\n\n## Installation\n\nYou can install Jardinero just like any other PyPI package for your Python distribution:\n\n```bash\npip install info.gianlucacosta.jardinero\n```\n\n## Running Jardinero\n\n1. Jardinero requires a _linguistic module_ - for example, [Cervantes](github.com/giancosta86/Cervantes/), dedicated to the Spanish language:\n\n   ```bash\n   pip install info.gianlucacosta.cervantes\n   ```\n\n1. Jardinero should preferably be run with Python's **-OO** and **-m** command-line arguments:\n\n   ```bash\n   python -OO -m info.gianlucacosta.jardinero <linguistic module>\n   ```\n\n   which, in the case of Cervantes, becomes:\n\n   ```bash\n   python -OO -m info.gianlucacosta.jardinero info.gianlucacosta.cervantes\n   ```\n\n1. Then, you can just point any browser to http://localhost:7000/\n\n## Running in developer mode\n\nBy omitting the **-OO** (and even the **-O**) flag, Jardinero will start in _developer mode_ - which enables additional aspects:\n\n- Flask running with **file watching** enabled\n\n- More fine-grained **logging**\n\n- **HTTP redirection** to the Webpack development server\n\n- Python's **\\_\\_debug\\_\\_** global variable set to **true** - for example, in this case, Cervantes downloads from localhost and not from Wikcionario's official website\n\nFor simplicity, Jardinero's TOML project includes auxiliary scripts:\n\n- Webpack's frontend development server, in watch mode:\n\n  ```bash\n  poetry run poe setup-frontend\n  ```\n\n  ```bash\n  poetry run poe start-frontend\n  ```\n\n- Python's static HTTP server, serving files from your **$HOME/Downloads** directory:\n\n  ```bash\n  poetry run poe start-static\n  ```\n\nThe above command lines can be further simplified if you add the following alias to your shell configuration - especially **.profile** for Bash:\n\n```bash\nalias poe='poetry run poe'\n```\n\nOnce the above commands have been issued, you can just start Jardinero in development mode:\n\n```bash\npython -m info.gianlucacosta.jardinero <linguistic module>\n```\n\nand finally open your browser to the usual address - http://localhost:7000/\n\n## Extending Jardinero\n\nJardinero is designed to be extensible! I created it to explore the nuances of the Spanish language, but it can support arbitrary combinations of parameters:\n\n- **source wiki URL** - provided it points to a BZ2-compressed file\n\n- **term-extraction algorithm** from each wiki page\n\n- **SQL schema** in the SQLite db\n\nIt is definitely up to your needs and creativity! 😊\n\nYour _linguistic module_ can be just a Python module (or a package) - within the current Python module search path - containing these functions:\n\n- **get_wiki_url**: a **() -> str** function returning the URL of a BZ2-compressed XML wiki file, which in turn should have the format described in [WikiPrism](https://github.com/giancosta86/WikiPrism) documentation\n\n- **extract_terms**: a **(Page) -> list\\[TTerm\\]** function, extracting a list of terms from a given wiki page\n\n- **create_sqlite_dictionary**: a **(Connection) => SqliteDictionary\\[TTerm\\]** function creating an instance of a WikiPrism **SqliteDictionary** from the given SQLite connection. In particular, _it is the Dictionary that actually responds to queries_, so you might want to design your own DSL via a custom subclass.\n\nThe exact meaning of **TTerm** depends on your linguistic model: to explore a real-world example, please refer to [Cervantes](https://github.com/giancosta86/Cervantes) - my library dedicated to the analysis of the Spanish language.\n\n## Final thoughts\n\nJardinero's core point is the web UI for creating and querying custom dictionaries, as well as its extensible engine.\n\nOf course, there are limitations: if you need advanced features like pagination, charts, and even more analysis tools, you can still run Jardinero to create your custom SQL db, that will be stored at:\n\n> $HOME/.jardinero/\\<module name\\>/dictionary.db\n\nThen, you can also use your favorite database explorer - such as the excellent, open source [DB Browser for SQLite](https://sqlitebrowser.org/).\n\n## Further references\n\n[The making of Jardinero](https://speakerdeck.com/giancosta86/the-making-of-jardinero) - _Story of a software engineer who wanted to learn Spanish_\n\n[Cervantes](https://github.com/giancosta86/Cervantes) - Extract a compact Spanish dictionary from Wikcionario, with elegance\n\n[WikiPrism](https://github.com/giancosta86/WikiPrism) - Parse wiki pages and create dictionaries, fast, with Python\n\n[Eos-core](https://github.com/giancosta86/Eos-core) - Type-checked, dependency-free utility library for modern Python\n\n## Special thanks\n\n- [Rainbow loader](https://icons8.com/preloaders/en/circular/rainbow/) from [Preloaders.net](https://icons8.com/preloaders/)\n",
    'author': 'Gianluca Costa',
    'author_email': 'gianluca@gianlucacosta.info',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/giancosta86/Jardinero',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
