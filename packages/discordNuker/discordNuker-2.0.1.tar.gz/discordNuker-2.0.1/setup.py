from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
]

setup(
    name='discordNuker',
    version='2.0.1',
    description='A Nuke library for discord.py',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='DestructiveLone',
    author_email='lambo.blac123@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='nuker',
    packages=find_packages(),
    install_requires=['requests']
)