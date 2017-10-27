import os
import sys
import click

from .cli import cli, log_message, dump_envs, dump_sysinfo

@cli.command()
@click.argument('args', nargs = -1)
@click.pass_context
def run(ctx, args):
    '''Execute this command line for a Python application, force the agent automatically bootstrap before your program.

    This is a shortcut method for bootstrap a python application without any manually code changes.
    '''

    log_message("TracePlus-Cli Script (%s)", __file__, fg = 'green')

    log_message('working_directory = %r', os.getcwd())
    log_message('current_command = %r', sys.argv)

    dump_sysinfo()

    # Detect module root
    from traceplus import __file__ as module_file

    module_root = os.path.dirname(module_file)
    bootstrap_root = os.path.join(module_root, 'bootstrap')

    log_message('module_root = %r', module_root)
    log_message('bootstrap_root = %r', bootstrap_root)

    # inject python path
    python_path = bootstrap_root

    if 'PYTHONPATH' in os.environ:
        path = os.environ['PYTHONPATH'].split(os.path.pathsep)
        if bootstrap_root not in path:
            python_path = "%s%s%s" % (bootstrap_root, os.path.pathsep, os.environ['PYTHONPATH'])

    os.environ['PYTHONPATH'] = python_path
    os.environ['TRACEPLUS_BOOTSTRAP_DEBUG'] = '1' if ctx.obj['BOOTSTRAP_DEBUG'] else '0'
    os.environ['TRACEPLUS_PYTHON_PREFIX'] = os.path.realpath(
            os.path.normpath(sys.prefix))
    os.environ['TRACEPLUS_PYTHON_VERSION'] = '.'.join(
            map(str, sys.version_info[:2]))

    dump_envs()

    program_exe_path = args[0]

    if not os.path.dirname(program_exe_path):
        program_search_path = os.environ.get('PATH', '').split(os.path.pathsep)
        for path in program_search_path:
            path = os.path.join(path, program_exe_path)
            if os.path.exists(path) and os.access(path, os.X_OK):
                program_exe_path = path
                break

    log_message('program_exe_path = %r', program_exe_path)
    log_message('execl_arguments = %r', (program_exe_path, ) + args)

    os.execl(program_exe_path, *args)
