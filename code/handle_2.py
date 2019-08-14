import math
import re
from ctypes import *
from datetime import datetime 
from collections import defaultdict

# sortest_chain_in_ubuntu
def sortest_chain_in_ubuntu(num):
    asp = cdll.LoadLibrary('./asp.so')
    asp.asp_main.restype = c_char_p
    b = []
    for j in range(100):
        a = asp.asp_main(j,num)
        a = a.split(".")
        a.pop()
        for index,i in enumerate(a):
            a[index] = int(i)
        if(a == []):
            #print("NOT FOUND!")
            pass
        else:
            for i in a:
                b.append(bin(i)[2:])
            return b,j

# sortest_chain_in_windows
def sortest_chain_in_windows(num):
    # asp = cdll.LoadLibrary('./asp.so')
    asp = cdll.LoadLibrary("./asp.dll")
    asp.asp_main.restype = c_char_p
    b = []
    for j in range(100):
        a = asp.asp_main(j,num)
        a = a.split(".")
        a.pop()
        for index,i in enumerate(a):
            a[index] = int(i)
        if(a == []):
            #print("NOT FOUND!")
            pass
        else:
            for i in a:
                b.append(bin(i)[2:])
            return b,j


def save_to_file(file_name, contents):
    fh = open(file_name, 'w')
    fh.write(contents)
    fh.close()

def sort_array(array):
    array_tmp = list(set(array))
    array_tmp = map(int, array_tmp)
    array_tmp.sort()
    # print(array)
    array_tmp = map(str, array_tmp)
    return array_tmp

def get_initarray(bin_num):
    initarray = list(set(bin_num.split("0")))
    if('' in initarray):
        initarray.remove('')
    return initarray

def IntegrationList(result):
    tmp = []
    for i in result:
        tmp.append(i[0])
    return tmp

def findIndex(num, result_tuple):
    result_list = IntegrationList(result_tuple)
    # print(result_tuple)
    # print("result_list = " + str(result_list))
    # print(num)
    for i in range(len(result_list)):
        if(result_list[i] == num):
            return i+1

def findadd(number, initarray):
    for i in range(len(initarray)):
        for j in range(len(initarray)):
            if(int(initarray[i],2) + int(initarray[j],2) == number):
                return i+1, j+1

def initarray2tuple(initarray, result):
    # print(initarray)
    for i in range(len(initarray)):
        if(initarray[i] == '1'):
            if(1 not in IntegrationList(result)):
                result.append((1,))
        elif(initarray[i] == '10'):
            if(2 not in IntegrationList(result)):
                result.append((2,))
        else:
            tmp = int(initarray[i], 2)
            # print(result)
            # print(tmp)
            x, y = findadd(tmp, initarray)
            result_list = IntegrationList(result)
            if(tmp in result_list):
                pass
            else:
                result.append((tmp,i, x-1, y-1))
    return result

def diffarray(A, B):
    leftover = list(set(A).difference(set(B)))
    return leftover

def combine_chain(array, sortchain):
    leftover = diffarray(array, sortchain)
    # print("+++++++++++++++++  combine chain  ++++++++++++++++++")
    # print("array element = " + str(array))
    # print("sortchain element = " + str(sortchain))
    # print("leftover element = " + str(leftover))
    for i in leftover:
        tmp = []
        for j in sortchain:
            sub_tmp = int(i, 2) - int(j, 2)
            if(sub_tmp > 0):
                tmp.append(sub_tmp)
        suitable_number = sortchain[len(tmp) - 1]
        array_tmp, _  = sortest_chain_in_windows(int(i, 2))
        leftover_tmp = diffarray(array_tmp, sortchain)
        # print("leftover_tmp = " + str(leftover_tmp))
        if(i in leftover_tmp):
            leftover_tmp.remove(i)
        sortchain = sortchain + leftover_tmp
        sortchain.append(i)
    sortchain = sort_array(sortchain)
    # print(sortchain)
    # print("+++++++++++++++++  combine chain  ++++++++++++++++++")
    return sortchain

# def generate_begin_chain(bin_num, addchain):
#     addchain_int = map(int, addchain)
#     # print(addchain)
#     # print("===================================")
#     max_len = len(str(max(addchain_int)))
#     for i in range(0,max_len):
#         tmp = bin_num[0:max_len - i]
#         if(tmp in addchain):
#             # if(len(tmp) == max_len):
#             return addchain, len(tmp)

# def generate_begin_chain(bin_num, addchain, initchain):
#     if(bin_num[0:winsize] in addchain):
#         pass
#     else:
#         # print(addchain)
#         begin_chain, _ = sortest_chain_in_windows(int(bin_num[0:winsize], 2))
#         addchain = combine_chain(begin_chain, addchain)
#         result_tuple = initarray2tuple(addchain, result_tuple)

def return_list_vaule(result_tuple, index):
    tmp = IntegrationList(result_tuple)
    return tmp[index]
    
def generate_chain(bin_num, initarray, result_tuple):
    initarray = sort_array(initarray)

    # handle the max num
    max_num = initarray[-1]
    len_max_num = len(max_num)
    # print("len_max_num = " + str(len_max_num))
    add_seq_tmp, _ = sortest_chain_in_windows(len_max_num)
    add_seq = []
    for i in add_seq_tmp:
        add_seq.append(int(i, 2))
    # add_seq = map(int, add_seq)

    sub_add_seq = []
    for i in range(1, len(add_seq)):
        sub_add_seq.append(add_seq[i] - add_seq[i-1])
    # print(sub_add_seq)
    sub_str_key = {}
    addchain = []
    # print(add_seq)
    initarray_tmp = initarray[0:-1]


    for i in initarray_tmp:
        sub_add_seq.append(len(i))
    sub_add_seq = list(set(sub_add_seq))

    # for i in initarray_tmp:
    #     if(str(i) in add_seq):
    #         # print("reomve = " + str(i))
    #         initarray_tmp.remove(i)
    max_len = 0
    if(initarray_tmp):
        initarray_tmp = sort_array(initarray_tmp)
        max_len = len(initarray_tmp[-1])
        for i in add_seq:
            if(i <= max_len):
                initarray_tmp.append(bin_num[0:i])
        if(bin_num[0:max_len] not in initarray_tmp):
            initarray_tmp.append(bin_num[0:max_len])
        # print("initarray_tmp = " + str(initarray_tmp))
    if(initarray_tmp):
        if(initarray_tmp[-1] == "1" ):
            pass
        else:
            initchain, _ = sortest_chain_in_windows(int(initarray_tmp[-1], 2))
            initchain = combine_chain(initarray_tmp, initchain)
            addchain = initchain
            result_tuple = initarray2tuple(initchain, result_tuple)
            # print(result_tuple)
        
    for i in addchain:
        if(len(i) == i.count("1")):
            if(len(i) in sub_add_seq):
                index_tmp = findIndex(int(i,2),result_tuple)
                sub_str_key[i] = index_tmp - 1
            
    
    # print("addchain = " + str(addchain))
    # print("add_seq = " + str(add_seq))
    # print(sub_str_key)

    
    flag = 0
    add_seq_del = []
    for i in range(len(add_seq)):
        if(add_seq[i] == max_len):
            flag = i
            break
        # add_seq_del.append(add_seq[i])

    # print("flag = " + str(flag))
    for i in range(flag, len(add_seq)):
        tmp = add_seq[i]*"1"
        # print(tmp)
        if(tmp in addchain):
            add_begin_len = add_seq[i + 1] - add_seq[i]
            for i in range(add_begin_len):
                addchain.append(tmp + "0"*(i+1))
                result_tuple.append((int(tmp + "0"*(i+1), 2), len(result_tuple), len(result_tuple) - 1, len(result_tuple) - 1))
            continue
        if(tmp == '1'):
            if(1 not in IntegrationList(result_tuple)):
                result_tuple.append((1,))
            if('1' not in addchain):
                addchain.append('1')
                sub_str_key['1'] = 0
        elif(tmp == '10'):
            if(2 not in IntegrationList(result_tuple)):
                result_tuple.append((2,))
            if('10' not in addchain):
                addchain.append('10')
        else:
            addchain.append(tmp) 
            # print("===========")
            # print(result_tuple[len(result_tuple) - add_seq[i-1] - 3])
            # print(result_tuple[len(result_tuple) - 1])
            # print(str(int(tmp, 2)))
            # print(add_seq[i-1])
            # print("===========")
            # print((add_seq[i] - add_seq[i-1])*"1")
            # print(sub_str_key)
            index_add = sub_str_key[(add_seq[i] - add_seq[i-1])*"1"]
            result_tuple.append((int(tmp, 2), len(result_tuple), len(result_tuple) - 1, index_add))
            if(len(tmp) in sub_add_seq):
                sub_str_key[tmp] = len(result_tuple) - 1
        if(i != (len(add_seq) - 1)):
            sub_len = add_seq[i + 1] - add_seq[i]
            for i in range(sub_len):
                addchain.append(tmp + "0"*(i+1))
                result_tuple.append((int(tmp + "0"*(i+1), 2), len(result_tuple), len(result_tuple) - 1, len(result_tuple) - 1))
    # print(sub_str_key)
    # print(addchain[-1])
    # get leftover
    long_tmp = addchain[-1]
    len_long_tmp = len(long_tmp)
    if(bin_num[0:len_long_tmp] == "1"*len_long_tmp):
        # print("get the longest 11111  in the begin of bin_num.")
        initarray.pop()
        bin_num_last = bin_num[len_long_tmp:]
        # print("bin_num_last = " + str(bin_num_last))
        flag = 0
        tmp_1 = ""
        for i in bin_num_last:
            if(i == "0"):
                if(flag == 1):
                    flag = 0
                    last_tmp = addchain[-1]
                    for j in range(len(tmp_1)):
                        # print("+++++++++++++++++++++++++++++++++++")
                        addchain.append(last_tmp + (j+1)*"0")
                        result_tuple.append((int(last_tmp + (j+1)*"0", 2), len(result_tuple), len(result_tuple) - 1, len(result_tuple) - 1))
                            
                    index_add = sub_str_key[(tmp_1)]
                    result_tuple.append((int(last_tmp+tmp_1, 2), len(result_tuple), len(result_tuple) - 1, index_add))

                    addchain.append(last_tmp+tmp_1)
                    tmp_1 = ""
                result_tuple.append((int(addchain[-1] + i, 2), len(result_tuple), len(result_tuple) - 1, len(result_tuple) - 1))  # add zero
                addchain.append(addchain[-1] + i)
            else:
                tmp_1 += "1"
                flag = 1

    else:
        pass
    if(tmp_1 == ""):
        pass
    else:
        last_tmp = addchain[-1]
        for j in range(len(tmp_1)):
            addchain.append(last_tmp + (j+1)*"0")
            result_tuple.append((int(last_tmp + (j+1)*"0", 2), len(result_tuple), len(result_tuple) - 1, len(result_tuple) - 1))
        addchain.append(last_tmp+tmp_1)
        tmp_number = int(tmp_1, 2)
        init_index = findIndex(tmp_number, result_tuple[0:50])
        if(str(init_index) == "None"):
            print(tmp_number)
            print(result_tuple[0:10])
            print("erro...None")
        result_tuple.append((int(last_tmp+tmp_1, 2), len(result_tuple), len(result_tuple) - 1, init_index - 1))
        
    # check......
    if(addchain[-1] != bin_num):
        print("not seam")
        tmp_1_len = len(tmp_1)
        # print(tmp_1)
        # for i in range(tmp_1_len):
        #     addchain.append(addchain[-1] + (i)*"0")
        tmp_number = int(tmp_1, 2)
        init_index = findIndex(tmp_number, result_tuple[0:50])
        result_tuple.append((int(addchain[-1] + tmp_1, 2), len(result_tuple), len(result_tuple) - 1, init_index - 1))
        addchain.append(addchain[-1] + tmp_1)

    return addchain, result_tuple

def defaultdict_min(defaultdict, flag): 
    min_count = 1000
    min_count_keys = ""
    count_tmp = 0
    for i in defaultdict:
        count_tmp = defaultdict[i][flag]
        if(count_tmp < min_count):
            min_count = count_tmp
            min_count_keys = i
    return min_count_keys,min_count

def print_result(result_tuple):
    str_result = "v0=1,v1=2"
    tmp = ""
    for i in result_tuple:
        if(i[0] == 1 or i[0] == 2):
            continue
        str_result += ",v" + str(i[1]) + "=" + str(i).replace(" ","")
        tmp += " " + bin(i[0])[2:]
    print(tmp)
    return str_result

def check_the_result(result_tuple):
    result_tuple_re = result_tuple[::-1]
    for i in result_tuple_re:
        if(i == (1,) or i == (2,)):
            continue
        if(result_tuple[i[2]][0] + result_tuple[i[3]][0] == i[0]):
            pass
        else:
            print(i[0])
            return True
    return False

def exp(num):
    bin_num = bin(num)[2:]
    print("binary of number = " + bin_num)
    up = len(bin_num) - 1 + bin_num.count("1")
    low = len(bin_num) - 1 + math.log(bin_num.count("1"),2)
    # print("the number of " + str(num) + "'s length = " + str(len(bin_num)))
    # print("the number of " + str(num) + "'s Lower bound = " + str(low))
    # print("the number of " + str(num) + "'s Upper Bound = " + str(up))

    # begin
    initarray = get_initarray(bin_num)
    # print("initarray = " + str(initarray))
    result_tuple = []
    addchain, result_tuple = generate_chain(bin_num, initarray, result_tuple)
    # print("addchain's len = " + str(addchain[0:30]))
    print("addchain's len = " + str(len(addchain)-1))
    print("result_tuple = " + str(result_tuple[-1]))
    if(check_the_result(result_tuple)):
        print("wrong...")
        print(result_tuple[0:50])
    else:
        print("win...")
        pass

    return addchain, result_tuple

# num = 57896044618658097711785492504343953926634992332820282019728792003956564819949 - 5
num = 6703903964971298549787012499102923063739682910296196688861780721860882015036773488400937149083451713845015929093243025426876941405973284973216824503042031 - 5
num = 1099511627775

begin = datetime.now() 
AspOfTen_record = defaultdict(list)
for i in range(10):
    print("==========================================================")
    addchain, result_tuple = exp(num+i)
    AspOfTen_record[str(i)].append(num + i)
    AspOfTen_record[str(i)].append(len(addchain) -1) 
    AspOfTen_record[str(i)].append(addchain) 
    AspOfTen_record[str(i)].append(result_tuple) 

bin_num = bin(num)[2:]
up = math.floor(math.log(num,2)) + bin_num.count("1")
low = math.floor(math.log(num,2)) + math.log(bin_num.count("1"),2)
min_keys,min_value = defaultdict_min(AspOfTen_record, 1)
print("min value = " + str(min_value) + " " + str(AspOfTen_record[min_keys][0]) + ' ' + str(AspOfTen_record[min_keys][1]) + ' ' + str(len(AspOfTen_record[min_keys][3])))

end = datetime.now() 
print("total time = " + str((end - begin)))
AspOfTen_record[min_keys].append(str((end - begin))) # time

filename = "second_" + str(AspOfTen_record[min_keys][0])[-10:] + '.txt'
result_filename = "second_" + str(AspOfTen_record[min_keys][0])[-10:] + "_result " + '.txt'

content = "up = " + str(up) + "low = " + str(low) + print_result(AspOfTen_record[min_keys][3])

content = content.replace("L","")
if(check_the_result(AspOfTen_record[min_keys][3])):
    print("wrong...")
else:
    print("win...")


save_to_file(filename, str(AspOfTen_record[min_keys]))
save_to_file(result_filename, content)

# filename = "second_" + str(AspOfTen_record[min_keys][0])[-10:] + '.txt'
# save_to_file(filename, str(AspOfTen_record[min_keys]))
