====================================
byov: build your own virtual machine
====================================

This projects helps maintain throw-away virtual machines (vm) in a simple and
consistent way.

It collects various recipes used to build virtual machines for different
virtualization tools (kvm, nova, scaleway and lxd) and relies on cloud-init
and ssh access.

Virtual machines are described in a configuration file capturing their
definition in a few lines and allowing image-based workflows to be defined
by chaining vms definitions.

Lacking documentation accessible inline or from the command line, the next
best thing is to look at byov/config.py where all options are documented
individually, grouped by topic (backend (nova, lxd) or command (apt, ssh)).

