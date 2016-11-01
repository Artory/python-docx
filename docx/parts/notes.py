# encoding: utf-8

"""
Provides NotesPart and related objects
"""
import re

from ..opc.part import XmlPart
from ..shared import ElementProxy


tag_strip_regex = re.compile(r'{.*}')


class NotesPart(XmlPart):
    """
    Proxy for the notes.xml part containing footnotes and endnotes for a
    document.
    """

    @property
    def notes(self):
        return [Notes(n) for n in self.element.notes_lst]

class Note(ElementProxy):
    """
    Proxy object wrapping the ``<w:endnoteReference>`` and
    ``<w:footnoteReference>`` elements.
    """

    __slots__ = ()

    @property
    def name(self):
        tag_name = tag_strip_regex.sub('', self._element.tag)
        return tag_name

    @property
    def id(self):
        items = { tag_strip_regex.sub('', k): v
                for k, v
                in self._element.items() }
        return items.get('id', None)
