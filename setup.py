from setuptools import setup


install_requires = [
    'celery',
    'aiofiles',
    'aiohttp',
    'vk_api',
]

setup(
    name='reedit-to-vk',
    version='0.1',
    install_requires=install_requires,
)