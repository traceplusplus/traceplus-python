"""
BSD 3-Clause License

Copyright (c) 2017, gethunter.io
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

from __future__ import absolute_import
import os

__all__ = ('VERSION', 'Tracer', 'initialize_from_module', 'initialize_from_file')

VERSION = '0.0.1'

def init_from_module(settings_module = None, ignore_errors = True):
    """
    Initialize TracerPlus's tracer based on config module.
    If the parameter is None, then use ``os.environ['TRACEPLUS_SETTINGS_MODULE']``
    initialize the tracer.

    After initialize the tracer, set this instance to opentracing.tracer as
    a global default tracer.

    >>> import traceplus

    >>> # Or specify a local config file explicitly
    >>> agent = traceplus.init_from_module(settings_module = 'traceplusapp.settings')

    :param settings_module: the tracer's local configuration module.
    :param ignore_errors: ignore startup errors
    :return: Tracer instance
    """

    from traceplus.conf import settings, ENVIRONMENT_VARIABLE

    if settings_module is None:
        config = os.environ.get(ENVIRONMENT_VARIABLE)

    return settings.initialize(settings_module, ignore_errors)

def init_from_file(settings_file = None, ignore_errors = True):
    """
    Initialize TracerPlus's tracer based on config file.
    If the parameter is None, then use ``os.environ['TRACEPLUS_SETTINGS_FILE']``
    initialize the tracer.

    After initialize the tracer, set this instance to opentracing.tracer as
    a global default tracer.

    >>> import traceplus

    >>> # Or specify a local config file explicitly
    >>> agent = traceplus.init_from_file(settings_file = 'traceplusapp.settings')

    :param settings_file: the tracer's local configuration file.
    :param ignore_errors: ignore startup errors
    :return: Tracer instance
    """
    pass
