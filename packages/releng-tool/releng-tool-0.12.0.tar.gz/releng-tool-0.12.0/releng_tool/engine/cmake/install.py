# -*- coding: utf-8 -*-
# Copyright 2018-2021 releng-tool

from releng_tool.tool.cmake import CMAKE
from releng_tool.util.io import prepare_arguments
from releng_tool.util.io import prepare_definitions
from releng_tool.util.log import err
from releng_tool.util.log import verbose
from releng_tool.util.string import expand

def install(opts):
    """
    support installation cmake projects

    With provided installation options (``RelengInstallOptions``), the
    installation stage will be processed.

    Args:
        opts: installation options

    Returns:
        ``True`` if the installation stage is completed; ``False`` otherwise
    """

    if not CMAKE.exists():
        err('unable to install package; cmake is not installed')
        return False

    # check if the no-install flag is set
    if opts._cmake_noinstall:
        verbose('configured to skip install stage for cmake')
        return True

    # default definitions
    cmake_defs = {
    }
    if opts.install_defs:
        cmake_defs.update(expand(opts.install_defs))

    # default options
    cmake_opts = {
        # build RelWithDebInfo (when using multi-configuration projects)
        '--config': 'RelWithDebInfo',
        # default install using the install target
        '--target': 'install',
    }
    if opts.install_opts:
        cmake_opts.update(expand(opts.install_opts))

    # argument building
    cmake_args = [
        '--build',
        opts.build_output_dir,
    ]
    cmake_args.extend(prepare_definitions(cmake_defs, '-D'))
    cmake_args.extend(prepare_arguments(cmake_opts))

    # prepare environment for installation request; an environment dictionary is
    # always needed to apply a custom DESTDIR during each install request
    env = expand(opts.install_env)
    if not env:
        env = {}

    # install to each destination
    for dest_dir in opts.dest_dirs:
        env['DESTDIR'] = dest_dir
        if not CMAKE.execute(cmake_args, env=env):
            err('failed to install cmake project: {}', opts.name)
            return False

    return True
