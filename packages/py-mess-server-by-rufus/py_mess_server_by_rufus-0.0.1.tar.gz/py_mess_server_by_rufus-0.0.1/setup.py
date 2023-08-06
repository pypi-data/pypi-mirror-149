from setuptools import setup, find_packages

setup(name="py_mess_server_by_rufus",
      version="0.0.1",
      description="Mess Server",
      author="Antonv",
      author_email="11@11.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      scripts=['server/server_run']
      )
