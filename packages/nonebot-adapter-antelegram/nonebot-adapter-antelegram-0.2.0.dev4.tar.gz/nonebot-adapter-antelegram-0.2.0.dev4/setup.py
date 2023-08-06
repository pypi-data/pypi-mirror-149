# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot', 'nonebot.adapters.telegram']

package_data = \
{'': ['*']}

install_requires = \
['aiocache>=0.11.1,<0.12.0', 'httpx==0.20.0', 'nonebot2>=2.0.0-beta.2,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-adapter-antelegram',
    'version': '0.2.0.dev4',
    'description': 'Another unofficial Telegram adapter for nonebot2',
    'long_description': '# nonebot-adapter-telegram\n（施工中）自己用的非官方nonebot2 telegram adapter，代码全靠糊  \n开发中代码没有经过清理和优化，不能与官方版本共存  \n当前仅支持有限类型的消息解析和发送（接受私聊/群聊文字/图片，发送私聊/群聊文字/图片/语音，入群事件）  \n如果使用webhook工作方式需要公网ip或者frp  \n演示bot[@aya_od_bot](https://t.me/aya_od_bot)  \n## 使用方法\n如果要试毒的话  \n真的要的话  \n```shell\npip install nonebot-adapter-antelegram\n```\n## 上路\n一、  \n新建项目文件夹  \n二、  \n在nonebot2的配置文件中配置以下选项  \n```shell\nbot_token=your_bot_token  #telegram bot token，需要事先申请，参考https://core.telegram.org/bots#3-how-do-i-create-a-bot\ntelegram_bot_api_server_addr=https://api.telegram.org #可选，应该大概也可以替换为反代的域名，不设置默认官方\ntelegram_bot_api_proxy=proxy_server_addr #可选，代理服务器地址\n\n#如果需要使用webhook方式接受消息，进行如下设置（推荐但是麻烦）\ndriver=~fastapi\nhost=127.0.0.1 # 配置 NoneBot 监听的 IP / 主机名  \nport=xxxxx     # 配置 NoneBot 监听的端口  \nwebhook_host=https://your_domain # 配置telegram webhook域名，由于telegram要求webhook地址必须为https，需要自行配置反向代理，也可以参考telegram文档自建本地bot api，本地api无需https  \n\n#如果需要长轮训方式接受消息，进行如下设置（推荐，长轮询比轮训接受消息更及时，资源占用更小）\ndriver=~httpx\ntelegram_polling_interval=0 #不使用轮训\ntelegram_long_polling_timeout=20 #长轮训超时时间\n\n#如果需要轮训方式接受消息，进行如下设置（不推荐，仅建议调试网络时使用）\ndriver=~httpx\ntelegram_polling_interval=5 #轮训间隔\ntelegram_long_polling_timeout=0 #不使用长轮训\n\n#注意：使用driver=~fastapi+~httpx时会使用httpx作为Driver并启动fastapi，用于需要轮训且同时启动fastapi服务器的情况\n\n```\n三、（仅使用webhook方式需要）  \n将webhook域名解析到本机，用你喜欢的方式配置反代将webhook域名的流量转发到nonebot2的监听端口（如果不使用本地bot api）  \n四、  \n开始写机器人（摸鱼）  \n\n## 已知问题（短时间内并不会解决）  \n仅支持接受有限种类的消息  \n仅支持发送有限种类的消息  \n有亿点点小bug  \n~~可能存在内存泄漏问题~~  \n\n## 最简单的例子\nbot.py\n```python\nimport nonebot\nfrom nonebot.adapters.telegram.adapter import Adapter\n\nnonebot.init()\ndriver = nonebot.get_driver()\ndriver.register_adapter(Adapter)\nnonebot.load_plugin("plugins.echo")\n\nif __name__ == "__main__":\n    nonebot.run()   \n```\nplugins/echo.py\n```python\nfrom nonebot.plugin import on_command\nfrom nonebot.adapters.telegram import Bot, MessageEvent, Message, MessageSegment\nfrom nonebot.rule import to_me\n\necho = on_command("echo",to_me())\n\n@echo.handle()\nasync def echo_escape(bot: Bot, event: MessageEvent):\n    await bot.send(event, event.get_message())\n\n#await bot.send(event, "114514") #发送文字\n#await bot.send(event, MessageSegment.photo(pic_url)) #发送图片 支持file:///，base64://，bytes，file_id，url(由Telegram服务器下载)  \n#\n```\n运行机器人，向bot私聊发送/echo 123，bot会将消息原样重新发送  \n\n\n',
    'author': 'ColdThunder11',
    'author_email': 'lslyj27761@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ColdThunder11/nonebot-adapter-telegram',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
