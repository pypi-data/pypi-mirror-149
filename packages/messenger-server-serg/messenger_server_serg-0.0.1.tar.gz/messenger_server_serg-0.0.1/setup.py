from setuptools import setup, find_packages

setup(name="messenger_server_serg",
      version="0.0.1",
      description="Server",
      author="Sergei Metelskiy",
      author_email="serguchers@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
