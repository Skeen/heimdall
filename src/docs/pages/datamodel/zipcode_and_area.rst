----------------------------------
ZipCode, Area and TransportPointSpec
----------------------------------

 .. image:: ../../static/zipcode_and_area.png

For details on the individual classes, inspect the :ref:`API documentation
<Automatic API>`

To model zip codes and areas consisting of multiple zip codes, the datamodel
includes :code:`ZipCode` and :code:`Area` shown above. Rule implementation
classes utilising them are also shown.

A :code:`ZipCode` consists of a four-digit number and an optional town name.
It thus implements the Danish zip code format. Note that the datamodel's
:code:`Address` (not shown) class does not utilise ZipCode.

An :code:`Area` is simply a number of ZipCodes labeled with a name. This is
useful for defining for instance the Roskilde area, and for point zones as
described below.
The system's configuration of Areas can be seen in
:code:`webapp/models/gen/Area.py`.

:code:`TransportPointSpec` stores point specifications for
:code:`TransportRule`. They specify how many points should be awarded for
applicants depending on the area in which they live and in which their
education is located. Generally, for an area
of education (for instance Roskilde or Copenhagen) three Areas and
TransportPointSpecs exist: a central area triggering no transport points (ie.
living downtown, close to the education), a wider circle area triggering a
medium amount of points, and finally the rest of Denmark triggering a
maximum amount of points.
The system's configuration of point specifications can be
seen in :code:`webapp/models/gen/TransportPointSpec.py`.