from setuptools import setup, find_packages

setup(name="beksilter_messenger_client",
      version="0.0.1",
      description="Beksilter_Pyqt_Messenger,
      author="Beksilter",
      author_email="Beksilter@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )