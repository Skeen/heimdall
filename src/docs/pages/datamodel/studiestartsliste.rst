----------------------------------
Planned extension: Studiestartslisten
----------------------------------

When educations start in September, housing applicants have an option to
apply via  a special scheme, "Studiestartslisten". In this
case, an applicant will apply for all tenancies fulfilling certain
conditions and within a reasonable range of their place of education. In
return, they receive a significant amount of extra points. The
applicant may only reject a limited number of offers before losing the extra
points.

Below is shown a suggestion for an extension of the datamodel for supporting
this.

 .. image:: ../../static/studiestartsliste.png

Classes :code:`SCList`, :code:`SpecialConditions` are suggested model
additions. :code:`SpecialCondListComputer` and :code:`ListComputerSSL` are
regular Python classes. The others are existing models.

The exact specification of which tenancies are to be included for a given
applicant should be obtained from UBS. This proposal supports a set of
tenancies computed uniquely for each applicant.

An instance of :code:`SpecialConditions` models a specific scheme of
conditions, for instance Studiestartslisten. It references an implementation
class (a :code:`SpecialCondListComputer`) that is able to compute a list of
tenancies for a given applicant. Note: The signature of the compute_list-method
should be defined in  interface :code:`SpecialCondListComputer`.
Once computed, the list is persisted as an :code:`SCList`. The system creates
the necessary applications, that will be tagged as created by the system. The
applicant may not cancel these applications individually, but may choose to
leave the Studiestartsliste which will cancel all of them.

A new point rule implementation class (not shown) should then award suitable
points for the applicant for the correct tenancies. The PointRule model
should be extended as shown, with an optional reference to a
SpecialConditions instance. Since PointValues (not
shown) are tied directly to applicants, and not applications, the point rule
implementation class will have to perfom a lookup to check if an applicant
has a system-created application for the right instance of SpecialConditions.