from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf8') as f:
    readme = f.read()

setup(
    name='mantrack',
    version='1.0.0',
    description='CLI program to track your favorite manga updates.',
    url='https://github.com/avidito/manga_tracker',
    author='Leonardi Fabianto',
    author_email='av.leonardif@gmail.com',

    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'beautifulsoup4',
        'requests',
        'terminaltables'
    ],
    entry_points={
        'console_scripts': [
            'mantrack = manga_tracker.scripts.cli_interface:cli',
        ],
    },
)
