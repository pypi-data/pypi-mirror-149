import os

import setuptools

setuptools.setup(
    name='lingwa_demo',
    version='2019.03.31',
    keywords='demo',
    description='A demo for python packaging.',
    long_description=open(
        os.path.join(
            os.path.dirname(__file__),
            'README.md'
        )
    ).read(),
    author='LingWang',      # 替换为你的Pypi官网账户名
    author_email='lingwang@wcysite.com',  # 替换为你Pypi账户名绑定的邮箱
    packages=setuptools.find_packages(),
    license='MIT',
    install_package_data=True
)