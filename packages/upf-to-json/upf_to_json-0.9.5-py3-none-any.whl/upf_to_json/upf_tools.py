import click

# from upf_to_json import upf_to_json

@click.command()
@click.argument('fname')
def info(fname):
    """"""
    print('info', fname)


@click.command()
@click.argument('fname')
def bas(fname):
    """"""
    print('bas', fname)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('infile', type=click.File(mode='r'))
@click.argument('outfile', type=click.File(mode='w'), default='-')
def convert(infile, outfile):
    """Convert UPF to json format."""
    # click.echo(click.format_filename(filename))
    print(type(infile))
    # pass


if __name__ == '__main__':
    cli()
   # info()
   # bas()
