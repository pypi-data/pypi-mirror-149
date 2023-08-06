from setuptools import setup, find_packages

classifiers = [
    'Intended Audience :: Developers',
    'Operating System :: POSIX :: Linux',
    'Operating System :: MacOS',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='zmqpubsub',
    version='0.0.1',
    description='Python package to create publishers & subscribers to send JSON payloads over ZMQ.',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Vincent Charpentier',
    author_email='vincent.charpentier@imec.be',
    license='MIT',
    classifiers=classifiers,
    keywords='zmq, publisher, subscriber',
    packages=find_packages(),
    install_requires=['zmq']
)