# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['PicImageSearch', 'PicImageSearch.model']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0', 'lxml>=4.8.0,<5.0.0', 'pyquery>=1.4.3,<2.0.0']

setup_kwargs = {
    'name': 'picimagesearch',
    'version': '3.3.1',
    'description': 'PicImageSearch APIs for Python 3.x 适用于 Python 3 以图搜源整合API',
    'long_description': "# PicImageSearch\n![release](https://img.shields.io/github/v/release/kitUIN/PicImageSearch)\n![issues](https://img.shields.io/github/issues/kitUIN/PicImageSearch)\n![stars](https://img.shields.io/github/stars/kitUIN/PicImageSearch)\n![forks](https://img.shields.io/github/forks/kitUIN/PicImageSearch)  \n聚合识图引擎  \n整合图片识别api,用于以图搜源(以图搜图，以图搜番)，支持SauceNAO,tracemoe,iqdb,ascii2d,google(谷歌识图),baidu(百度识图),E-Hantai,ExHantai识图\n# [文档](https://www.kituin.fun/wiki/picimagesearch/)\n\n## 支持\n- [x] [SauceNAO](https://saucenao.com/)\n- [x] [TraceMoe](https://trace.moe/)\n- [x] [Iqdb](http://iqdb.org/)\n- [x] [Ascii2D](https://ascii2d.net/)\n- [x] [Google谷歌识图](https://www.google.com/imghp)  \n- [x] [BaiDu百度识图](https://graph.baidu.com/)\n- [x] [E-Hantai](https://e-hentai.org/)  \n- [x] [ExHantai](https://exhentai.org/)  \n- [x] 同步/异步\n## 简要说明\n\n详细见[文档](https://www.kituin.fun/wiki/picimagesearch/) 或者[`demo`](https://github.com/kitUIN/PicImageSearch/tree/main/demo)  \n`同步`请使用`from PicImageSearch.sync import ...`导入  \n`异步`请使用`from PicImageSearch import Network,...`导入  \n**推荐使用异步**  \n\n## 简单示例\n```python\nfrom loguru import logger\nfrom PicImageSearch.sync import SauceNAO\n\nsaucenao = SauceNAO()\nres = saucenao.search('https://pixiv.cat/77702503-1.jpg')\n# res = saucenao.search(r'C:/kitUIN/img/tinted-good.jpg') #搜索本地图片\nlogger.info(res.origin)  # 原始数据\nlogger.info(res.raw)  #\nlogger.info(res.raw[0])  #\nlogger.info(res.long_remaining)  # 99\nlogger.info(res.short_remaining)  # 3\nlogger.info(res.raw[0].thumbnail)  # 缩略图\nlogger.info(res.raw[0].similarity)  # 相似度\nlogger.info(res.raw[0].title)  # 标题\nlogger.info(res.raw[0].author)  # 作者\nlogger.info(res.raw[0].url)\n```\n\n```python\nfrom PicImageSearch import SauceNAO, Network\n\nasync with Network() as client:  # 可以设置代理 Network(proxies='http://127.0.0.1:10809')\n    saucenao = SauceNAO(client=client)  # client不能少\n    res = await saucenao.search('https://pixiv.cat/77702503-1.jpg')\n    # 下面操作与同步方法一致\n```\n### 安装\n- 此包需要 Python 3.6 或更新版本。\n- `pip install PicImageSearch`\n- 或者\n- `pip install PicImageSearch -i https://pypi.tuna.tsinghua.edu.cn/simple`\n\n",
    'author': 'kitUIN',
    'author_email': 'kulujun@gmail.com',
    'maintainer': 'kitUIN',
    'maintainer_email': 'kulujun@gmail.com',
    'url': 'https://github.com/kitUIN/PicImageSearch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
