from setuptools import setup, find_packages

setup(name="my_py_mess_server",
      version="0.0.2",
      description="my_py_mess_server",
      author="Pavel Chetverikov",
      author_email="kas62-96@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'PyQt5-tools', 'sqlalchemy', 'pycryptodome']
      )
