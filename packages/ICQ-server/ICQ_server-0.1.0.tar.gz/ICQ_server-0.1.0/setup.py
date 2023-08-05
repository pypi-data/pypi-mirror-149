from setuptools import setup, find_packages

setup(name='ICQ_server',
      version='0.1.0',
      description='ICQ_server',
      author='Evseev Yurii',
      author_email='mousedrw@ya.ru',
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )