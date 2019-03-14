from stanfordcorenlp import StanfordCoreNLP
import nltk
from nltk.tree import Tree as nltkTree

nlp = StanfordCoreNLP(r'D:\\stanford-corenlp\\stanford-corenlp-full-2018-10-05') 

class Word:
	def __init__(self,token = ".*",pos = ".*"):
		self.token = token
		self.pos = pos 


def get_word_list(sentence):

	return [Word(word,pos) for word, pos in nlp.pos_tag(sentence)]


sentence_list = [
	"What is the name of littlejun ？",
	"What is the age of chacha ?" ,
	"What is the username of scc ?" ,
	"Whose age is larger than 18 ? " ,
	"What is the phone number of chacha ? " ,
	"What is the password of littlejun ? "
]

# for s in sentence_list:
# 	word_list = [Word(word,pos) for word, pos in nlp.pos_tag(s)]

# 	for w in word_list:
# 		print(w.token,": ",w.pos,end = " ")
# 	print()