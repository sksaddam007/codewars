import re
import collections

operators = { '+': True, '-': True, '*': True, '/': True}

operations = { '+': lambda a,b : a+b, '-': lambda a,b : a-b, '*': lambda a,b : a*b, '/': lambda a,b : a/b }

def samePrecedence(operator1, operator2):
  return (operator1 == operator2) or (operator1 == '*' and operator2 == '/') or (operator1 == '/' and operator2 == '*') or (operator1 == '+' and operator2 == '-') or (operator1 == '-' and operator2 == '+')

def higherPrecedence(operator1, operator2):
  return (operator1 == '*' or operator1 == '/') and (operator2 == '+' or operator2 == '-')

def higherOrSamePresendence(operator1, operator2):
  return samePrecedence(operator1, operator2) or higherPrecedence(operator1, operator2)


class Compiler(object):
    
    def compile(self, program):
        return self.pass3(self.pass2(self.pass1(program)))
        
    def tokenize(self, program):
        """Turn a program string into an array of tokens.  Each token
           is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
           name or a number (as a string)"""
        token_iter = (m.group(0) for m in re.finditer(r'[-+*/()[\]]|[A-Za-z]+|\d+', program))
        return [int(tok) if tok.isdigit() else tok for tok in token_iter]
      
    def parseArguments(self, tokens):
      errorMessage = 'Invalid argument list.'
      args = {}
      argCount = 0
      for i in range(0,len(tokens)):
        token = tokens[i]
        if (i == 0 and token != '['):
          raise Exception(errorMessage)
        elif (i > 0):
          if (token == ']'):
            return args, i
          args[token] = argCount
          argCount += 1
      raise Exception(errorMessage)
      
    def tokensToAST(self, args, tokens):
      outputStack = []
      operatorStack = collections.deque([])
      def pushOperation():
        output_dict = {}
        sinl_dict = {}
        sinl_dict['op']= operatorStack.popleft()
        b = outputStack.pop()
        a = outputStack.pop()
        sinl_dict['a']= a
        sinl_dict['b']= b
        outputStack.append(sinl_dict)
      for i in range(0,len(tokens)):
        token = tokens[i]
        if (not (token in operators) and token != '(' and token != ')') :
          if (type(token) is int):
            outputStack.append({ 'op': 'imm', 'n': token })
          else:
            outputStack.append({ 'op': 'arg', 'n': args[token]})
        elif (token in operators):
          while (len(operatorStack) and higherOrSamePresendence(operatorStack[0], token)):
            pushOperation()
          operatorStack.append(token)
          operatorStack.rotate(1)
        elif (token == '('):
          operatorStack.append(token)
          operatorStack.rotate(1)
        elif (token == ')'):
          while (len(operatorStack) and operatorStack[0] != '('):
            pushOperation()
          if operatorStack[0] == '(':
            operatorStack.popleft()
      while (len(operatorStack)):
        pushOperation();
      return outputStack.pop()

    def pass1(self, program):
        """Returns an un-optimized AST"""
        tokens = self.tokenize(program);
        args, i = self.parseArguments(tokens)
        return self.tokensToAST(args, tokens[i+1:])
      
    def performOperation(self, node):
      if (operators.get(node['op'])):
        if (node['a']['op'] != 'imm'):
          node['a'] = self.performOperation(node['a'])
        if (node['b']['op'] != 'imm'):
          node['b'] = self.performOperation(node['b'])
        if (node['a']['op'] == 'imm' and node['b']['op'] == 'imm'):
          return { 'op': 'imm', 'n': operations[node['op']](node['a']['n'], node['b']['n'])}
      return node
  
    def pass2(self, ast):
        """Returns an AST with constant expressions reduced"""
        return self.performOperation(ast)

    def pass3(self, ast):
      """Returns assembly instructions"""
      operationInstructions = { 
        '+': 'AD',
        '-': 'SU',
        '*': 'MU',
        '/': 'DI'
      }
      def generateCode(node):
        if (operationInstructions.get(node['op'])):
          return [*generateCode(node['a']), 'PU', *generateCode(node['b']), 'SW', 'PO', operationInstructions[node['op']]]
        instructions = collections.deque([])
        if (node['op'] == 'imm'):
          instructions.append(f"IM {node['n']}")
          instructions.rotate(1)
        elif (node['op'] == 'arg'):
          instructions.append(f"AR {node['n']}")
          instructions.rotate(1)
        return list(instructions)
      return generateCode(ast)

