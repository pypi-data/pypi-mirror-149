"""
Utilities related to using reldi in the pipeline.
"""
import re
from reldi_tokeniser.tokeniser import ReldiTokeniser


class ReldiTrainer:
    def __init__(self, lang='sl', type='standard'):
        """ Construct a reldi-based tokenizer by loading the reldi pipeline.
        """
        if lang not in ['sl', 'hr', 'sr', 'bg', 'mk']:
            raise Exception("Reldi tokenizer is currently only allowed in Slovene, Croatian, Serbian, Bulgarian and Macedonian pipelines.")

        nonstandard = False
        if type == 'nonstandard':
            nonstandard = True

        self.tokenizer = ReldiTokeniser(lang, conllu=True, nonstandard=nonstandard, tag=True)

    def tokenize(self, document):
        """ Tokenize a document with the reldi tokenizer and add results to document.conll_file.
        """
        raw_text = '\n'.join(document) if isinstance(document, list) else document
        list_of_lines = [el + '\n' for el in raw_text.split('\n')]

        document = []
        metadocument = []

        for doc in self.tokenizer.run(list_of_lines, mode='object'):
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
