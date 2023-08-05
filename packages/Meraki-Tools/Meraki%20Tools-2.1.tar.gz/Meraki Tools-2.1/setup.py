
"""
setup for click
"""
from setuptools import setup,find_packages
req = ['aiohttp','async-timeout','attrs','bcolors',
'certifi','chardet','idna','meraki','multidict','requests',
'typing-extensions','urllib3','yarl','http3','click','pandas',
'tabulate','python-dateutil','automodinit','python-dotenv','wheel',"deepdiff","jsonpickle","viptela","flask","werkzeug",
       "flask-restful","flask-jwt-extended","sqlalchemy"]
setup(
    name='Meraki Tools',
    version='2.1',
    author='Josh Lipton',
    author_email='joliptn@cisco.com',
    description='Meraki Tools is a system that can either run from the CLI or as a webserver that will receive API calls to run sync functionas agains mulitapl meraki orginizations' \
                  'Please use the new enverment variable to set the config file location MERAKI_TOOLS_CONFIG=/path/to-config-file',
	packages=find_packages(),
    packages_data=['merakitools'],
    include_package_data=True,
	install_requires=[req],
    entry_points="""
        [console_scripts]
        merakitools=merakitools.cli.cli:cli
    """,
)
