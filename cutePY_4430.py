#Nikos Bampalis,4430,cse84430 

import sys
import string 
import random

class Token: 

    

    def __init__(self,recognised_string,family,line_number):

        self.recognised_string = recognised_string
        self.family = family
        self.line_number = line_number



    def __str__(self):
        return f'string: {self.recognised_string}\tfamily: {self.family}\tline_number: {self.line_number}'



class Lex:


	def __init__(self,file_name,current_line):
		self.file_name = file_name
		self.current_line = current_line
		self.token = Token(None,None,None)
		


	def next_token(self):	

		#alphabet for seperation between identifiers
		alphabet={"keywords": ["main","def","#def",
					"#int","global",
					"if","elif","else",
					"while",
					"print",
					"return",
					"input","int",
					"and","or","not"]}
		
		state = "start"
		

		while(state!="finito"):

			inp = self.file_name.read(1) # read one characted at a time
			self.token.line_number = self.current_line

			
			#Beggining lex_analyzer's algorithm
			if( inp.isspace()==True and inp!= '\n'): # avoid whitespace characters in the beggining
				inp.replace(inp,"")


			elif( state == "start" and  inp.isdigit() ): # searching for number

				state = "dig"
				self.token.recognised_string = inp
				self.token.family = "numbers"
				inp = self.file_name.read(1)
				if(inp.isspace()==True and inp == '\n'):
					self.current_line+=1
					state = "finito"
				elif(inp.isspace()==True):
					inp.replace(inp,"")
					state = "finito"
				else:
					pos = self.file_name.tell()  #In order to not consume the last character we read
					self.file_name.seek(pos-1,0) 

			elif(  state == "dig" and inp.isdigit()  ):
				self.token.recognised_string += inp


			elif( state == "dig" ):

				if(int(self.token.recognised_string) >= (-(32767)) and int(self.token.recognised_string) <= 32767): # defined by pronunciation
					state = "finito"
				else:
					raise Exception("Value beyond accepted limitations at "+" line" + str(self.token.line_number)) 
				pos = self.file_name.tell()    #In order to not consume the last character we read
				self.file_name.seek(pos-1,0) 

			elif( state == "start" and  ((inp >= 'a' and inp <= 'z') or (inp >= 'A' and inp <= 'Z')) ): # search for identifier or keyword
					
				state = "idk"
				self.token.recognised_string = inp
				self.token.family = "identifier"
				inp = self.file_name.read(1)
				if(inp.isspace()==True and inp == '\n'):
					self.current_line+=1
					state = "finito"
				elif(inp.isspace()==True):
					inp.replace(inp,"")
					state = "finito"
				else:
					pos = self.file_name.tell()
					self.file_name.seek(pos-1,0) #In order to not consume the last character we read


			elif( state == "idk" and  ((inp >= 'a' and inp <= 'z') or (inp >= 'A' and inp <= 'Z')  or inp.isdigit()) ):

				self.token.recognised_string += inp
				if( self.token.recognised_string in alphabet.get("keywords") ): 
					self.token.family = "keywords"
					state = "finito"
					
					
			elif( state == "idk" ):
					
				pos = self.file_name.tell()    #In order to not consume the last character we read
				self.file_name.seek(pos-1,0)
				state = "finito"
					

			
			elif( state == "start" and (inp == "+" or inp == "-") ): # search for add-minus operator

				self.token.recognised_string = inp
				self.token.family = "addoperator"
				state = "finito"


			elif( state == "start" and  (inp == "*" or inp == "/" or inp == "%") ): # search for mul-div operator

				self.token.recognised_string =inp
				self.token.family = "muloperator"
				if(inp=="/"):

					if(self.file_name.read(1)=="/"):
						self.token.recognised_string = "//"
						state = "finito"
					else:
						raise Exception("False use of characters at "+" line" + str(self.token.line_number))

				state = "finito"
				

			elif( state == "start" and ( inp =="(" or inp == "#" or inp == ")" ) ) 	: # search for groubsymbols
					

				self.token.recognised_string = inp
				self.token.family = "GroupSymbols"
				if(inp=="#"):

					y = self.file_name.read(1)
					self.token.recognised_string += y
					if(y=="i" or y=="d"):
						for i in range(2): # the two words we are looking for is #def and #int , that's why we need two steps 
							y = self.file_name.read(1) 
							self.token.recognised_string += y
						if(self.token.recognised_string in alphabet.get("keywords")):
							self.token.family = "keywords"
							state = "finito"
						else:
							raise Exception("There is no such word in mininal++ at "+ " line" + str(self.token.line_number) )

					elif(y=="#"): # first duo of comments
						self.token.family = "Comments"
						x = self.file_name.read(1)
						while(x!='#'):
							x = self.file_name.read(1)
						if(x == "#"):
							if(self.file_name.read(1)=="#"): # second duo of comments
								state = "finito"
							else:
								raise Exception("Wrong use of comments at "+ " line" + str(self.token.line_number))
						else:
							raise Exception("Wrong use of comments at "+ " line" + str(self.token.line_number))


					elif(y == "}" or y == "{"):
						state = "finito"

					else:
						raise Exception("Incorrect use of #  at "+" line" + str(self.token.line_number))

				state = "finito"
			



			elif( state == "start" and  (inp==',' or inp==':') ):  #search for demiliter symbols

				self.token.recognised_string = inp 
				self.token.family = "delimiter"
				state="finito"


			elif( state == "start" and (inp == "<" or inp == ">" or inp == "=" or inp == "!") ): #search for reloperator 

				self.token.recognised_string = inp
				self.token.family = "reloperator" 
				if(inp == "="):
					if(self.file_name.read(1) == "="):
						state = "finito"
					else:
						self.token.family= "assignment"
						state = "finito"
						pos = self.file_name.tell()
						self.file_name.seek(pos-1,0)

				elif(inp == "<"):

					y = self.file_name.read(1)
					if(y == ">" or y == "!"):
						raise Exception("Incorrect use of reloperator at "+" line" + str(self.token.line_number))
					elif(y == "="):
						self.token.recognised_string += y
					else:
						pos = self.file_name.tell()		#In order to not consume the last character we read
						self.file_name.seek(pos-1,0)
					state = "finito"

				elif(inp == ">"):

					y = self.file_name.read(1)
					if(y == "<" or y == "!"):
						raise Exception("Incorrect use of reloperator at "+" line" + str(self.token.line_number))
					elif(y == "="): 
						self.token.recognised_string += y
					else:
						pos = self.file_name.tell() 	#In order to not consume the last character we read
						self.file_name.seek(pos-1,0)
					state = "finito"

				else:

					if(self.file_name.read(1) == "="):
						self.token.recognised_string = "!="
						state = "finito"
					else:
						raise Exception("Incorrect use of reloperator at "+" line" + str(self.token.line_number))




			elif( inp == '' ):
				self.token.recognised_string = "EOF"
				state = "finito"
				#exit In order you want to run only lex_analyzer


				
			elif( inp == '\n' ):
				self.current_line += 1

				

			else:
				raise Exception("ERRORRR")
					

		if((self.token.family=="identifier" and len(self.token.recognised_string) > 30) ):
			raise Exception("Use of no valid identifier or expression at line " + str(self.token.line_number) + "!!")
		else:

			return self.token
	
	

		
	

class Parser:
	
	global global_variables,def_names,total_def_names
	global_variables = list()
	def_names = list()
	total_def_names = list()

	def __init__(self,lexical_analyzer):

		global quad
		self.lexical_analyzer = lexical_analyzer
		quad = Quad(99,'','','','')


	
	def syntax_analyzer(self):

		global token 
		token = self.get_token()
		self.program()
		if(token.recognised_string == "EOF"):
			print('compilation successfully completed!!!!')
			


	def get_token(self):

		global tok
		tok = self.lexical_analyzer.next_token()
		if(tok.recognised_string == "##"):
			self.get_token()
		return tok
		
		
	def program(self):

		global token,quad,table,scope
		self.declarations()
		table = Table()
		self.functions()
		self.call_main_part()
		

		
	def functions(self):

		global token,quad
		self.function()
		while(token.recognised_string == "def"): 
			self.function()
	

	def function(self):

		global token,quad,scope,table
		if(token.recognised_string == "def"):
			token = self.get_token()
			try:
				scope.level
				scope = Scope(scope.level+1)
				table.add_scope(scope)
			except:
				scope = Scope(0)
				table.add_scope(scope)
				pass
			def_names.append(token.recognised_string)
			total_def_names.append(token.recognised_string)
			if(token.family == "identifier"):
				token = self.get_token()
				if(token.recognised_string == "("):
					token = self.get_token()
					self.var_list()
					if(token.recognised_string == ")"):
						token = self.get_token()
						if(token.recognised_string == ":"):
							token = self.get_token()
							if(token.recognised_string =="#{"):
								token = self.get_token()
								self.declarations()
								self.functions()
								quad.genQuad("begin_block",def_names[-1],'','')
								self.globals()
								self.code_block()
								if(token.recognised_string == "#}"):
									#print
									table.close_scope()
									quad.genQuad("end_block",def_names[-1],'','')
									def_names.pop()
									token = self.get_token()
								else:
									sys.exit("End of comments expected at line "+str(token.line_number)+"!")
							else:	
								sys.exit("Start of comments expected at line "+str(token.line_number)+"!")
						else:
							sys.exit("Delimiter expected at line "+str(token.line_number)+"!")
					else:
						sys.exit("Groupsymbol ) expected at line "+str(token.line_number)+"!")
				else:
					sys.exit("Groupsymbol ( expected at line "+str(token.line_number)+"!")
			

		



	def declarations(self):
		global token,quad
		while(token.recognised_string=="#int"):
			token = self.get_token()
			if(token.family=="identifier"):
				global_variables.append(token.recognised_string)
				token = self.get_token()
				while(token.recognised_string==","):
					token = self.get_token()
					if(token.family=="identifier"):
						global_variables.append(token.recognised_string)
						token = self.get_token()
					else:
						sys.exit("ID expected at line "+str(token.line_number)+"!")

	def var_list(self):

		global token,quad,scope,offset
		if(token.family=="identifier"):
			token = self.get_token()
			while(token.recognised_string==","):
				token = self.get_token()
				if(token.family=="identifier"):
					token = self.get_token()
				else:
					sys.exit("ID expected at line "+str(token.line_number)+"!")
		
	def globals(self):

		global token,quad

		if(token.recognised_string == "global"):
			token = self.get_token()
			if(token.recognised_string in global_variables):
				token = self.get_token()
				while(token.recognised_string==","):
					token = self.get_token()
					if(token.recognised_string in global_variables):
						token = self.get_token()
					else:
						sys.exit("Global ID  expected at line "+str(token.line_number)+"!")
			else:
				sys.exit("Global ID  expected at line "+str(token.line_number)+"!")



	def assignment_stat(self):

		global token,quad
		if(token.family == "identifier"):
			ID = token.recognised_string  
			if(ID in total_def_names):
				token = self.get_token()
				self.idtail()
				quad.genQuad('call','','',ID)
			else:
				token = self.get_token()
				if(token.family == "assignment"):
					token = self.get_token()
					if(token.recognised_string == "int"):
						token = self.get_token()
						if(token.recognised_string == "("):
							token = self.get_token()
							if(token.recognised_string == "input"):
								token = self.get_token()
								w = quad.newTemp()
								quad.genQuad('in','int','',w)
								if(token.recognised_string == "("):
									token = self.get_token()
									if(token.recognised_string == ")"):
										token = self.get_token()
										if(token.recognised_string == ")"):
											quad.genQuad('=',w,'',ID)
											token = self.get_token()
										else:
											sys.exit("Groupsymbol ) expected at line "+str(token.line_number)+"!")
									else:	
										sys.exit(" expected at line "+str(token.line_number)+"!")
								else:
									sys.exit("Groupsymbol ( expected at line "+str(token.line_number)+"!")
							else:
								sys.exit("Input expected at line "+str(token.line_number)+"!")
						else:
							sys.exit("Groupsymbol ( expected at line "+str(token.line_number)+"!")
					else:
						self.expression()
						quad.genQuad('=',E_place,'',ID)
				else:
					sys.exit("Assignment expected at line "+str(token.line_number)+"!")




	def print_stat(self):

		global token,quad,E_place
		if(token.recognised_string=="("):
			token = self.get_token()
			self.expression()
			quad.genQuad('out',E_place,'','')
			if(token.recognised_string==")"):
				token = self.get_token()
			else:
				sys.exit("Groupsymbol ) expected at line "+str(token.line_number)+"!")
		else:
			sys.exit("Groupsymbol ( expected at line "+str(token.line_number)+"!")
		


	def return_stat(self):
		
		global token,quad,E_place
		self.expression()
		quad.genQuad("ret",E_place,'','')


	def statement(self):

		global token,quad
		if(token.family=="identifier" or token.recognised_string=="return" or token.recognised_string=="print"):
			self.simple_statement()
		elif(token.recognised_string=="if" or token.recognised_string=="while"):
			self.structured_statement()


	def code_block(self):

		global token,quad
		self.statement()
		while(token.family=="identifier" or token.recognised_string=="return" or token.recognised_string=="print" or token.recognised_string=="if" or token.recognised_string=="while"):
			self.statement()

	def statement_or_block(self):
		
		global token,quad
		if(token.recognised_string == "#{"):
			token = self.get_token()
			self.code_block();
			if(token.recognised_string == "#}"):
				token = self.get_token()
			else:
				sys.exit("Groupsymbol expected at line "+str(token.line_number)+"!")
		elif(token.family == "identifier" or token.recognised_string == "return" or token.recognised_string == "print" or token.recognised_string == "if" or token.recognised_string == "while"):
			self.statement()


	def simple_statement(self):

		global token,quad
		if(token.family=="identifier"):
			self.assignment_stat()
		elif(token.recognised_string=="print"):
			token = self.get_token()
			self.print_stat()
		elif(token.recognised_string=="return"):
			token = self.get_token()
			self.return_stat()


	def structured_statement(self):

		global token,quad
		if(token.recognised_string=="if"):
			token = self.get_token()
			self.if_stat()
		elif(token.recognised_string=="while"):
			token = self.get_token()
			self.while_stat()

	def if_stat(self):

		global token,quad
		self.condition()
		quad.backpatch(Condition_true,quad.nextQuad())
		ifList = []
		elifList = []
		if(token.recognised_string==":"):
			token = self.get_token()
			self.statement_or_block()
			ifList = quad.makeList(quad.nextQuad())
			quad.genQuad('jump','','','')
			quad.backpatch(Condition_false,quad.nextQuad())
			while(token.recognised_string=="elif"):
				token = self.get_token()
				self.condition()
				quad.backpatch(Condition_true,quad.nextQuad())
				if(token.recognised_string==":"):
					token = self.get_token()
					self.statement_or_block()
					elifList = quad.makeList(quad.nextQuad())
					quad.genQuad('jump','','','')
					quad.backpatch(Condition_false,quad.nextQuad())
				else:
					sys.exit("Delimiter expected at line "+str(token.line_number)+"!")	
			if(token.recognised_string == "else"):
				token = self.get_token()
				if(token.recognised_string == ":"):
					token = self.get_token()
					self.statement_or_block()
				else:
					sys.exit("Delimiter expected at line "+str(token.line_number)+"!")	
			quad.backpatch(ifList,quad.nextQuad())
			quad.backpatch(elifList,quad.nextQuad())
		else:
			sys.exit("Delimiter expected at line "+str(token.line_number)+"!")	
		
		
		
				
		
		

	def while_stat(self):

		global token,quad,Condition_true,Condition_false
		condQuad = quad.nextQuad()
		self.condition()
		quad.backpatch(Condition_true,quad.nextQuad())
		if(token.recognised_string==":"):
			token = self.get_token()
			self.statement_or_block()
			quad.genQuad("jump",'','',condQuad)
			quad.backpatch(Condition_false,quad.nextQuad())
		else:
			sys.exit("Delimiter expected at line "+str(token.line_number)+"!")		
			
		

	
	def expression(self):

		global token,quad,E_place,T_place,opt_sign
		try:
			token.recognised_string == '+' or '-'
			self.optional_sign()	
			b = quad.newTemp()
			quad.genQuad(opt_sign,0,token.recognised_string,b)
			T1_place = b 
		except:
			T1_place = token.recognised_string
			pass
		self.term()
		if(T_place):
				T1_place = T_place
		while(token.family == "addoperator"):
			sign = token.recognised_string  #in order to save wheth er it is +/-
			token = self.get_token()
			T2_place = token.recognised_string
			self.term()
			if(T_place):
				T2_place = T_place
			w = quad.newTemp()
			quad.genQuad(sign, T1_place, T2_place, w)
			T1_place = w
			
		E_place = T1_place

				

	def term(self):

		global token,quad,T_place
		T1_place = token.recognised_string
		self.factor()
		while(token.family=="muloperator"):
			sign = token.recognised_string
			token = self.get_token()
			T2_place = token.recognised_string
			self.factor()
			w = quad.newTemp()
			quad.genQuad(sign, T1_place, T2_place, w)
			T1_place = w

			
		T_place = T1_place



	def factor(self):

		global token,quad
		if(token.family=="numbers"):
			token = self.get_token()
		elif(token.recognised_string=="("):
			token = self.get_token()
			self.expression()
			if(token.recognised_string==")"):
				token = self.get_token()
		elif(token.family=="identifier"):
			function_name = token.recognised_string
			token = self.get_token()
			self.idtail()
			if(function_name in total_def_names):
				w = quad.newTemp()
				quad.genQuad('par',w,'ret','')	
				quad.genQuad('call','','',function_name)
			


	def idtail(self):

		global token,quad
		if(token.recognised_string=="("):
			token = self.get_token()
			self.actual_par_list()
			if(token.recognised_string==")"):
				token = self.get_token()

	def actual_par_list(self):

		global token,quad
		self.expression()
		quad.genQuad('par',E_place,'CV','')
		while(token.recognised_string==","):
			token = self.get_token()
			self.expression()
			quad.genQuad('par',E_place,'CV','')

	
		
	def optional_sign(self):

		global token,quad,flag,opt_sign
		if(token.family=="addoperator"):
			opt_sign = token.recognised_string
			token = self.get_token()


	def condition(self):

		global token,quad,Condition_true,Condition_false
		self.bool_term()
		Condition_true = Bool_term_true
		Condition_false = Bool_term_false
		while(token.recognised_string=="or"):
			quad.backpatch(Condition_false,quad.nextQuad())
			token = self.get_token()
			self.bool_term()
			Condition_true = quad.mergeList(Condition_true,Bool_term_true)
			Condition_false = Bool_term_false

	def bool_term(self):

		global token,quad,Bool_term_true,Bool_term_false
		self.bool_factor()
		Bool_term_true = Bool_factor_true
		Bool_term_false = Bool_factor_false
		while(token.recognised_string=="and"):
			quad.backpatch(Bool_term_true,quad.nextQuad())
			token = self.get_token()
			self.bool_factor()
			Bool_term_false = quad.mergeList(Bool_term_false,Bool_factor_false)
			Bool_term_true = Bool_factor_true	


	def bool_factor(self):

		global token,quad,Bool_factor_true,Bool_factor_false
		if(token.recognised_string=="not"):
			token = self.get_token()
			self.expression()
			T1_place = E_place
			if(token.family == "reloperator"):
				comp_oper = token.recognised_string #stands for comparison reloperator
				token = self.get_token()
				self.expression()
				T2_place = E_place
				Bool_factor_false = quad.makeList(quad.nextQuad())
				quad.genQuad(comp_oper,T1_place,T2_place,'')
				Bool_factor_true = quad.makeList(quad.nextQuad())
				quad.genQuad('jump','','','')

		elif(token.family == "addoperator" or token.family == "numbers" or token.family == "identifier" or token.recognised_string == "("):	
			self.expression()
			T1_place = E_place
			if(token.family=="reloperator"):
				comp_oper = token.recognised_string #stands for comparison operator
				token = self.get_token()
				self.expression()
				T2_place = E_place
				Bool_factor_true = quad.makeList(quad.nextQuad())
				quad.genQuad(comp_oper,T1_place,T2_place,'')
				Bool_factor_false = quad.makeList(quad.nextQuad())
				quad.genQuad('jump','','','')

			else:
				sys.exit("Reloperator expected at line "+str(token.line_number)+"!")
		

	



	def call_main_part(self):

		global token,quad,scope,table
		if(token.recognised_string == "#def"):
			token = self.get_token()
			try:
				scope.level
				scope = Scope(scope.level+1)
				table.add_scope(scope)
			except:
				scope = Scope(0)
				table.add_scope(scope)
				pass
			if(token.recognised_string == "main"):
				quad.genQuad("begin_block","main",'','')
				token = self.get_token()
				self.declarations()
				self.code_block()
				#print
				table.close_scope()
				quad.genQuad('halt','','','')
				quad.genQuad("end_block","main",'','')
				

	
	

	

class Quad:
	
	global temporary_variables
	temporary_variables = []
	global programList	
	programList = []

	


	def __init__(self,label,operator,operand1,operand2,operand3):

		global quad
		self.label = label 
		self.operator = operator
		self.operand1 = operand1
		self.operand2 = operand2
		self.operand3 = operand3
		
		

	


	def genQuad(self,operator,operand1,operand2,operand3):

		global quad 
		quad = Quad(self.nextQuad(),operator,operand1,operand2,operand3) #it has to be named quad in main 
		programList.append(quad)
		return quad

	def nextQuad(self):

		global quad
		return quad.label + 1

	def newTemp(self):

		global quad
		next_var = len(temporary_variables) + 1
		temporary_variables.append("T_" + str(next_var))
		return temporary_variables[-1]

	def emptyList(self):
		
		global empty_list
		empty_list = []
		return empty_list


	def makeList(self,label):

		global label_list
		label_list = [label]
		return label_list


	def mergeList(self,list1,list2):

		global merge_list
		merge_list = list1 + list2
		return merge_list

	def backpatch(self,listt,label):

		for x in listt:
			for y in range(0,len(programList)): 
				if(programList[y].label == x):
					programList[y].operand3 = label
		listt.clear()


from abc import ABCMeta

class Entity(metaclass=ABCMeta):

	def __init__(self,name):
		self.name = name
		super(Entity,self).__init__()
		


class Scope:

	global entity_list  #list of entity for each level
	entity_list = []

	def __init__(self,level):

		self.level = level


class Table:

	def __init__(self):
		
		self.sum_scope = [] #list of scopes for final table 

	def add_Entity(self,name):
		self.sum_scope[-1].entity_list.append(name)

	def add_scope(self,scope):
		self.sum_scope.append(scope)

	def close_scope(self):
		self.sum_scope.pop()

	#def update_fields(self,framelength,startingQuad):
		#for x in self.sum_scope[-1].entity_list:

	#def search_record(self,name):
		#i = -1
		#for x in self.sum_scope[-1].entity_list:
			#if(x == name):
				#return 



class Variable(Entity):

	def __init__(self,name,datatype,offset):

		super().__init__(name)
		self.datatype = datatype
		self.offset = offset


class TemporaryVariable(Variable,Entity):
	pass


class Parameter(Variable):

	def __init__(self,name,datatype,offset,mode):

		Variable.__init__(self,name,datatype,mode)
		self.mode = mode


class FormalParameter:

	def __init__(self,datatype,mode):

		self.datatype = datatype 
		self.mode = mode


class Function(Entity):

	def __init__(self,name,datatype,startingQuad,framelength,formalParameters):

		super().__init__(name)
		self.datatype = datatype 
		self.startingQuad = startingQuad 
		self.framelength = framelength 
		self.formalParameters = formalParameters




class SymbolicConstant(Entity):

	def __init__(self,name,datatype,value):

		super().__init__(name)
		self.datatype = datatype 
		self.value = value



if __name__=="__main__":
	x = sys.argv[1]
	with open(x,"r+") as file_name:
		y = Lex(file_name,1)
		d = Parser(y)
		d.syntax_analyzer()
		#z = input("Are you ready for the first step of the compilation? ") #Comment syntax_analyzer and you can run lex until the end of file
		#while(file_name):
			#token = y.next_token()
			#print(token)
			#if(token.recognised_string == 'EOF'):
				#break
	

	str_string = string.ascii_letters + string.digits
	gen_string = random.choice(str_string) + '.int'
	int_outpout  = open(gen_string,"w+")
	for x in programList:
		int_outpout.write(str(x.operator) +'\b'+ str(x.operand1) +'\b'+  str(x.operand2) +'\b'+  str(x.operand3) +'\b'+  str(x.label) +'\n')
