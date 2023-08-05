from setuptools import setup, find_packages

setup(name="py_mess_server_dr0n",
      version="0.0.3",
      description="Mess Server",
      author="Andrey Bozhkov",
      author_email="dr0nx@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      scripts=['server/server_run']
      )
