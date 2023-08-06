# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_wordle']

package_data = \
{'': ['*'], 'nonebot_plugin_wordle': ['resources/fonts/*', 'resources/words/*']}

install_requires = \
['Pillow>=8.0.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot2>=2.0.0-beta.1,<3.0.0',
 'pyenchant>=3.2.2,<4.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-wordle',
    'version': '0.1.7',
    'description': 'Nonebot2 wordle猜单词插件',
    'long_description': '# nonebot-plugin-wordle\n\n适用于 [Nonebot2](https://github.com/nonebot/nonebot2) 的 wordle 猜单词插件\n\n\n### 安装\n\n- 使用 nb-cli\n\n```\nnb plugin install nonebot_plugin_wordle\n```\n\n- 使用 pip\n\n```\npip install nonebot_plugin_wordle\n```\n\n\n### 使用\n\n**以下命令需要加[命令前缀](https://v2.nonebot.dev/docs/api/config#Config-command_start) (默认为`/`)，可自行设置为空**\n\n```\n@机器人 + 猜单词\n```\n\n绿色块代表此单词中有此字母且位置正确\n\n黄色块代表此单词中有此字母，但该字母所处位置不对\n\n灰色块代表此单词中没有此字母\n\n猜出单词或用光次数则游戏结束\n\n可发送“结束”结束游戏；可发送“提示”查看提示\n\n可使用 -l / --length 指定单词长度，默认为 5\n\n可使用 -d / --dic 指定词典，默认为 CET4\n\n支持的词典：GRE、考研、GMAT、专四、TOEFL、SAT、专八、IELTS、CET4、CET6\n\n\n或使用 `wordle` 指令：\n\n```\nwordle [-l --length <length>] [-d --dic <dic>] [--hint] [--stop] [word]\n```\n\n\n### 示例\n\n<div align="left">\n  <img src="https://s2.loli.net/2022/03/25/nuNRBUgy8KsEjiW.png" width="400" />\n</div>\n\n\n### 特别感谢\n\n- [SAGIRI-kawaii/sagiri-bot](https://github.com/SAGIRI-kawaii/sagiri-bot) 基于Graia Ariadne和Mirai的QQ机器人 SAGIRI-BOT\n',
    'author': 'meetwq',
    'author_email': 'meetwq@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MeetWq/nonebot-plugin-wordle',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
