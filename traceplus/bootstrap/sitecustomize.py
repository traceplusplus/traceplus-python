from __future__ import print_function, unicode_literals

import os
import time
import sys
import imp

bootstrap_debug = os.environ.get('TRACE_PLUS_BOOTSTRAP_DEBUG', 0)

def console_message(text, *args):
    if not bootstrap_debug:
        return

    text %= args
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    sys.stdout.write('TracePlus-CLI: %s (%d) - %s\n' % (timestamp, os.getpid(), text))
    sys.stdout.flush()

console_message('TracePlus Bootstrap (%s)', __file__)
console_message('working_directory = %r', os.getcwd())
console_message('sys.prefix = %r', os.path.normpath(sys.prefix))

if hasattr(sys, 'real_prefix'):
    console_message('sys.real_prefix = %r', sys.real_prefix)

console_message('sys.version_info = %r', sys.version_info)
console_message('sys.executable = %r', sys.executable)

if hasattr(sys, 'flags'):
    console_message('sys.flags = %r', sys.flags)

console_message('sys.path = %r', sys.path)

for name in sorted(os.environ.keys()):
    if name.startswith('TRACE_PLUS_') or name.startswith('PYTHON'):
        console_message('%s = %r', name, os.environ.get(name))

bootstrap_root = os.path.dirname(__file__)
module_root = os.path.dirname(os.path.dirname(bootstrap_root))

console_message('module_root = %r', module_root)
console_message('bootstrap_root = %r', bootstrap_root)

# remove bootstrap's path after load this, for load more user sitecustomize
path = list(sys.path)
if bootstrap_root in path:
    del path[path.index(bootstrap_root)]

try:
    (file, pathname, description) = imp.find_module('sitecustomize', path)
except ImportError:
    pass
else:
    console_message('sitecustomize = %r', (file, pathname, description))
    imp.load_module('sitecustomize', file, pathname, description)

expected_python_prefix = os.environ.get('TRACE_PLUS_PYTHON_PREFIX')
actual_python_prefix = os.path.realpath(os.path.normpath(sys.prefix))

console_message('expected_python_prefix = %r', expected_python_prefix)
console_message('actual_python_prefix = %r', actual_python_prefix)

expected_python_version = os.environ.get('TRACE_PLUS_PYTHON_VERSION')
actual_python_version = '.'.join(map(str, sys.version_info[:2]))

console_message('expected_python_version = %r', expected_python_version)
console_message('actual_python_version = %r', actual_python_version)

if expected_python_prefix == actual_python_prefix and expected_python_version == actual_python_version:
    console_message('initialize_agent')

    do_insert_path = module_root not in sys.path
    if do_insert_path:
        sys.path.insert(0, module_root)

    import traceplus

    console_message('agent_version = %r', traceplus.version)

    if do_insert_path:
        try:
            del sys.path[sys.path.index(module_root)]
        except Exception:
            pass

    # Finally initialize the agent.

    # traceplus.Tracer()
