===============
NEWS about byov
===============

Overview of changes to byov in reverse chronological order.

2.3.3
=====

  * Add {docker.setup.done} (retried following {docker.setup.timeouts}) at
    the end of the `docker` containers setup. This provides a way to better
    control when the container is ready to be used.

  * Add {docker.container.stop.timeout} to control grace period before
    killing the container. This helps with tests, `byot-run -c4 docker` goes
    from "Ran 31 tests in 241.148s" to "Ran 31 tests in 182.339s".

  * Fix regression in `ssh-register` when the host was a docker container.

  * Catch TIMEOUT in `qemu` teardown to make it more robust.

  * Introduced a way to lock stores against concurrent access from different
    processes, details are in `byov.tests.test_config.TestLocked and
    TestLocked. This is aimed mostly at tests running concurrently needing
    to share some resources.

  * Add {pip.install.command} so user can decide between:
    - `pip.command=pip3` and `pip.command.install=install,--user` (the
      default, installing under `~/.local`
    - and `pip.command=sudo,pip3` and `pip.command.install=install`
      (site-wide install).

  * Fix interactive shell (broken a while ago).

  * Introduce {docker.base} so tests can be properly isolated by running in
    their own dir while still being able to create docker containers.

  * Also obey the `BYOV_PATH` environment variable as a default for
    `byov.path`.

2.3.2
=====

  * Turn `byov.path` option into the `byov.path` python variable (a list)
    and the associated `BYOY_PATH` environment variable.  This is needed to
    build config stacks and as such cannot be described inside a config
    file. This is for the benefit of projects like `byoci` that want to
    layout an additional set of config files on top of the `byov` ones via
    the `byov.conf.d/byov.py` hook.

2.3.1
=====

  * Fix setup to require python3-byoc, byoc author on pypi didn't reply to
    inquiries.

2.3.0
=====

  * Add support for `byov.path`, a list of directories where scripts can be
    searched when used in hooks or other script related options. This is a
    backward compatible change, `byov.path` defaulting to the current
    directory when `byov` is invoked.


2.2.4
=====

  * Fix regression in `shell` behavior: since stdout and stderr are captured
    and an exception thrown on error, some `byoci` tests failed. The current
    fix is to ouput the captured out/err on stdout/stderr. This may not be
    sufficient, so feedbak welcome.


2.2.3
=====

  * Introduce a console script `byov`, keeping `byovm` for backwards
    compatibility. The later will be removed in 3.0.

  * Since debian packaging is out of date and requires significant work to
    upgrade, pypi releases are now preferred.

2.2.2
=====

Catchup with pypi where a wrong 2.2.1 version was (wrongly) present.

2.2.1
=====

  * Add `docker.create.image.hook` option to run on host before image
    creation.

  * Add support for {docker.ports} to bind host ports to container ones.

  * Add support for {docker.mounts} allowing `bind`, `tmpfs` and `volume`
    types.

  * All instances, images and snaphosts on ec2 are tagged with test ids to
    monitor usage and detect leaks. As a side-effect, all images and
    snapshots now have proper names in the aws web ui.

  * `ec2.image` defaults to a regexp from ec2.distribution.images if not set.

  * Expand {docker.file} for options and set {docker.file.expanded} to the
    resulting file. {docker.image.build.command} is expected to refer to the
    later.

  * Since `sudo` is not available/neeeded in docker containers, the default
    {pip.command} should not use it. Instead, pip packages are installed
    with the `--user` option.

  * Add support for a `docker` backend. Better fit for experimentation than
    production at this point. See `byovm help docker` for vm related options.

  * Add `pip.command` and `pip.packages` to install python packages with
    pip after distribution packages have been installed.

  * `scripts/create-lxd-amazon-image` can be used to bootstrap lxd images
    supporting cloud-init and ssh.

  * Add `dnf.command`, `dnf.options` and `dnf.packages` to install packages
    on rpm-based distributions. In practice, this can be reverted to `yum`
    rather than `dnf` when the later is not yet available.

  * The `override_logging` fixtures now defaults to `DEBUG` (the environment
    variable which can be set from the command line) to activate debug
    logging while running tests.
  
2.2.0
=====

  * Drop python2 support.

  * Add support for an `ec2` backend. Better fit for experimentation than
    production at this point. See `byovm help ec2` for vm related options.

  * byov can load a `byov.py` file in the configuration directories
    (./byov.conf.d, ~/.config/byov/conf.d and /etc/byov/conf.d). This allows
    registering options and other various byov customisations. This API may
    evolve in the future.

  * A new `ssh-register` command is available allowing a vm to register
    another vm in the ~<vm.user>/.ssh/known_hosts file.

  * A new `ssh-authorize` command is available to add a key to the
    ~<vm.user>/.ssh/authorized_keys file.

  * Find user name in a more robust way (USER is not always set in the
    environment so neither should LOGNAME. Using the passwd entry has to
    work).

  * Add a `scaleway.public_ip` option that can be used to assign an reserved
    IP to a given vm.

  * Support ssh server keys outside of `vm.config_dir`.

  * `byovm help` now accepts regular expressions as option names to make it
    easier to discover options.

  * Add support for a `qemu` backend. Better fit for experimentation than
    production at this point. See `scripts/first-use/qemu` to setup the
    host. See `byovm help qemu` for vm related options.
  
  * The `--download` setup parameter has been removed, it was used only by
    and for libvirt/qemu to bootstrap local images. The `qemu` backend
    handles downloads transparently respecting user configuration. (See
    `byovm help qemu.image qemu.download`).

  * The `libvirt` backend has been removed, its tests being broken for
    years. The `qemu` backend already provides more features.

  * `vm.published_as` is now a required option to use `publish`. The
    implementation is not homogeneous across backends so the feature
    definition is still in flux and should only be used for experimentation
    (feedback welcome).

  * Add a `qemu.disks` option so user can mount additional disks. The
    definition will probably evolve to make it easier for users to manage
    those disks.

  * Add `qemu.image.setup` and `qemu.image.teardown` options to define how
    the vm image should be managed. Associated actions are defined:
    `qemu.clone`, `qemu.convert`, `qemu.copy`, `qemu.create`,
    `qemu.download` and `qemu.resize`. This is still in flux but support
    more workflows and should allow to test some more (feedback welcome).

  * When qemu cannot be spawned properly, report the stderr file
    content. This may help fix some issues.

  * Add `options.TimeoutsOption` supporting exponential backoff timeouts to
    be defined as options.

  * Rely on `/var/run/reboot-required` to reboot when needed during setup.

  * Add a `vm.chpasswd` option wired to the `chpasswd` cloud-init one. This
    helps debugging network issues by allowing console logins.

2.1.1
=====

  * Add support for bionic to scripts/bootstrap-scaleway-image and
    unminimize the resulting image.

  * Add a `gitlab.login` option relying on a similarly named git config
    option.

  * Fix lxd > 3.0 compatibility: lxc info error message spelling has
    changed.

  * Fix compatibility with byoc default values.

  * Fix the long standing issue around unprintable exceptions.

  * Catch and log errors during hook executions to help debug.

  * Better skip tests if a scaleway image is not available.

  * Add `vm.user.home` and `vm.user.shell` options for use cases where
    distribution defaults doesn't fit.

  * Add support for local boots on scaleway via the `scaleway.boot.local`
    option.

2.1.0
=====

  * Fix `lxd.remote` not being saved in the existing vms configuration file.

  * Add a `lxd.mac.address` option to support stable IPs.

  * Add user and group id options for lxd mounts. There is no good default
    to be used when dealing with remote lxds, these options provide the
    needed hooks: `lxd.user_mounts.host.uid`, `lxd.user_mounts.host.gid`,
    `lxd.user_mounts.container.uid` and `lxd.user_mounts.container.gid`. The
    defaults are the python `os.get[ug]id()` for the host and 1000,1000
    inside the container (which were the previously hard-coded values).

  * Add a `lxd.config.boot.autostart` option so containers can be started
    when their host boot.

  * Add vm.name in most of the logging messages for clarity.
  
  * Allows scaleway images to be selected via their id (kludge, will change
    later).

  * Fix cloud-init conflicting with scaleway scripts (#1775086).

  * Support START1-XS type by building a dedicated image.


2.0.2
=====

  * Take `*.conf` files under `byov.conf.d`, `~/.config/byov/conf.d` and
    `/etc/byov/conf.d` into account.

  * Support test config files in `~/.config/byov/` and
    `~/.config/byov/conf.d` if they are suffixed with `-tests` so
    credentials can be provided while keeping main test config file under
    version control.

  * Add a `vm.start.hook` configuration option to execute a command on the
    *host* or a script if prefixed with `@`.

  * Section names are now matched across files to avoid more specific
    sections being masked by less specific ones in files defined earlier in
    the stack definition.

  * A new `push` command is available allowing a file to be uploaded to a
    virtual machine, expanding options if the local file is prefixed with
   `@`.

  * A new `pull` command is available allowing a file to be downloaded from
    a virtual machine.

  * Expose `apt.command` as an option.

  * Fix `vm.run_hook()` swallowing errors in scripts.
  
  * A new `lxd.remote` option is available to use remote lxd servers rather
    than the local one.

  * `vm.user` can now be set to something different than the distribution
    default user and gained some additional options: `vm.user.home`,
    `vm.user.system` and `vm.user.sudo`

  * `vm.password` has been deleted. Authentication is via ssh. Always.

2.0.0
=====

  * The new name is byov (formerly ols-vms) acronimizing Build Your Own
    Virtual machine.


1.3.1
=====

  * Fix debian support for ephemeral-lxd.

  * Add a `version` command.

  * `ols-vms config` now expand options in a file when using `@<file path>`
    as the option name. This is not (yet) documented as the API may change
    in the future.

  * `teardown` now accepts a `--force` parameter which stops the vm if it's
    running. The default is to raise an error.

  * Support more setup for ephemeral lxds (setup_over_ssh() which is
    installing packages and running additional setup).

  * Add a `vm.setup.hook` configuration option to execute a command on the
    *host* or a script if prefixed with `@`.

  * `teardown --force` has been re-implemented to give more freedom to
    backend implementations. The `scaleway` backend has a way to terminate a
    server when stopping it which benefits from the new implementation.

  * A new `scaleway` backend has been implemented as well as a
    `bootstrap-scaleway-image` script to create up to date images including
    cloud-init.
  
1.3.0
=====

  * Provide `scripts/create-lxd-debian-image` to create lxd images
    suitable for ols-vms use (i.e. add ssh and cloud-init to the image
    provided by lxd `images` server).

  * Add a `vm.distribution` configuration option defaulting to `ubuntu`
    for backwards compatiblity.

  * Add `debian` and `ubuntu` configuration namespaces for distributions.

  * Consistently use `vm.user` instead of `ubuntu`. The default value is
    `{vm.distribution}.user`.

  * The `lxd.image` configuration option now defaults to
    `{vm.distribution}.lxd image` so each distribution can use different
    conventions.

  * The `vm.password` configuration option now defaults to
    `{vm.user}`. Setting up ssh access remains the preferred model
    nevertheless.

  * The `vm.ubuntu_script` configuration option has been renamed
    `vm.user_script`. Users must upgrade their configurations if they were
    using it.

  * Catch-up with ols-config now showing more verbose exceptions.

  * Drop lxc/ephemeral-lxc support. lxd is better for all use cases.

1.2.4
=====

* Fix setup failure when running on a host where bzr is not installed.

1.2.3
=====

* Fix exception logging (the str(exception) returned an empty string in
  python2 :-/).


1.2.2
=====

* Fix VM.shell() and VM.run_script() returned values.

* Fix unicode support for subprocesses.


1.2.1
=====

* Fix a leak where `exsiting-vms.conf` content wasn't properly saved when a
  container was tear down.

* Add `logging.format` to allow users to specify the logging format to be
  used.

* Properly report invalid values for `lxd.nesting`.
    
1.2.0
=====

* `lxd.user_mounts` path pairs are now using `<host path>:<vm path>` rather
  than `<host path>,<vm path>`.

* `ols-vms help` is now targeted at options rather than commands. `ols-vms
  help olsvms.commands` replaces the previous use case.


1.1.9
=====

* `lxd.profiles` is the new name for `lxd.network` but the scope is
  expanded: any profile can be specified (unless they rely on cloud-init as
  that would conflict with ols-vms).

* Allow ephemeral lxds to use `lxd.user_mounts` but only if the backing vm
  didn't.


1.1.8
=====

* ubuntu wily has reached EOL.

* Add `lxd.user_mounts` to mount host paths inside lxd containers. This is a
  first release of the feature (i.e. experimental but tested in nested
  unprivileged containers), rough edges expected. Since this requires the
  user to configure /etc/subuid and /etc/subgid appropriately with
  `root:<id>:1` lines, this is checked before configuring the mounts.

* Add `lxc.bind_home` (formerly `vm.bind_home) and `lxc.user` to separate
  the lxc specific feature from `vm.user`.

* `lxd.nesting` is now an integer option specifying the number of testing
  the vm is expected to be configured with. Since this requires the user to
  configure /etc/subuid and /etc/subgid appropriately for `root` and `lxd`
  this is checked before creating the vm.
    
1.1.7
=====

* `vm.hash_setup()` now properly detect changes in files prefixed with `@`
  in `vm.packages`.

1.1.6
=====

* `vm.setup.digest.options`, `apt.setup.digest.options`,
  `ssh.setup.digest.options`, `nova.setup.digest.options` and
  `lxd.setup.digest.options` list the options that define a vm. Their values
  are hashed into `vm.setup.digest` as well as the content of the referenced
  files (but no deeper).

* A new `digest` command is available exposing the current value of
  `vm.hash_setup()` (stored as `vm.setup.digest` for existing vms) and can
  be used to control when a vm should be rebuilt.

* `start` now properly updates `vm.ip` in `existing-vms.conf`.
    
* Remove `vm.network` which was never used properly across all backends.

* `launchpad.login` support has been fixed for python3.

* `zesty` is opened and supported.

* `vivid` is EOL`ed, there is no cloud image for it anymore.

1.1.5
=====

* `setup` now accepts a `--force` parameter which stops the vm if it's
  running. The default is to raise an error.

* `@` path in `vm.packages` now supports `~` expansion.

1.1.4
=====

* Fix `vm.ubuntu_script` support which has been broken for a long time.

* Fix `ols-vms shell` to pass arguments to @script and not swallow errors.

1.1.3
=====

* Fix ephemeral lxd/lxd to save the basic options defining the vm at start
  time.

* Rename `launchpad.login` from `launchpad.id`. Support for the old
  `vm.launchpad_id` was incomplete and has been removed.

1.1.2
=====

* All commands now support --option=name=value to override configuration
  options for the duration of the command.

* Add support for ephemeral lxd containers (vm.class = ephemeral-lxd), first
  version, use with care, report bugs.

* `launchpad.id` now defaults to $(bzr lp-login) (or ${USER}) and was
  renamed from `vm.launchpad_id`.

* Fix an edge case where existing vms configs could leak into other vms
  (namely when one vm name was matching as a prefix for another one).

* Properly cleanup the ~/.config/ols-vms directory when a vm is teared
  down. Also cleanup existing-vms.conf at that point.

* Add xenial and yakkety to nova tests.


1.1.1
=====

* `lxd.image` now defaults to ubuntu:{vm.release}/{vm.architecture} which is
   the most common use case.

* `ssh.options` now defaults to -oUserKnownHostsFile=/dev/null,
  -oStrictHostKeyChecking=no, -oIdentityFile={ssh.key} which is the most
  useful default ssh scheme to use: this avoid polluting
  `~/.ssh/known_hosts` and doesn't require anything in `~/.ssh/config`. This
  completes the set of default values for `ssh.*` options to make them usable
  out of the box.

* Support `~` in `@` shell scripts and vm.setup_scripts.

* Add `lxc.nesting` option to help support nested containers.

* Work around sudo access in lxc when using home bound mounts, the user
  receives a password less sudo access in the guest instead.

1.1.0
=====

* `vm.ip` can now be used to get the network address for an exising vm.

* The kvm vm.class has been renamed `libvirt` anticipating the libvirt
  deprecation.

* The user configuration file is now at ~/.config/ols-vms/ols-vms.conf and
  the exsiting vms configuration options are not saved there
  anymore. Instead, they are now in
  ~/.config/ols-vms/existing-vms.conf. This makes it easier to use them,
  once they are setup, without requiring their defining ols-vms.conf to be
  in the working directory.
    
* Many config options have been renamed to better organize them by
  topic. Notably `lxd`, `lxc`, `libvirt` and `nova` now have their own
  namespace. Also `vm.cpu_model` has been renamed to `vm.architecture` as
  it's more commonly used. `lxd.image` and `nova.image` have always been
  different so `vm.image` is not used anymore. The full list is:

  kvm.network                -> libvirt.network
  vm.apt_proxy               -> apt.proxy
  vm.apt_sources             -> apt.sources
  vm.cloud_image_name        -> libvirt.cloud_image.name
  vm.cloud_image_url         -> libvirt.cloud_image.url
  vm.cpu_model               -> vm.architecture
  vm.download_cache          -> libvirt.download_cache
  vm.image                   -> lxd.image, nova.image
  vm.images_dir              -> libvirt.images_dir     
  vm.iso_name                -> libvirt.iso.name
  vm.iso_url                 -> libvirt.iso.url
  vm.lxc.set_ip_timeouts     -> lxc.setup_ip_timeouts
  vm.lxc.ssh_setup_timeouts  -> lxc.setup_ssh_timeouts
  vm.lxcs_dir                -> lxc.containers_dir
  vm.lxcs_dir                -> lxc.containers_dir
  vm.lxd.cloud_init_timeouts -> lxd.cloud_init_timeouts
  vm.lxd.ssh_setup_timeouts  -> lxd.setup_ssh_timeouts
  vm.net_id                  -> nova.net_id
  vm.nova.boot_timeout       -> nova.boot_timeout
  vm.nova.cloud_init_timeout -> nova.cloud_init_timeouts
  vm.nova.set_ip_timeout     -> nova.setup_ip_timeouts
  vm.os.auth_url             -> nova.auth_url
  vm.os.flavors              -> nova.flavors
  vm.os.password             -> nova.password
  vm.os.region_name          -> nova.region_name
  vm.os.tenant_name          -> nova.tenant_name
  vm.os.username             -> nova.username
  vm.qemu_etc_dir            -> libvirt.etc_dir
  vm.ssh_authorized_keys     -> ssh.authorized_keys
  vm.ssh_key                 -> ssh.key
  vm.ssh_keys                -> ssh.server_keys
  vm.ssh_opts                -> ssh.opts
  
* Fix IP detection to accept either eth0 or ens3 in the cloud-init output.

* If the command passed to `ols-vms shell` starts with a `@` it's
  interpreted as a path to a local script which is expanded, uploaded and
  executed in the guest.

* Implement logging. The `logging.level` option can be used to change the
  default (ERROR), the `LOG_LEVEL` environment variable can also be used.

* The lxd backend will now forcefully stop and teardown vms. This better
  reflects the ols-vms commands intent.

* `vm.setup_scripts` allows a list of scripts to be uploaded and executed on
  the guest.


1.0.3
=====

* Issue a proper error message when `vm.release` or `vm.cpu_model` is not
  provided for the lxc backend.

* `vm.update` and `vm.packages` are now handled once the vm provides ssh
  access (cloud-init handling it previously). This should make debugging
  installation issues easier.

* `apt.update.timeouts` has been renamed from `vm.apt.update.timeouts`.

* `vm.ssh_key` has been renamed from `vm.ssh_key_path`.

* `vm.poweroff` is now under user control, no vm is stoppped at the end of
  setup by default.

1.0.2
=====

* Add a new `publish` command and the associated `vm.published_as` option
  for lxd containers.

* Add `vm.manage_etc_hosts` to fix collisions with puppet.

* Fix lxd to properly wait for cloud-init completion.

* --ssh-keygen is now implied for vm.ssh_keys that don't exist. Using it
  force the keys to be generated again.


1.0.1
=====

* Add `vm.fqdn` so a fully qualified domain name can be specified via
  cloud-init.

* Add `vm.locale` so a specific locale can be configured.

* Avoid spurious failures of olsvms.tests.test_vms.TestEphemeralLXC.test_stop.

* Better detect wrong package names to catch typos in the vm description.

* Fix a test isolation issue for nova when acquiring credentials from the
  user env.

* Fix compatibility with recent lxc (lxc-start-ephemeral has been replaced
  by lxc-copy -e).

* Fix compatibility with recent lxd (lxc info format has changed again).

* Fix lxc support to install apt-transport-https so private PPAs can be used.

* Fix `ppa:` support for apt_sources for lxc, software-properties-common has
  to be installed explicitly.

* Fix the `foo` vm leaking from tests.

* Fix `vm.root_script` to run with `bootcmd` instead of `runcmd`.

* `lxc image copy` replaces `lxc-images` which has been removed.

* lxd.network is now a profile name as that better fit lxd.

* Use nova v2 API if available to silence warnings about v1.1 becoming
  obsolete.

  
1.0.0
=====

* The new name is ols-vms (formerly uci-vms).

0.2.0
=====

* Add lxd support.

* Options for cloud-init are not generated anymore unless they have a non
  empty value. This makes it easier to override default values.

* When --ssh-keygen is specified, existing keys are deleted before
  generating the new ones. This fixes a bug where ssh-keygen was prompting
  for deleting the old keys but the prompt was swallowed and uci-vms was
  hanging.

* Add support for OpenStack nova (vm.class = nova).

* Fix the script name in the help output.

* Restore python2 support.

* Since timeouts are used in a `try/sleep` loop, force the last value to be
  zero since there is no point waiting if no further attempt is to be made.

0.1.5
=====

* Fix systemd support (from vivid onwards) by picking an appropriate message
  to detect cloud-init end.

* `uci-vms config foo` won't show the config twice when run from the home
  directory. I.e. ~/uci-vms.conf is taken into account only if the current
  directory is not the home directory.

* The no-name section is now shown in `uci-vms config` output with a `[]`
  pseudo section name to separate it from the previous (named) section (no
  clue was given previously that the options were not part of the named
  section).

0.1.4
=====

* Remove a useless sudo requirement for the vm console file.

* Raise the default timeouts for IP/ssh detection as it can take more than a
  minute for lxc under heavy load.

0.1.3
=====

* Switch to python3.

* Support vivid.

* Add support for ephemeral lxc containers (vm.class = ephemeral-lxc).

* Add `vm.ssh_opts` to fine tune ssh connections. A useful default can be
  `-oUserKnownHostsFile=/dev/null -oStrictHostKeyChecking=no` so the host
  keys are not checked. Without these options the `known_hosts` ssh file
  tends to be polluted and may lead to collisions when IP addresses are
  reused.

* `vm.packages` can now use `@filename` to include packages from a file (one
  per line).

* Lxc vms can now use vm.bind_home to mount the home directory of $USER
  inside the vm. This is inherited by ephemeral containers based on these
  vms.

* Implement a `status` command.

* Sections in config files will now match if the vm name starts with the
  section name. This make ephemeral lxc easier to use as a single section
  can defined several vms, getting the vm name straight from the user (on
  the command line).

* Under load, lxc containers can be slow to start, wait for the IP address
  to become available and for ssh to be reachable.
    
0.1.2
=====

* Add `vm.final_message` so VM daughter classes with specific needs can
  override (LP: #1328170).

0.1.1
=====

* Add debian packaging (ubuntu native for now).

* Makes `vm.vms_dir` a PathOption to get `~` support.

* Add `vm.poweroff` as a config option defaulting to True so new VM classes
  (or users) can override if/when needed.

* Fix test issue uncovered in trusty/utopic.

* Fix minor compatibility changes with uci-tests.

0.1.0
=====

* Add uci-vms config command.

0.0.1
=====

First release.
