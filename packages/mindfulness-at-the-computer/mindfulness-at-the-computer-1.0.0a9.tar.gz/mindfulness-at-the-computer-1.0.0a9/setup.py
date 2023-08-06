from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
# -there's no setuptools.command.uninstall (or similar)
import os
import matc.constants

long_description_str = ""
this_dir_abs_path_str = os.path.dirname(__file__)
readme_abs_path_str = os.path.join(this_dir_abs_path_str, "README.md")


class PostDevelopCommand(develop):
    def run(self):
        develop.run(self)
        import extra_setup
        extra_setup.do_extra_setup()


class PostInstallCommand(install):
    def run(self):
        install.run(self)
        import extra_setup
        extra_setup.do_extra_setup()


try:
    with open(readme_abs_path_str, "r") as file:
        long_description_str = '\n' + file.read()
except FileNotFoundError:
    long_description_str = matc.constants.SHORT_DESCR_STR

setup(
    name=matc.constants.APPLICATION_NAME,
    version=matc.constants.APPLICATION_VERSION,
    packages=['matc', 'matc.gui'],
    url="https://mindfulness-at-the-computer.gitlab.io",
    license='GPLv3',
    author='Tord Dellsén, and others',
    author_email='tord.dellsen@gmail.com',
    description=matc.constants.SHORT_DESCR_STR,
    include_package_data=True,
    install_requires=["PyQt5>=5.15.2"],
    entry_points={"console_scripts": [f"{matc.constants.APPLICATION_NAME}=matc.main:main"]},
    long_description_content_type='text/markdown',
    long_description=long_description_str,
    python_requires='>=3.6.0',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Other/Nonlisted Topic'
    ],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand
    }
)
"""
Ubuntu versions and Python versions:
18.04 LTS: 3.6 - f-strings,
3.7 - 
20.04 LTS: 3.8 - 
21.04: 3.9 - 
22.04 - 3.10 - 

To install earlier versions:
https://www.digitalocean.com/community/questions/how-to-install-a-specific-python-version-on-ubuntu

https://www.python.org/downloads/
tar xzvf Python-3.5.0.tgz
cd Python-3.5.0
./configure
make
sudo make install
https://askubuntu.com/a/727814/360991

sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.6
https://askubuntu.com/a/682875/360991
Doesn't work for 3.6

List of classifiers:
https://pypi.org/classifiers/

"""
