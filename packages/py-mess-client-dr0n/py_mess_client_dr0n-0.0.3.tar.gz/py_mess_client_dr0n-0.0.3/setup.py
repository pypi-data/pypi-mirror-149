from setuptools import setup, find_packages

setup(name="py_mess_client_dr0n",
      version="0.0.3",
      description="Mess Client",
      author="Andrey Bozhkov",
      author_email="dr0nx@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
