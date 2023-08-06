from setuptools import setup,find_packages
import io
import re

with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

with io.open('dg_sdk/dg_client.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setup(
    name='dg_sdk',
    version=version,
    author="huifu developers",
    author_email="yingyong.wang@huifu.com",
    install_requires=['requests>=2.22.0',
                      'pycryptodome>=3.8.2',
                      'Crypto',
                      'chardet',
                      'fishbase==1.5'],
    url='https://paas.huifu.com/',
    description='汇付天下为了提高客户的接入体验，特提供封装的开发SDK，使用本SDK将极大的简化开发者的工作，开发者将无需考虑通信、签名、验签等，只需要关注业务参数的拼装',
    long_description=readme,
    packages=find_packages(),
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]

)
