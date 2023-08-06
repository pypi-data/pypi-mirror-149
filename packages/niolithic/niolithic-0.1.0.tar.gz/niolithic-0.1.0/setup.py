# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['niolithic']

package_data = \
{'': ['*']}

install_requires = \
['Markdown>=3.3.7,<4.0.0',
 'matrix-nio[e2e]>=0.19.0,<0.20.0',
 'rich>=12.3.0,<13.0.0']

setup_kwargs = {
    'name': 'niolithic',
    'version': '0.1.0',
    'description': 'A simple Matrix client library wrapped around `matrix-nio`',
    'long_description': '# Niolithic\n\nA simple Matrix client library wrapped around `matrix-nio`.\n\nIt\'s meant to ressemble the very easy to work with design of `discord.py`. The intention is to make it quicker and simpler to set up a bot regardless of your skill level. But if you want to make a full-blown application or intricate bot, you should use `matrix-nio` as it is.\n\n## Example\n\n```py\nfrom niolithic import SimpleClient\n\n\nclass MyBot(SimpleClient):\n    async def on_ready(self):\n        print(\'Bot is live!\')\n\n    async def on_message(self, room: MatrixRoom, event: RoomMessageText):\n        print(\n            f"Message received in room {room.display_name}\\n"\n            f"{room.user_name(event.sender)} | {event.body}"\n        )\n\n        command, *args = event.body.split()\n\n        if command == \'!clear\':\n            # Remove the last N messages\n            \n            if len(args) < 1:\n                await self.send_text(\n                    room.room_id,\n                    \'You need to provide the number of messages to clear out. Ex. `!clear 10`\'\n                )\n                return\n\n            limit = int(args[0]) + 1  # Plus 1 to include the command\n            \n            async for message in self.get_messages(\n                    room.room_id, (RoomMessageText,), limit=limit):\n\n                await self.redact_event(message, reason=\'Mass deletion by `!clear`\')\n\n            print(f\'{limit} messages redacted.\')\n\n\nclient = MyBot(\n    \'https://matrix.org\',       # Homeserver\n    \'@username123:matrix.org\',  # User ID\n    \'MyBot\',                    # Device name\n)\nclient.run()\n```',
    'author': 'Maximillian Strand',
    'author_email': 'maximillian.strand@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/deepadmax/niolithic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
