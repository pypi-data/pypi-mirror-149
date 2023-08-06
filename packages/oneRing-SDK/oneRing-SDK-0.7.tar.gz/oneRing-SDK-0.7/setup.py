from distutils.core import setup
setup(
  name = 'oneRing-SDK',
  packages = ['oneRing'],
  version = '0.7',
  license='MIT',
  description = 'SDK for a public Lord of the Rings API',
  author = 'Aaron Hesse',
  author_email = 'aaronhesse@protonmail.com',
  url = 'https://github.com/aaronhesse/oneRing-SDK',
  download_url = 'https://github.com/aaronhesse/oneRing-SDK/archive/refs/tags/v0.7.tar.gz',
  keywords = ['API', 'SDK', 'Lord of The Rings', 'oneRing'],
  install_requires = [
          'requests',
          'urllib3'
      ],
  classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)