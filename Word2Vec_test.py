# -*- coding=utf-8 -*-
from GetWordSeq import *
from Huffman import *
import math
from sklearn import preprocessing
import numpy as np


# 输出函数
def sigmoid(value):
	return 1/(1+math.exp(-value))


def is_stop_word(word):
	if len(word) == 0:
		return True
	return False


class Word2Vec:

	def __init__(self, vec_len=15000, learn_rate=0.025, win_len=5):
		"""

		:param vec_len: the num of vector
		:param learn_rate:
		:param win_len:
		"""
		self.cutted_text_list = None
		self.vec_len = vec_len
		self.learn_rate = learn_rate
		self.win_len = win_len
		self.word_dict = None  # each element is a dict, including: word,possibility,vector,huffmancode
		self.huffman = None  # the object of HuffmanTree

	def build_word_dict(self, word_freq):
		# word_dict = {word: {word, freq, possibility, init_vector, huffman_code}, }
		word_dict = {}
		freq_list = [x[1] for x in word_freq]
		sum_count = sum(freq_list)
		for item in word_freq:
			temp_dict = dict(
					word=item[0],
					freq=item[1],
					possibility=item[1] / sum_count,
					vector=np.random.random([1, self.vec_len]),
					Huffman=None
			)
			word_dict[item[0]] = temp_dict
		self.word_dict = word_dict

	def train(self, word_list, model='cbow', ignore=0):
		# build word_dict and huffman tree
		if self.huffman is None:
			if self.word_dict is None:
				counter = WordCounter(word_list)
				self.build_word_dict(counter.count_res.larger_than(ignore))
				self.cutted_text_list = counter.word_list
			self.huffman = HuffmanTree(self.word_dict, vec_len=self.vec_len)
		# get method
		if model == 'cbow':
			method = self.CBOW
		else:
			method = self.SkipGram
		# start to train word vector
		before = (self.win_len - 1) >> 1
		after = self.win_len - 1 - before
		total = len(self.cutted_text_list)
		count = 0
		for line in self.cutted_text_list:
			line_len = len(line)
			for i in range(line_len):
				word = line[i]
				if is_stop_word(word):
					continue
				context = line[max(0, i - before):i] + line[i + 1:min(line_len, i + after + 1)]
				method(word, context)
			count += 1

	def CBOW(self, word, context):
		if not word in self.word_dict:
			return
		# get sum of all context words' vector
		word_code = self.word_dict[word]['code']
		gram_vector_sum = np.zeros([1, self.vec_len])
		for i in range(len(context))[::-1]:
			context_gram = context[i]  # a word from context
			if context_gram in self.word_dict:
				gram_vector_sum += self.word_dict[context_gram]['vector']
			else:
				context.pop(i)
		if len(context) == 0:
			return
		# update huffman
		error = self.update_huffman(word_code, gram_vector_sum, self.huffman.root)
		# modify word vector
		for context_gram in context:
			self.word_dict[context_gram]['vector'] += error
			self.word_dict[context_gram]['vector'] = preprocessing.normalize(self.word_dict[context_gram]['vector'])

	def SkipGram(self, word, gram_word_list):
		if not word in self.word_dict:
			return
		word_vector = self.word_dict[word]['vector']
		for i in range(len(gram_word_list))[::-1]:
			if not gram_word_list[i] in self.word_dict:
				gram_word_list.pop(i)
		if len(gram_word_list) == 0:
			return
		for u in gram_word_list:
			u_huffman = self.word_dict[u]['code']
			error = self.update_huffman(u_huffman, word_vector, self.huffman.root)
			self.word_dict[word]['vector'] += error
			self.word_dict[word]['vector'] = preprocessing.normalize(self.word_dict[word]['vector'])

	def update_huffman(self, word_code, input_vector, root):
		node = root
		error = np.zeros([1, self.vec_len])
		for level in range(len(word_code)):
			branch = word_code[level]
			p = sigmoid(input_vector.dot(node.value.T))
			grad = self.learn_rate * (1 - int(branch) - p)
			error += grad * node.value
			node.value += grad * input_vector
			node.value = preprocessing.normalize(node.value)
			if branch == '0':
				node = node.right
			else:
				node = node.left
		return error

	def __getitem__(self, word):
		if not word in self.word_dict:
			return None
		return self.word_dict[word]['vector']


if __name__ == '__main__':
	# data = ['Merge multiple sorted inputs into a single sorted output',
     #        'The API below differs from textbook heap algorithms in two aspects']
	# wv = Word2Vec(vec_len=50)
	# wv.train(data, model='cbow')
	# print(wv['into'])
	print('测试')
	file = open('news/education.txt', 'r', encoding='utf-8')
	sentence_list = []
	for txt in file.readlines():
		txt = txt.replace(r'[', '').replace(r']', '').strip()
		txt = ''.join(txt.split())
		sentence_list.append(txt)
	file.close()
	print(len(sentence_list))