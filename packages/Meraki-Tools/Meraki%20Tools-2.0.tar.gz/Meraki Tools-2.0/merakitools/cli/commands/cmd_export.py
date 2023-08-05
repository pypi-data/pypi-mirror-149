import os
import click
from merakitools import lib

@click.group()
def cli():
	""" Export of Cache MNET datafile to JSON Formated file """
	pass


@click.command(name='json',help="Exports MNET Files to JSON Formted")
@click.option('-i', '--cachefile', required=True,
              help='Full Path and file name to .mnet file EX: /opt/data/cache/golden/MyOrg-1223431.mnet')
@click.option('-d', '--outputdir', required=True,
              help='Output direcotry for JSON file EX: ~/output')
def exportjson(cachefile,outputdir):
	lib.dump_cache_file_to_json(cachefile,outputdir)


cli.add_command(exportjson)
