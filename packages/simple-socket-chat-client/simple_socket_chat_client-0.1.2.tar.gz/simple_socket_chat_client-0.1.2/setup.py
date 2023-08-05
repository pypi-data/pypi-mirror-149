from setuptools import setup, find_packages

setup(name="simple_socket_chat_client",
      version="0.1.2",
      description="Simple Socket Chat Client",
      author="Ilya Zaytsev",
      author_email="intiguan@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
