'''
1、What is the name of sb-uname？
2、What is the age of sb-uname ?
3、What is the username of sb-uname?
4、Whose age is larger than number ?
5、What is the phone number of sb-uname?
6、What is the password of sb-name?
'''
from refo import finditer,Predicate,Star,Any,Disjunction
import re

#前缀模板
prefix_temp ="""
    PREFIX ps:<http://solicucu/person/#>
    PREFIX us:<http://solicucu/user/#>
    PREFIX vocab: <http://solicucu/vocab/>
"""

# 问题模板
sparql_select_temp = u"""
	{prefix}
	select distinct {select} where {{
	{expression}
	}}
"""
#两个大括号是表示 一个大括号

# 定义一个词汇类,继承Predicate 
class W(Predicate):
	#token 词汇的字面符号 pos 词汇的属性
	def __init__(self,token=".*",pos=".*"):
		self.token = re.compile(token + "$")
		self.pos = re.compile(pos+"$")
		super(W, self).__init__(self.match) # 不可缺少

	def match(self,word):
		m1 = self.token.match(word.token)
		m2 = self.pos.match(word.pos)
		return m1 and m2

# 定义一些规则，相当与正则表达式的某个模式
class Rule(object):
	#匹配的条件数 和条件，以及action 回调函数
	def __init__(self,condition_num,condition=None,action=None):
		assert condition and action 
		self.condition = condition
		self.action = action 
		self.condition_num = condition_num

	def apply(self,word_list):
		#因为可能满足条件的有多处，所以用matches列表存储
		matches = []
		# 用条件去找匹配的词汇，finditer 里面用到了yeild，就是每次找到一个结果返回一次，继续找
		# 可以理解为finditer 返回的值可以迭代
		for m in finditer(self.condition,word_list):
			i,j = m.span()
			matches.extend(word_list[i:j]) # 提取出被匹配的句子区间划出，其中可能有其他杂词汇

		return self.action(matches),self.condition_num

class KeywordRule(object):
	#匹配的条件数 和条件，以及action 回调函数
	def __init__(self,condition=None,action=None):
		assert condition and action 
		self.condition = condition
		self.action = action 

	def apply(self,word_list):
		#因为可能满足条件的有多处，所以用matches列表存储
		matches = []
		# 用条件去找匹配的词汇，finditer 里面用到了yeild，就是每次找到一个结果返回一次，继续找
		# 可以理解为finditer 返回的值可以迭代
		for m in finditer(self.condition,word_list):
			i,j = m.span()
			matches.extend(word_list[i:j]) # 提取出被匹配的句子区间划出，其中可能有其他杂词汇

		if(len(matches)>0):
			return self.action() # 无条件返回了
		return None 



attr_list = ["name","username","age","password","phone"]
# 问题模板
sparql_select_temp = u"""
	{prefix}
	select {select} where {{
	{expression}
	}}
"""


## 定义相关规则
pos_whp = "WP"
pos_number = "CD"
pos_common_noun = "NN"


class AttrQuestionSet:
	def __init__(self):
		pass
	# 1 what is the name of sb-uname ?
	@staticmethod
	def what_name(word_list):
		# if(len(word_list)):
		# 	print("成功匹配问题")
		# 	for w in word_list:
		# 		print(w.token,end = " ")
		
		sparql = None
		select = "?name"
		for w in reversed(word_list):
			# 找到第一个普通名词
			if(w.pos == pos_common_noun): 
				e = " ps:{person} vocab:person_name ?name .".format(person = w.token)
				sparql = sparql_select_temp.format(prefix = prefix_temp, 
					                               select = select,
					                               expression = e)
				break

		return sparql 

	# 2  What is the age of sb-uname ?
	@staticmethod
	def what_age(word_list):

		sparql = None
		select = "?age"
		for w in reversed(word_list):
			# 找到第一个普通名词
			if(w.pos == pos_common_noun): 
				e = " ps:{person} vocab:person_age ?age .".format(person = w.token)
				sparql = sparql_select_temp.format(prefix = prefix_temp, 
					                               select = select,
					                               expression = e)
				break

		return sparql 

	# 3  What is the username of sb-uname?
	@staticmethod
	def what_username(word_list):

		sparql = None
		select = "?username"
		for w in reversed(word_list):
			# 找到第一个普通名词
			if(w.pos == pos_common_noun): 
				e = " ?s vocab:person_name '{person}' .\n" \
				    " ?s vocab:person_username ?username .".format(person = w.token)

				sparql = sparql_select_temp.format(prefix = prefix_temp, 
					                               select = select,
					                               expression = e)
				break

		return sparql 

	# 4 What is the phone number of sb-uname?
	@staticmethod
	def what_phone(word_list):

		sparql = None
		select = "?phone"
		for w in reversed(word_list):
			# 找到第一个普通名词
			if(w.pos == pos_common_noun): 
				e = " ps:{person} vocab:person_phone ?phone .".format(person = w.token)
				sparql = sparql_select_temp.format(prefix = prefix_temp, 
					                               select = select,
					                               expression = e)
				break

		return sparql 
	# 5 What is the password of sb-name?
	@staticmethod
	def what_password(word_list):
		sparql = None
		select = "?password"
		for w in reversed(word_list):
			# 找到第一个普通名词
			if(w.pos == pos_common_noun): 
				e = " us:{person} vocab:user_password ?password .".format(person = w.token)
				sparql = sparql_select_temp.format(prefix = prefix_temp, 
					                               select = select,
					                               expression = e)
				break

		return sparql 

attr_question = {
	"name":AttrQuestionSet.what_name,
	"username":AttrQuestionSet.what_username,
	"age":AttrQuestionSet.what_age,
	"phone":AttrQuestionSet.what_phone,
	"password":AttrQuestionSet.what_password
}

class QuestionSet:
	def __init__(self):
		pass 
	@staticmethod
	def proccess_attr_noun(word_list):
		for r in attr_keyword_rules:

			attr_noun = r.apply(word_list)  # 返回的是一个字符串

			if(attr_noun is not None): # 只有关键字不为空才能调用
				return attr_question[attr_noun](word_list) #查询特定属性，定位问题
				
		
	# 6 Whose age is larger than 18 ?
	def who_age_compare(word_list):

		sparql = None
		select = "?username"

		# 确认关键词是larger 或者 smaller
		mark = None
		for  r in compare_rules:
			mark = r.apply(word_list)
			if(mark is not None):
				break 
		for w in reversed(word_list):
			if(w.pos == pos_number):  #???
				e = " ?s vocab:person_age ?age .\n" \
				    " ?s vocab:person_username ?username .\n" \
					" filter(?age {mark} {number})".format(mark = mark, number = w.token)
				sparql = sparql_select_temp.format(prefix = prefix_temp, 
					                               select = select,
					                               expression = e)
				break 

		return sparql 
		

class KeywordValue:
	def __init__(self):
		pass

	@staticmethod
	def get_name():
		return "name"
	@staticmethod
	def get_username():
		return "username"
	@staticmethod
	def get_age():
		return "age"
	@staticmethod
	def get_phone():
		return "phone"
	@staticmethod
	def get_password():
		return "password"
	@staticmethod
	def get_bigger():
		return ">"
	@staticmethod
	def get_smaller():
		return "<"



# 疑问代词关键字 who what 
what = (W("what")|W("What"))
whose = (W("whose")|W("Whose"))
of = W("of")
wh_entity = (what | whose)

number_entity = W(pos="CD")

# 属性关键字
username = W("username")
name = W("name")
phone = W("phone")
age  = W("age")
password = W("password")

attr_noun  = (username | name | phone | phone | age | password)
#普通名词
common_noun = W(pos = pos_common_noun) 

#比较关键词
larger = (W("bigger")|W("larger"))
smaller = (W("smaller")|W("lower"))
compare = (larger | smaller )


rules = [
	# What is the name of sb-uname？
	# What is the age of sb-uname ?
	# What is the username of sb-uname?
	# What is the phone number of sb-uname?
	# What is the password of sb-name?
	Rule(condition_num = 3 ,condition = what + Star(Any(),greedy = False) + attr_noun + Star(Any(),greedy = False) + of + common_noun + Star(Any(),greedy = False),action = QuestionSet.proccess_attr_noun),
	# Whose age is larger than 18 ?
	Rule(condition_num = 4,condition = whose + attr_noun + Star(Any(),greedy = False) + compare + Star(Any(),greedy = False) + number_entity + Star(Any(),greedy = False),action = QuestionSet.who_age_compare )
]

# 合并的好处是，减少上面的规则数，遍历更快，如果吧下面的放在上面，拿那么如果访问比较多最后一类，那效率就很低
attr_keyword_rules = [
	KeywordRule(condition = what + Star(Any(),greedy = False) + name + Star(Any(),greedy = False) + of + common_noun + Star(Any(),greedy = False),action = KeywordValue.get_name),
	KeywordRule(condition = what + Star(Any(),greedy = False) + age + Star(Any(),greedy = False) + of + common_noun + Star(Any(),greedy = False),action = KeywordValue.get_age),
	KeywordRule(condition = what + Star(Any(),greedy = False) + username + Star(Any(),greedy = False) + of + common_noun + Star(Any(),greedy = False),action = KeywordValue.get_username ),
	KeywordRule(condition = what + Star(Any(),greedy = False) + phone + Star(Any(),greedy = False) + of + common_noun + Star(Any(),greedy = False),action =KeywordValue.get_phone ),
	KeywordRule(condition = what + Star(Any(),greedy = False) + password + Star(Any(),greedy = False) + of + common_noun + Star(Any(),greedy = False),action = KeywordValue.get_password)
]
compare_rules = [
	KeywordRule(condition = Star(Any(),greedy = False) + larger + Star(Any(),greedy = True),action = KeywordValue.get_bigger),
	KeywordRule(condition = Star(Any(),greedy = False) + smaller + Star(Any(),greedy = True),action = KeywordValue.get_smaller ),

]

