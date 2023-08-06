"""
Utilities related to using reldi in the pipeline.
"""
import re

import obeliks


def check_reldi():
    """
    Import necessary components from reldi to perform tokenization.
    """
    try:
        import classla
    except ImportError:
        raise ImportError(
            "Reldi is used but not present on your machine. Make sure you run 'git submodule init' and 'git submodule update' commands."
        )
    return True


class ObeliksTrainer():
    def __init__(self, lang='sl', type='standard', annotate_pos=False):
        """ Construct a reldi-based tokenizer by loading the reldi pipeline.
        """
        if lang not in ['sl']:
            raise Exception("Obeliks tokenizer is currently only allowed in Slovene.")

    @staticmethod
    def tokenize(document):
        """ Tokenize a document with the obeliks tokenizer and add results to appropriate format.
        """
        raw_text = '\n'.join(document) if isinstance(document, list) else document

        document = []
        metadocument = []

        for doc in obeliks.run(raw_text, object_output=True):
            for sentence in doc:
                for word in sentence['sentence']:
                    if word['lemma'] == '_':
                        del (word['lemma'])
                    if word['xpos'] == '_':
                        del (word['xpos'])
                    if word['upos'] == '_':
                        del (word['upos'])
                    if word['misc'] == '_':
                        del (word['misc'])
                document.append(sentence['sentence'])
                metadocument.append(sentence['metadata'])

        return raw_text, document, metadocument
