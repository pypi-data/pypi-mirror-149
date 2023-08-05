from setuptools import setup, find_packages

setup(name="aaznutii_messenger_server",
      version="0.0.1",
      description="Messenger Server",
      author="Arjanov Alexey",
      author_email="aaznutii@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
