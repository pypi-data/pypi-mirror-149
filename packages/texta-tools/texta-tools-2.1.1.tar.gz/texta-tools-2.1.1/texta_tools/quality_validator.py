import os
import math
import pickle
from typing import List


class QualityValidator:
    """ Validates the quality of a text: does it contain any actual words?
        Useful for validating OCR output.
    """
    def __init__(self):
        self.model_dir = os.path.join(os.path.dirname(__file__), "models", "gibberish_model.pki")
        self.model = pickle.load(open(self.model_dir, "rb"))
        self.accepted_chars = "abcdefghijklmnopqrstuvwxyzõäöü "
        self.pos = dict([(char, idx) for idx, char in enumerate(self.accepted_chars)])


    def _normalize(self, line: str) -> List[str]:
        """ Return only the subset of chars from accepted_chars.
        This helps keep the  model relatively small by ignoring punctuation,
        infrequently symbols, etc.
        """
        return [c.lower() for c in line if c.lower() in self.accepted_chars]


    def _ngram(self, n: int, text: str):
        """ Return all n grams from text after normalizing.
        """
        filtered = self._normalize(text)
        for start in range(0, len(filtered) - n + 1):
            yield "".join(filtered[start:start + n])


    def _get_avg_transition_prob(self, text: str, log_prob_mat: float) -> float:
        """ Return the average transition prob from text through log_prob_mat.
        """
        log_prob = 0.0
        transition_ct = 0
        for a, b in self._ngram(2, text):
            log_prob += log_prob_mat[self.pos[a]][self.pos[b]]
            transition_ct += 1
        # The exponentiation translates from log probs to probs.
        return math.exp(log_prob / (transition_ct or 1))


    def is_valid(self, text: str) -> bool:
        """ Check if text contains valid content.
        """
        model_mat = self.model['mat']
        threshold = self.model['thresh'] + 0.01 # Use a bit higher threshold

        if not self._get_avg_transition_prob(text, model_mat) > threshold:
            return False
        return True
