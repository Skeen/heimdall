Boligadmin - UBSBolig
---------------------

# Status

[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)

| Task | Status |
| :--- | :----: |
| Check docker image | [!['Check docker image' Status](http://ubsjenkins.atlas.magenta.dk/job/Check%20docker%20image/badge/icon)](http://ubsjenkins.atlas.magenta.dk/job/Check%20docker%20image/) |
| Checking           | [!['Checking' Status](http://ubsjenkins.atlas.magenta.dk/job/Checking/badge/icon)](http://ubsjenkins.atlas.magenta.dk/job/Checking/) |
| Documentation      | [!['Documentation' Status](http://ubsjenkins.atlas.magenta.dk/job/Documentation/badge/icon)](http://ubsjenkins.atlas.magenta.dk/job/Documentation/) |
| End-to-End Tests   | [!['End-to-End Tests' Status](http://ubsjenkins.atlas.magenta.dk/job/End-to-End%20Tests/badge/icon)](http://ubsjenkins.atlas.magenta.dk/job/End-to-End%20Tests/) |
| Integration Tests  | [!['Integration Tests' Status](http://ubsjenkins.atlas.magenta.dk/job/Integration%20Tests/badge/icon)](http://ubsjenkins.atlas.magenta.dk/job/Integration%20Tests/) |
| UBS                | [!['UBS' Status](http://ubsjenkins.atlas.magenta.dk/job/UBS/badge/icon)](http://ubsjenkins.atlas.magenta.dk/job/UBS/) |


# Quick start

## Clone the project

To clone this repository recursively, please run:

    git clone --recursive git@github.com:magenta-aps/boligadmin.git

Or using older versions of git:

    git clone git@github.com:magenta-aps/boligadmin.git
    cd boligadmin
    git submodule update --init --recursive


## Start development instance

From the `boligadmin` directory, run `./start_dev.sh`. This will spin up a vagrant virtual machine and start the Django server with some fake testing data already loaded. 
Then open a browser on your host and go to http://localhost:8000/ to use the web application.
Other interesting URLS to check out:

* http://localhost:8000/webapp/login/ - UI for applicants to manage their profiles and applications. Default user/password is ubsuser/ubsuser.
* http://localhost:8000/adminapp/ - UI for waiting list admins. Default user/password is ubsadmin/ubsadmin.
* http://localhost:8000/admin/ - Django default admin UI. Accessible by admins.
* http://localhost:8000/api/ - Browse the REST API available to the web application.


## Poking around inside the vagrant box

In order to access your vagrant machine, go to the vagrant directory in the boligadmin project and use the `vagrant ssh` command.
```
cd vagrant
vagrant ssh
```


# Django

For information about the Django project, please check:

* [src/README.rst](src/README.rst)

Which contains information about how to setup the project.


# Documentation


## Vagrant
For information on the Vagrantfile, and Ansible, please check:
[This repository](https://github.com/magenta-aps/vagrant-ansible-example)

*Note: When using vagrant with Virtualbox, you'll be prompted to choose a 
bridged network interface. Select the interface that is being used to connect
to the internet.*


## Autogen

This may not be up-to-date.

For information about the Visual paradigm XML-to-DjangoModel converters, please check:

* [autogen/visual_paradigm_database/README.md](autogen/visual_paradigm_database/README.md)
* [autogen/visual_paradigm_uml/README.md](autogen/visual_paradigm_uml/README.md)

which contains information about how to use these tools.
