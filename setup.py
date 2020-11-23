from setuptools import setup, find_packages
import os
import re

# specify requirements of your package here
REQUIREMENTS = ['BeautifulSoup4','requests','soupsieve','urllib3','six']

setup(
    name='WebEdge',
    version='1.0.0',
    license='MIT License',
    author='MLH Fellowship Team 1',
    author_email='erbeusgriffincasper@gmail.com',
    description='Bringing Edge to your Web Performance',
    url='https://github.com/HarshCasper/WebEdge',
    install_requires=REQUIREMENTS,
    packages=find_packages(exclude = ["*.tests", "*.tests.*", "tests.*", "tests"]),
    entry_points={
        'console_scripts': [
            'webedge = webedge.webedge:main'
        ]
    }
)
