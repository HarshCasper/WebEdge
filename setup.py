from setuptools import setup, find_packages

with open('requirements.txt') as f:
    REQUIREMENTS = f.read().splitlines()
with open('README.md', encoding='utf8') as f:
    README = f.read()

setup(
    name='WebEdge',
    version='1.0.1',
    license='MIT License',
    author='MLH Fellowship Team 1',
    author_email='erbeusgriffincasper@gmail.com',
    description='Bringing Edge to your Web Performance',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/HarshCasper/WebEdge',
    install_requires=REQUIREMENTS,
    packages=find_packages(exclude = ["*.tests", "*.tests.*", "tests.*", "tests"]),
    entry_points={
        'console_scripts': [
            'webedge = webedge.webedge:main'
        ]
    }
)
