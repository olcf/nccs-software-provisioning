
Setting Up a System
===================

This tutorial will walk you through setting up NSP for a simple mock system so you can play around with it.

.. important::

    You will need to have ansible installed. This can be in a python environment (``venv`` or ``conda``). Just run
    ``pip install ansible``.

.. note::

    This tutorial is not comprehensive in the details of each role. If you want a detailed explanation of how each
    role works see :doc:`/reference/roles`. This tutorial is designed to give you working configuration files that
    you can explore and use the detailed docs to clarify if you have questions.

Setup Configuration Repository
##############################

Create a folder and initialize an empty git repository.

.. code-block:: bash

    $ mkdir nsp_tutorial && cd nsp_tutorial
    $ git init --initial-branch=main
    Initialized empty Git repository in /home/software/nsp_docs/.git/

Next add the NSP repository as a submodule in the roles directory.

.. note::

    You can create you own ``ansible.cfg`` but we provide one with good defaults in the nsp repository which we
    suggest you link in.

.. code-block:: bash

    $ git submodule add https://github.com/olcf/nccs-software-provisioning.git roles
    Cloning into '/home/software/nsp_tutorial/roles'...
    Username for 'https://github.com': REDACTED
    Password for 'https://REDACTED@github.com':
    remote: Enumerating objects: 115, done.
    remote: Counting objects: 100% (115/115), done.
    remote: Compressing objects: 100% (77/77), done.
    remote: Total 115 (delta 17), reused 110 (delta 12), pack-reused 0 (from 0)
    Receiving objects: 100% (115/115), 33.95 KiB | 331.00 KiB/s, done.
    Resolving deltas: 100% (17/17), done.
    $ ln -s roles/ansible.cfg ansible.cfg
    $ git add .gitmodules roles/ ansible.cfg
    $ git commit -m "Adding NSP submodule."
    [main (root-commit) 5310052] Adding NSP submodule.
    2 files changed, 4 insertions(+)
    create mode 100644 .gitmodules
    create mode 120000 ansible.cfg
    create mode 160000 roles

Add a New System
################

Create a directory with the name of your system. For this tutorial we use the name ``moria``.

.. code-block::

    $ mkdir moria

Next create a new playbook in the directory you just created for your system.

.. code-block:: yaml
    :caption: ``moria/playbook.yaml``

    - name: Deploy Moria
      hosts: localhost

      vars:
        NSP_system_name: moria
        NSP_install_root: "{{ ['/tmp', NSP_system_name] | path_join }}"
        NSP_help_email: example@example.com
        NSP_site_name: MySiteName

      roles: [ ]




To validate your setup run.

.. code-block:: text

    $ ansible-playbook moria/playbook.yaml
    PLAY [Deploy Moria] ************************************************************************************************

    TASK [Gathering Facts] *********************************************************************************************
    ok: [localhost]

    PLAY RECAP *********************************************************************************************************
    localhost                  : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


Init Scripts
############

For most of our systems, we maintain a set of init scripts that are sourced when a user logs in. These scripts allow us
to fine tune Lmod, set up convenience variables and more. As a first step for our new system we will add the
:ref:`init_role` role to ``moria/playbook.yaml``

.. code-block:: yaml
    :caption: ``moria/playbook.yaml``
    :emphasize-lines: 10-11

    - name: Deploy Moria
      hosts: localhost

      vars:
        NSP_system_name: moria
        NSP_install_root: "{{ ['/tmp', NSP_system_name] | path_join }}"
        NSP_help_email: example@example.com
        NSP_site_name: MySiteName

      roles:
        - role: init

Various roles in NSP will add to the init scripts but if you have extra content, that you want added to the init
scripts, you can do so by creating a ``profile.j2`` and/or ``cshrc.j2`` file in ``<system>/init``. For this tutorial we
will add some content to our init scripts that prints a welcome message.

.. code-block:: jinja
    :caption: ``moria/init/profile.j2``

    echo "Welcome to {{ NSP_system_name }}!!!"

.. code-block:: jinja
    :caption: ``moria/init/cshrc.j2``

    echo "Welcome to {{ NSP_system_name }}!!!"

Let's run our playbook now and see what happens.

.. code-block:: bash

    $ ansible-playbook moria/playbook.yaml

If you look, you will see that NSP has deployed our init scripts to ``/tmp/moria/init``.

.. code-block:: text
    :caption: ``tree /tmp/moria``

    /tmp/moria/
    └── init
        ├── cshrc
        └── profile

.. code-block:: bash
   :caption: ``/tmp/moria/init/profile``

    #!/usr/bin/env bash
    ##
    #| WARNING! This file is managed by Ansible.
    #| Do NOT make manual changes to this file.
    #| Please email example@example.com to request a change.
    #
    #| Info:
    #|   Role: init
    #|   Template: profile.j2
    #|   User: software
    ##

    # BEGIN INIT MANAGED
    echo "Welcome to moria!!!"
    # END INIT MANAGED

.. code-block:: csh
   :caption: ``/tmp/moria/init/cshrc``

    #!/usr/bin/env csh
    ##
    #| WARNING! This file is managed by Ansible.
    #| Do NOT make manual changes to this file.
    #| Please email example@example.com to request a change.
    #
    #| Info:
    #|   Role: init
    #|   Template: cshrc.j2
    #|   User: software
    ##

    # BEGIN INIT MANAGED
    echo "Welcome to moria!!!"
    # END INIT MANAGED

Bootstrap Lmod
##############

The next step in setting up a system is installing Lmod. We will have to add a little more configuration to lmod
when we get to setting up the :ref:`spack_role` role but for now let's add the :ref:`lmod_role` role to
our playbook.

.. code-block:: yaml
   :caption: ``moria/playbook.yaml``
   :emphasize-lines: 12-15

   - name: Deploy Moria
     hosts: localhost

     vars:
       NSP_system_name: moria
       NSP_install_root: "{{ ['/tmp', NSP_system_name] | path_join }}"
       NSP_help_email: example@example.com
       NSP_site_name: MySiteName

     roles:
       - role: init
       - role: lmod
         vars:
           NSP_LMOD_version: 8.7.37
           NSP_LMOD_install_type: internal

After we run our playbook again we can source the init script and see our new software stack!

.. code-block::

    $ ansible-playbook moria/playbook.yaml
    ...
    $ source /tmp/moria/init/profile
    $ module avail

    ------------------------------------------------- [ Base Modules ] -------------------------------------------------
       DefApps (L)

      Where:
       L:  Module is loaded

    If the avail list is too long consider trying:

    "module --default avail" or "ml -d av" to just list the default modules.
    "module overview" or "ml ov" to display the number of modules for each name.

    Use "module spider" to find all possible modules and extensions.
    Use "module keyword key1 key2 ..." to search for all possible modules matching any of the "keys".

If you were to look at the init scripts you would see that they now have an additional section that was added by lmod.

.. code-block:: bash
    :caption: ``/tmp/moria/init/profile``
    :emphasize-lines: 17-34

    #!/usr/bin/env bash
    ##
    #| WARNING! This file is managed by Ansible.
    #| Do NOT make manual changes to this file.
    #| Please email example@example.com to request a change.
    #
    #| Info:
    #|   Role: init
    #|   NSP Template: profile.j2
    #|   User: software
    ##

    # BEGIN INIT MANAGED
    echo "Welcome to moria!!!"
    # END INIT MANAGED

    # BEGIN LMOD MANAGED
    type module > /dev/null 2>&1
    if [ "$?" -eq 0 ]; then
        clearLmod -q > /dev/null 2>&1
        unset LMOD_MODULEPATH_INIT
    fi

    export LMOD_SYSTEM_NAME=moria
    export LMOD_SYSTEM_DEFAULT_MODULES=DefApps
    export LMOD_PACKAGE_PATH=/tmp/moria/lmod/hooks
    export LMOD_AVAIL_STYLE=nsp-pretty:system
    export LMOD_MODULERCFILE=/tmp/moria/lmod/etc/rc.lua
    export LMOD_ADMIN_FILE=/tmp/moria/lmod/etc/admin.list
    export LMOD_RC=/tmp/moria/lmod/etc/lmodrc.lua

    source /tmp/moria/lmod/lmod/init/profile
    module --initial_load --no_redirect restore
    # END LMOD MANAGED

Adding Software
###############

We can now add a variety of software through different :doc:`roles </reference/roles>`. For our purposes we will add
one version of ``miniforge3``, ``gcc`` and ``llvm`` each. Run the playbook and observe where they are installed and
where their module files are placed.

.. note::

    The ``gcc`` and ``llvm`` builds can take some time so be patient.

.. code-block:: yaml
    :caption: ``moria/playbook.yaml``
    :emphasize-lines: 16-25

    - name: Deploy Moria
      hosts: localhost

      vars:
        NSP_system_name: moria
        NSP_install_root: "{{ ['/tmp', NSP_system_name] | path_join }}"
        NSP_help_email: example@example.com
        NSP_site_name: MySiteName

      roles:
        - role: init
        - role: lmod
          vars:
            NSP_LMOD_install_type: internal
            NSP_LMOD_version: 8.7.37
        - role: miniforge3
          vars:
            NSP_MINIFORGE3_version: 24.11.3
        - role: gcc
          vars:
            NSP_GCC_version: 14.2.0
        - role: llvm
          vars:
            NSP_LLVM_version: 19.1.0
            # if your system architecture is not x86_64 you will need to set `NSP_LLVM_targets`

.. code-block:: text

    $ source /tmp/moria/init/profile
    $ module avail

    ------------------------------------------------- [ Base Modules ] -------------------------------------------------
       DefApps (L)    gcc/14.2.0    llvm/19.1.0    miniforge3/24.11.3-0

      Where:
       L:  Module is loaded

    If the avail list is too long consider trying:

    "module --default avail" or "ml -d av" to just list the default modules.
    "module overview" or "ml ov" to display the number of modules for each name.

    Use "module spider" to find all possible modules and extensions.
    Use "module keyword key1 key2 ..." to search for all possible modules matching any of the "keys".

.. code-block:: bash
    :emphasize-lines: 3-4,8-9,16-17,20-22

    $ tree -L 2 /tmp/moria/
    /sw/moria/
    ├── gcc
    │ └── 14.2.0
    ├── init
    │ ├── cshrc
    │ └── profile
    ├── llvm
    │ └── 19.1.0
    ├── lmod
    │ ├── 8.7.37
    │ ├── bootstrap
    │ ├── cache
    │ ├── etc
    │ └── lmod -> 8.7.37
    ├── miniforge3
    │ └── 24.11.3-0
    └── modules
        ├── DefApps.lua
        ├── gcc
        ├── llvm
        └── miniforge3

Spack
#####

We are going to set up spack for the system gcc (mine is 13.3.0 but yours may be different) and the gcc and llvm versions
that we built above. We will have a ``Core`` set of modules built by the system gcc and then a software stack
built on gcc 14.2.0 and llvm 19.1.0.

We will name our spack environments according to the following schema ``core<year>.<month>`` and
``sw<year>.<month>`` (in this tutorial we will use ``core25.02`` and ``sw25.02``). Create the following files:

.. code-block:: jinja
    :caption: ``moria/spack/environments/concretizer.yaml.j2``

    {{ ansible_managed | comment(beginning="##", end="##", decoration="#", prefix_count=0, postfix_count=0) }}

    concretizer:
      reuse: false
      targets:
        granularity: microarchitectures
        host_compatible: true
      unify: false
      duplicates:
        strategy: none

.. code-block:: jinja
    :caption: ``moria/spack/environments/config.yaml.j2``

    {{ ansible_managed | comment(beginning="##", end="##", decoration="#", prefix_count=0, postfix_count=0) }}

    config:
      install_tree:
        root: {{ [NSP_install_root, 'spack/envs', _SPACK_environment_name, 'opt'] | path_join }}
        projections:
          all: '{compiler.name}-{compiler.version}/{name}-{version}-{hash}'

      template_dirs:
        - $spack/share/spack/templates

      license_dir: $spack/etc/spack/licenses

      build_stage:
        - {{ [NSP_scratch_directory, "spack/stage", _SPACK_environment_name] | path_join }}

      test_stage: {{ [NSP_scratch_directory, "spack/test", _SPACK_environment_name] | path_join }}
      source_cache: {{ [NSP_install_root, "spack/envs/scache"] | path_join }}
      misc_cache: {{ [NSP_install_root, "spack/envs", _SPACK_environment_name, "mcache"] | path_join }}

      extensions: [ ]

      connect_timeout: 10
      verify_ssl: true
      ssl_certs: $SSL_CERT_FILE
      suppress_gpg_warnings: false
      checksum: true
      deprecated: false
      dirty: false
      build_language: C
      locks: true
      url_fetch_method: urllib
      build_jobs: {{ NSP_max_threads }}
      ccache: false
      concretizer: clingo
      db_lock_timeout: 60
      package_lock_timeout: null

      shared_linking:
        type: rpath
        bind: false

      allow_sgid: true
      install_status: true
      binary_index_ttl: 600

      flags:
        keep_werror: 'none'

      aliases:
        rm: remove
        search: list

.. code-block:: jinja
    :caption: ``moria/spack/environments/modules.yaml.j2``

    {{ ansible_managed | comment(beginning="##", end="##", decoration="#", prefix_count=0, postfix_count=0) }}

    modules:
      prefix_inspections:
        bin:
          - PATH
        man:
          - MANPATH
        share/man:
          - MANPATH
        share/aclocal:
          - ACLOCAL_PATH
        lib:
          - LD_LIBRARY_PATH
        lib64:
          - LD_LIBRARY_PATH
        lib/pkgconfig:
          - PKG_CONFIG_PATH
        lib64/pkgconfig:
          - PKG_CONFIG_PATH
        share/pkgconfig:
          - PKG_CONFIG_PATH
        .:
          - CMAKE_PREFIX_PATH
      default:
        roots:
          lmod: {{ [NSP_install_root, "spack/modules"] | path_join }}
        enable:
          - lmod
        arch_folder: false
        lmod:
          core_compilers:
            - gcc@{{ system_gcc.version }}
          all:
            environment:
              set:
                {{ NSP_site_name.upper() }}_{NAME}_ROOT: "{prefix}"
            autoload: none
            suffixes:
              ^llvm-amdgpu: gpu
              ^cuda: gpu
              ^mpi: mpi
              +openmp: omp
              threads=omp: omp
          exclude_implicits: true
          verbose: true
          exclude: [ ]
          hash_length: 0
          hierarchy:: [ ]
          projections:
            ^llvm-amdgpu ^mpi: "{^mpi.name}-{^mpi.version}/rocm-{^llvm-amdgpu.version}/{compiler.name}-{compiler.version}/{name}/{version}"
            ^cuda ^mpi: "{^mpi.name}-{^mpi.version}/cuda-{^cuda.version}/{compiler.name}-{compiler.version}/{name}/{version}"
            ^llvm-amdgpu: "rocm-{^llvm-amdgpu.version}/{compiler.name}-{compiler.version}/{name}/{version}"
            ^cuda: "cuda-{^cuda.version}/{compiler.name}-{compiler.version}/{name}/{version}"
            ^mpi: "{^mpi.name}-{^mpi.version}/{compiler.name}-{compiler.version}/{name}/{version}"
            all: "{compiler.name}-{compiler.version}/{name}/{version}"
          core_specs: []

.. code-block:: jinja
    :caption: ``moria/spack/environments/packages.yaml.j2``

    {{ ansible_managed | comment(beginning="##", end="##", decoration="#", prefix_count=0, postfix_count=0) }}

    packages:
      all:
        buildable: true
        providers:
          blas: [openblas]
          lapack: [openblas]
          mpi: [openmpi]
      gcc:
        externals:
        # System GCC 
        - spec: gcc@{{ system_gcc.version }}
          prefix: /usr
          extra_attributes:
            compilers:
              c: /usr/bin/gcc
              cxx: /usr/bin/g++
              fortran: /usr/bin/gfortran
          modules: [ ] 
        # GCC Compiler
        - spec: gcc@{{ gcc.version }}
          prefix: {{ [NSP_install_root, 'gcc', gcc.version] | path_join }}
          extra_attributes:
            compilers:
              c: {{ [NSP_install_root, 'gcc', gcc.version, 'bin/gcc'] | path_join }}
              cxx: {{ [NSP_install_root, 'gcc', gcc.version, 'bin/g++'] | path_join }}
              fortran: {{ [NSP_install_root, 'gcc', gcc.version, 'bin/gfortran'] | path_join }}
          modules: [gcc/{{ gcc.version }}] 
      # LLVM Compiler
      llvm:
        externals:
        - spec: llvm@{{ llvm.version }}
          prefix: {{ [NSP_install_root, 'llvm', llvm.version] | path_join }}
          extra_attributes:
            compilers:
              c: {{ [NSP_install_root, 'llvm', llvm.version, 'bin/clang'] | path_join }}
              cxx: {{ [NSP_install_root, 'llvm', llvm.version, 'bin/clang++'] | path_join }}
              fortran: {{ [NSP_install_root, 'gcc', gcc.version, 'bin/gfortran'] | path_join }}
          modules: [llvm/{{ llvm.version }}] 

.. code-block:: jinja
    :caption: ``moria/spack/environments/core25.02/spack.yaml.j2``

    {{ ansible_managed | comment(beginning="##", end="##", decoration="#", prefix_count=0, postfix_count=0) }}

    # OLCF {{ NSP_system_name }} {{ _SPACK_environment_name }} Spack Environment

    spack:
      view: false
      include:
        - concretizer.yaml
        - modules.yaml
        - config.yaml
        - packages.yaml

      modules:
        default:
          lmod:
            core_compilers: [ gcc@{{ system_gcc.version }} ]
            projections:
              # core
              '%gcc@{{ system_gcc.version }}': '25.02/{name}/{version}'

      # -------------------------------------------------------------------
      # Specs Definitions
      # -------------------------------------------------------------------

      definitions:
        - core_compiler:
          - '%gcc@{{ system_gcc.version }}'

        - core_25.02:
          - matrix:
            - - cmake
              - tmux
              - wget
            - - $core_compiler

      specs:
        - $core_25.02

.. code-block:: jinja
    :caption: ``moria/spack/environments/sw25.02/spack.yaml.j2``

    {{ ansible_managed | comment(beginning="##", end="##", decoration="#", prefix_count=0, postfix_count=0) }}

    # OLCF {{ NSP_system_name }} {{ _SPACK_environment_name }} Spack Environment

    spack:
      view: false
      include:
      - concretizer.yaml
      - modules.yaml
      - config.yaml
      - packages.yaml

      # -------------------------------------------------------------------
      # Specs Definitions
      # -------------------------------------------------------------------

      definitions:
      - gcc_compilers:
        - '%gcc@{{ gcc.version }}'
      - llvm_compilers:
        - '%clang@{{ llvm.version }}'
      - all_compilers:
        - $gcc_compilers
        - $llvm_compilers

      - sw-25.02:
        - boost ~mpi
        - boost +mpi
        - openmpi

      # -------------------------------------------------------------------
      # Final Spec Matrices
      # -------------------------------------------------------------------

      - sw_cpu:
        - matrix:
          - - $sw-25.02
          - - $all_compilers

      specs:
      - $sw_cpu

.. code-block:: jinja
    :caption: ``moria/spack/environments/sw25.02/variables.yaml``

    # system gcc
    system_gcc:
      version: 13.3.0
    # GCC
    gcc:
      version: 14.2.0
    # LLVM
    llvm:
      version: 19.1.0
    # OS
    os:
      identifier: ubuntu24.04

.. code-block:: text
    :caption: ``moria/spack/environments/core25.02/variables.yaml``

    # this should be a symlink to `moria/spack/environments/sw25.02/variables.yaml`

Finally we will need to add the spack role to our playbook.

.. code-block:: yaml
    :caption: ``moria/playbook.yaml``
    :emphasize-lines: 26-40

    - name: Deploy Moria
      hosts: localhost

      vars:
        NSP_system_name: moria
        NSP_install_root: "{{ ['/tmp', NSP_system_name] | path_join }}"
        NSP_help_email: example@example.com
        NSP_site_name: MySiteName

      roles:
        - role: init
        - role: lmod
          vars:
            NSP_LMOD_install_type: internal
            NSP_LMOD_version: 8.7.37
        - role: miniforge3
          vars:
            NSP_MINIFORGE3_version: 24.11.3
        - role: gcc
          vars:
            NSP_GCC_version: 14.2.0
        - role: llvm
          vars:
            NSP_LLVM_version: 19.1.0
            # if your system architecture is not x86_64 you will need to set `NSP_LLVM_targets`
        - role: spack
          vars:
            _shared_templates: &shared_L
              - concretizer
              - config
              - modules
              - packages
            _specific_templates: &specific_L
              - spack
            NSP_SPACK_versions:
              v1.0.0:
                git_reference: 73eaea1
            NSP_SPACK_environments:
              core25.02: { spack_version: v1.0.0, specific_templates: *specific_L, shared_templates: *shared_L }
              sw25.02: { spack_version: v1.0.0, specific_templates: *specific_L, shared_templates: *shared_L }

After running the playbook explore ``/tmp/moria/spack/configs``. To install our software via spack run the following.

.. code-block:: bash

    $ cd /tmp/moria/spack/configs
    $ source spacktivate   # choose the core25.02 env
    $ spack concretize
    $ spack install
    $ source spacktivate   # choose the sw25.02 env
    $ spack concretize
    $ spack install

All of our software should now be installed to ``/tmp/moria/spack/envs``; however, none of it shows up for
``module avail`` yet, but all of the modules are in ``/tmp/moria/spack/modules``.

Lmod Hook & Core
################

The final part of our Lmod configuration is setting up the NSP hook. This will make the software that we built with
our ``sw25.02`` spack environment visible. We will also create a module file to add the ``Core`` (a.k.a ``core25.02``)
environment that we installed.

.. code-block:: jinja
    :caption: ``moria/files/Core/25.02.lua``

    {{ ansible_managed | comment(beginning="--[[", end="]]--", decoration="", prefix_count=0, postfix_count=0) }}

    help("Add path for Core 25.02 modules to MODULEPATH")

    prepend_path{"MODULEPATH", "{{ [NSP_install_root, 'spack/modules/Core/25.02'] | path_join }}", priority=10}

Modify the playbook to include configuration for our hook and the :ref:`files_role` role which is where we are keeping
the ``Core`` module files. Also add some modules to lmod's :ref:`NSP_LMOD_DefApps_modules_variable`.

.. code-block:: yaml
    :caption: ``moria/playbook.yaml``
    :emphasize-lines: 16-30,56-60

    - name: Deploy Moria
      hosts: localhost

      vars:
        NSP_system_name: moria
        NSP_install_root: "{{ ['/tmp', NSP_system_name] | path_join }}"
        NSP_help_email: example@example.com
        NSP_site_name: MySiteName

      roles:
        - role: init
        - role: lmod
          vars:
            NSP_LMOD_install_type: internal
            NSP_LMOD_version: 8.7.37
            NSP_LMOD_DefApps_modules:
              - Core/25.02
              - gcc/14.2.0
            NSP_LMOD_hierarchy:
              compiler:
                members: [ gcc, llvm ]
                paths:
                  - {path: '|compiler.name|-|compiler.version|', weight: 20}
                  - {path: '|mpi.name|-|mpi.version|/|compiler.name|-|compiler.version|', weight: 30}
                level: 0
              mpi:
                members: [ openmpi ]
                paths:
                  - {path: '|mpi.name|-|mpi.version|/|compiler.name|-|compiler.version|', weight: 30}
                level: 1
        - role: miniforge3
          vars:
            NSP_MINIFORGE3_version: 24.11.3
        - role: gcc
          vars:
            NSP_GCC_version: 14.2.0
        - role: llvm
          vars:
            NSP_LLVM_version: 19.1.0
            # if your system architecture is not x86_64 you will need to set `NSP_LLVM_targets`
        - role: spack
          vars:
            _shared_templates: &shared_L
              - concretizer
              - config
              - modules
              - packages
            _specific_templates: &specific_L
              - spack
            NSP_SPACK_versions:
              v1.0.0:
                git_reference: 73eaea1
            NSP_SPACK_environments:
              core25.02: { spack_version: v1.0.0, specific_templates: *specific_L, shared_templates: *shared_L }
              sw25.02: { spack_version: v1.0.0, specific_templates: *specific_L, shared_templates: *shared_L }
        - role: files
          vars:
            NSP_FILES_inventory:
              - src: Core
                dest: "{{ [NSP_module_root, 'Core'] | path_join }}"


After running the playbook again our example software stack is complete! Run the playbook, source the init scripts
and test out the new stack.

.. code-block:: bash

    $ ansible-playbook moria/playbook.yaml
    ...
    $ source /tmp/moria/init/profile
    $ module load openmpi boost

.. code-block:: bash

    $ module avail

    ------------------------------------------ [ gcc/14.2.0, openmpi/5.0.5 ] -------------------------------------------
       boost/1.86.0-mpi

    -------------------------------------------------- [ gcc/14.2.0 ] --------------------------------------------------
       boost/1.86.0 (D)    openmpi/5.0.5 (L)

    -------------------------------------------------- [ Core/25.02 ] --------------------------------------------------
       cmake/3.30.5    tmux/3.4    wget/1.24.5

    ------------------------------------------------- [ Base Modules ] -------------------------------------------------
       Core/25.02 (L)    DefApps (L)    gcc/14.2.0 (L)    llvm/19.1.0    miniforge3/24.11.3-0

      Where:
       L:  Module is loaded
       D:  Default Module

    ...

.. code-block:: bash

    $ ml load llvm

    Lmod is automatically replacing "gcc/14.2.0" with "llvm/19.1.0".


    Due to MODULEPATH changes, the following have been reloaded:
      1) boost/1.86.0     2) openmpi/5.0.5

.. code-block:: text

    $ module avail

    ------------------------------------------ [ llvm/19.1.0, openmpi/5.0.5 ] ------------------------------------------
       boost/1.86.0-mpi

    ------------------------------------------------- [ llvm/19.1.0 ] --------------------------------------------------
       boost/1.86.0 (D)    openmpi/5.0.5 (L)

    -------------------------------------------------- [ Core/25.02 ] --------------------------------------------------
       cmake/3.30.5    tmux/3.4    wget/1.24.5

    ------------------------------------------------- [ Base Modules ] -------------------------------------------------
       Core/25.02 (L)    DefApps (L)    gcc/14.2.0    llvm/19.1.0 (L)    miniforge3/24.11.3-0

    ...
