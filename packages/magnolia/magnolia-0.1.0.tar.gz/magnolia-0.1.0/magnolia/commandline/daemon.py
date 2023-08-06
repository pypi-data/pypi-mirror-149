import click


@click.group(help='Daemon commands')
def daemon():
    pass


@daemon.command(name='run', help='Run the magnolia daemon')
@click.pass_context
def daemon_run(ctx):
    pass


daemon.add_command(daemon_run)
