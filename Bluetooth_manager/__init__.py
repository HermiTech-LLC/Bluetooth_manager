from setuptools import setup, find_packages

setup(
    name='bluetooth_manager',
    version='0.1.0',
    packages=find_packages(),
    description='A package to manage Bluetooth devices using bluetoothctl',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='anthonygreene2007@gmail.com',
    url='https://github.com/LoQiseaking69/BT_manager',
    install_requires=[
        # Dependencies
    ],
    python_requires='>=3.6',
)
