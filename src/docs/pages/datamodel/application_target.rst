---------------------------
ApplicationTarget
---------------------------
At the core of the datamodel is the :code:`ApplicationTarget` hierarchy,
which models the buildings and tenancies that are administered by the system.

 .. image:: ../../static/application_target.png

Only key fields are shown in the above diagram.
For details on the individual classes, inspect the
:ref:`API documentation <Automatic API>`

The key classes here are :code:`ApplicationTarget` and subclasses
:code:`ApprobationCommittee`, :code:`Building`, :code:`TenancyGroup` and
:code:`Tenancy`.

An :code:`ApprobationCommittee` is an organisation administering allocation of
tenancies to eligible applicants. The committee administers a number of
:code:`Buildings` each containing a number of named :code:`TenancyGroups`,
which in turn each contains a number of :code:`Tenancies`. The committee thus
forms the root of a tree with tenancies as leaves.
Applicants create :code:`Applications` to apply for tenancies. If an
:code:`Application`'s target is any of  :code:`ApprobationCommittee`,
:code:`Building` and :code:`TenancyGroup`, the semantic is that the
application applies for all child tenancies of the target.

A :code:`Building` can actually represent multiple co-located physical
buildings. The possibly more suitable name Property was bypassed to avoid
confusion.
A :code:`Building` has an attached :code:`BuildingAdministrator`
which is responsible for the operation of the building. This is the entity
the approbation committee notifies (by phone or email) when a tenancy in the
building has been allocated.
A :code:`Building` also has an attached :code:`Caretaker`, who is usually an
employee of the :code:`BuildingAdministrator`. When a tenancy is not
inhabited, the caretaker is the point of contact for applicants to visit the
tenancy before responding to an offer.

A :code:`TenancyGroup` is a logical grouping of identical or similar
:code:`Tenancies` within a :code:`Building`.

A :code:`Tenancy` models an actual flat or dorm room. It holds a reference to
an :code:`Address` which describes it's physical address. Note that the
:code:`Address` class is referenced by many other classes not shown here.

:code:`Tenancy` and :code:`TenancyGroup` both hold a reference to a
:code:`TenancyProperties` object. This describes detailed properties of a
tenancy, such as number of rooms, area in squaremeters, and
facilities. In case a Tenancy does not have its properties reference set, its
group's properties will be applicable instead. The enables changing properties
for an entire tenancy group at once. This inheritance of a group's
properties was not yet implemented at the time of writing (March 27 2018).

For modelling expenses such as rent, electricity and
deposit, :code:`TenancyProperties` can have a number of :code:`Expense`
instances attached. They simply specify a monetary amount, and in turn
reference an :code:`ExpenseDefinition` which names the expense, e.g.
'electricity'. This way, the same :code:`ExpenseDefinition` can be reused
for different tenancies with their own :code:`Expense` instances, thus
promoting reuse of expense names.

Note that the references between :code:`Tenancy` and :code:`TenancyGroup`,
:code:`TenancyGroup` and :code:`Building`, and :code:`Building` and
:code:`ApprobationCommittee` all are implemented on top of
:code:`ApplicationTarget`'s parent-children-link which is persisted in the
database.

:code:`Building` and :code:`Tenancy` both extend :code:`Publishable` and
:code:`Deletable`.
Note that both are marked as abstract, which means they do not give rise to
corresponding database tables. Instead, their fields are added to the tables of
their subclasses.
:code:`Pulishable` adds a 'publishtime' field. Tenancies or
Buildings with no publishtime (or one in the future) should not be visible to
applicants. Implementation of this behavior was unverified as of April 5 2018.
:code:`Deletable` adds a deletetime field. This enables marking an
object as deleted while still retaining it in the database.

An :code:`ApplicationTarget` may also define a number of
:code:`AbstractRules`, describing constraints on as well as points for
applications.
This is described in more detail in :doc:`constraints_and_points`.

:code:`TenancyProfile` was an idea for aggregating tenancies in predefined
groups, such as "1-room flats in Copenhagen center" or similar. This would
mean, however, that the hierarchy under an ApprobationCommittee would not be
constrained to a tree. For this reason, TenancyProfile is not in use at the
time of writing (April 2 2018).

:code:`HasProperties` was intended to allow administrative users to dynamically
define fields on models. It is elaborated in :doc:`has_properties`.