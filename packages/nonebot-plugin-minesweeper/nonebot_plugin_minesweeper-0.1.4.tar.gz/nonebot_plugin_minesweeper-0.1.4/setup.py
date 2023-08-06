# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_minesweeper']

package_data = \
{'': ['*'],
 'nonebot_plugin_minesweeper': ['resources/fonts/*', 'resources/skins/*']}

install_requires = \
['Pillow>=8.0.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot2>=2.0.0-beta.1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-minesweeper',
    'version': '0.1.4',
    'description': 'Nonebot2 扫雷插件',
    'long_description': '# nonebot-plugin-minesweeper\n\n适用于 [Nonebot2](https://github.com/nonebot/nonebot2) 的 扫雷插件\n\n\n### 安装\n\n- 使用 nb-cli\n\n```\nnb plugin install nonebot_plugin_minesweeper\n```\n\n- 使用 pip\n\n```\npip install nonebot_plugin_minesweeper\n```\n\n\n### 使用\n\n**以下命令需要加[命令前缀](https://v2.nonebot.dev/docs/api/config#Config-command_start) (默认为`/`)，可自行设置为空**\n\n```\n@机器人 + 扫雷 / 扫雷初级 / 扫雷中级 / 扫雷高级\n```\n\n*注：若命令前缀为空则需要 @机器人，否则可不@*\n\n可使用 -r/--row ROW 、-c/--col COL 、-n/--num NUM 自定义行列数和雷数；\n\n可使用 -s/--skin SKIN 指定皮肤，默认为 winxp；\n\n当前支持的皮肤：narkomania, mine, ocean, scratch, predator, clone, winxp, hibbeler, symbol, pacman, win98, winbw, maviz, colorsonly, icicle, mario, unknown, vista\n\n使用 挖开/open + 位置 来挖开方块，可同时指定多个位置；\n\n使用 标记/mark + 位置 来标记方块，可同时指定多个位置；\n\n位置为 字母+数字 的组合，如“A1”\n\n\n或使用 `minesweeper` 指令：\n\n```\nminesweeper [-r --row ROW] [-c --col COL] [-n --num NUM] [-s --skin SKIN] [--show] [--stop] [--open POSITIONS] [--mark POSITIONS]\n```\n\n\n### 示例\n\n<div align="left">\n  <img src="https://s2.loli.net/2022/04/05/RJtDHAcsY2j6T5p.png" width="400" />\n</div>\n\n\n### 特别感谢\n\n- [mzdluo123/MineSweeper](https://github.com/mzdluo123/MineSweeper) Mirai的扫雷小游戏\n- [Minesweeper X](http://www.curtisbright.com/msx/) A minesweeper clone with extra features\n',
    'author': 'meetwq',
    'author_email': 'meetwq@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MeetWq/nonebot-plugin-minesweeper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
