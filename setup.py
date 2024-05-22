from setuptools import setup, find_packages

with open("README.md", "r") as f:
  description = f.read()

setup(
  name = 'pyHomie',
  packages = find_packages(),
  version = '0.0.4',
  license='MIT',
  description = 'A Python library for Homie Convention',
  author = 'Markus Schiesse',
  author_email = 'M.Schiesser@gmail.com',
  url = 'https://github.com/ms412/pyHomie',
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',
  keywords = ['mqtt', 'paho-mqtt', 'homie'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second

      ],
  classifiers =[
    'Development Status :: 3 - Alpha',
    'Environment :: Other Environment',
    'Intended Audience :: Developers',
    'Intended Audience :: Information Technology',
    'License :: Freeware',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.12',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Home Automation',
    ],
  long_description=description,
  long_description_content_type="text/markdown",
)