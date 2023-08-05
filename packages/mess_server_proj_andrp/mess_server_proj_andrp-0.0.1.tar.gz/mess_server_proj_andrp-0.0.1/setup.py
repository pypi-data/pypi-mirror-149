from setuptools import setup, find_packages

setup(name="mess_server_proj_andrp",
      version="0.0.1",
      description="mess_server_proj_andrp",
      author="Petr Andreev",
      author_email="pandreev@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
