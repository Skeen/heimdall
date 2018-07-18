-----------------------------
Applicant
-----------------------------
Another key part of the datamodel is the :code:`Applicant`, which
models the physical people that apply for tenancies.

 .. image:: ../../static/applicant.png

Only key fields are shown in the above diagram.
For details on the individual classes, inspect the
:ref:`API documentation <Automatic API>`

An :code:`Applicant` is a person that wishes to apply for tenancies in
the system. The :code:`Applicant` model holds a number of data fields
with various information that is used to determine whether this applicant is
eligible to apply, and how many points should be awarded for his/her
applications. These can be inspected in the API documentation. Details on key
relations with other models are given below.

An :code:`Applicant` always has a one-to-one mapping with a :code:`User`,
which is part of the Django framework. This enables the applicant to log in
to the system. The applicant's name and email is also stored here. We use
applicants' email as their username, so the presence of both username and
email fields is redundant. This could be improved by configuring Django
to use a custom user model instead of the current default one.

Administrative users may make internal :code:`Notes` on applicants. These may
contain any special information on the applicant's situation that cannot be
stored elsewhere. The notes are only visible to administrative users, not the
applicants themselves.

An applicant may register any number of :code:`Educations` with start and end
dates. Applicants must have one active (or upcoming within three months)
education to be eligible to apply for tenancies.

In some cases applicants must upload material to document their situation
and thus be eligible to apply and receive the correct amount of points
for appliations. When uploaded, these documents are stored in the
:code:`DocumentForApplicant` model.

:code:`Applicant` has two relations to :code:`Message`. In the case where an
applicant via a message has been reminded to upload documentation for
transportation or residence situation, the relations point out the concrete
(latest) message. This enables the system to check the date of the last
message and thus avoid repeating messages.

An applicant may create any number of :code:`Applications`, each referencing
an :code:`ApplicationTarget`.
Some tenancies require two residents. In this case, two applicants must
register an :code:`Application` together to be eligible for offers on such a
tenancy. To do this, one applicant must create an application and
subsequently invite the second applicant with an :code:`ApplicationInvite`.
If the recipient accepts, he/she will be registered on the application as well.
Note that there is no distinction between the two applicants on an
application. Neither is considered primary nor secondary, and both are able
to cancel the application and respond to offers received from it.

The :code:`ApplicantCommitteeProperties` class models applicant data that is
specific to an approbation committee, such as approval status and latest
renewal date.

Applicants may be active or on hold. This is modeled
by the :code:`StatusChange` class, whose instances contain a date of the
change and a status label indicating the new status. The model thus maintains
a trace of historical status changes.
Possible values for the status field are :code:`active`, :code:`abroad`,
:code:`on_hold` and :code:`deleted`. To be active and earn points, an applicant
must have at least one application, and one active or upcoming education. An
inactive applicant will not receive any housing offers, and does not earn any
points. An applicant abroad earns points at a reduced rate.
The points are calculated by :code:`webapp.domain.pointrules.DateRankingRule`
which is introduced in :doc:`point_rule_impl_classes`.
A :code:`StatusChange` caused by the beginning/end of a stay abroad will hold
a reference to the :code:`StayAbroad` instance. This makes it easier to
verify that a :code:`StayAbroad` has created the correct status changes.
A nightly background job defined in :code:`webapp/tasks/status_abroad.py`
detects any starting or ending :code:`StayAbroad` and creates corresponding
:code:`StatusChanges`.

Applicants may be put (temporarily) in quarantine if they for instance reject
one or more housing offers. This is modeled by the :code:`QuarantinePeriod`
class. An applicant in quarantine may not receive any housing offers.

The diagram shows that :code:`Applicant`,
:code:`ApplicantCommitteeProperties`, :code:`Education` and :code:`Address`
extend the abstract :code:`HistoricalModel`. This enables historic revisions
of those objects to be saved whenever content of data fields is changed. The
same mechanism is in place for the Django :code:`User` model, but since we
cannot add a superclass to the Django User class, the history is enabled
with a few lines in :code:`webapp/apps.py` instead.
The model history framework is documented at
`<https://django-simple-history.readthedocs.io/en/latest>`_