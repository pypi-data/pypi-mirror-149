import os
import click
from merakitools.api.server import app

@click.group()
def cli():
	""" BETA - Starts Meraki SYNC API Server Default part 8080"""
	pass


@click.command(name='start',help="BETA - Starts API Server")
@click.option('--debug/--no-debug', help="Enables Debug Mode",default=False)
@click.option('--port', help="Port to run webserver one",default=8080)
def start(debug,port):
	if debug:
		app.run(debug=True,host="0.0.0.0",port=port)
	else:
		app.run(host="0.0.0.0",port=port)


cli.add_command(start)