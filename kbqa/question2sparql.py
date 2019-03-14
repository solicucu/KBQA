import question_temp
import word_tag

# sentence = "What is the username of scc ?" 

# 获取分词列表
sentence_list = [
	"What is the name of littlejun ？",
	"What is the age of chacha ?" ,
	"What is the username of scc ?" ,
	"Whose age is larger than 18 ? " ,
	"What is the phone number of chacha ? " ,
	"What is the password of littlejun ? "
]
def get_sparql(sentence):

	word_list = word_tag.get_word_list(sentence)
	# for w in word_list:
	# 	print(w.token,w.pos,end = " ")
	# print()
	query = None
	queries_dict = dict()
	for rule in question_temp.rules:
		query,num = rule.apply(word_list)
		if(query is not None):
			queries_dict[num] = query

	if len(queries_dict) == 0 :
		return None
	elif len(queries_dict) == 1:
		# 要转化为list才可以用索引访问
		return list(queries_dict.values())[0]
	else:                                     #  key 就是对多元组的排序指定列 item的名字随便，表示列表的元素，item[0] 表示那个值                                       
		sorted_dict = sorted(queries_dict.iteritems(),key=lambda item:item[0],reversed = True)
		return sorted_dict[0][1] 

# for sentence in sentence_list:
# 	print(get_sparql(sentence))

'''
for sentence in sentence_list:
	word_list = word_tag.get_word_list(sentence)
	# for w in word_list:
	# 	print(w.token,w.pos,end = " ")
	# print()
	query = None

	for rule in question_temp.rules:
		query,num = rule.apply(word_list)
		if(query is not None):
			break 

	if(query is None):
		print("sorry,I can't understand your means")
	else:
		print(query,num)
'''