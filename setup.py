from setuptools import setup

setup(name='gdrive',
      version='0.1',
      description='Server-to-server easy connection to Google Drive',
      url='http://github.com/delormev/',
      author='Vincent Delorme',
      author_email='vincent.delorme@gmail.com',
      license='MIT',
      packages=['gdrive'],
      install_requires=['oauth2client','httplib2',],
      zip_safe=False)