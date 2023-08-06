from setuptools import setup, find_packages

setup(name="mess_server_8",
      version="0.0.1",
      description="mess_server_8",
      author="Aleksey Tveretin",
      author_email="g100m8888@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
