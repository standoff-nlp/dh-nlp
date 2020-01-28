import standoffconverter
import spacy

def init(nlp):
    return DHnlp(nlp)


class DHDoc:
    
    def __init__(self, text, standoff, doc):
        self.standoff = standoff
        self.doc = doc

    def get_char_inds(self, spacy_obj):

        if type(spacy_obj) == spacy.tokens.token.Token:
            begin_token = spacy_obj
            end_token = spacy_obj

        elif len(spacy_obj) == 1:
            begin_token = spacy_obj[0]
            end_token = spacy_obj[0]

        else:
            begin_token = spacy_obj[0]
            end_token = spacy_obj[-1]

        begin_char_without_excludes = self.standoff["begin"] + begin_token.idx

        begin_char = begin_char_without_excludes

        end_char_without_excludes = begin_char + (end_token.idx - begin_token.idx) + len(end_token)

        end_char = end_char_without_excludes
        return begin_char, end_char


class DHnlp:

    def __init__(self, nlp):
        self.nlp = nlp
        self.docs = []

    def __call__(self, filtersets):

        texts, standoffs = [],[]
        for ap in filtersets:
            texts.append(ap.get_text())
            standoffs.append(ap.so.__dict__)

        spacified = list(self.nlp.pipe(texts))

        for text, standoff, doc in zip(texts, standoffs, spacified):
            self.docs.append(DHDoc(text, standoff, doc))

        for doc in self.docs:
            yield doc





# def add_spacy_annotations(so, doc, inds, labels, attributes, depths=None, unique=True):
#     """add a standoff annotations from a spacy document.

#     In order to add annotations from a spacy document, the annotations need to be 
#     converted from token-level annotations to character-level annotations

#     arguments:
#     so standoffconverter object -- A standoffconverter object to that the annotations 
#                                     should be added.
#     doc (spacy.tokens.Doc) -- A Document that was created from self.plain
#     inds (list) -- the list of *token* indices
#     labels (list) -- the list of labels to be used as XML tags
#     attributes (list) -- the list of attributes (dicts) to be used as XML attributes

#     keyword arguments:
#     depths (list) -- list of depths for each attribute. The depth specifies the order 
#                         of XML tags that have the same beginning and ending index.
#                         for the same begin and end, a lower depth annotation includes 
#                         a higher depth annotation.
#     unique (bool) -- whether to allow for duplicate annotations
#     """

#     if depths is None:
#         depths =  [None]*len(inds)
    
#     assert (doc.text == so.plain), "spacy document does not fit the so.plain text."

#     assert len(inds) == len(labels) == len(attributes) == len(depths), "new standoff\
#         params have to have all same lengths."

#     tokeni2idx = {t.i:(t.idx,t.idx+tchar) for t in doc for tchar in range(len(t.text)+1)} 

#     for ind, label, attribute, depth in zip(inds, labels, attributes, depths):
#         begin, end = tokeni2idx[ind]
#         so.add_annotation(begin, end, label, depth, attribute, unique)