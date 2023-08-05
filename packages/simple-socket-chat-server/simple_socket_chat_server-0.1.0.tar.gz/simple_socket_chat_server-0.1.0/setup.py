from setuptools import setup, find_packages

setup(name="simple_socket_chat_server",
      version="0.1.0",
      description="Simple Socket Chat Server",
      author="Ilya Zaytsev",
      author_email="intiguan@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      scripts=['server/server_run']
      )
