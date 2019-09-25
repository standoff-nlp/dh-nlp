

def add_spacy_annotations(so, doc, inds, labels, attributes, depths=None, unique=True):
    """add a standoff annotations from a spacy document.

    In order to add annotations from a spacy document, the annotations need to be 
    converted from token-level annotations to character-level annotations

    arguments:
    so standoffconverter object -- A standoffconverter object to that the annotations 
                                    should be added.
    doc (spacy.tokens.Doc) -- A Document that was created from self.plain
    inds (list) -- the list of *token* indices
    labels (list) -- the list of labels to be used as XML tags
    attributes (list) -- the list of attributes (dicts) to be used as XML attributes

    keyword arguments:
    depths (list) -- list of depths for each attribute. The depth specifies the order 
                        of XML tags that have the same beginning and ending index.
                        for the same begin and end, a lower depth annotation includes 
                        a higher depth annotation.
    unique (bool) -- whether to allow for duplicate annotations
    """

    if depths is None:
        depths =  [None]*len(inds)
    
    assert (doc.text == so.plain), "spacy document does not fit the so.plain text."

    assert len(inds) == len(labels) == len(attributes) == len(depths), "new standoff\
        params have to have all same lengths."

    tokeni2idx = {t.i:(t.idx,t.idx+tchar) for t in doc for tchar in range(len(t.text)+1)} 

    for ind, label, attribute, depth in zip(inds, labels, attributes, depths):
        begin, end = tokeni2idx[ind]
        so.add_annotation(begin, end, label, depth, attribute, unique)