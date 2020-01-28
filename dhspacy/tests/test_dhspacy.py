import unittest
from lxml import etree
from unittest import TestCase
import spacy

import standoffconverter
import dhspacy

input_xml = '''<W>
    <text type="a">
        <p label="CARDINAL">three</p>
        <p type="b">The answer is 42.</p>
        <p type="b">The answer is 43.</p>
        <p type="b">The answer is 44.</p>
        <p type="b">The answer is 45.</p>
    </text>
    <text type="a">
        <p type="b">The answer is 46.</p>
        <p type="b">The answer is 47.</p>
        <p type="b">The answer is 48.</p>
    </text>
</W>'''

nlp = spacy.blank("en")

class TestDHSpaCy(unittest.TestCase):

    def test_get_char_inds(self):
        tree = etree.fromstring(input_xml)
        so = standoffconverter.Converter.from_tree(tree)


        filterset = so.collection[0].xpath("//p")
        dhnlp = dhspacy.init(nlp)

        for dhdoc in dhnlp(filterset):

            for token in dhdoc.doc:
                begin, end = dhdoc.get_char_inds(token)
                self.assertTrue(
                    so.plain[begin:end] == token.text
                )

if __name__ == '__main__':
    unittest.main()