from setuptools import setup, find_packages

setup(name="ApplicationClientServer_server",
      version="0.1",
      description="applicationclientserver_server",
      author="Larisa Polozova",
      author_email="larolimp@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']

      )
