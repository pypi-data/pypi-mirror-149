import click as click

from transgit.exceptions import catch, TransGitError


@click.command(help="Teste")
def transgit():
    print("s")


def main():
    catch(transgit)()
