import re
import math
import random
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

def dict2list(dict):
    tmp = []
    for i in dict:
        tmp.append(i[0])
    return tmp

def Remove_duplicate(array):
    array_remove = list(set(array))
    array_remove.sort(key=array.index)
    return array_remove


def hanming(str):
    return str.count("1")

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



def calc_sortchain_inclued_array(array):
    global initarray
    times = 0 
    array = sort_array(array)
    # print(array)
    sortchain,size = sortest_chain_in_windows(int(str(array[-1]), 2))
    if(set(array) < set(sortchain)):
        # print("all in")
        times = times + len(sortchain) - 1
    else:
        sortchain = combine_chain(array, sortchain)
        times = times + len(sortchain) - 1
    # print("sortchain = " + str(sortchain))
    # print("times = " + str(times))
    return sortchain

def generate_begin_chain(bin_num, addchain):
    addchain_int = map(int, addchain)
    # print(addchain)
    # print("===================================")
    max_len = len(str(max(addchain_int)))
    for i in range(0,max_len):
        tmp = bin_num[0:max_len - i]
        if(tmp in addchain):
            # if(len(tmp) == max_len):
            return addchain, len(tmp)
    '''    
    # print(max_len)
    begin_tmp = bin_num[0:max_len]
    # print(begin_tmp)
    sortchain_begin, _ = sortest_chain_in_windows(int(begin_tmp, 2))
    leftover_begin = diffarray(sortchain_begin, addchain)
    if(leftover_begin == []):
        pass
    else:
        chain_tmp = combine_chain(leftover_begin, addchain)
        addchain += chain_tmp
    return addchain, max_len
    '''



def fixed_win(bin_num, win):
    init_array_fix = []
    len_win = len(bin_num)/win
    for i in range(len_win):
        init_array_fix.append(int(bin_num[i*win:i*win+win]))
    if(i*win+win != len(bin_num)):
        init_array_fix.append(int(bin_num[i*win+win:]))

    init_array_fix = list(Remove_duplicate(init_array_fix))
    # print(init_array_fix)
    # init_array_fix.sort()  # Sort ascending
    if(0 in init_array_fix):
        init_array_fix.remove(0) 
    init_array_fix = map(str, init_array_fix)
    # init_array_fix = cutlast0(init_array_fix)
    return init_array_fix

# def generate_chain_(bin_num, addchain, initarray):
    addchain, max_len = generate_begin_chain(bin_num, addchain)
    # print("addchain = " + str(addchain))
    bin_num_begin = bin_num[0:max_len]
    bin_num_tmp = bin_num[max_len:]
    flag = 0
    chain = bin_num_begin
    # print("bin_num = " + bin_num_begin + bin_num)
    index = max_len
    # while(index <= len(bin_num)):


    tmp = ""
    for i in bin_num_tmp:
        if(i == "0"):
            if(flag == 1 and ("1" in tmp)):
                chain = chain[0:-len(tmp)]
                addchain.append(chain + tmp)
                chain = chain + tmp
                flag = 0
            tmp = ""
        else:
            flag = 1
            tmp += "1"
        chain += "0"
        addchain.append(chain)
    
    if(addchain[-1] == bin_num):
        # print("addchain[-1] = " + str(addchain[-1]))
        return addchain
    else:

        # print("else addchain[-1] = " + str(addchain[-1]))
        # print(int(addchain[-1]))
        # print(int(bin_num))
        # print(int(bin_num) - int(addchain[-1]))
        sub = str(int(bin_num) - int(addchain[-1]))
        if(sub in addchain):
            addchain.append(bin_num)
            return addchain
        else:
            print(sub)
            if(sub in addchain):
                addchain.append(bin_num)
            else:
                sub_array = []
                sub_array.append(sub)
                addchain = combine_chain(sub_array, addchain)
                addchain.append(bin_num)
            print("combine_chain again in last number in addchain.")
            return addchain

def fixwin_generate_chain(bin_num, addchain, initchain, winsize, result_tuple):
    if(bin_num[0:winsize] in addchain):
        pass
    else:
        # print(addchain)
        begin_chain, _ = sortest_chain_in_windows(int(bin_num[0:winsize], 2))
        addchain = combine_chain(begin_chain, addchain)
        result_tuple = initarray2tuple(addchain, result_tuple)
        # print("result_tuple = " + str(result_tuple))
    # print(bin_num)
    # print(addchain)
    # list of result_tuple's first value
    result_list = IntegrationList(result_tuple)

    index = winsize
    cur_bin = bin_num[0:winsize]
    while(index < len(bin_num)):
        if((len(bin_num) - index) > winsize):
            tmp_number = int(bin_num[index:index + winsize], 2)
            index += winsize
            for i in range(winsize):
                addchain.append(cur_bin + (i+1)*"0")
                result_tuple.append((int(cur_bin + (i+1)*"0", 2), len(result_tuple), len(result_tuple) - 1, len(result_tuple) - 1))
            addchain.append(bin_num[0:index])
            cur_bin = bin_num[0:index]
            if(tmp_number == 0):
                pass
            else:
                # print(tmp_number)
                # print(result_tuple)
                init_index = findIndex(tmp_number, result_tuple)
                result_tuple.append((int(cur_bin, 2), len(result_tuple), len(result_tuple) - 1 , (init_index - 1)))
            # print("cur_bin = " + str(cur_bin))
        else:
            tmp_len = len(bin_num) - index
            # print("tmp_len = " + str(tmp_len))
            tmp_number = int(bin_num[index:index+tmp_len], 2)
            for i in range(tmp_len):
                addchain.append(cur_bin + (i+1)*"0")
                result_tuple.append((int(cur_bin + (i+1)*"0", 2), len(result_tuple), len(result_tuple) - 1, len(result_tuple) - 1))
            addchain.append(bin_num)
            if(tmp_number == 0):
                pass
            else:
                init_index = findIndex(tmp_number, result_tuple)
                result_tuple.append((int(bin_num, 2), len(result_tuple), len(result_tuple) - 1, (init_index - 1)))
            index = len(bin_num)
    return addchain, result_tuple


def generate_chain(bin_num, addchain, initchain,result_tuple):
    addchain, max_len = generate_begin_chain(bin_num, addchain)
    # print("addchain = " + str(addchain))
    # print("initchain = " + str(initchain))
    # print("max_len = " + str(max_len))
    cur_bin = bin_num[0:max_len]
    flag = 0
    # print("bin_num = " + bin_num_begin + bin_num)
    index = max_len
    first = 0
    while(index <= len(bin_num)):
        # print(cur_bin)
        for i in initchain:
            str_len = len(i)
            find = 0
            if(bin_num[index:index+str_len] == i):
                find = 1
                for j in range(str_len):
                    if(first == 0):
                        tmp_number = int(cur_bin + (j+1)*"0", 2)
                        tmptmp = IntegrationList_bin(result_tuple)
                        # print(tmptmp)
                        x, y = findadd(tmp_number, IntegrationList_bin(result_tuple))
                        result_tuple.append((int(cur_bin + (j+1)*"0", 2), len(result_tuple), (x - 1), (y - 1)))
                        first = 1
                        if((cur_bin + (j+1)*"0") not in addchain):
                            addchain.append(cur_bin + "0"*(j + 1))
                        continue
                    addchain.append(cur_bin + "0"*(j + 1))
                    result_tuple.append((int(cur_bin + (j+1)*"0", 2), len(result_tuple), len(result_tuple) - 1, len(result_tuple) - 1))
                addchain.append(cur_bin + i)
                tmp_number = int(i, 2)
                # print(tmp_number)
                # print(result_tuple)
                init_index = findIndex(tmp_number, result_tuple)
                cur_bin = cur_bin + i
                index += str_len
                result_tuple.append((int(cur_bin, 2), len(result_tuple), len(result_tuple) - 1, (init_index - 1)))
                break
        if(find == 0 ):
            if(bin_num[index] == "1"):
                if((cur_bin + "1") in addchain):
                    cur_bin = cur_bin + "1"
                    pass
                else:
                    if(first == 0):
                        tmp_number = int(cur_bin + "0", 2)
                        tmptmp = IntegrationList_bin(result_tuple)
                        # print("tmp_number = " + str(tmp_number))
                        x, y = findadd(tmp_number, IntegrationList_bin(result_tuple))
                        result_tuple.append((int(cur_bin + "0", 2), len(result_tuple), (x - 1), (y - 1)))
                        first = 1
                    addchain.append(cur_bin + "0")
                    result_tuple.append((int(cur_bin + "0", 2), len(result_tuple), len(result_tuple) - 1, len(result_tuple) - 1))
                    addchain.append(cur_bin + "1")
                    result_tuple.append((int(cur_bin + "1", 2), len(result_tuple), len(result_tuple) - 1, 0))
                    cur_bin = cur_bin + "1"
            else:
                if((cur_bin + "0") in addchain):
                    cur_bin = cur_bin + "0"
                    pass
                else:
                    if(first == 0):
                        tmp_number = int(cur_bin + "0", 2)
                        tmptmp = IntegrationList_bin(result_tuple)
                        # print("tmp_number = " + str(tmp_number))
                        x, y = findadd(tmp_number, IntegrationList_bin(result_tuple))
                        result_tuple.append((int(cur_bin + "0", 2), len(result_tuple), (x - 1), (y - 1)))
                        first = 1
                    else:
                        result_tuple.append((int(cur_bin + "0", 2), len(result_tuple), len(result_tuple) - 1, len(result_tuple) - 1))
                    addchain.append(cur_bin + "0")
                    cur_bin = cur_bin + "0"
            index += 1
        if((index) == len(bin_num)):
            break
    # checking
    # print("cur_bin =" + str(cur_bin))
    if(int(bin_num, 2) - int(cur_bin,2)):
        # print("cur_bin =" + str(cur_bin))
        # print("sub = " + str(int(bin_num, 2) - int(cur_bin,2)))
        last_tmp = bin(int(bin_num, 2) - int(cur_bin,2))[2:]
        if(last_tmp in addchain):
            addchain.append(bin_num)
            cur_bin = bin_num
        else:
            tmp_chain = sortest_chain_in_windows(last_tmp)
            addchain = combine_chain(tmp_chain, addchain)
            cur_bin = bin_num
        
        tmp_number = int(last_tmp, 2)
        init_index = findIndex(tmp_number, result_tuple)
        result_tuple.append((int(bin_num, 2), len(result_tuple), len(result_tuple) - 1 , (init_index - 1)))
    # print("index =" + str(index))
    # print("cur_bin =" + str(cur_bin))
    return addchain, result_tuple


def sort_array(array):
    array_tmp = list(Remove_duplicate(array))
    array_tmp = map(int, array_tmp)
    array_tmp.sort()
    # print(array)
    array_tmp = map(str, array_tmp)
    return array_tmp

# Dynamic
def D_get_initarray(bin_num):
    initchain_1 = list(Remove_duplicate(bin_num.split("0")))
    initchain = initchain_1
    if('' in initchain):
        initchain.remove('')
    
    # print(initchain)
    # print(len(initchain))
    initchain_int = map(int, initchain)
    # print("===================================")
    max_len = len(str(max(initchain_int)))
    bin_begin = bin_num[0:max_len]
    if(bin_begin in initchain):
        pass
    else:
        initchain.append(bin_begin)
    
    addchain = []
    initchain = sort_array(initchain)
    addchain, _ = sortest_chain_in_windows(int(initchain[-1], 2))
    addchain = combine_chain(initchain, addchain)
    # print("addchain = " + str(addchain))
    # print("initchain = " + str(initchain))
    addchain = cut_the_initchain(addchain, initchain)
    # print("addchain = " + str(addchain))
    # print(array_tmp)
    return addchain, initchain_1

def D_generate_chain(bin_num, addchain):
    addchain, max_len = generate_begin_chain(bin_num, addchain)
    # print("addchain = " + str(addchain))
    # print("max_len = " + str(max_len))

    bin_num_begin = bin_num[0:max_len]
    bin_num_tmp = bin_num[max_len:]
    flag = 0
    chain = bin_num_begin
    # print("bin_num = " + bin_num_begin + bin_num)
    # index = bin_num_begin
    # while(index <=len(bin_num)):


    tmp = ""
    for i in bin_num_tmp:
        if(i == "0"):
            if(flag == 1 and ("1" in tmp)):
                chain = chain[0:-len(tmp)]
                addchain.append(chain + tmp)
                chain = chain + tmp
                flag = 0
            tmp = ""
        else:
            flag = 1
            tmp += "1"
        chain += "0"
        addchain.append(chain)
    if(addchain[-1] == bin_num):
        return addchain
    else:
        # print(int(addchain[-1]))
        # print(int(bin_num))
        # print(int(bin_num) - int(addchain[-1]))
        sub = str(int(bin_num) - int(addchain[-1]))
        if(sub in addchain):
            addchain.append(bin_num)
            return addchain
        else:
            print(sub)
            addchain = combine_chain(sub, addchain)
            print("combine_chain again in last number in addchain.")
            return addchain

def cutlast0(initarray):
        # cut the "00" behind the number
    for i in range(len(initarray)):
        if(int(initarray[i])%2 == 0):
            tmp = int(initarray[i],2)
            while(tmp%2 == 0):
                tmp = tmp/2
            initarray[i] = bin(tmp)[2:]
    return list(Remove_duplicate(initarray))


def D2_get_initarray(bin_num):
    initarray_1 = re.split('0{3,}', bin_num)
    if('' in initarray_1):
        initarray_1.remove('')
    initarray_1 = cutlast0(initarray_1)
    initarray = initarray_1
    initarray = list(Remove_duplicate(initarray))
    # print(initarray)



    initarray = sort_array(initarray)
    array_tmp, _  = sortest_chain_in_windows(int(initarray[-1], 2))
    initarray = sort_array(initarray)
    addchain, _  = sortest_chain_in_windows(int(initarray[-1], 2))
    addchain = combine_chain(initarray, addchain)
    # print("addchain = " + str(addchain))
    
    return addchain, initarray_1

def D3_get_initarray(bin_num, topN):
    initarray_1 = re.split('0{3,}', bin_num)
    if('' in initarray_1):
        initarray_1.remove('')
    initarray_1 = cutlast0(initarray_1)
    initarray_1 = sort_array(initarray_1)
    max_len = len(initarray_1[-1])

    dict = {}
    # print(" max_len = " + str(max_len))
    # print(" pow(2,max_len) = " + str(pow(2,max_len)))
    # generate dict which hamimg weight is not zero and count it's scores out
    for i in range(2,pow(2,max_len)):
        tmp = bin(i)[2:]
        count_1 = hanming(tmp) - 1
        if(count_1 == 0):
            pass
        elif(tmp[-1] == "0"):  # cut the initarry which the last num is 0
            pass
        else:
            tmp = bin(i)[2:]
            count = bin_num.count(tmp)
            dict[tmp] = count
    dict_top = sorted(dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    # print(dict_top)
    dict_top = dict_top[0:topN]
    dict_keys = dict2list(dict_top)
    # print(dict_keys)

    initarray_1 = sort_array(dict_keys)
    # generate the initarry
    initarray, _ = sortest_chain_in_windows(int(initarray_1[-1], 2))
    initarray = combine_chain(initarray_1, initarray)
    # print("initarray_1 = " + str(initarray_1))
    # print("initarray = " + str(initarray))
    return initarray, dict_keys

def findadd(number, initarray):
    for i in range(len(initarray)):
        for j in range(len(initarray)):
            if(int(initarray[i],2) + int(initarray[j],2) == number):
                return i+1, j+1
    return False

def findadd_bool(number, initarray):
    for i in range(len(initarray)):
        for j in range(len(initarray)):
            if(int(initarray[i],2) + int(initarray[j],2) == number):
                return True
    return False

def IntegrationList(result):
    tmp = []
    for i in result:
        tmp.append(i[0])
    return tmp

def IntegrationList_bin(result):
    tmp = []
    for i in result:
        tmp.append(bin(i[0])[2:])
    return tmp

def findIndex(num, result_tuple):
    result_list = IntegrationList(result_tuple)
    # print(result_list)
    # print(num)
    for i in range(len(result_list)):
        if(result_list[i] == num):
            return i+1

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

def cut_the_initchain(initchain, initarry):
    initarry_record = defaultdict(list)
    # print(initchain)
    # all possibility
    for i in range(len(initarry)):
        for j in initchain:
            for k in initchain:
                if(initarry[i] == "1"):
                    initarry_record[str(initarry[i])].append(('1'))
                if(int(j,2) + int(k,2) == int(initarry[i],2)):
                    initarry_record[str(initarry[i])].append((k,j))
    
    # print(initarry_record)
    sort_initarry_record = defaultdict(list)
    times = 0
    while(times < 30):
        tmp = []
        for j in range(len(initarry_record)):
            tmp_list = initarry_record[initarry[j]]
            if(len(tmp_list) == 0):
                continue
            # print(tmp_list)
            # print(len(tmp_list))
            loc = random.randint(1,len(tmp_list))
            # print(loc)
            tmp_ = list(tmp_list[loc - 1])
            for i in tmp_:
                tmp.append(i)
            tmp.append(initarry[j])
        tmp = list(set(tmp))
        sort_initarry_record[str(times)].append(tmp)
        sort_initarry_record[str(times)].append(len(tmp))
        times += 1
        # print("tmp = " +str(tmp))
        for i in tmp:
            # print("i = " +str(i))
            if(i == "1"):
                pass
            else:
                if(findadd_bool(int(i, 2), tmp)):
                    pass
                else:
                    tmpchain, _ = sortest_chain_in_windows(int(i, 2))
                    for j in tmpchain:
                        tmp.append(j)
    # for i in initarry_record
    min_keys, min_value = defaultdict_min(sort_initarry_record, 1)

    return sort_initarry_record[min_keys][0]

def method1(bin_num):
    print("===============method1====================")
    method1_record = defaultdict(list)
    for i in range(3,6):
        initarray = []
        addchain = []
        # print("++++++++++++++++++++++++++++++++++")
        # print("bin_num = " + bin_num)
        # print("win size = " + str(i))

        # step 1 , generate initchain with fixed win
        array = fixed_win(bin_num, i)  # get initarray by fixed win 
        print(array)
        addchain = calc_sortchain_inclued_array(array) # get the totally chain which include initarray
        print("addchain = " + str(addchain))

        # result 
        result_method1 = []
        # addchain = cut_the_initchain(addchain, array)
        addchain = sort_array(addchain)
        result_tuple = initarray2tuple(addchain, result_method1)
        # step 2 , generate chain by n
        addchain, result_tuple = fixwin_generate_chain(bin_num, addchain, array, i, result_tuple)

        # print("addchain = " + str(addchain))
        # print("addchain's len = " + str(len(addchain) - 1))
        method1_record[str(i)].append(addchain)
        method1_record[str(i)].append(len(addchain))
        method1_record[str(i)].append(result_tuple)
    
    min_keys, min_value = defaultdict_min(method1_record, 1)
    print("min_value(len) = " + str(min_value) + " " + str(method1_record[min_keys]))
    return method1_record[min_keys][0], method1_record[min_keys][2]

def method2(bin_num):
    print("===============method2====================")
    # print(bin_num)
    D_initarry, initchain_1  = D_get_initarray(bin_num)
    # print(" initchain_1 = " + str(initchain_1))
    # print(" D_initarry = " + str(D_initarry))
    initchain_1 = sort_array(initchain_1)
    initchain_1.reverse()
    # print(" initchain_1 = " + str(initchain_1))
    # print(" D_initarry = " + str(D_initarry))
    result_method2 = []
    # D_initarry = cut_the_initchain(D_initarry, initchain_1)
    D_initarry = sort_array(D_initarry)
    result_tuple = initarray2tuple(D_initarry, result_method2)
    D_addchain, result_tuple = generate_chain(bin_num, D_initarry, initchain_1, result_tuple)

    print("D_addchain = " + str(D_addchain))
    print("D_addchain's len = " + str(len(D_addchain) - 1))
    print(result_tuple)
    return D_addchain, result_tuple

def method3(bin_num):
    print("===============method3====================")
    D2_initarry,initarray_1 = D2_get_initarray(bin_num)
    # print("D2_initarry = " + str(D2_initarry))
    result_method3 = []
    result_tuple = []
    # D2_initarry = cut_the_initchain(D2_initarry, initarray_1)
    D2_initarry = sort_array(D2_initarry)
    result_tuple = initarray2tuple(D2_initarry, result_method3)
    D2_addchain, result_tuple = generate_chain(bin_num, D2_initarry, initarray_1, result_tuple)
    # print("D2_addchain = " + str(D2_addchain))

    print("D2_addchain = " + str(D2_addchain))
    print("D2_addchain 's len = " + str(len(D2_addchain) - 1))
    print(result_tuple)
    return D2_addchain,result_tuple

def method4(bin_num):
    print("===============method4====================")
    method4_record = defaultdict(list)
    for i in range(2,5):
        D3_initarry,initarray_1 = D3_get_initarray(bin_num, i)
        print("D3_initarry = " + str(D3_initarry))
        # print("initarray_1 = " + str(initarray_1))

        result_method4 = []
        D3_initarry = cut_the_initchain(D3_initarry, initarray_1)
        # print("after cut_the_initchain D3_initarry = " + str(D3_initarry))

        D3_initarry = sort_array(D3_initarry)
        result_tuple = initarray2tuple(D3_initarry, result_method4)
        # print("after result_tuple D3_initarry = " + str(D3_initarry))

        D3_addchain, result_tuple = generate_chain(bin_num, D3_initarry, initarray_1, result_tuple)
        # print("D3_addchain = " + str(D3_addchain))
        method4_record[str(i)].append(D3_addchain)
        method4_record[str(i)].append(len(D3_addchain) - 1)
        # method4_record[str(i)].append(D3_initarry)
        method4_record[str(i)].append(initarray_1)
        method4_record[str(i)].append(result_tuple)

    min_keys,min_value = defaultdict_min(method4_record, 1)
    print("min value = " + str(min_value) + " "  + str(method4_record[min_keys]))
    # print("D3_addchain = " + str(D3_addchain))
    # print("D3_addchain 's len = " + str(len(D3_addchain) - 1))    
    print(result_tuple)
    return method4_record[min_keys]

def defaultdict_max(defaultdict, flag): 
    max_score = 0
    max_score_keys = ""
    score_tmp = 0
    for i in defaultdict:
        score_tmp = defaultdict[i][flag]
        if(score_tmp > max_score):
            max_score = score_tmp
            max_score_keys = i
    return max_score_keys,max_score

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

def save_to_file(file_name, contents):
    fh = open(file_name, 'w')
    fh.write(contents)
    fh.close()

def print_result(result_tuple):
    str_result = "v0=1,v1=2"
    for i in result_tuple:
        if(i[0] == 1 or i[0] == 2):
            continue
        str_result += ",v" + str(i[1]) + "=" + str(i).replace(" ","")
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
    # num = raw_input("please input the number = ")
    asp_record = defaultdict(list)
    bin_num = bin(int(num))[2:]
    print("binary of number = " + bin_num)
    up = len(bin_num) - 1 + bin_num.count("1")
    low = len(bin_num) - 1 + math.log(bin_num.count("1"),2)
    print("the number of " + str(num) + "'s length = " + str(len(bin_num)))
    print("the number of " + str(num) + "'s Lower bound = " + str(low))
    print("the number of " + str(num) + "'s Upper Bound = " + str(up))

    result = []
    # fixed win size
    addchain1, result_tuple = method1(bin_num)
    asp_record["1"].append("method1")
    asp_record["1"].append(addchain1)
    asp_record["1"].append(len(addchain1) - 1)
    asp_record["1"].append(result_tuple)

    # Dynamic window size ; Split by 0.
    addchain2, result_tuple = method2(bin_num)
    asp_record["2"].append("method2")
    asp_record["2"].append(addchain2)
    asp_record["2"].append(len(addchain2) -1 )
    asp_record["2"].append(result_tuple)

    # Dynamic window size ; Split by 0 if the number of continuous 0 more than 3/4/5.
    addchain3, result_tuple = method3(bin_num)
    asp_record["3"].append("method3")
    asp_record["3"].append(addchain3)
    asp_record["3"].append(len(addchain3) - 1)
    asp_record["3"].append(result_tuple)


    method4_record = method4(bin_num)
    asp_record["4"].append("method4")
    asp_record["4"].append(method4_record[0])
    asp_record["4"].append(method4_record[1])
    asp_record["4"].append(method4_record[3])

    min_keys,min_value = defaultdict_min(asp_record, 2)
    # print("min value = " + str(min_value) + " " + str(asp_record[min_keys]))

    return asp_record[min_keys]

begin = datetime.now() 
# num = 10445360463911 - 5
# num = 211108170305887 - 5
# num = 13835058061724614657 - 1
num = 255211775190703851000955237173238443091 - 3
# num = 57896044618658097711785492504343953926634992332820282019728792003956564819949 - 5
# num = 6703903964971298549787012499102923063739682910296196688861780721860882015036773488400937149083451713845015929093243025426876941405973284973216824503042031 - 5

result = []
AspOfTen_record = defaultdict(list)

for i in range(10):
    sortestchain = exp(num + i)
    # print(sortestchain)
    print("========================")
    AspOfTen_record[str(i)].append(num + i)
    AspOfTen_record[str(i)].append(sortestchain[0]) # method number
    AspOfTen_record[str(i)].append(sortestchain[1]) # addchain
    AspOfTen_record[str(i)].append(sortestchain[2]) # addchain len
    AspOfTen_record[str(i)].append(sortestchain[3]) # result_tuple


min_keys,min_value = defaultdict_min(AspOfTen_record, 3)


num = AspOfTen_record[min_keys][0]
bin_num = bin(num)[2:]
up = math.floor(math.log(num,2)) + bin_num.count("1")
low = math.floor(math.log(num,2)) + math.log(bin_num.count("1"),2)

end = datetime.now() 
print("total time = " + str((end - begin)))
AspOfTen_record[min_keys].append(str((end - begin))) # time

if(check_the_result(AspOfTen_record[min_keys][4])):
    print("wrong...")
else:
    print("win...")


filename = "first_" + str(AspOfTen_record[min_keys][0])[-10:] + '.txt'
result_filename = "first_" + str(AspOfTen_record[min_keys][0])[-10:] + "_result " + '.txt'

content = "up = " + str(up) + "low = " + str(low) + print_result(AspOfTen_record[min_keys][4])
content = content.replace("L","")
save_to_file(filename, str(AspOfTen_record[min_keys]))
save_to_file(result_filename, content)

print("min value = " + str(min_value) + " " + str(AspOfTen_record[min_keys]))
# 10011000000000000000000000000000000000100111

