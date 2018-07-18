-----------------------------
Paragraph
-----------------------------
The datamodel includes a simple way of storing arbitrary UI text, namely the
:code:`Paragraph` model:

 .. image:: ../../static/paragraph.png

The :code:`name` of :code:`ParagraphGroup` must be unique and should be
suitable for lookup of the instance. A :code:`Paragraph` should then by uniquely
identified by its group's name along with its own, though there is no
enforcement of uniqueness for :code:`Paragraph.name`.
:code:`Paragraph` then contains :code:`heading` and :code:`text` for display
in UI.
