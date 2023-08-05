import asyncio
import click
from merakitools.main import run
from merakitools import const

@click.group()
def cli():
    """ Tasks to start configuration of Meraki Devices by tag based on golden configurations """
    pass


@click.command(name="port-config",help='Meraki Switch port configuration based on tag')
@click.option('-f','--configfile', help='Config File')
def port_config(configfile=None,):
    if configfile is not None:
        run(configfile, 'device_config')

cli.add_command(port_config)
