from distutils.core import setup
setup(
  name = 'AESRLib',
  packages = ['AESRLib'],
  version = 'v1.0-beta',
  license='MIT',
  description = 'Crypto package based on var key with mix of AES and Randomization',
  author = 'Shubham Chakraborty',
  author_email = 'cosmoscandium@gmail.com',
  url = 'https://github.com/me-yutakun/AESRLib',
  download_url = 'https://github.com/me-yutakun/AESRLib/archive/refs/tags/v1.0-beta.tar.gz',
  keywords = ['AES', 'Random', 'base64'],
  install_requires=[
          'pycryptodome',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.10',
  ],
)