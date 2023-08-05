# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['innertube']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0', 'mediate>=0.1.2,<0.2.0']

setup_kwargs = {
    'name': 'innertube',
    'version': '2.0.0',
    'description': "Python Client for Google's Private InnerTube API. Works with Youtube, YouTube Music and more!",
    'long_description': '# innertube\nPython Client for Google\'s Private InnerTube API. Works with **YouTube**, **YouTube Music**, **YouTube Kids**, **YouTube Studio** and more!\n\n## About\nThis library handles low-level interactions with the underlying InnerTube API used by each of the YouTube services.\n\nHere are a few articles available online relating to the InnerTube API:\n* [Gizmodo - How Project InnerTube Helped Pull YouTube Out of the Gutter](https://gizmodo.com/how-project-innertube-helped-pull-youtube-out-of-the-gu-1704946491)\n* [Fast Company - To Take On HBO And Netflix, YouTube Had To Rewire Itself](https://www.fastcompany.com/3044995/to-take-on-hbo-and-netflix-youtube-had-to-rewire-itself)\n\n## Installation\n`innertube` uses [Poetry](https://github.com/python-poetry/poetry) under the hood and can easily be installed from source or from PyPI using *pip*.\n\n### Latest Release\n```console\npip install innertube\n```\n\n### Bleeding Edge\n```console\npip install git+https://github.com/tombulled/innertube@develop\n```\n\n## Usage\n```python\n>>> import innertube\n>>>\n>>> # Construct a client\n>>> client = innertube.InnerTube("WEB")\n>>>\n>>> # Get some data!\n>>> data = client.search(query="foo fighters")\n>>>\n>>> # Power user? No problem, dispatch requests yourself\n>>> data = client("browse", body={"browseId": "FEwhat_to_watch"})\n>>>\n>>> # The core endpoints are implemented, so the above is equivalent to:\n>>> data = client.browse("FEwhat_to_watch")\n```\n\n## Comparison with the [YouTube Data API](https://developers.google.com/youtube/v3/)\nThe InnerTube API provides access to data you can\'t get from the Data API, however it comes at somewhat of a cost *(explained below)*.\n|                                       | This Library | YouTube Data API |\n| ------------------------------------- | ------------ | ---------------- |\n| Google account required               | No           | Yes              |\n| Request limit                         | No           | Yes              |\n| Clean data                            | No           | Yes              |\n\nAs the InnerTube API is used by the variety of YouTube services and is not designed for consumption by users. Therefore, the data returned by the InnerTube API will need to be parsed and sanitised to extract data of interest.\n\n## Endpoints\nCurrently only the following core, unauthenticated endpoints are implemented:\n|                                | YouTube | YouTubeMusic | YouTubeKids | YouTubeStudio |\n| ------------------------------ | ------- | ------------ | ----------- | ------------- |\n| config                         | &check; | &check;      | &check;     | &check;       |\n| browse                         | &check; | &check;      | &check;     | &check;       |\n| player                         | &check; | &check;      | &check;     | &check;       |\n| next                           | &check; | &check;      | &check;     |               |\n| search                         | &check; | &check;      | &check;     |               |\n| guide                          | &check; | &check;      |             |               |\n| music/get_search_suggestions   |         | &check;      |             |               |\n| music/get_queue                |         | &check;      |             |               |\n\n## Authentication\nThe InnerTube API uses OAuth2, however this has not yet been implemented, therefore this library currently only provides unauthenticated API access.',
    'author': 'Tom Bulled',
    'author_email': '26026015+tombulled@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/innertube/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
