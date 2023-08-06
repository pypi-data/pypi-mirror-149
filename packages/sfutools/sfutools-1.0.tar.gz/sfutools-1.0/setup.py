from distutils.core import setup
from setuptools import find_packages
 
setup(name = 'sfutools',     # 包名
      version = '1.0',  # 版本号
      description = 'Some simple, fast, and useful tools help you programming(Maybe).',
      long_description = '', 
      author = 'eternalbluephy',
      author_email = '',
      url = '',
      license = '',
      install_requires = [],
      classifiers = [
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities'
      ],
      keywords = '',
      packages = find_packages('src'),  # 必填，就是包的代码主目录
      package_dir = {'':'src'},         # 必填
      include_package_data = True,
)
#!/usr/bin/env python
 