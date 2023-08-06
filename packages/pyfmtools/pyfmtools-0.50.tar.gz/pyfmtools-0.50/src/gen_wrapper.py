import pandas as pd
import re


def prepare_parameter_for_c_function_call( str_cfunc, has_env, param_count, param_type, param_name):
    this_param = param_name.replace( "*", "")
    str_cffi = ""

    # check whether this is a pointer?
    if "*" in param_type:
        # assumption: memory is allocated of length n or env.m
        if has_env: str_mem_size = "env.m"
        else: str_mem_size = "n"
    
        if "int" in param_type:
            this_param = "p" + param_name
            str_cffi = "    " + param_name + ", " + this_param + " = " + "create_intc_zeros_as_CFFI_int( " + str_mem_size + ")"
        elif "double" in param_type:
            this_param = "p" + param_name
            str_cffi =  "    " + param_name + ", " + this_param + " = " + "create_float_zeros_as_CFFI_double( " + str_mem_size + ")"
        elif "int_64" in param_type:
            str_cffi = ""   
        elif "struct_fm_env" in param_type:
            str_cffi = ""
        elif "struct_fm_env_sparse" in param_type:
            str_cffi = ""
        else:
            print( "unknown parameter type: ", param_type, "in c function: ", str_cfunc)
    
    if param_count > 0:
        this_param = ", " + this_param
        
    return this_param, str_cffi


# generate python wrapper code for one C function
# input:  C function 
# output: python wrapper code
def gen_py_code_for_c_function( str_cfunc):
    py_func_code = []
    py_func_calls_to_allocate_data = []
    str_return = ""
    has_env = False
    if "env" in str_cfunc: has_env = True
    # scan function and generate tokens
    # tokens[0]: return type
    # tokens[1]: function name
    # tokens[2]: parameter 1 type
    # tokens[3]: parameter 2 type
    # ...
    temp = str_cfunc.replace( "(", " ").replace( ")", "").replace( ",", "")
    temp = re.sub( r"[ ]+", " ", temp)
    tokens = re.split( ",| ", temp)
    # print( "tokens: ", tokens)
        
    # initial comment
    str_wrapper_func = str_cfunc.replace( "py_", "")
    str_in_comment = "# " + str_cfunc
    py_func_code.append( str_in_comment)
    # print( str_in_comment)
        
    # function header
    token_iter = iter( tokens) 
    return_type = next( token_iter)
    func_name = next( token_iter).replace( "py_", "")
    str_py_header = "def " + func_name + "("
    param_count = 0
    c_params = ""
    while True:
        try:
            param_type = next( token_iter)
            param_name = next( token_iter)
            if param_count == 0: 
                str_py_header += param_name
            else:
                str_py_header += ", " + param_name
            this_param, str_cffi = prepare_parameter_for_c_function_call( str_cfunc, has_env, param_count, param_type, param_name)
            c_params += this_param.replace( "*", "")
            if str_cffi: py_func_calls_to_allocate_data.append( str_cffi)
            param_count += 1
        except StopIteration:
            str_py_header += "):"
            break
    py_func_code.append( str_py_header)
    # print( str_py_header)
        
    # trace
    str_trace = "    trace( '""'" + str_wrapper_func + "'""')" 
    py_func_code.append( str_trace)
    # print( str_trace)
    
    # prepare parameters for C function call
    py_func_code.extend( py_func_calls_to_allocate_data)
        
    # C function call and return statement
    if "void" in return_type: 
        str_c_func_call = "    fm." + func_name + "( " + c_params + ")";
        str_return = ""
    else:
        str_c_func_call = "    yy = fm." + func_name + "( " + c_params + ")";
        str_return = "    return yy"
    py_func_code.append( str_c_func_call)
    if str_return: py_func_code.append( str_return)    

    return py_func_code





list_of_c_functions = "list_of_c_functions.txt" 
generated_py_code = "generated_py_code.py"

py_code = []
with open( list_of_c_functions, 'r') as fh_read:
    for line in fh_read:
        # remove whitespaces and ";"
        aline = line.strip().replace( ";", "").replace( "struct ", "struct_")
        py_code.extend( gen_py_code_for_c_function( aline))
        # add 2 empty lines
        py_code.append( "\n\n")

fh_write = open( generated_py_code, 'w')
fh_write.writelines( "%s\n" % l for l in py_code)

# the end
