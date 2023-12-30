##################### BOILERPLATE BEGINS ############################

# Token types enumeration
##################### YOU CAN CHANGE THE ENUMERATION IF YOU WANT #######################
from collections import defaultdict
class TokenType:
    IDENTIFIER = "IDENTIFIER"
    KEYWORD = "KEYWORD"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    SYMBOL = "SYMBOL"

# Token hierarchy dictionary
token_hierarchy = {
    "if": TokenType.KEYWORD,
    "else": TokenType.KEYWORD,
    "print": TokenType.KEYWORD
}


# helper function to check if it is a valid identifier
def is_valid_identifier(lexeme):
    if not lexeme:
        return False

    # Check if the first character is an underscore or a letter
    if not (lexeme[0].isalpha() or lexeme[0] == '_'):
        return False

    # Check the rest of the characters (can be letters, digits, or underscores)
    for char in lexeme[1:]:
        if not (char.isalnum() or char == '_'):
            return False

    return True


# Tokenizer function
def tokenize(source_code):
    tokens = []
    position = 0

    while position < len(source_code):
        # Helper function to check if a character is alphanumeric
        def is_alphanumeric(char):
            return char.isalpha() or char.isdigit() or (char=='_')

        char = source_code[position]

        # Check for whitespace and skip it
        if char.isspace():
            position += 1
            continue

        # Identifier recognition
        if char.isalpha():
            lexeme = char
            position += 1
            while position < len(source_code) and is_alphanumeric(source_code[position]):
                lexeme += source_code[position]
                position += 1

            if lexeme in token_hierarchy:
                token_type = token_hierarchy[lexeme]
            else:
                # check if it is a valid identifier
                if is_valid_identifier(lexeme):
                    token_type = TokenType.IDENTIFIER
                else:
                    raise ValueError(f"Invalid identifier: {lexeme}")

        # Integer or Float recognition
        elif char.isdigit() or (char == '-' and position + 1 < len(source_code) and source_code[position + 1].isdigit()):
            lexeme = char
            position += 1
            is_float = False
            while position < len(source_code):
                next_char = source_code[position]
                # checking if it is a float, or a full-stop
                if next_char == '.':
                    if (position + 1 < len(source_code)):
                        next_next_char = source_code[position+1]
                        if next_next_char.isdigit():
                            is_float = True

                # checking for illegal identifier
                elif is_alphanumeric(next_char) and not next_char.isdigit():
                    while position < len(source_code) and is_alphanumeric(source_code[position]):
                        lexeme += source_code[position]
                        position += 1
                    if not is_valid_identifier(lexeme):
                        raise ValueError(f"Invalid identifier: {str(lexeme)}\nIdentifier can't start with digits")

                elif not next_char.isdigit():
                    break

                lexeme += next_char
                position += 1

            token_type = TokenType.FLOAT if is_float else TokenType.INTEGER

        # Symbol recognition
        else:
            lexeme = char
            position += 1
            token_type = TokenType.SYMBOL

        tokens.append((token_type, lexeme))

    return tokens

########################## BOILERPLATE ENDS ###########################
rules={
    "S": ["BA","SS","notifelse()"],
    "B":["if"],
    "K":["SV"],
    "V":["LS"],
    "A":["CS","CK"],
    "L":["else"],
    "C":["RM","CM","YM","isintegervar()","notifelse()"],
    "M":["OR","OC","OY"],
    "O":["+","-","*","/","^","<",">","="],
    "R":["isintegervar()"],
    "Y":["notifelse()"]
}
def cykFun(substr,rules,cyk,x):
    res=set()
    for k in range(x-1):
        var1=cyk["".join(substr[:k+1])]
        var2=cyk["".join(substr[k+1:])]
        for var in [x+y for x in var1 for y in var2]:
            for key in rules:
                if var in rules[key]:
                    res.add(key)
    cyk["".join(substr)]=res
    return cyk
def checkGrammar(tokens):
    addtokens=[]
    for token in tokens:
        addtokens.append(token[1])
    cyk=defaultdict(set)
    for i in range(1,len(tokens)+1):
        for j in range(len(tokens)+1-i):
            substr=addtokens[j:j+i]
            if i==1:
                substr="".join(substr)
                if substr=="if":
                    cyk[substr].add("B")
                if substr=="else":
                    cyk[substr].add("L")
                if substr not in ["if","else","+","-","*","/","^","<",">","="]:
                    cyk[substr].add("Y")
                    cyk[substr].add("S")
                    cyk[substr].add("C")
                if substr in ["+","-","*","/","^","<",">","="]:
                    cyk[substr].add("O")
                if substr.isalnum() and substr!="if" and substr!="else" and substr!="print":
                    cyk[substr].add("R")
            else:
                cyk=cykFun(substr,rules,cyk,i)
    return cyk
def check_syntax(tokens, grammar_rules):
    stack = ["S"]  # Start with the "S" symbol
    token_index = 0
    while stack:
        current_symbol = stack.pop()
        if current_symbol in grammar_rules:
            if token_index < len(tokens):
                next_token_type, next_token_value = tokens[token_index]
                if next_token_value in grammar_rules[current_symbol]:
                    token_index += 1
                else:
                    print(f"Unexpected token: {next_token_value}. Expected: {grammar_rules[current_symbol]}")
                    return False
            else:
                print(f"Missing tokens for symbol: {current_symbol}")
                return False
        else:
            print(f"Invalid grammar rule: {current_symbol}")
            return False
    if token_index < len(tokens):
        print(f"Extra tokens at the end of input: {tokens[token_index:]}")
        return False
    return True
if __name__ == "__main__":
    source_code = "if 2 print else if 2"
    try:
        tokens = tokenize(source_code)
        addtokens=[]
        for token in tokens:
            addtokens.append(token[1])
        cyk = checkGrammar(tokens)  # You are tasked with implementing the function checkGrammar
        if "S" in cyk["".join(addtokens)]:
            for token in tokens:
                print(f"Token Type: {token[0]}, Token Value: {token[1]}")
        else:
            print("!!!!!!Incorrect Syntax!!!!!!")
            check_syntax(tokens,rules)
            print("Please verify")
    except ValueError as e:
        print(e)