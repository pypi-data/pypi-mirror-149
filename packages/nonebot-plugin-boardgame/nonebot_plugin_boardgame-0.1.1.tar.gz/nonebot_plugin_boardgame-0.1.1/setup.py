# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_boardgame']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot-plugin-htmlrender>=0.0.4',
 'nonebot2>=2.0.0-beta.1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-boardgame',
    'version': '0.1.1',
    'description': '适用于 Nonebot2 的棋类游戏插件',
    'long_description': '## nonebot-plugin-boardgame\n\n适用于 [Nonebot2](https://github.com/nonebot/nonebot2) 的棋类游戏插件。\n\n抄自隔壁 koishi（：[koishi-plugin-chess](https://github.com/koishijs/koishi-plugin-chess)\n\n\n### 安装\n\n- 使用 nb-cli\n\n```\nnb plugin install nonebot_plugin_boardgame\n```\n\n- 使用 pip\n\n```\npip install nonebot_plugin_boardgame\n```\n\n\n### 使用\n\n目前支持的规则有：\n\n- 五子棋\n- 围棋（禁全同，暂时不支持点目）\n- 黑白棋\n\n**以下命令需要加[命令前缀](https://v2.nonebot.dev/docs/api/config#Config-command_start) (默认为`/`)，可自行设置为空**\n\n#### 开始和停止棋局\n\n@机器人 发送 “围棋” 或 “五子棋” 或 “黑白棋” 开始一个对应的棋局，一个群组内同时只能有一个棋局。\n\n或者使用 `boardgame` 指令：\n\n```\nboardgame --rule <rule> [--size <size>]\n```\n\n| 快捷名 | 规则名 | 默认大小 |\n|:-:|:-:|:-:|\n| 围棋 | go | 19 |\n| 五子棋 | gomoku | 15 |\n| 黑白棋 / 奥赛罗 | othello | 8 |\n\n输入 `停止下棋` 或者 `boardgame --stop` 可以停止一个正在进行的棋局。\n\n#### 落子，悔棋和跳过\n\n输入 `落子 position` 如 `落子 A1` 或者 `boardgame position` 进行下棋。\n\n当棋局开始时，第一个落子的人为先手，第二个落子的人为后手，此时棋局正式形成，其他人无法继续加入游戏。而参与游戏的两人可以依次使用“落子”指令进行游戏。\n\n输入 `悔棋` 或者 `boardgame --repent` 进行悔棋，游戏会向前倒退一步。\n\n输入 `跳过回合` 或者 `boardgame --skip` 可以跳过一个回合。\n\n输入 `查看棋局` 或者 `boardgame --view` 可以查看当前棋局。\n',
    'author': 'meetwq',
    'author_email': 'meetwq@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/noneplugin/nonebot-plugin-boardgame',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
