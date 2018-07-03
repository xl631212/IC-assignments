import re
def DetectArray(func_str,def_str):
    array_list = re.findall(r'[^0-9a-zA-Z_]([a-zA-Z0-9_]+)\[',func_str)#find all array variable in function body
    array_ele=list(set(array_list))#remove duplicate elements
    for item in array_ele:
        if def_str.find(item+'[')<0:#if array size is not defined
            reg = r'([a-zA-Z0-9_])([^a-zA-Z0-9_]*)'+item+r'([^a-zA-Z0-9_])'
            def_str = re.sub(reg,r'\1[1]\2'+item+r'\3',def_str)#default array size is 1
        else:
            reg = r'([a-zA-Z0-9_])([^a-zA-Z0-9_]*)'+item+r'(\[[0-9]+\])'#rearrange string, change 'real A[30]=..' to 'real[30] A=..'
            def_str = re.sub(reg,r'\1\3\2'+item,def_str)
    s=def_str+"{"+func_str+"}"#return the whole program
    return s
def OpenCLToSOAP(s):
    s = re.sub(r'\/\/.+','',s)#remove // comments
    s = re.sub(r'[ \t]+',' ',s)
    s = re.sub(r'([a-zA-Z0-9_])[ ]*([\[\]\(\)\{\}\;])',r'\1\2',s)#remove blankspaces between variables and punctuations, e.g. 'A [0]' -> 'A[0]'
    s = re.sub(r'__kernel (void|float|int)?',"def ",s)
    s = re.sub(r'(__global|__local|__constant|__private) (const|unsigned)? ?','',s)#remove OpenCL qualifiers
    s = re.sub(r'(u)?(long|int|short|size_t|ptrdiff_t|intptr_t|uintptr_t)[0-9]* (\*)?',"int ",s)
    s = re.sub(r'(u)?(double|float|half)[0-9]* (\*)?',"real ",s)
    s = re.sub(r'get_(global|local)_(id|size)\(0\)',"0",s)
    spec_start = s.find("soap_spec")
    spec_end = s.find("*/",spec_start)
    spec_str = s[spec_start:spec_end]#get specification
    spec_str = re.sub(r'[ \t\s]+',' ',spec_str)
    return_list = re.findall('[^0-9a-zA-Z_](return [0-9a-zA-Z_,\[\]]+)[; \/]',spec_str)#get the 'return' statement
    data_range = re.findall(r'(([a-zA-Z0-9_]+[ ]*(\[[0-9a-zA-Z_\-\+\*\/]+\])?)[ ]*=(\[[0-9.]+[, \t\s]+[0-9.]+\])+)',spec_str)#get all specifications
    data_range_list=list(sum(data_range,()))#flatten the list
    def_start = s.find("def ")
    def_end = s.find("{",def_start)
    def_str = s[def_start:def_end]#get the function declaration lines
    
    for item in data_range_list:
        a=item.split("=");
        if len(a)>1:
            a[0]=re.sub(r'\[[0-9]+\]',"",a[0])
            reg = r'([^a-zA-Z0-9_])'+a[0]+r'([^a-zA-Z0-9_])'
            def_str=re.sub(reg,r'\1'+item+r'\2',def_str)#replace the variable with specified data range
    last_brac = s.rfind('}')
    s = s[0:def_start]+def_str+s[def_end:last_brac]+return_list[0]+';'+s[last_brac:]
    s = re.sub(r'\/\*[a-zA-Z0-9_ :=\[\],\.\/\\\r\n;\'\-!"\$%\^\(\)&\*@~#]+\*\/','',s,re.DOTALL) #remove /**/ comments
    s = re.sub(r'([^a-zA-Z0-9_])([a-zA-Z0-9_]+[ ]*(\[[0-9a-zA-Z_\-\+\*\/]+\])?)[ ]*([\+\-\/\*])=',r'\1\2=\2\4',s)# replace 'a+=1' with 'a=a+1', 'a[i]+=1' with 'a[i]=a[i]+1'
    s = s.replace('\n','').replace('\r', '')#remove newlines
    func_str = s[s.find("{")+1:s.rfind("}")]#get the function body
    s = DetectArray(func_str,def_str)
    return s

#=== test ===
prog = """
/*soap_spec:
variable[array_size] = [lower_bond, upper_bound][error_min, error_max]
A[30]=[0,20][0.1, 0.2]
B=[0,3]
return B//define the return variable(s)
*/
__kernel void simple_op(__global float *A, __global const float *B){
	int i = get_global_id(0);
B[i] +=(A[i]+A[i-1]); 
//B[i]+=A[i];
A[i]*=A[i+1];
//comment
}
"""
prog_transformed = OpenCLToSOAP(prog)
print (prog_transformed)
