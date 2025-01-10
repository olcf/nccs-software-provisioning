'''
OLCF Custom Spack Utilities.
============================

Custom utilities for the OLCF to manage common spack processes. This script must
be setup as a [custom extension](https://spack.readthedocs.io/en/latest/extensions.html) and invoked
as a spack subcommand.

show-env: Display the long-form concretized specs in a Spack environment lock
          file. An environment name is required if a spack environment is not
          already active.

          ```
          spack [-E env_name] olcf show-env
          ```
'''

import collections
import sys
import os
import argparse

from llnl.util import filesystem, tty

import spack
import spack.repo
import spack.config
import spack.spec
import spack.environment as ev
import spack.cmd
import spack.modules
import spack.modules.common
import spack.store

from spack.cmd.modules import check_module_set_name

description = 'Custom utilities used by the OLCF'
section = "olcf"
level = "long"

#: List of subcommands of `spack env`
subcommands = [
    ['show-env', 'show'],
    'deploy',
    'find-missing-modules',
    'find-implicit-roots',
    'mark-implicit-roots-explicit',
]

subcommand_functions = {}


def display_specs(concretized_specs):
    """Displays the list of specs returned by `Environment.concretize()`.

    Args:
        concretized_specs (list): list of specs returned by
            `Environment.concretize()`
    """

    def _tree_to_display(spec):
        format_ = '{namespace}.{name}{@version}'
        format_ += '{%compiler.name}{@compiler.version}{compiler_flags}'
        format_ += '{variants}{arch=architecture}'
        return spec.tree(
            format=format_,
            recurse_dependencies=True,
            status_fn=spack.spec.Spec.install_status,
            show_types=True,
            hashlen=7,
            hashes=True)

    for user_spec, concrete_spec in concretized_specs:
        tty.msg('Concretized {0}'.format(user_spec))
        sys.stdout.write(_tree_to_display(concrete_spec))
        print('')


class OLCFEnv(ev.Environment):
    '''Derived environment class to wrap specific methods.'''

    def _install(self, spec, **install_args):
        display_specs([spec])
        spec.package.do_install(**install_args)

        # Make sure log directory exists
        log_path = self.log_path
        filesystem.mkdirp(log_path)

        with filesystem.working_dir(self.path):
            # Link the resulting log file into logs dir
            build_log_link = os.path.join(
                log_path, '%s-%s.log' % (spec.name, spec.dag_hash(7)))
            if os.path.lexists(build_log_link):
                os.remove(build_log_link)
            os.symlink(spec.package.build_log_path, build_log_link)


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='olcf_command')

    for name in subcommands:
        if isinstance(name, (list, tuple)):
            name, aliases = name[0], name[1:]
        else:
            aliases = []

        # add commands to subcommands dict
        function_name = 'olcf_%s' % name.replace('-', '_')
        function = globals()[function_name]
        for alias in [name] + aliases:
            subcommand_functions[alias] = function

        # make a subparser and run the command's setup function on it
        setup_parser_cmd_name = 'olcf_%s_setup_parser' % name.replace('-', '_')
        setup_parser_cmd = globals()[setup_parser_cmd_name]

        subsubparser = sp.add_parser(
            name, aliases=aliases, help=setup_parser_cmd.__doc__)
        setup_parser_cmd(subsubparser)


def olcf_show_env_setup_parser(subparser):
    """Show concretized specs in the environment"""


def olcf_deploy_setup_parser(subparser):
    """Install concretized specs in the environment"""


def olcf_find_missing_modules_setup_parser(subparser):
    """Find installed packages that should - but do not - have a modulefile"""


def olcf_find_implicit_roots_setup_parser(subparser):
    """Find root specs mistakenly marked as implicit"""


def olcf_mark_implicit_roots_explicit_setup_parser(subparser):
    """Mark as explicit root specs mistakenly marked as implicit"""


def olcf(parser, args):
    """Look for a function called olcf_<name> and call it."""
    action = subcommand_functions[args.olcf_command]
    action(args)


def olcf_show_env(args):
    '''Shows the concretized specs in an environment.'''
    env = ev.active_environment()
    if not env:
        raise ev.SpackEnvironmentError('No environment found')

    concretized_specs = list(env.concretized_specs())
    display_specs(concretized_specs)


def olcf_find_missing_modules(args):
    '''Shows package builds missing a modulefile'''
    env = ev.active_environment()
    if not env:
        raise ev.SpackEnvironmentError('No environment found')

    specs = list(env.concretized_specs())

    # TODO: Take an argument for different module types
    module_type = 'lmod'

    # TODO: Take an argument for different module sets
    module_set_name = 'default'
    check_module_set_name(module_set_name)

    existing_modulefiles = []
    packages_without_modules = []
    print("Checking environment specs ...")
    for input_spec, concrete_spec in specs:
        if not concrete_spec.install_status():
            continue
        if not concrete_spec._installed_explicitly():
            continue
        try:
            print("  -", input_spec)
            existing_modulefiles.append(
                spack.modules.common.get_module(
                    module_type,
                    concrete_spec,
                    get_full_path=True,
                    module_set_name=module_set_name,
                    required=True)
            )
        except spack.modules.common.ModuleNotFoundError as e:
            packages_without_modules.append((input_spec, concrete_spec))

    existing_modulefiles = list(x for x in existing_modulefiles if x)
    print('Packages with existing modules:')
    print('\n'.join(sorted(existing_modulefiles)))
    print()
    packages_without_modules = sorted(packages_without_modules)
    hash_list = set()
    specs_without_modules = list()
    for _, concrete_spec in packages_without_modules:
        spec_hash = concrete_spec.dag_hash()
        if spec_hash not in hash_list:
            hash_list.add(concrete_spec.dag_hash())
            specs_without_modules.append(concrete_spec)

    print('Saving spec hashes to "./specs_missing_modules.txt"')
    with open("specs_missing_modules.txt", mode="w") as f:
        formatted_spec_hashes = [
            '/{0}'.format(spec.dag_hash(7)) for spec in specs_without_modules
        ]
        f.write(' '.join(formatted_spec_hashes))
    print('')

    msg = 'You are about to regenerate {types} module files for:\n'
    tty.msg(msg.format(types=module_type))
    spack.cmd.display_specs(specs_without_modules, long=True)

    answer = tty.get_yes_or_no('Do you want to proceed?')
    if not answer:
        tty.die('Module file regeneration aborted.')

    # Cycle over the module types and regenerate module files
    cls = spack.modules.module_types[module_type]

    # Skip unknown packages.
    writers = [
        cls(spec, module_set_name) for spec in specs_without_modules
        if spack.repo.path.exists(spec.name)]

    # Filter blacklisted packages early
    writers = [x for x in writers if not x.conf.blacklisted]

    # Detect name clashes in module files
    file2writer = collections.defaultdict(list)
    for item in writers:
        file2writer[item.layout.filename].append(item)

    if len(file2writer) != len(writers):
        message = 'Name clashes detected in module files:\n'
        conflict_format = '{/hash:7} {name}{@version}'
        conflict_format += '{%compiler.name}{@compiler.version}{compiler_flags}'
        conflict_format += '{variants}{arch=architecture}'
        for filename, writer_list in file2writer.items():
            if len(writer_list) > 1:
                message += '\nfile: {0}\n'.format(filename)
                for x in writer_list:
                    message += 'spec: {0}\n'.format(
                        x.spec.format(format_string=conflict_format))
        tty.error(message)
        tty.error('Operation aborted')
        raise SystemExit(1)

    if len(writers) == 0:
        msg = 'Nothing to be done for {0} module files.'
        tty.msg(msg.format(module_type))
        return
    # If we arrived here we have at least one writer
    module_type_root = writers[0].layout.dirname()

    # Proceed regenerating module files
    tty.msg('Regenerating {name} module files'.format(name=module_type))
    filesystem.mkdirp(module_type_root)

    # Dump module index after potentially removing module tree
    spack.modules.common.generate_module_index(
        module_type_root, writers, overwrite=False)
    for x in writers:
        try:
            x.write(overwrite=False)  # FIXME: could be overwrite=True, in theory
        except Exception as e:
            tty.debug(e)
            msg = 'Could not write module file [{0}]'
            tty.warn(msg.format(x.layout.filename))
            tty.warn('\t--> {0} <--'.format(str(e)))


def olcf_deploy(args):
    '''Install concretized specs in the environment.'''
    if hasattr(args, 'package') or hasattr(args, 'specfiles'):
        tty.die("olcf deploy acts on an environment, not individual packages")
    env, env_arg = None, getattr(args, 'env', None)
    if env_arg:
        if ev.exists(env_arg):
            ev.validate_env_name(env_arg)
            env = OLCFEnv(ev.root(env_arg))
        elif ev.is_env_dir(env_arg):
            env = OLCFEnv(env_arg)
        else:
            raise SpackEnvironmentError('no environment in %s' % env_arg)
    if ev._active_environment:
        env = ev._active_environment
    else:
        tty.die(
            '`spack olcf deploy` requires an environment',
            'activate an environment first:',
            '    spack env activate ENV',
            'or use:',
            '    spack -e ENV %s ...' % cmd_name)
    if env:
        if not hasattr(args, 'only_concrete'):
            # Concretize new specs
            concretized_specs = env.concretize()
            display_specs(concretized_specs)
            env.write()
        tty.msg("Installing environment %s" % env.name)
        env.install_all(args)
        return
    else:
        raise ev.SpackEnvironmentError('No environment found')


def olcf_find_implicit_roots(args, show=True):
    env = ev.active_environment()

    if not env:
        raise ev.SpackEnvironmentError('No environment found')

    tmp = []
    roots = env.concrete_roots()
    for spec in roots:
        if not spec._installed_explicitly():
            tmp.append(spec)
    if len(tmp) < 1:
        tty.msg('No root marked as implicit found')
        return False
    else:
        if show:
            spack.cmd.display_specs(tmp, long=True)
        return tmp


def olcf_mark_implicit_roots_explicit(args):
    tmp = olcf_find_implicit_roots(args, show=False)

    if tmp:
        tty.msg('You are about to mark as explicit the following root specs:\n')
        spack.cmd.display_specs(tmp, long=True)
        answer = tty.get_yes_or_no('Do you want to proceed?')
        if not answer:
            tty.die('Operation aborted.')

        for spec in tmp:
            spack.store.STORE.db.update_explicit(spec, True)
