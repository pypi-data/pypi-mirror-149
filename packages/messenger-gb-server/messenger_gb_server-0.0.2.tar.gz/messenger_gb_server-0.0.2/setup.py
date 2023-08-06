from setuptools import setup, find_packages

setup(name="messenger_gb_server",
      version="0.0.2",
      description="messenger_gb_server",
      author="Alexey Kh",
      author_email="mraxe@bk.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      scripts=['server/server_run']
      )

