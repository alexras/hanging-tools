#!/usr/bin/env python

import unittest

from make_word import score_word

class TestScoreWord(unittest.TestCase):
    def test_no_mults(self):
        self.assertEqual(score_word("wave", None, None), 11)
        self.assertEqual(score_word("quizzer", None, None), 35)

    def test_double_letter_score(self):
        self.assertEqual(score_word("wave", "double-letter", 3), 16)
        self.assertEqual(score_word("quizzer", "double-letter", 4), 45)

    def test_double_word_score(self):
        self.assertEqual(score_word("wave", "double-word", 3), 22)
        self.assertEqual(score_word("quizzer", "double-word", 3), 70)

    def test_triple_letter_score(self):
        self.assertEqual(score_word("wave", "triple-letter", 3), 21)
        self.assertEqual(score_word("quizzer", "triple-letter", 4), 55)

    def test_triple_word_score(self):
        self.assertEqual(score_word("wave", "triple-word", 3), 33)
        self.assertEqual(score_word("quizzer", "triple-word", 3), 105)


    def test_out_of_bounds_multipliers(self):
        self.assertEqual(score_word("wave", "double-word", 5),
                         score_word("wave", None, None))
        self.assertEqual(score_word("wave", "double-letter", 5),
                         score_word("wave", None, None))
        self.assertEqual(score_word("wave", "triple-letter", 5),
                         score_word("wave", None, None))
        self.assertEqual(score_word("wave", "triple-word", 5),
                         score_word("wave", None, None))


if __name__ == "__main__":
    unittest.main()
