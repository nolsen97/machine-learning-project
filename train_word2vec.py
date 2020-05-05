# -*- coding: utf-8 -*-

import word2vec

word2vec.word2phrase('./text8', './text8-phrases', verbose=True)
word2vec.word2vec('./text8-phrases', './text8.bin', size=100, verbose=True)

# model = word2vec.load('../project_extra/text8.bin')
# indexes, metrics = model.similar("dog")

# print(model.generate_response(indexes, metrics).tolist())
