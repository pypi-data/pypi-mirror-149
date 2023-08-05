from setuptools import setup, find_packages

setup(name="salmin_server",
      version="0.0.2",
      description="salmin_server",
      author="Oleg Salmin",
      author_email="olegsalmin74@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
