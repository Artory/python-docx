# encoding: utf-8

"""
Custom element classes related to foot and endnotes (CT_Note).
"""

from .ns import qn
from .simpletypes import ST_NoteType, XsdInt
from .xmlchemy import (
    BaseOxmlElement, OptionalAttribute, ZeroOrMore, ZeroOrOne
)


class CT_Footnotes(BaseOxmlElement):
    """
    ``<w:footnotes>`` element, the root element of a footnotes.xml file
    """
    footnotes = ZeroOrOne('w:footnotes')

    @property
    def footnote_lst(self):
        """
        Return a list containing a reference to each ``<w:footnote>`` element
        in the footnotes.xml file, in the order encountered.
        """
        return self.xpath('.//w:footnote')


class CT_Footnote(BaseOxmlElement):
    """
    ``<w:footnote>`` element, containing the properties and text for a footnote.
    """
    type = OptionalAttribute('w:type', ST_NoteType)
    id = OptionalAttribute('w:id', XsdInt)

    rPr = ZeroOrOne('w:rPr')
    p = ZeroOrMore('w:p')


class CT_Endnotes(BaseOxmlElement):
    """
    ``<w:endnotes>`` element, the root element of a endnotes.xml file
    """
    endnotes = ZeroOrOne('w:endnotes')

    @property
    def endnote_lst(self):
        """
        Return a list containing a reference to each ``<w:endnote>`` element
        in the endnotes.xml file, in the order encountered.
        """
        return self.xpath('.//w:endnote')


class CT_Endnote(BaseOxmlElement):
    """
    ``<w:endnote>`` element, containing the properties and text for a endnote.
    """
    type = OptionalAttribute('w:type', ST_NoteType)
    id = OptionalAttribute('w:id', XsdInt)

    rPr = ZeroOrOne('w:rPr')
    p = ZeroOrMore('w:p')
