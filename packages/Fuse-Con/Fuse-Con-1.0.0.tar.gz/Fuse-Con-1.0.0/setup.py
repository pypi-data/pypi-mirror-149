from setuptools import setup, find_packages


setup(
    name='Fuse-Con',
    description='Fuse is a content aggregation CLI tool written in Python',
    version='v1.0.0',
    license='MIT',
    author="Eliran Turgeman",
    author_email='email@example.com',
    python_requires=">=3.7",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Eliran-Turgeman/Fuse',
    keywords='Fuse aggregation',
    install_requires=[
          'feedparser==6.0.8',
          'praw==6.4.0',
          'colorama==0.4.4'
      ],

)
