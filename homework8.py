############################################################
# CIS 521: Homework 7
############################################################
# Imports
############################################################
import re
import random
import math
############################################################

student_name = "Jingjing Bai"

############################################################
# Imports
############################################################
import re
import random
import math
############################################################
# Section 1: Markov Models
############################################################

def tokenize(text):
    return re.findall(r"[\w]+|[^\s\w]", text)


def ngrams(n, tokens):
    padded_tokens = ["<START>"]*(n-1) + tokens + ["<END>"]
    return [(tuple(padded_tokens[i-n+1:i]), token)
        for i, token in enumerate(padded_tokens) if i >= n-1]


class NgramModel(object):

    def __init__(self, n):
        self.n = n
        self.context_dic = {}
        self.context_count_dic = {}
        return

    def update(self, sentence):
        for context, token in ngrams(self.n, tokenize(sentence)):
            # keep count
            if context in self.context_count_dic:
                self.context_count_dic[context] += 1
            else:
                self.context_count_dic[context] = 1

            # insert data
            if context in self.context_dic:
                token_dic = self.context_dic.get(context)
                if token in token_dic:
                    token_dic[token] += 1
                else:
                    token_dic[token] = 1
            else:
                self.context_dic[context] = {token: 1}
        return

    def prob(self, context, token):
        if context in self.context_dic:
            token_dic = self.context_dic[context]
            if token in token_dic:
                return float(token_dic[token])\
                    / self.context_count_dic[context]
            else:
                return 0.0
        else:
            return 0.0

    def random_token(self, context):
        r = random.random()

        if context in self.context_dic:
            denominator = self.context_count_dic[context]
            token_dic = self.context_dic[context]
            sorted_keys = sorted(token_dic.keys())

            for i, token in enumerate(sorted_keys):
                minus_i_sum = sum([token_dic[k] for k in sorted_keys[:i]])
                if float(minus_i_sum)/denominator <= \
                   r < float(minus_i_sum +\
                   token_dic[sorted_keys[i]])/denominator:
                    return token

        else:
            return None

    def random_text(self, token_count):

        if self.n != 1:
            context = ("<START>",) * (self.n-1)
            generated = []

            for __ in range(token_count):
                token = self.random_token(context)
                generated.append(token)

                if token != "<END>":
                    context = context[1:] + (token,)
                else:
                    context = ("<START>",) * (self.n-1)

            return " ".join(generated)
        else:
            return " ".join(
                [self.random_token(())
                 for __ in range(token_count)])

    def perplexity(self, sentence):
        product = 0
        tokenized = tokenize(sentence)

        for context, token in ngrams(self.n, tokenized):
            product += math.log(self.prob(context, token))
        return (1/math.exp(product)) ** (float(1)/(len(tokenized)+1))


def create_ngram_model(n, path):
    model = NgramModel(n)

    with open(path, 'r+') as f:
        for line in f:
            model.update(line)

    return model


############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = 3

feedback_question_2 = """
It is hard to think about language models in different languages
"""

feedback_question_3 = """
The slides are easy to follow and implement in the homework
"""
