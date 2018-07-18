===========================
Datamodel and functionality
===========================
These documents will introduce the system datamodel, which is implemented using
`Django's ORM functionality`_.
Reading this document should provide a new developer with an initial
understanding of the foundation of the system.

Database tables are defined as Python classes, abstracting away the
underlying database platform. The datamodel consists of ~60 classes, which
are described in the documents below. They are intended to be read in the given
sequence.

.. _`Django's ORM functionality`: https://docs.djangoproject.com/en/1.11/topics/db


.. toctree::
    application_target
    applicant
    application
    constraints_and_points
    point_rule_impl_classes
    zipcode_and_area
    message
    paragraph
    has_properties
    studiestartsliste
    translation

TODO
----------

- CommonID
- Constraint rule impl classes
