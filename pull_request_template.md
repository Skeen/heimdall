* **Please check that the following is true**
    - [ ] Redmine Ticket ID is in branch name
    - [ ] Appropriate labels and milestone has been added on the pull request
    - [ ] Appropriate reviewers have been added to the pull request
    - [ ] Prosa documentation has been adjusted if necessary
    - [ ] Local ansible scripts have been adjusted if necessary
    - [ ] Production ansible scripts have been adjusted if necessary

* **Please check that your PR does not introduces any of the below**
    - [ ] Pylint disables (`# pylint: disable=*`)
    - [ ] Coverage no-covers (`# pragma: no cover`)
    - [ ] Pyflake noqa (`# flake8: noqa`)
    - [ ] New database migrations
    - [ ] Changes to the Solr Schema
    - [ ] Breaking changes
    - [ ] Changes project default settings
    - [ ] New or updated packages

*If any of the above are left unchecked, please document and argue why this is the case*
