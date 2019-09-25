import unittest
from lxml import etree
from unittest import TestCase
import spacy

import standoffconverter
import dhspacy

input_xml1 = b'''<W><text type='a'>A B C</text></W>'''
input_xml2 = b'''<W><text type='a'>The answer is 42.</text></W>'''

nlp = spacy.blank("en")

class TestDHSpaCy(unittest.TestCase):
    def test_add_spacy_annotations(self):
                
        tree = etree.fromstring(input_xml2)
        so = standoffconverter.Standoff.from_lxml_tree(tree)

        spacified = nlp(so.plain)
        inds = []
        labels = []
        attributes = []
        for itoken, token in enumerate(spacified):
            if token.is_digit:
                inds.append(itoken)
                labels.append("digit")
                attributes.append({"resp":"spacy"})

        dhspacy.add_spacy_annotations(so, spacified, inds, labels, attributes)

        output_xml = so.to_xml()
        expected_output = "<W><text type='a'>The answer is <digit resp='spacy'>42</digit>.</text></W>"
        self.assertTrue(expected_output == output_xml)  


if __name__ == '__main__':
    unittest.main()