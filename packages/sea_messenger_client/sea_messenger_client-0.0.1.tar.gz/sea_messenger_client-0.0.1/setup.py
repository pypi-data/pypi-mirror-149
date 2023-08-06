from setuptools import setup, find_packages

setup(name="sea_messenger_client",
      version="0.0.1",
      description="sea_messenger_client",
      author="SEugene",
      author_email="sea.05@list.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
