
from sys import argv
# import regex as re
def Lexer(data):
    
    cache = ''
    
    TOKEN = []
    
    items = []
    
    collecting_string = False
    collecting_broket = False
    collecting_var = False
    collecting_list = False
    collecting_condition = False
    check_calling_var = False
    check_calling_list = False
    
    for char in data:
        
        if collecting_condition:
            
            if "then" in cache:
                IF = cache.split("then")[0]
                TOKEN.append("IF:" + IF)
                # print("sss")
                
                cache = ""   
                continue  
              
        
            if "end" in cache   :
                    
                TOKEN.append("ENDIF")
                collecting_condition = False  
                cache = ""
                continue
        
        if cache == "if":
                
            
            cache = ''
            collecting_condition = True
            continue

        
        if char == "\n":
            if check_calling_list and cache.endswith("]") :
                
                TOKEN.append("CALL_LIST:" + cache)
                check_calling_list = False   
                cache = ""            
                continue
                    
            if check_calling_var :
                
                TOKEN.append("CALL_VAR:" + cache)
                check_calling_var = False   
                cache = ""
            continue
                

        
        if char == '"':
            if (not collecting_broket):
                collecting_string = True if not collecting_string else False
                check_calling_var = False  
                
                if not collecting_string:
                    TOKEN.append("STRING:" + cache)
                
                
                cache = ""
                continue
                

        if char == '[' or char == ']' :
            
            if (not collecting_string and not check_calling_list):
                
                collecting_broket = True if not collecting_broket else False
                check_calling_var = False  
                check_calling_list = False  
                
                if not collecting_broket:
                    TOKEN.append("BROKET:"+cache)
                
                
                cache = ""
                continue       
        
        # elif char in "+-*/=":
        #     TOKEN.append("expression:"+ char)
        #     check_calling_var = False 
        #     continue
        # elif re.match(r"[.0-9]+", char):
        #     TOKEN.append("number:"+ char)
        #     check_calling_var = False 
        #     continue
        

        

                

                
        
        if cache == "var":
            collecting_var = True
            cache = ''
            continue
        
        if cache == "list":
            collecting_list = True
            cache = ''
            continue
        
        if collecting_var:
            if "=" in cache:
                var_name = cache.split("=")[0]
                TOKEN.append("VAR:" + var_name)
                collecting_var = False
                cache = ""
                continue
        
        if collecting_list:
            if "=" in cache:
                var_name = cache.split("=")[0]
                TOKEN.append("LIST:" + var_name)
                collecting_list = False
                cache = ""
                continue       
        
        if cache == "print":
            TOKEN.append("PRINT")
            check_calling_var = True    
            check_calling_list = True    
            cache = ''
            
        if char == " ": 
            if not collecting_string or not collecting_broket:
                continue

        
        cache += char
           

        
        # print(cache)
    return TOKEN


def Parser(TOKEN):
    
    Is_print = False
    skiping_condition = False
    definding_var = False
    definding_list = False

    Is_e = False
    Is_n = False
    inst_line = ""
    
    VAR = {}
    LIST = {
        
    }
    current_var = ""
    current_list = ""
    
    for token in TOKEN:
        
        if skiping_condition:
            if token == "ENDIF":
                skiping_condition = False
            continue
        
        if token.startswith("IF:"):
            condition = token.split(":")[1]
            
            # condition = condition.replace("barabarboodba" , "==")
            
            for k,v in VAR.items():
                if k in condition:
                    condition = condition.replace(k,f"'{v}'")
            
            if eval(condition):
                
                continue 
            else:  
                             
                skiping_condition = True        
        
        if token == "PRINT":
            Is_print = True
            continue
        

        
        if token.startswith("CALL_VAR:"):
            var = token.split(":")[1]
            if Is_print:
                try:
                    print(VAR[var]) 
                except:
                    print(LIST[var]) 
                       
                
                
                Is_print = False 

        if token.startswith("CALL_LIST:"):
            var = token.split(":")[1]
            var_name = var.split("[")[0]
            var_num = var.split("[")[1].split("]")[0]
            
            
            
            if Is_print:
                if var.endswith("]"):
                    str_var = LIST[var_name][int(var_num)]
                    print(str_var.split('"')[1].split('"')[0])
                
                       
                
                
                Is_print = False 
                        
        if token.startswith("number:"):
            
            number = token.split(":")[1]
            inst_line += number
            
        if token.startswith("expression:"):
            
            expression = token.split(":")[1]
            inst_line += expression
            Is_e = True
        
        if token.startswith("VAR:"):
            var_name = token.split(":")[1]
            VAR[var_name] = ""
            current_var = var_name
            definding_var = True
            continue
        if token.startswith("LIST:"):
            list_name = token.split(":")[1]
            LIST[list_name] = ""
            current_list = list_name
            definding_list = True
            continue        
        if token.startswith("STRING:"):
            text = token.split(":")[1]
            if Is_print:
                print(text)    
                Is_print = False 
                   
            if definding_var:
                VAR[current_var] = text
                current_var = ""
                definding_var = False
        if token.startswith("BROKET:"):
            text = token.split(":")[1]
            if Is_print:
                print(text)    
                Is_print = False 
                   
            if definding_list:
                lists =  text.split(",")
                
                LIST[current_list] = lists
                # print(LIST)
                current_list = ""
                definding_list = False       
        # else:
        #     if Is_print :
        #         print(inst_line)
        #         # print(eval(""))

        # print(LIST)
            
            
            
            

with open("Example/test.per","r+") as f:
    data = f.read() + "\n"
    
token = Lexer(data)
# print(token)
Parser(TOKEN=token)

