from setuptools import setup, find_packages

setup(name="messenger_gb_client",
      version="0.0.1",
      description="messenger_gb_client",
      author="Alexey Kh",
      author_email="mraxe@bk.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      scripts=['client/client_run']
      )
