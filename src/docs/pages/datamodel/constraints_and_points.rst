-----------------------------
Constraints and points
-----------------------------

 .. image:: ../../static/constraints_and_points.png

Only key fields are shown in the above diagram.
For details on the individual classes, inspect the
:ref:`API documentation <Automatic API>`

Applicants must fulfil a number of constraints to be eligible for housing
offers.
These are modeled with the :code:`ConstraintRule` class and associated
implementation classes (not shown).

When applicants apply for tenancies, they are awarded points based on their
current housing situation, distance to education, number of days active, and
other factors. These rules are modeled by the :code:`PointRule` class and
associated implementation classes (not shown).

The rule implementation classes are documented in
:doc:`point_rule_impl_classes`.

The system's configuration of constraint and point rules with implementation
classes can be seen in :code:`webapp/models/gen/ConstraintRule.py` and
:code:`webapp/models/gen/PointRule.py`.

Generally, an :code:`AbstractRule` (:code:`ConstraintRule` and
:code:`PointRule`'s common
superclass) is defined by an :code:`ApplicationTarget`.
The majority of rules will be defined by ApprobationCommittees, but it is
also possible for instance for a Building to define specific rules.

To compute a rule for a concrete applicant, its referenced implementation
class is instantiated and called. The result (a boolean for constraint
rules, an int for points) is then stored as a :code:`ConstraintValue` or
:code:`PointValue`.
:code:`AbstractRule.values_on_level` defines to which level in the hierarchy
of application targets values should be attached. Possible values are in
:code:`webapp/models/util.py`:

.. code:: console

    HIERARCHY_COMMITTEE = '0'
    HIERARCHY_BUILDING = '1'
    HIERARCHY_TENANCY_GROUP = '2'
    HIERARCHY_TENANCY = '3'

For instance, a PointRule configured with the
:code:`webapp.domain.pointrules.TransportRule` implementation class will be
defined by an ApprobationCommittee, but have values attached to tenancies,
since the points awarded for transport depends on the address of the applied
tenancy.

On the other hand  a PointRule configured with the
:code:`webapp.domain.pointrules.ResidSituationRule` class will both be defined
by an ApprobationCommittee and have values attached that level, since the points
for an applicant's current housing situation are the same regardless of which
Building or Tenancy he/she applies for.

Computed results may be overriden by administrators by filling in
:code:`ConstraintValue.manual_override` or
:code:`PointValue.manual_override`. When these fields are set, the
computed value is ignored. :code:`PointValues` can also have their computed
value adjusted by setting the :code:`manual_adjust` field.

:code:`ConstraintRule`\s are recomputed every night, as defined by the
background job in
:code:`webapp/tasks/recalculate_constraints.py`.
A :code:`PointRule` may have its :code:`periodic` field set to True, which
will cause it to be included in the nightly job defined in
:code:`webapp/tasks/recalculate_points.py`.This is relevant for the
implementation class :code:`webapp.domain.pointrules.DateRankingRule` which
awards points based on the number of days the applicant has had active
applications.

Rules may be configurable, for instance with number of points or other
parameters needed by their implementation class. To store these arbitrary
parameters, a persistable dictionary is implemented with the
:code:`Dictionary` model, which utilises :code:`KeyValuePair` to persist
individual dict entries.