from setuptools import setup, find_packages

setup(name="beksilter_messenger_server",
      version="0.0.1",
      description="Beksilter_Pyqt_Messenger_Server-side",
      author="Beksilter",
      author_email="Beksilter@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )