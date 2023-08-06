from distutils.core import setup
setup(
  name='gifering',
  packages=['gifering'],
  version='0.1',
  license='MIT',
  description='A cli application to convert a bunch of .webp files into .gif files',
  author='André Carvalho',
  author_email='alac1984@gmail.com',
  url='https://github.com/alac1984/gifering',
  download_url='https://github.com/alac1984/gifering/archive/refs/tags/0.1.tar.gz',
  keywords=['converter', 'webp', 'gif'],
  install_requires=[
          'pillow',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.10',
  ],
)
