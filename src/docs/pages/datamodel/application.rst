-------------------------------
Application and Offer
-------------------------------
 .. image:: ../../static/application.png

Only key fields are shown in the above diagram.
For details on the individual classes, inspect the
:ref:`API documentation <Automatic API>`

An applicant may create any number of :code:`Applications`, each referencing
an :code:`ApplicationTarget`. If an
:code:`Application`'s target is any of  :code:`ApprobationCommittee`,
:code:`Building` and :code:`TenancyGroup` (not shown), the semantic is that the
application applies for all child tenancies of the target.

Some tenancies require two residents. In this case, two applicants must
register an :code:`Application` together to be eligible for offers on such a
tenancy. To do this, one applicant must create an application and
subsequently invite the second applicant with an :code:`ApplicationInvite`.
If the recipient accepts, he/she will be registered on the application as well.
Note that there is no distinction between the two applicants on an
application. Neither is considered primary nor secondary, and both are able
to for cancel the application and respond to offers received from it.

The applications will appear on dynamically computed waiting lists for each
of their tenancies. When a tenancy becomes available, an administrative user
may choose to create an :code:`Offer` for that tenancy, and send the offer
to a subset of the applications on the waiting list. This is modeled with
instances of the :code:`OfferSent` class, which links the offer to a
specific receiving application, and which subsequently will store response
(accept or reject) from the applicant(s).
An :code:`Offer` has a deadline, before which applicants must respond.
If no response is given before the deadline, it counts as a rejection.

An :code:`Offer` can be in one of the following states:

Editing
    The offer has been created, but not yet sent to any applications/applicants.

Open
    The offer has been sent, and is awaiting responses from applicants.

Finished
    The offer deadline has passed, and applicants may no longer respond to
    the offer.

Closed
    The offer was closed by assigning the tenancy to one of the recipients, who
    will then become the new tenant.

Aborted
    The offer was closed without assigning the tenancy to anyone.

A nightly background job (implemented using the Celery framework)
automatically checks if any open :code:`Offer` has passed its deadline, and if
so changes the state from 'open' to 'finished'.
