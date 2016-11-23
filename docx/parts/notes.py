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
    Proxy for the Package parts that contain footnotes and endnotes for a
    Document.
    """

    @property
    def notes(self):
        note_els = []
        if hasattr(self.element, 'footnote_lst'):
            note_els += self.element.footnote_lst
        if hasattr(self.element, 'endnote_lst'):
            note_els += self.element.endnote_lst
        return [Note(n, self) for n in note_els]



class Note(ElementProxy):
    """
    Proxy object wrapping footnotes and endnotes.

    This may not be the most effectively designed class, since this handles
    both footnotes and endnotes, as well as references to them (i.e. all of
    the ``<w:endnoteReference>``, ``<w:footnoteReference>``, ``<w:endnote>``,
    and ``<w:footnote>`` elements.
    """

    __slots__ = ('__notes_by_id', '__paragraphs')


    def __init__(self, element, parent=None):
        super(Note, self).__init__(element, parent=parent)
        self.__notes_by_id = None
        self.__paragraphs = None


    @property
    def name(self):
        tag_name = tag_strip_regex.sub('', self._element.tag)
        return tag_name


    @property
    def id(self):
        if hasattr(self.element, 'id'):
            # the actual note case
            return self.element.id

        # the note reference case
        items = { tag_strip_regex.sub('', k): v
                for k, v
                in self._element.items() }
        return items.get('id', None)


    @property
    def type(self):
        if hasattr(self.element, 'type'):
            return self.element.type

        items = { tag_strip_regex.sub('', k): v
                for k, v
                in self._element.items() }
        return items.get('type', None)


    @property
    def _notes_by_id(self):
        if self.__notes_by_id is None:
            self.__notes_by_id = { n.id: n for n in self.part.document.notes }
        return self.__notes_by_id


    @property
    def paragraphs(self):
        """
        The paragraphs that make up the note.  In the case of note references,
        this method resolves the note reference into its actual note so that
        it can return its paragraphs.
        """
        if self.__paragraphs is None:
            if not hasattr(self.element, 'p_lst'):
                try:
                    relevant_note = self._notes_by_id[self.id]
                except KeyError as e:
                    int_id = int(self.id)
                    relevant_note = self._notes_by_id[int_id]
                self.__paragraphs = relevant_note.paragraphs
            else:
                from ..text.paragraph import Paragraph
                self.__paragraphs = [Paragraph(p, self) for p
                                     in self.element.p_lst]
        return self.__paragraphs
