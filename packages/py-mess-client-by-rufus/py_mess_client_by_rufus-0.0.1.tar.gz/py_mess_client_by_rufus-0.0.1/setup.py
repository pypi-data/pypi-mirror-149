from setuptools import setup, find_packages

setup(name="py_mess_client_by_rufus",
      version="0.0.1",
      description="Mess Client",
      author="Anton",
      author_email="11@11.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
