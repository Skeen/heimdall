-------------------
Model translation
-------------------

To support translation of database fields, the `django-modeltranslation`_
framework is used. It enables translation of any field by adding additional
fields of the same name, suffixed with :code:`_en_us` or :code:`_da_dk`. This
happens without modifying the model class. The version of a field to be served
is then selected based on Django's current language setting.
The configuration of translatable fields can be seen in
:code:`webapp/translation.py`.

.. _`django-modeltranslation`: http://django-modeltranslation.readthedocs.io/en/latest
