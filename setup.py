from setuptools import setup

import sys
if sys.version_info < (3,5):
    sys.exit('Sorry, Python 3.5 or newer is required (async/await)')

setup(name='slackbot',
      version='0.2',
      description='simple slack bot',
      url='https://github.com/gdamjan/slack-bot/',
      author='gdamjan',
      author_email='gdamjan@gmail.com',
      license='MIT',
      install_requires=open('requirements.txt').readlines(),
      packages=['slackbot'],
      zip_safe=False,
      package_data={'slackbot': ['smarties.txt']},
      include_package_data=True,
      entry_points = {
        'console_scripts':
            ['slackbot=slackbot.__main__:main']
      },
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
      ]
)
