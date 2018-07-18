-----------------------------
Message
-----------------------------

The system implements messaging between applicants and administrators based
on the models below:

 .. image:: ../../static/message.png

Messages are sent between Django :code:`User` instances, and are always
between an administrator and an applicant (or multiple applicants). The
applicant's :code:`User` instance will be referenced by a corresponding
:code:`Applicant` instance. An administrative :code:`User` exists solely as
such, with no further modeling.

To model that a message may have multiple recipients, its model is split in
:code:`MessageContent` which references the sender and contains the actual
message text, and a :code:`Message` instance for each recipient, referencing
the recipient and also storing a boolean indicating whether the recipient has
read the message.

A new message will give rise to a new :code:`MessageThread`, and subsequent
responses will be attached to the same thread. The :code:`status` field
indicates to the administrators whether any action is currently needed in
relation to this correspondance.

Both :code:`MessageThread` and :code:`MessageContent` have a :code:`subject`
field. The relationship between these is unclear to the author (Ubbe, April
18 2018).

Sending a message happens simply by creating the appropriate
:code:`MessageContent` and :code:`Message` instances. Applicants should have
the option to receive an email when they have a new message, but this was not
yet implemented at the time of writing (April 18 2018).