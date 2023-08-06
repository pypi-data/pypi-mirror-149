import hashlib
import os
import regex as re
from nltk.tokenize import WordPunctTokenizer

class SpaceTokenizer:
    """
    Tokenize by splitting the text on space characters.
    """
    def __init__(self):
        pass

    def tokenize(self, text: str):
        return text.split(' ')


class StopWords:
    """
    Stop word remover using existing lists.
    """
    def __init__(self, custom_stop_words=[], ignore_numbers=False, ignore_punctuation=True, tokenizer=None):
        self.stop_words = self._get_stop_words(custom_stop_words)
        self.ignore_numbers = ignore_numbers
        self.ignore_punctuation = ignore_punctuation
        self.tokenizer = self._get_tokenizer(tokenizer)

    @staticmethod
    def _get_stop_words(custom_stop_words):
        stop_words = {}
        stop_word_dir = os.path.join(os.path.dirname(__file__), 'stop_words')
        for f in os.listdir(stop_word_dir):
            with open('{0}/{1}'.format(stop_word_dir, f), encoding="utf8") as fh:
                for stop_word in fh.read().strip().split('\n'):
                    stop_words[stop_word] = True

        for custom_stop_word in custom_stop_words:
            stop_words[custom_stop_word] = True

        return stop_words


    def _get_tokenizer(self, tokenizer):
        if not tokenizer:
            # If tokenizer is not defined, use simple space tokenizer
            return SpaceTokenizer()
        return tokenizer


    def _is_numerical(self, word):
        if any(chr.isdigit() for chr in word):
            return True
        return False


    def _is_punctuation(self, word):
        if self.ignore_punctuation and re.fullmatch(r"\W+", word):
            return True
        return False


    def remove(self, text):
        if isinstance(text, str):
            return ' '.join([lemma for lemma in self.tokenizer.tokenize(text) if lemma not in self.stop_words and not self._is_numerical(lemma) and not self._is_punctuation(lemma)])

        elif isinstance(text, list):
            return [lemma for lemma in text if lemma not in self.stop_words and not self._is_numerical(lemma) and not self._is_punctuation(lemma)]

        else:
            return None


class TextProcessor:
    """
    Processor for processing texts prior to modelling
    """

    def __init__(self, lemmatizer=None, phraser=None, tokenizer=None, remove_stop_words=True, sentences=False, 
                 words_as_list=False, custom_stop_words=[], input_texts=None, ignore_numbers=False, ignore_punctuation=False, text_hashing=False):
        # processing resources
        self.lemmatizer = lemmatizer
        self.phraser = phraser
        self.tokenizer = tokenizer
        self.word_punct_tokenizer = WordPunctTokenizer()
        self.space_tokenizer = SpaceTokenizer()

        self.stop_words = StopWords(custom_stop_words=custom_stop_words, ignore_numbers=ignore_numbers, ignore_punctuation=ignore_punctuation)
        # processing options
        self.remove_stop_words = remove_stop_words
        self.sentences = sentences
        self.words_as_list = words_as_list
        self.text_hashing = text_hashing
        # this is for when processor is used as an iterator (e.g. for gensim training)
        self.input_texts = input_texts



    def __iter__(self):
        if self.input_texts:
            for input_text in self.input_texts:
                processed = self.process(input_text)
                if processed:
                    yield processed[0]


    def _tokenize_and_lemmatize(self, text):
        """
        Tokenizes and lemmatizes text using MLP if asked.
        :param: str text: Input text to be tokenized & lemmatized.
        :return: Tokenized & lemmatized text.
        """
        # MLP lemmatizer tokenizes text anyway, so we don't need to do it again
        if self.lemmatizer:
            return self.lemmatizer.lemmatize(text)
        # tokenize without lemmatizing
        if self.tokenizer:
            return self.tokenizer.process(text)["text"]["text"]
        # return input text if nothing done
        return text
    

    def _hash_tokens(self, tokens):
        """
        Replaces tokens with MD5 hashes.
        """
        if self.text_hashing:
            return [hashlib.md5(token.encode()).hexdigest() for token in tokens]
        else:
            return tokens


    def process(self, input_text):
        if isinstance(input_text, str):
            stripped_text = input_text.strip()
            if self.sentences:
                list_of_texts = stripped_text.split('\n')
            else:
                list_of_texts = [stripped_text]
        else:
            # whetever obscure was found, output is as string
            list_of_texts = [str(input_text)]
        out = []
        for text in list_of_texts:
            if text:
                # make sure it is a string
                text = str(text)
                # tokenize & lemmatize if asked
                text = self._tokenize_and_lemmatize(text)
                # lower & strip
                text = text.lower().strip()
                # apply word punct tokenizer
                tokens = self.word_punct_tokenizer.tokenize(text)
                # convert string to list of tokens
                #tokens = self.space_tokenizer.tokenize(text)
                # remove stop words
                if self.remove_stop_words:
                    tokens = self.stop_words.remove(tokens)
                # use phraser
                if self.phraser:
                    tokens = self.phraser.phrase(tokens)
                # remove empty tokens
                tokens = [token for token in tokens if token]
                # prepare output
                if not self.words_as_list:
                    tokens = [token.replace(' ', '_') for token in tokens]
                    tokens = self._hash_tokens(tokens)
                    out.append(' '.join(tokens))
                else:
                    tokens = self._hash_tokens(tokens)
                    out.append(tokens)

        # return list of strings
        if self.sentences or self.words_as_list:
            return out
        # return first value as string
        elif out:
            return out[0]
        else:
            return ""
