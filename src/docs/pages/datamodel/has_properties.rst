-----------------------------
HasProperties
-----------------------------

To enable administrative users to dynamically define new data fields on
models, the datamodel includes the :code:`HasProperties` framework shown below.
It was not in use at the time of writing (April 18 2018), and not planned for
use in the first release. It is introduced here for future reference. Note
that only the data model is present. Use will require implementation as
described below.

 .. image:: ../../static/has_properties.png

A model wishing to implement dynamic properties must extend the
:code:`HasProperties` class. The model (for instance :code:`Applicant`) should
furthermore be registered as a :code:`HasPropertiesMember`. Then, a named
:code:`PropertyCategory` may be defined for that member
(e.g. 'applicant personal data').
:code:`PropertyCategory.position` specifies sorting order in UI.

A property may then be defined as a named and typed
:code:`PropertyDefinition` (e.g. 'hair color', data type 'char').
Concrete values are then stored as :code:`PropertyValue` instances with the
relevant value field populated (e.g. value_string = 'brown'), and associated
with the relevant :code:`HasProperties` instance (e.g. an :code:`Applicant`).
The system should verify that values are only assigned to instances of the
class identified by their category.

It is possible to restrict the legal values for a :code:`PropertyDefinition`
by creating the desired acceptable :code:`PropertyValue` instances, leaving
their :code:`def_for` reference blank and instead assigning their
:code:`legal_for_def` reference to the relevant :code:`PropertyDefinition`.
Any new value created can then be matched against
:code:`PropertyDefinition.legal_values`.

Values could also be validated against the user-specified
:code:`PropertyDefinition.validation_regexp`.

List values are supported. :code:`PropertyDefinition.list` must be set to
:code:`True`, and values are modeled as :code:`PropertyValueList` instances.
Individual list elements exist as regular :code:`PropertyValue` instances,
but with their :code:`in_list` reference pointing to the
:code:`PropertyValueList` instance.
The :code:`PropertyValue.position` field specifies sorting order in UI when the
value is part of a list.


