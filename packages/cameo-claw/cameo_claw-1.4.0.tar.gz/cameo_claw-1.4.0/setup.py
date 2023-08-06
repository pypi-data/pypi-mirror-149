from setuptools import setup

setup(
    name='cameo_claw',
    version='1.4.0',
    description='Multiprocessing download, filter, streaming. ⚡️FAST⚡️ remove pandas',
    url='https://github.com/bohachu/cameo_claw',
    author='Bowen Chiu',
    author_email='bohachu@gmail.com',
    license='BSD 2-clause',
    packages=['cameo_claw'],
    install_requires=[
        'requests',
        'polars',
        'tqdm',
        'fastapi',
        'uvicorn',
        # 'pandas==1.4.1',
        'filelock',
        'glob2',
        'Jinja2',
        'pyarrow',
        'httpx',
        # 'asyncio==3.4.3',
        'msgpack'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
