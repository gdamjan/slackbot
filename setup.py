from setuptools import setup

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
      }
)
