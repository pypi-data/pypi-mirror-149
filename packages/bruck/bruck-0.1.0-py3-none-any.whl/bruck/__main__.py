from bruck import interpreter

import click

BRUCK_VERSION = '0.1.0'
PACKAGE_NAME = 'bruck'
PROGRAM_NAME = 'Bruck'

def print_version(ctx, params, value):
    click.echo('Bruck %s' % BRUCK_VERSION)
    ctx.exit()

def eval(ctx, params, value):
    if not value or ctx.resilient_parsing:
        return
    bruckInterpreter = interpreter.BruckInterpreter(value)
    bruckInterpreter.exec()
    ctx.exit()

@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(BRUCK_VERSION, '-v', '--version', package_name=PACKAGE_NAME, prog_name=PROGRAM_NAME)
@click.option('-e', '--eval', callback=eval, is_eager=True, expose_value=False, help='Execute the program read from stdin instead of from file.')
@click.argument('program', type=click.File('r'))
def main(program):
    bruckInterpreter = interpreter.BruckInterpreter(program.read())
    bruckInterpreter.exec()

if __name__ == '__main__':
    main()
