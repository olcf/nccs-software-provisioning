
Ansible Roles
=============

Documentation for NSP ansible roles.

--------------------------------------------------------------------------------

.. _files_role:

files
-----

`Description`
^^^^^^^^^^^^^

Deploys files and directories to specified locations. All of the source files should be stored in your home
directory under a folder called ``files``.

`Variables`
^^^^^^^^^^^

.. _NSP_FILES_inventory_variable:

``NSP_FILES_inventory``
"""""""""""""""""""""""

:Type: **list**

:Required: **false**

:Default: ``[]``

:Description: Mapping of file/directories and their target locations. Each entry is a dictionary that takes two keys ``src`` and ``dest``.

.. code:: yaml

    NSP_FILES_inventory:
      - src: <some file or dir in `playbook_dir`/files>
        dest: <destination on machine>

--------------------------------------------------------------------------------

.. _gcc_role:

gcc
---

`Description`
^^^^^^^^^^^^^

Installs GCC and optionally generates a module file.

`Variables`
^^^^^^^^^^^

.. _NSP_GCC_version_variable:

``NSP_GCC_version``
"""""""""""""""""""

:Type: **str**

:Required: **true**

:Description: The version to install.

.. _NSP_GCC_enabled_languages_variable:

``NSP_GCC_enabled_languages``
"""""""""""""""""""""""""""""

:Type: **list**

:Required: **false**

:Default: ``["c", "c++", "fortran"]``

:Description: The languages that the build will support.

.. _NSP_GCC_create_module_variable:

``NSP_GCC_create_module``
"""""""""""""""""""""""""

:Type: **bool**

:Required: **false**

:Default: ``true``

:Description: Toggles module generation.

.. _NSP_GCC_clear_source_variable:

``NSP_GCC_clear_source``
""""""""""""""""""""""""

:Type: **bool**

:Required: **false**

:Default: ``true``

:Description: Clear previous build source files.

--------------------------------------------------------------------------------

.. _init_role:

init
----

`Description`
^^^^^^^^^^^^^

The init role initializes the system init scripts and adds your content to them.
To add contents, create a directory called ``init`` in the directory that contains your playbook.
In the ``init`` directory create the files ``profile.j2`` and ``cshrc.j2`` with your desired content.

.. note::

   The ``init`` directory and accompanying files are completely optional. Without them, blank init script
   will be created.

`Variables`
^^^^^^^^^^^

.. _NSP_INIT_wipe_variable:

``NSP_INIT_wipe``
"""""""""""""""""

:Type: **bool**

:Required: **false**

:Default: ``false``

:Description: Wipe and recreate the init scripts on every run.

--------------------------------------------------------------------------------

.. _llvm_role:

llvm
----

`Description`
^^^^^^^^^^^^^

Installs LLVM and optionally generates a module file.

`Variables`
^^^^^^^^^^^

.. _NSP_LLVM_version_variable:

``NSP_LLVM_version``
""""""""""""""""""""

:Type: **str**

:Required: **true**

:Description: The version to install.

.. _NSP_LLVM_projects_variable:

``NSP_LLVM_projects``
"""""""""""""""""""""

:Type: **list**

:Required: **false**

:Default: ``["clang", "lld", "openmp", "compiler-rt"]``

:Description: LLVM projects to build.

.. _NSP_LLVM_runtimes_variable:

``NSP_LLVM_runtimes``
"""""""""""""""""""""

:Type: **list**

:Required: **false**

:Default: ``["libcxx", "libcxxabi", "libunwind"]``

:Description: Library runtimes to build.

.. _NSP_LLVM_create_module_variable:

``NSP_LLVM_create_module``
""""""""""""""""""""""""""

:Type: **bool**

:Required: **false**

:Default: ``true``

:Description: Toggles module generation.

.. _NSP_LLVM_clear_source_variable:

``NSP_LLVM_clear_source``
"""""""""""""""""""""""""

:Type: **bool**

:Required: **false**

:Default: ``true``

:Description: Clear previous build source files.

--------------------------------------------------------------------------------

.. _lmod_role:

lmod
----

`Description`
^^^^^^^^^^^^^

The lmod role configures and under certain circumstances installs lmod.
The main part of the configuration is a custom lmod hook that can be configured to look for modules in spack
projections and add paths to ``MODULEPATH`` when appropriate. It also supports having custom lmod
`rc.lua <https://lmod.readthedocs.io/en/latest/093_modulerc.html>`_,
`admin.list <https://lmod.readthedocs.io/en/latest/140_deprecating_modules.html>`_, and
`lmodrc.lua <https://lmod.readthedocs.io/en/latest/145_properties.html>`_ files. These files
should be placed in a directory named ``lmod`` that resides with your system playbook.

.. note::

    The ``lmod`` directory and accompanying files are completely optional. If no template files are provided
    the lmod role will skip generating them.

`Variables`
^^^^^^^^^^^

.. _NSP_LMOD_install_type_variable:

``NSP_LMOD_install_type``
"""""""""""""""""""""""""

:Type: **str**

:Required: **true**

:Allowed Values: ``["internal", "external"]``
:Description: This toggles the lmod role installing its own lmod or using an external installation.

.. _NSP_LMOD_version_variable:

``NSP_LMOD_version``
""""""""""""""""""""

:Type: **str**

:Required: **false**

:Description: The version to install (only applies if :ref:`NSP_LMOD_install_type_variable` = ``internal``).

.. _NSP_LMOD_enable_tcl_variable:

``NSP_LMOD_enable_tcl``
"""""""""""""""""""""""

:Type: **bool**

:Required: **false**

:Default: ``false``

:Description: Build support for tcl module files (only applies if :ref:`NSP_LMOD_install_type_variable` = ``internal``).

.. _NSP_LMOD_default_modules_variable:

``NSP_LMOD_default_modules``
""""""""""""""""""""""""""""

:Type: **list**

:Required: **false**

:Default: ``[]``

:Description: A list of modules to load in the ``DefApps`` module.

.. note::

    If you are installing lmod with NSP then the ``DefApps`` module will be set to load automatically.
    If you are using an external lmod installation you will have to configure loading ``DefApps`` outside
    of NSP.

.. _NSP_LMOD_default_module_paths_variable:

``NSP_LMOD_default_module_paths``
"""""""""""""""""""""""""""""""""

:Type: **list**

:Required: **false**

:Default: ``[]``

:Description: List of paths to add to ``MODULEPATH`` (only applies if :ref:`NSP_LMOD_install_type_variable` = ``internal``).

.. note::

    The path in ``NSP_module_root`` will automatically be added. So, there is no need to add it
    to ``NSP_LMOD_default_module_paths``.

.. _NSP_LMOD_spack_modules_variable:

``NSP_LMOD_spack_modules``
""""""""""""""""""""""""""

:Type: **path**

:Required: **false**

:Default: ``"{{ [NSP_SPACK_root | default([NSP_install_root, 'spack'] | path_join), 'modules'] | path_join }}"``

:Description: Path to the spack generated module files.

.. _NSP_LMOD_hierarchy_variable:

``NSP_LMOD_hierarchy``
""""""""""""""""""""""

:Type: **dict**

:Required: **false**

:Default: ``{}``

:Description: This variable holds a list of components for module projections.

For example:

.. code:: yaml

    NSP_LMOD_hierarchy:
      compiler:
        members: ['gcc', 'llvm']
        paths:
          - {path: '|compiler.name|-|compiler.version|', weight: 20}
          - {path: '|mpi.name|-|mpi.version|/|compiler.name|-|compiler.version|', weight: 30}
        level: 0
      mpi:
        members: ['openmpi', 'mpich']
        paths:
          - {path: '|mpi.name|-|mpi.version|/|compiler.name|-|compiler.version|', weight: 30}
        level: 1

Notice the two components named ``compiler`` and ``mpi``. Each component has a list of ``members``. These
members are the names of modules that belong to that component. In the module files for these members,
they should share the same ``family("...")`` so that they are mutually exclusive. For each component we
also define a list of ``paths``. These paths template the paths that the hook should add/remove from
``MODULEPATH``. Take for example the first path defined for compiler. If ``gcc/12.3.0`` were loaded then
``|compiler.name|-|compiler.version|`` would become ``gcc-12.3.0``. These paths are combined with
:ref:`NSP_LMOD_spack_modules_variable` to create the final path to add to ``MODULEPATH``. If
:ref:`NSP_LMOD_enable_spack_compiler_projections_variable` is set then additional parts are added to the path
to accommodate spack's automatic additions for compiler and version. Each path also has an associated
``weight``. The last item in each component is ``level`` which sets the order that the different component
members are printed in the lmdo header for ``module avail``.

.. _NSP_LMOD_nv_mappings_variable:

``NSP_LMOD_nv_mappings``
""""""""""""""""""""""""

:Type: **dict**

:Required: **false**

:Default: ``{}``

:Description: Converts module names to their package names in spack.

For example:

.. code:: yaml

    NSP_LMOD_nv_mappings:
        gcc-native/12.3.0: {name: 'gcc', version: '%s'} # maps to gcc/12.3.0
        # %s substitutes in the value from the system module

Sometimes, spack uses a different name for a package than the system does. For example, on Cray systems we
now have ``gcc-native`` but spack just uses ``gcc``. By default the hook will not pick up on the difference.
In order to fix this problem you can define an entry here that will remap a module name to the spack
equivalent.

.. _NSP_LMOD_path_names_variable:

``NSP_LMOD_path_names``
"""""""""""""""""""""""

:Type: **dict**

:Required: **false**

:Default: ``[]``

:Description: Defines lmod section header names for paths that meet the specified regexes.

For example:

.. code:: yaml

    NSP_LMOD_path_names:
      /opt/cray: "[ Cray Programming Environment ]"

All modules that reside somewhere under ``/opt/cray`` will appear in the ``[ Cray Programming Environment ]``
section when using ``module avail``.

.. _NSP_LMOD_enable_spack_compiler_projections_variable:

``NSP_LMOD_enable_spack_compiler_projections``
""""""""""""""""""""""""""""""""""""""""""""""

:Type: **bool**

:Required: **false**

:Default: ``true``

:Description: Toggles that addition of paths in the hook that spack's automatic additions for compiler and version.

.. caution::

    When in doubt, leave this variable with its default value.

.. _NSP_LMOD_enable_logging_variable:

``NSP_LMOD_enable_logging``
"""""""""""""""""""""""""""

:Type: **bool**

:Required: **false**

:Default: ``false``

:Description: Enable logging of module loads.

.. _NSP_LMOD_logging_url_variable:

``NSP_LMOD_logging_url``
""""""""""""""""""""""""

:Type: **str**

:Required: **false**

:Default: ``"http://localhost:8080/"``

:Description: API URL to send module loads to.

--------------------------------------------------------------------------------

.. _miniforge3_role:

miniforge3
----------

`Description`
^^^^^^^^^^^^^

The miniforge3 role installs miniforge3 with the specified packages in the base environment.
And optionally generates a module file.

`Variables`
^^^^^^^^^^^

.. _NSP_MINIFORGE3_version_variable:

``NSP_MINIFORGE3_version``
""""""""""""""""""""""""""

:Type: **str**

:Required: **true**

:Description: The version to install.

.. _NSP_MINIFORGE3_revision_variable:

``NSP_MINIFORGE3_revision``
"""""""""""""""""""""""""""

:Type: **str**

:Required: **false**

:Default: ``"0"``

:Description: The version revision to install.

.. _NSP_MINIFORGE3_base_packages_variable:

``NSP_MINIFORGE3_base_packages``
""""""""""""""""""""""""""""""""

:Type: **list**

:Required: **false**

:Default: ``[]``

:Description: A list of packages to install in the base environment.

.. _NSP_MINIFORGE3_clean_install_variable:

``NSP_MINIFORGE3_clean_install``
""""""""""""""""""""""""""""""""

:Type: **bool**

:Required: **false**

:Default: ``true``

:Description: Delete installer and re-download.

.. _NSP_MINIFORGE3_create_module_variable:

``NSP_MINIFORGE3_create_module``
""""""""""""""""""""""""""""""""

:Type: **bool**

:Required: **false**

:Default: ``true``

:Description: Toggles module generation.

--------------------------------------------------------------------------------

.. _nsp_role:

nsp
---

`Description`
^^^^^^^^^^^^^

This is a meta role that sets up needed infrastructure for the other NSP roles.

`Variables`
^^^^^^^^^^^

.. _NSP_system_name_variable:

``NSP_system_name``
"""""""""""""""""""

:Type: **str**

:Required: **true**

:Description: The system's name.

.. _NSP_help_email_variable:

``NSP_help_email``
""""""""""""""""""

:Type: **str**

:Required: **true**

:Description: Help email.

.. _NSP_site_name_variable:

``NSP_site_name``
"""""""""""""""""

:Type: **str**

:Required: **true**

:Description: Name of HPC site.

.. _NSP_install_root_variable:

``NSP_install_root``
""""""""""""""""""""

:Type: **path**

:Required: **false**

:Default: ``"{{ ['/sw', NSP_system_name] | path_join }}"``

:Description: The path prefix to NSP installed software.

.. _NSP_module_root_variable:

``NSP_module_root``
"""""""""""""""""""

:Type: **path**

:Required: **false**

:Default: ``"{{ [NSP_install_root, 'modules'] | path_join }}"``

:Description: The path prefix to NSP software modules.

.. _NSP_max_threads_variable:

``NSP_max_threads``
"""""""""""""""""""

:Type: **int**

:Required: **false**

:Default: ``"{{ [((ansible_processor_nproc * 0.75) | int | abs), 16] | min }}"``

:Description: Number of threads to use when building software.

.. _NSP_scratch_directory_variable:

``NSP_scratch_directory``
"""""""""""""""""""""""""

:Type: **path**

:Required: **false**

:Default: ``"{{ ['/tmp', ansible_user_id] | path_join }}"``

:Description: Scratch directory to perform builds in.

.. _NSP_keep_scratch_clear_variable:

``NSP_keep_scratch_clear``
""""""""""""""""""""""""""

:Type: **bool**

:Required: **false**

:Default: ``false``

:Description: Toggle retention of scratch directory contents after builds.

.. _NSP_user_variable:

``NSP_user``
""""""""""""

:Type: **str**

:Required: **false**

:Default: ``"{{ ansible_user_uid }}"``

:Description: The unix user for software installations.

.. _NSP_group_variable:

``NSP_group``
"""""""""""""

:Type: **str**

:Required: **false**

:Default: ``"{{ ansible_user_gid }}"``

:Description: The unix group for software installation.

.. _NSP_file_permissions_variable:

``NSP_file_permissions``
""""""""""""""""""""""""

:Type: **str**

:Required: **false**

:Default: ``"644"``

:Description: The unix permissions for files (non-executables).

.. _NSP_executable_permissions_variable:

``NSP_executable_permissions``
""""""""""""""""""""""""""""""

:Type: **str**

:Required: **false**

:Default: ``"755"``

:Description: The unix permissions for executables (including folders).

--------------------------------------------------------------------------------

.. _spack_role:

spack
-----

`Description`
^^^^^^^^^^^^^

The spack role templates spack environments for deployment. If you have any spack extentions they should be
placed in the playbook directory under ``spack/extentions``. All patch files should go in the playbook
directory under ``spack/patches``.

`Variables`
^^^^^^^^^^^

.. _NSP_SPACK_root_variable:

``NSP_SPACK_root``
""""""""""""""""""

:Type: **path**

:Required: **false**

:Default: ``"{{ [NSP_install_root, 'spack'] | path_join }}"``

:Description: This sets the root directory to deploy spack in.

.. _NSP_SPACK_repo_variable:

``NSP_SPACK_repo``
""""""""""""""""""

:Type: **str**

:Required: **false**

:Default: ``"https://github.com/spack/spack.git"``

:Description: The Spack repo to clone.

.. _NSP_SPACK_versions_variable:

``NSP_SPACK_versions``
""""""""""""""""""""""

:Type: **dict**

:Required: **true**

:Description: Defines available spack versions for the environments.

.. code:: yaml

    NSP_SPACK_versions:
      v0.23.1:
        git_reference: 2bfcc69
        patch: v0.23.1.patch

.. _NSP_SPACK_environments_variable:

``NSP_SPACK_environments``
""""""""""""""""""""""""""

:Type: **dict**

:Required: **true**

:Description: Defines spack environments.

For example:

.. code:: yaml

    NSP_SPACK_environments:
      example_env:
        spack_version: v0.23.1
        extensions:
          - spack-olcf
        specific_templates:
          - packages
        shared_templates:
          - mirrors

For each environment you should create a directory with the same name in the playbook directory under
``spack/environments``.

``spack_version`` should reference a spack version defined in
:ref:`NSP_SPACK_versions_variable` and ``extensions`` should be a list of extensions that can be found
in the playbook directory under ``spack/extensions``.

We like to split our spack configuration for each environment into multiple files. ``specific_templates``
are templates that are specific to each environment. They should be places under
``spack/environments/<environment_name>``. ``shared_templates`` are used by all of the environments and should
be placed under ``spack/environments``. There is a third catagory of templates that should not go into your
configuration but is important to know about. We call them ``nsp_templates`` these are templates that are
shared by all environment but instead of being in you playbook directory they are provided by the spack role
itself.
