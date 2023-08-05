from setuptools import setup, find_packages

setup(name="ApplicationClientServer_client",
      version="0.1",
      description="applicationclientserver_client",
      author="Larisa Polozova",
      author_email="larolimp@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']

      )
