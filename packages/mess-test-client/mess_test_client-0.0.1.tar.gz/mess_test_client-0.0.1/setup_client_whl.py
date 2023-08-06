from setuptools import setup, find_packages

setup(name="mess_test_client",
      version="0.0.1",
      description="mess_test_client",
      author="Aleksey Ovchinnikov",
      author_email="denetor89@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
