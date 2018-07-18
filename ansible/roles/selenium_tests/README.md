Python
======

Installs python, pip and virtualenv

Usage
-----

To utilize this role, add it to the `requirements.yml` file inside the ansible folder:

    - src: git+https://github.com/magenta-aps/ansible-role-python.git
      version: master
      name: python

Requirements
------------

Must be run against a `apt` capable system.

Example Playbook
----------------

    - hosts: all
      roles:
         - python

License
-------

MPLv2

Author Information
------------------

skeen - Emil Madsen
