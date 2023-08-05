from setuptools import setup, find_packages

setup(name="mess_client_test_Ensueno",
      version="0.8.7",
      description="mess_client",
      author="Ensueno",
      author_email="inspiracion@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
