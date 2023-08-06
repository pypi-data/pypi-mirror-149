# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pywebexmessage']

package_data = \
{'': ['*'], 'pywebexmessage': ['Template/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0', 'requests>=2.27.1,<3.0.0', 'rich-click>=1.3.0,<2.0.0']

entry_points = \
{'console_scripts': ['pyYAHTS = message_room.script:run']}

setup_kwargs = {
    'name': 'pywebexmessage',
    'version': '1.0.1',
    'description': 'WebEx Bot that generates adaptive cards to a WebEx Room',
    'long_description': '# pyWebExMessage - WebEx Bot that generates adaptive cards to a WebEx Room\n\n## Examples\nRunning the Bot (Questions)\n\n![Run the bot](readme/Example001.png)\n\nOutput\n\n![Run the bot](readme/Example002.png)\n\n## Getting Started with CLUS_2022 WebEx Message Room Bot\nAs a first time speaker I thought using WebEx to expand the interactivity and longevity of my sessions I wrote this bot. I wanted to share with other Speakers in case they wanted to use it for their sessions. \n\nTo get started with CLUS_2022 WebEx Bot, follow the steps below:\n### Create A Room for Your Session\nIn WebEx create and customize a room for your session\n![Create a WebEx Space](readme/001_create_space.png)\n\n### Get a 24-hour token and Room ID\nVisit the following developer.webex.com URL to get the room ID:\n[List_Rooms](https://developer.webex.com/docs/api/v1/rooms/list\n\n#### Get a 24-hour token\nClick the copy button to obtain a 24-hour token. This token will be used to access the room. Keep it safe and secure. I recommending using environment variables to store the token so you do not have to input it everytime you run the bot.\n![Create a WebEx Space](readme/002_get_webex_token.png)\n\n#### Get the Room ID\nNext get the room ID for the room you created. You need this to pass messages into the room with the bot. You can get the room ID in the browser directly or with a tool like Postman.\n\n##### In the browser \nClick Run\n![Get Rooms - Run](readme/003_run_in_browser01.png)\n\nFind your room\n![Get Rooms - Find your Room](readme/003_run_in_browser02.png)\n##### In Postman\nAfter you have the token and Rooms URL you can use Postman to get your rooms as well. Make a new GET request to the rooms URL. Specify Bearer token as the Authorization Type and paste in your token. Save this request if you would like in a Collection for reuse. \n\n![Setup Postman](readme/004_run_in_postman01.png)\n\n![Find Your Room](readme/004_run_in_postman02.png)\n### Installing the bot\nTo install the bot there are a few simple steps:\n#### Setup a virtual environment\n##### Ubuntu Linux \n###### The following instructions are based on Windows WSL2 and Ubuntu however any flavour of Linux will work with possibly slightly different commands.\n\n##### Confirm Python 3 is installed\n\n#####\n```console\n\n$ python3 -V\nPython 3.9.10\n\n```\n\n##### Create and activate a virtual environment\n\n#####\n```console\n\n$ sudo apt install python3-venv\n$ python3 -m venv message_room\n$ source message_room/bin/activate\n(message_room)$\n\n```\n#### Install the bot\n```console\n\n(message_room)$pip install \n\n```\n### Windows\n\n#### Confirm Python 3.9 is installed\n##### [Download Python](https://python.org)\n#### Create and activate a virtual environment\n#####\n```console\n\nC:\\>python3 -m venv message_room\nC:\\>message_room\\Scripts\\activate\n(message_room) C:\\>\n\n```\n#### Install the requirements\n```console\n\n(message_room)$pip install \n\n```\n\n### Using the bot\n#### Run the bot as an interactive session\n```console\n\n(message_room)$ cd CLUS_2022\n(message_room)~/CLUS_2022$ python3 message_room.py\n\n```\n#### The form questions:\n##### Question 1 - What is the roomID?\n##### Question 2 - What is the token?\n##### Question 3 - What is the title of the session?\n##### Question 4 - What is the description of the session?\n##### Question 5 - Where is the session?\n##### Question 6 - What day is the session?\n##### Question 7 - What time is the session?\n##### Question 8 - Who are the speakers?\n##### Question 9 - URL of the session or any other URL?\n##### Question 10 - A label for the URL button?\n#### Environment variables\nEvery question can be stored as a variable in the environment. This is useful if you want to reuse the same question in multiple messages.\nexport ROOMID=<roomID>\nexport TOKEN=<token>\nexport TITLE=<title>\nexport DESCRIPTION=<description>\nexport LOCATION=<location>\nexport DATE=<date>\nexport TIME=<time>\nexport SPEAKERS=<speakers>\nexport URL=<url>\nexport URL_LABEL=<url_label>',
    'author': 'John Capobianco',
    'author_email': 'ptcapo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
