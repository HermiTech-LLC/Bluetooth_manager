from setuptools import setup, find_packages

# Improved handling of README file for long description
try:
    with open('README.md', 'r', encoding='utf-8') as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "A detailed description is missing. Please check the README.md file."
    print("WARNING: README.md file not found.")

# Load requirements from requirements.txt file
try:
    with open('requirements.txt', 'r', encoding='utf-8') as fh:
        requirements = fh.readlines()
except FileNotFoundError:
    requirements = []
    print("WARNING: requirements.txt file not found. Continuing without installing any dependencies.")

setup(
    name='bluetooth_manager',
    version='0.1.0',
    packages=find_packages(),
    description='A package to manage Bluetooth devices using bluetoothctl',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ant O, Greene',
    author_email='anthonygreene2007@gmail.com',
    url='https://github.com/HermiTech-LLC/Bluetooth_manager',
    install_requires=[req.strip() for req in requirements],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    license='AGPLv3',
)
