----------------------------------
Point rule implementation classes
----------------------------------

 .. image:: ../../static/point_rule_impl_classes.png

Only key fields are shown in the above diagram.
For details on the individual classes, inspect the
:ref:`API documentation <Automatic API>`

These classes (that are not part of the datamodel) implement the various
politically decided rules for awarding
points for applicants. They are located in :code:`webapp/domain/pointrules/`.
The individual rule implementations all extend :code:`RuleImplBase` whose
constructor stores a reference to the :code:`webapp.models.PointRule` model
that instantiated this implementation class. :code:`RuleImplBase` also
defines the interface of the compute-method, which all subclasses must
implement. This method returns the number of calculated points as an int.

The system's configuration of point rules with the below implementation
classes can be seen in and :code:`webapp/models/gen/PointRule.py`.

The indivual rule implementation classes are introduced below.

Simple rules
--------------

:code:`NoopRule` always returns 0, and is used when creating
:code:`PointRules` to accommodate points manually inserted or imported.

:code:`DateRankingRule` provides points based on the number of days an
applicant has had status active (as opposed to on hold), which requires at least
one application and an active or upcoming education. Its containing
:code:`PointRule` should be configured to recompute every night.
Applicants spending time studying abroad may still earn ranking points, but
at a reduced rate and up to a maximum, which is also implemented.
Applicants should document their stays abroad to be receive the corresponding
points, but this is not currently enforced by the system.
The point rates are configurable.

:code:`ChildrenRule` simply awards the configured number of points based on
the applicant's provided information on number of children.

:code:`TransportRule` awards points depending on the applicant's distance
from current residence to education. This is based on zip code lists defining
the number of points awarded between residences and educations in various zip
codes. This is explained in more detail in the next
document, :doc:`zipcode_and_area`.

:code:`EducationLocationRule` awards points when an applicant's education is
located in a specific area, configured using the same modeling as
TransportRule above.

:code:`ResidSituationRule` awards points if the applicant's current lease
is temporary but with no termination date set, about to terminate (in 3-12
months) or the applicant is currently homeless. An applicant with lease
terminating less than 3 months qualifies as homeless.
Documentation for the current housing situation is required, and points
will only be awarded if documentation is present and not older than 6 months.


Meta rules
------------
Some rules depend on the result of other rules. A rule
extending :code:`MetaRuleBase` can be configured with a list of IDs of other
PointRules it can then instantiate and compute to take their results into
account.

:code:`ResidParentsRuleSimple` only awards its own configured points
if the configured referenced rules all yield 0 points. This is used for
awarding points for applicants living with parents, but only if
they do not receive points for transport or temporary/terminating lease.

:code:`ResidParentsRuleZipDep` acts in the same way as
:code:`ResidParentsRuleSimple`, but is able to award a different amount of
points for residents in a specific area. This is implemented by instantiating a
ResidParentsRuleSimple, configuring it with the desired number of points and
then calling its compute-method.

:code:`MetaRuleMax` can be configured with a maximum amount of points that
must not be exceeded by its configured rules combined. If they do, this rule
will award a negative number of points to compensate. This is used for
limiting the combined number of points from transport and residence situation.

:code:`MetaRuleMaxCountryDep` can be configured with different max amounts
for applicants residing in different countries.
Similarly to :code:`ResidParentsRuleZipDep`, this is implemented by
instantiating a :code:`MetaRuleMax`, configuring it with the desired
maximum number of points and calling its compute-method.
There is no immediate reason for :code:`MetaRuleMaxCountryDep` not extending
:code:`MetaRuleBase`, so that should probably be changed.

