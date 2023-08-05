from setuptools import setup, find_packages

setup(name="xartiou_csa_server",
      version="0.0.1",
      description="Client Server APP server_side",
      author="Ivan Xartiou",
      author_email="xartiou@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      scripts=['server/server_run']
      )