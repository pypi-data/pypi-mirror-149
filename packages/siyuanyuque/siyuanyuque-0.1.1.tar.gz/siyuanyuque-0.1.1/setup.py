# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['siyuanyuque']

package_data = \
{'': ['*']}

install_requires = \
['dynaconf>=3.1.8,<4.0.0',
 'httpx>=0.22.0,<0.23.0',
 'siyuanhelper>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['siyuanyuque = siyuanyuque.__main__:main']}

setup_kwargs = {
    'name': 'siyuanyuque',
    'version': '0.1.1',
    'description': 'Sync SiYuan with Yuque',
    'long_description': '# SiyuanYuque\n\n[Chinese Document](https://www.yuque.com/clouder0/siyuan/20210916225709-g7zckw3#533691a2)\n\nSync SiYuanNote & Yuque.\n\n- Sync Setting in doc attribute.\n- Batch Sync Via SQL\n- SiYuan Image Hosting Supported\n- Internal Link Supported\n\n## Install\n\nUse pip to install.\n\n```bash\npip install SiyuanYuque\n```\n\nExecute like this:\n\n```bash\npython -m SiyuanYuque\n```\n\nRemember to create a `sqconfig.toml` config file in the current directory.\n\n```ini\nuser_token = ""\nsiyuan_token = ""\napi_host = "https://www.yuque.com/api/v2"\nlast_sync_time = "20210915225457"\n```\n\nFill in your Yuque user_token and siyuan_token.\n\n![image](https://user-images.githubusercontent.com/41664195/133458286-41abaf7a-aab2-4c98-a758-e29f7512a8f6.png)\n\n![image](https://user-images.githubusercontent.com/41664195/133458339-69a698d8-a133-4ef8-9419-ccec7354ddc7.png)\n\n## Set Atrribute in SiyuanNote\n\nYou can only sync documents to Yuque.\n\nSet Attributes like this:\n\n![image](https://user-images.githubusercontent.com/41664195/133459061-737ca0ec-aa47-4294-b5db-4b6bb8d6a02d.png)\n\n```ini\nyuque: true\nyuque-workspace: your workspace\n```\n\nWorkspace format: `username/repo`\n\nThen run `python -m SiyuanYuque`, and check the attributes again.\n\n![image](https://user-images.githubusercontent.com/41664195/133459218-8bc181aa-2429-4075-b8b3-2b9af4f6ca7f.png)\n\nYou\'ll see `yuque-id` appended to your document\'s attributes. **Don\'t manually modify this unless you know what you are doing.**\n\nThat\'s the basic usage for the time being.\n\n**Remember not to edit the documents sync from SiYuan, as the update will be lost upon the next sync.**\n\n## Custom Sync\n\nIt is supported to sync documents by SQL.\n\nA simple example:\n\n```toml\nuser_token = ""\nsiyuan_token = ""\napi_host = "https://www.yuque.com/api/v2"\nlast_sync_time = "20210916223903"\nassets_replacement = "https://b3logfile.com/siyuan/1609132319768/assets"\n[[custom_sync]]\nsql = "select * from blocks where hpath like \'%Math/%\' and type=\'d\'"\nyuque-workspace = "clouder0/gaokao"\n```\n\nMultiple custom syncs can be defined.\n\n```toml\nuser_token = ""\nsiyuan_token = ""\napi_host = "https://www.yuque.com/api/v2"\nlast_sync_time = "20210916223903"\nassets_replacement = "https://b3logfile.com/siyuan/1609132319768/assets"\n[[custom_sync]]\nsql = "select * from blocks where hpath like \'%Math/%\' and type=\'d\'"\nyuque-workspace = "clouder0/gaokao"\n[[custom_sync]]\nsql = "select * from blocks where hpath like \'%Chinese/%\' and type=\'d\'"\nyuque-workspace = "clouder0/gaokao"\n```\n\n## More Config\n\n![image](https://user-images.githubusercontent.com/41664195/133639009-77031416-b9cd-4470-aa90-3f3ba00fbbd4.png)\n\nyuque-public: 1 for public and 0 for private.\n\nyuque-slug: the slug of the document. `https://www.yuque.com/siyuannote/docs/siyuanyuque`\n\n\n## Assets Replacement\n\nReplace the `assets` string in your markdown content to support SiYuan online image.\n\n## Internal Link\n\nSiYuan-Setting: Ref Block: Anchor Text with block URL.\n\nThis script will replace `siyuan://blocks` with `https://yuque.com/{workspace}` so that your ref blocks that have been exported and in the same workspace of yuque will be accessible.\n\n## Square Support\n\nFor yuque square, you can modify `api_host` to operate in squares.  \n\nFor example, you\'d like to sync in a square `clouder.yuque.com`, then you should change your config:\n\n```toml\napi_host = "https://clouder.yuque.com/api/v2"\n```\n\nDo bear in mind that once you decide to use a square, you can no longer stay synced with the original public `www.yuque.com`.  \nTheoretically, there exists the possibility to support both at the same time, but I haven\'t seen such demand yet.\n',
    'author': 'clouder',
    'author_email': 'clouder0@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.github.com/Clouder0/siyuanyuque',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
