# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['py3status_github_notifications']

package_data = \
{'': ['*']}

install_requires = \
['PyGithub>=1.55,<2.0', 'PyJWT==2.2.0', 'py3status>=3.36,<4.0']

entry_points = \
{'py3status': ['module = py3status_github_notifications.github_notifications']}

setup_kwargs = {
    'name': 'py3status-github-notifications',
    'version': '0.1.4',
    'description': 'py3status module to show your Github notifications',
    'long_description': '# py3status-github-notifications\npy3status module for showing your Github notifications in i3\n\n[![Downloads](https://static.pepy.tech/personalized-badge/py3status-github-notifications?period=total&units=international_system&left_color=blue&right_color=green&left_text=Downloads)](https://pepy.tech/project/py3status-github-notifications)\n\n## Screenshot\n![Status Bar with py3status-github-notifications](https://raw.githubusercontent.com/mcgillij/py3status-github-notifications/main/images/github_notifications.png)\n![Status Bar with py3status-github-notifications red](https://raw.githubusercontent.com/mcgillij/py3status-github-notifications/main/images/notifications_red.png)\n## Prerequisites\n\n* [i3wm](https://i3wm.org/)\n* [py3status](https://github.com/ultrabug/py3status)\n* [pygithub](https://github.com/PyGithub/PyGithub)\n* Notification API token from Github\n* [Awesome Terminal Fonts](https://github.com/gabrielelana/awesome-terminal-fonts)\n\n## Getting your Notification API Token\n\nYou can get this directly on Github, by going to your own *Account settings*, *Developer Settings* and finally **Personal access tokens**.\n\nMake sure to limit the access to **ONLY** notifications.\n\n![notifications only](https://raw.githubusercontent.com/mcgillij/py3status-github-notifications/main/images/notifications_only.png)\n\n## Installation\nThere are several methods to install py3status-github-notifications.\n\nDirectly from Github using git, pip / pipenv or poetry, the AUR (Arch package).\n\n### Direct From Github\n\nInstalling directly from Github with git, means you will need to make sure you have the dependencies already installed.\n\n``` bash\ngit clone git@github.com:mcgillij/py3status-github-notifications.git\nmkdir -p ~/.i3/py3status/ && cd ~/i3/py3status/\nln -s ../../py3status-github-notifications/src/py3status_github_notifications/github_notifications.py ./\n```\nAnd down to the configuration section.\n\n### Installing with Pip, Pipenv or Poetry\n\nYou will need to install the fonts separately to get the :octocat: emoji.\n\n``` bash\npip install py3status-github-notifications\npipenv install py3status-github-notifications\npoetry add py3status-github-notifications\n```\n\n### With `yay`\n``` bash\nyay -S py3status-github-notifications\n```\n\n## Configuration\n\nOnce you have the module installed using whichever method you chose above, edit your py3status configuration and add the following options.\n\n**~/.config/i3/i3status.conf**\n\n``` bash\n...\n\norder += "github_notifications"\n\ngithub_notifications {\n    gh_token = "PASTE YOUR NOTIFICATIONS ONLY TOKEN HERE"\n    on_click 1 = "exec xdg-open https://github.com/notifications"$\n}\n...\n\n```\nAnd restart **i3** and your should be good to go.\n\n## Configuration Options\n\nYou can pass in the following configuration options:\n\n* cache_timeout # default 300\n',
    'author': 'mcgillij',
    'author_email': 'mcgillivray.jason@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mcgillij/py3status-github-notifications',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
