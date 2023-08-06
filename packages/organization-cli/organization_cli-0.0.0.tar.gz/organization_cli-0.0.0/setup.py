from setuptools import setup, find_packages

setup(
    name = "organization_cli",
    version = '0.0.0',
    packages= find_packages(),
    install_requires= [
        'click', 'PyQt5', 'yaml','sys' , 'os' , 'sys', 'pathlib' ,'QtGui'
    ],
    entry_points = '''
    [console_scripts]
    '''
)