from SPARQLWrapper import SPARQLWrapper, JSON
import question2sparql as q2s 

sparql = SPARQLWrapper("http://localhost:3030/db/query")
sparql.setReturnFormat(JSON)

if __name__ == "__main__":
	# sentence = "What is the username of scc ?" 
	
	while True:
		sentence = input("please input the question ? input quit to leave\n")
		# print("question:",sentence)
		if(sentence == "quit"):
			break 
		str_sparql = q2s.get_sparql(sentence)
		if(str_sparql is not None):
			sparql.setQuery(str_sparql)
			results = sparql.query().convert()

			head =  results["head"]["vars"]
			values = results["results"]["bindings"] # 存储的结果
			if(len(values)==0):
				print("no relevant answer")
			else:
				print("the answer is :",end = " ")
				for v in values:  # 对于所有value ，通过varname 获取其值
					for varname in head:
						print(v[varname]["value"])
		else:
			print("sorry,I can't understand your means")