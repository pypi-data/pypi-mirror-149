import os
import click
from merakitools.adp.main import run_adp_sync

@click.group()
def cli():
	""" BETA - Adaptive policy cross orginaztion sync """
	pass


@click.command(name='sync',help=" BETA - Syncs Adaptive policy accorss orgs Server")
@click.option('--target', help="Comma separated list of orginaztions  namesto sync I.E. org1,org2,org3",required=True)
@click.option('--golden',help="Name of golden orginazatiopn in the meraki dashbaord",required=True)
def start(target,golden):
	run_adp_sync(target_list=target,golden_org=golden)
	


cli.add_command(start)