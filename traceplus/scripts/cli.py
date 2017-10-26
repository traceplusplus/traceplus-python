import click
import time
import os
import sys

@click.group()
@click.option('--bootstrap-debug/--no-bootstrap-debug', default=False, help = 'Show bootstrap debug information.')
@click.pass_context
def cli(ctx, bootstrap_debug):
    """
    The traceplus-cli helps you setup trace++ agent quickly.
    """
    ctx.obj = {'BOOTSTRAP_DEBUG': bootstrap_debug}

def log_message(text, *args, **kwargs):
    ctx = click.get_current_context()

    fg = kwargs.get('fg', None)
    if ctx.obj.get('BOOTSTRAP_DEBUG', False):
        msg = 'TracePlus-CLI: %s (%d) - %s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                                           os.getpid(), text % args)
        click.secho(text = msg, fg = fg)


def dump_sysinfo():
    log_message('sys.prefix = %r', os.path.normpath(sys.prefix))

    if hasattr(sys, 'real_prefix'):
        log_message('sys.real_prefix = %r', sys.real_prefix)

    log_message('sys.version_info = %r', sys.version_info)
    log_message('sys.platform = %r', sys.platform)
    log_message('sys.executable = %r', sys.executable)
    log_message('sys.flags = %r', sys.flags)
    log_message('sys.path = %r', sys.path)

def dump_envs():
    for key in sorted(os.environ.keys()):
        if key.startswith('TRACE_PLUS_') or key.startswith('PYTHON'):
            log_message('%s = %r', key, os.environ.get(key))
