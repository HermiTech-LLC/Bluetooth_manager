from setuptools import setup, find_packages
import os

# Improved handling of README file for long description
readme_file = 'README.md'
long_description = "A detailed description is missing. Please check the README.md file."
if os.path.exists(readme_file):
    with open(readme_file, 'r', encoding='utf-8') as fh:
        long_description = fh.read()
else:
    print("WARNING: README.md file not found.")

# Load requirements from requirements.txt file
requirements_file = 'requirements.txt'
requirements = []
if os.path.exists(requirements_file):
    with open(requirements_file, 'r', encoding='utf-8') as fh:
        requirements = [line.strip() for line in fh.readlines() if line.strip()]
else:
    print("WARNING: requirements.txt file not found. Continuing without installing any dependencies.")

setup(
    name='bluetooth_manager',
    version='0.1.0',
    packages=find_packages(),
    description='A package to manage Bluetooth devices using bluetoothctl',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ant O. Greene',
    author_email='anthonygreene2007@gmail.com',
    url='https://github.com/HermiTech-LLC/BT_manager',
    install_requires=requirements,
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
    keywords='bluetooth, bluetoothctl, device management',
    project_urls={
        'Documentation': 'https://github.com/HermiTech-LLC/BT_manager#readme',
        'Source': 'https://github.com/HermiTech-LLC/BT_manager',
        'Tracker': 'https://github.com/HermiTech-LLC/BT_manager/issues',
    },
)