import setuptools
import os

# with open('DESCRIPTION.txt') as file:
#     long_description = file.read()

# some more details
setuptools.setup(name="msd_ble_test",
                 version='1.0.2',
                 description='Ble Test App',
                 author='NogaCS',
                 author_email='noga@nogacs.com',
                 packages=['ble'],
                 package_dir={"ble": ""},
                 classifiers=[
                     'Development Status :: 4 - Beta',
                     'Intended Audience :: Developers',
                     'Topic :: Internet',
                     'Programming Language :: Python :: 3',
                     'Programming Language :: Python :: 3.3',
                     'Programming Language :: Python :: 3.4',
                     'Programming Language :: Python :: 3.5',
                     'Programming Language :: Python :: 3.6',
                     'Programming Language :: Python :: 3.7',
                     'Programming Language :: Python :: 3.8',
                     'Programming Language :: Python :: 3.9',
                     'Programming Language :: Python :: 3.10'

                 ],
                 install_requires=['bleak~=0.14.2'],
                 entry_points={
                     'console_scripts': [
                         'pre-build = msd_ble_test.pre_build:main',
                         'build = msd_ble_test.build:main', ],
                 }
                 )
