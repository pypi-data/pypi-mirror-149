# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chrome_local_storage']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.0,<3.0.0', 'trio-chrome-devtools-protocol>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'chrome-local-storage',
    'version': '0.5.1',
    'description': 'Interact with Google Chrome local storage',
    'long_description': '# Chrome Local Storage\n\nThis Python package makes it easy to interact with Google Chrome local storage,\neither a locally-running browser or any remote browser that supports remote\ndebugging (e.g. Chrome on Android via `adb` port forwarding).\n\n\n## Prerequisites\n\nInstallation is via `pip`:\n\n```bash\npip install chrome-local-storage\n```\n\nChrome must be running with the debugging port active for the library\nto connect. There are various methods to do this, for example, on Windows:\n\n```\nchrome.exe --remote-debugging-port=9222\n```\n\nAnd on MacOS:\n\n```\n/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222\n```\n\nThe library will also work on any mobile device that supports remote debugging on Chrome,\nFor example, on Android, use the [Android Debug Bridge](https://developer.android.com/studio/command-line/adb)\nto set up a port forward as follows:\n\n```bash\nadb forward tcp:9222 localabstract:chrome_devtools_remote\n```\n\nIn all of the above examples, the debugger will be available at `localhost:9222`\nwhich is what the library expects by default.\n\n\n## Usage\n\nBasic usage is as follows:\n\n```python3\nimport chrome_local_storage\n\nlocal_storage = chrome_local_storage.ChromeLocalStorage()\n\nlocal_storage.set(\'example.com\', \'my-key\', \'my-value\')\nvalue = local_storage.get(\'example.com\', \'my-key\')\nprint(value)\n```\n\nThe first parameter in both `get` and `set` determines the page\nwhose local storage will be used for the operation. The page must\nalready be open in the browser, and it does not have to be an exact\nmatch to the whole URL as long as it\'s unique across open pages.\n\nIn a more complex example, two constructors connect to two different\nChrome instances and copy Wordle statistics from one to the other\n(the desire to transfer my streak from one device to another was\nthe original motivation for building this library).\n\n```bash\nchrome --remote-debugging-port=9222 "https://nytimes.com/games/wordle"\nadb forward tcp:9223 localabstract:chrome_devtools_remote\n```\n\n```python3\nimport chrome_local_storage\n\nlaptop_storage = chrome_local_storage.ChromeLocalStorage(port=9222)\nphone_storage = chrome_local_storage.ChromeLocalStorage(port=9223)\n\nwordle_stats = laptop_storage.get(\'games/wordle\', \'nyt-wordle-statistics\')\nphone_storage.set(\'games/wordle\', \'nyt-wordle-statistics\', wordle_stats)\n```\n',
    'author': 'Judson Neer',
    'author_email': 'judson.neer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lordjabez/chrome-local-storage',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
