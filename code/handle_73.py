
import re
import math
import random
from ctypes import *
from datetime import datetime 
from collections import defaultdict
import logging
 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
 
# logger.info('This is a log info')
# logger.debug('Debugging')
# logger.warning('Warning exists')
# logger.info('Finish')

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

def sort_array(array):
    array_tmp = list(set(array))
    array_tmp = map(int, array_tmp)
    array_tmp.sort()
    # print(array)
    array_tmp = map(str, array_tmp)
    return array_tmp

def hanming(str):
    return str.count("1")

def dict2list(dict):
    tmp = []
    for i in dict:
        tmp.append(i[0])
    return tmp

def diffarray(A, B):
    leftover = list(set(A).difference(set(B)))
    return leftover

# calc the score of data
def str_scores(str_data):
    # print("str_data = " + str(str_data))
    count_1 = hanming(str_data) - 1
    return count_1

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

def Remove_duplicate(array):
    array_remove = list(set(array))
    array_remove.sort(key=array.index)
    return array_remove

# replace the continuous 1 which times = 5.6.7.8.....
def sub_continuous_one():
    global data
    global jihe
    global count_total
    global scores
    global bin_num
    # replace "11111111"
    # print(data)
    data_split_0 = list(Remove_duplicate(data.split("0")))
    if('' in data_split_0):
        data_split_0.remove('')
    # print(data_split_0)
    for i in xrange(0, 4): # 9\8\7\6\5
        replace_data = "1"*(8-i)
        if(data.count(replace_data) == 0):
            pass
        else:
            jihe.append(replace_data)
            count_total += data.count(replace_data)
            data = data.replace(replace_data,"0"*len(replace_data))
            scores += str_scores(replace_data)*count_total
    return data


def Calc_TopN(topN,select_N,n):
    global data
    global scores
    global jihe
    global count_total

    dict = {}
    # generate dict which hamimg weight is not zero and count it's scores out
    for i in xrange(2,pow(2,n)):
        tmp = bin(i)[2:]
        count_1 = hanming(tmp) - 1
        if(count_1 == 0):
            pass
        elif(tmp[-1] == "0"):  # cut the initarry which the last num is 0
            pass
        else:
            tmp = bin(i)[2:]
            count = data.count(tmp)
            dict[tmp] = count*count_1
    # print(sorted(dict))
    dict_top = sorted(dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    dict_top = dict_top[0:topN]
    # print(dict_top)

    dict_keys = dict2list(dict_top)
    # print(dict_keys)
    random.shuffle(dict_keys) 
    return dict_keys[0:select_N],dict_top

def cutout_one(topN):
    global data
    global scores
    global jihe
    global count_total

    dict = {}
    # generate dict which hamimg weight is not zero and count it's scores out
    for i in xrange(2,1024):
        tmp = bin(i)[2:]
        count_1 = hanming(tmp) - 1
        if(count_1 == 0):
            pass
        elif(tmp[-1] == "0"):  # cut the initarry which the last num is 0
            pass
        else:
            tmp = bin(i)[2:]
            count = data.count(tmp)
            dict[tmp] = count*count_1
    # print(sorted(dict))
    dict_top = sorted(dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    dict_top = dict_top[0:topN]
    # print(dict_top)

    dict_keys = dict2list(dict_top)

    random.shuffle(dict_keys)   # return None  --> random the topN
    # print(dict_keys)

    replace_keys = dict_keys[0]
    data = data.replace(replace_keys, "0"*len(replace_keys))
    jihe.append(replace_keys)
    # print(replace_keys)
    # print(dict[replace_keys])
    scores +=  dict[replace_keys]
    count_total += dict[replace_keys]/str_scores(replace_keys)
    # print(data)

def generate_chain(bin_num, initchain, jihe, result_tuple):
    addchain = initchain
    # print(addchain)
    index = 0
    find = 0
    cur_bin = ""
    first = 2
    # 
    initchain = sort_array(initchain)
    max_len = len(initchain[-1])
    begin_bin = bin_num[0:max_len]
    if(begin_bin not in initchain):
        print("not in")
    addchain = initchain
    # print(max_len)
    index = max_len
    cur_bin = bin_num[0:max_len]
    # print("bin_num = " + str(bin_num))
    # print(cur_bin)
    # print(jihe)
    jihe = initchain
    jihe = jihe[::-1]
    while(index <= len(bin_num)):
        # print(cur_bin)
        for i in jihe:
            str_len = len(i)
            find = 0
            if(bin_num[index:index+str_len] == i):
                find = 1
                for j in xrange(0, str_len):
                    addchain.append(cur_bin + "0"*(j+1))
                    result_tuple.append((int(cur_bin + "0"*(j+1), 2), len(result_tuple), len(result_tuple) - 1, len(result_tuple) - 1))
                    # addchain.append(cur_bin + "0")
                addchain.append(cur_bin + i)
                cur_bin = cur_bin + i
                # if(len(cur_bin) < 100):
                #     print(cur_bin)
                tmp_number = int(i, 2)
                init_index = findIndex(tmp_number, result_tuple[0:500])
                result_tuple.append((int(cur_bin, 2), len(result_tuple), len(result_tuple) - 1 , init_index - 1))
                index += str_len
                break
        if(find == 0):
            if(bin_num[index] == "1"):
                if(first == 2):
                    tmp_number = int(cur_bin + "0", 2)
                    # tmptmp = IntegrationList_bin(result_tuple)
                    # print(tmptmp)
                    x, y = findadd(tmp_number, IntegrationList_bin(result_tuple))
                    result_tuple.append((int(cur_bin + "0", 2), len(result_tuple), (x - 1), (y - 1)))
                    addchain.append(cur_bin + "0")
                    first = 3
                else:
                    addchain.append(cur_bin + "0")
                    result_tuple.append((int(cur_bin + "0", 2), len(result_tuple), len(result_tuple) - 1, len(result_tuple) - 1))
                addchain.append(cur_bin + "1")
                result_tuple.append((int(cur_bin + "1", 2), len(result_tuple), len(result_tuple) - 1, 0))
                cur_bin = cur_bin + "1"
            else:
                if(first == 2):
                    tmp_number = int(cur_bin + "0", 2)
                    # tmptmp = IntegrationList_bin(result_tuple)
                    # print(tmptmp)
                    x, y = findadd(tmp_number, IntegrationList_bin(result_tuple))
                    result_tuple.append((int(cur_bin + "0", 2), len(result_tuple), (x - 1), (y - 1)))
                    addchain.append(cur_bin + "0")
                    first = 3
                else:
                    result_tuple.append((int(cur_bin + "0", 2), len(result_tuple), len(result_tuple) - 1, len(result_tuple) - 1))
                    addchain.append(cur_bin + "0")
                cur_bin = cur_bin + "0"
            index += 1
        if((index) == len(bin_num)):
            break
    # checking
    # print("cur_bin =" + str(cur_bin))
    # print("sub = " + str(int(bin_num, 2) - int(cur_bin,2)))
    if(int(bin_num, 2) - int(cur_bin,2)):
        print("not_same")
        last_tmp = bin(int(bin_num, 2) - int(cur_bin,2))[2:]
        if(last_tmp in addchain):
            addchain.append(bin_num)
            cur_bin = bin_num

            tmp_number = int(last_tmp, 2)
            init_index = findIndex(tmp_number, result_tuple[0:50])
            result_tuple.append((int(cur_bin, 2), len(result_tuple), len(result_tuple) - 1 , init_index - 1))
        else:
            tmp_chain = sortest_chain_in_windows(last_tmp)
            addchain = combine_chain(tmp_chain, addchain)
            cur_bin = bin_num
    # print("index =" + str(index))
    # print("cur_bin =" + str(cur_bin))
    return addchain, result_tuple

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

# def findadd(number, initarray):
#     for i in range(len(initarray)):
#         for j in range(len(initarray)):
#             if(int(initarray[i],2) + int(initarray[j],2) == number):
#                 return i+1, j+1
def findadd(number, initarray):
    for i in xrange(0, len(initarray)):
        for j in xrange(0, len(initarray)):
            if(int(initarray[i],2) + int(initarray[j],2) == number):
                return i+1, j+1
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
    for i in xrange(0, len(result_list)):
        if(result_list[i] == num):
            return i+1

def initarray2tuple(initarray, result):
    # print(initarray)
    for i in xrange(0, len(initarray)):
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
                result.append((tmp,i, x - 1 , y - 1))
    return result

def save_to_file(file_name, contents):
    fh = open(file_name, 'w')
    fh.write(contents)
    fh.close()
    print(file_name + "have saved.")

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
            print(i)
            # print(result_tuple[i(2)])
            # print(result_tuple[i(3)])
            return True
    return False

def exp(num):
    global count_total
    global data
    global scores
    global jihe

    begin = datetime.now() 
    print(datetime.strptime(str(begin),"%Y-%m-%d %H:%M:%S.%f"))
    scores = 0 
    asp_record = defaultdict(list)
    times = 0
    bin_num = bin(int(num))[2:]
    # print("binary of number = " + bin_num)
    up = math.floor(math.log(num,2)) + bin_num.count("1")
    low = math.floor(math.log(num,2)) + math.log(bin_num.count("1"),2)
    # print("the number's length = " + str(len(bin_num)))
    print("the number's Lower bound = " + str(low))
    print("the number's Upper Bound = " + str(up))

    print("calculating......")

    # 1-10
    # begin = "99999"
    for times in xrange(0, 2500):
        # num = 1847699703211741474306835620200164403018549338663410171471785774910651696711161249859337684305435744585616061544571794052229717732524660960646946071249623720442022269756756687378427562389508764678440933285157496578843415088475528298186726451339863364931908084671990431874381283363502795470282653297802934916155811881049844908319545009848393775227257052578591944993870073695755688436933812779613089230392569695253261620823676490316036551371447913932347169566988069
        data = bin(int(num))[2:]
        scores = 0 
        count_total = 0
        jihe = [] 

        bin_num_ = sub_continuous_one()  # replace the data of continuous "1"

        # print("count_total = " + str(count_total))
        # print("scores = " + str(scores))

        # print("binary of number = " +str(bin_num))
        seq_num = []
        # for i in range(3):
        #     cutout_one(7)  # random from top10
        # seq_num = []

        # change the seq_num will be better.

        for i in xrange(0, 4):
            seq_num.append(random.randint(7,10))
        for i in xrange(0, 3):
            seq_num.append(random.randint(5,7))
        for i in xrange(0, 2):
            seq_num.append(random.randint(3,5))
        for i in xrange(0, 2):
            seq_num.append(random.randint(2,3))
        for i in xrange(0, 1):
            seq_num.append(random.randint(1,2))
        # print("seq = " + str(seq_num))

        # Traversing all of seq
        # seq_num = []
        # for i in begin:
        #     seq_num.append(i)
        # begin_int = int(begin,10)
        # begin = str(begin_int - 1)
        # if('0' in seq_num):
        #     continue
        
        for i in seq_num:
            cutout_one(int(i))
        
        # cutout_one(7) 
        # cutout_one(6) 
        # cutout_one(5) 
        # cutout_one(4) 
        # cutout_one(3) 

        if(times % 200 == 0):
            print(times)
            # print(seq_num)
        
        asp_record[str(times)].extend([
        scores, # 0
        count_total, # 1
        data.count("1"),  # 2 count_total 
        count_total + data.count("1"), # 3 count_total
        jihe, # 4
        seq_num]) # 5

        result_tuple = []
        # begin generate the initarry
        jihe = sort_array(jihe)[::-1]
        # print("jihe = " + str(jihe))
        # jihe = jihe[::-1]

        initarray = sort_array(jihe)
        # print("jihe = " + str(jihe))
        # print("initarray = " + str(initarray))
        max_len = len(initarray[-1])
        initarray.append(bin_num[0:max_len])
        initarray = sort_array(initarray)
        initchain, _ = sortest_chain_in_windows(int(initarray[-1],2))
        # print("initchain = " + str(initchain))
        
        initchain = combine_chain(initarray, initchain)
        # initchain = sort_array(initchain)
        # print("initchain = " + str(initchain))
        # print("initchain = " + str(len(initchain)))
        result_tuple = initarray2tuple(initchain, result_tuple)
        # print(result_tuple)

        # print(jihe)
        # print(initchain)
        addchain, result_tuple = generate_chain(bin_num, initchain, jihe, result_tuple) # give the replace seq from "jihe"
        # print(result_tuple[-1][0] == int(bin_num, 2))
        # print(result_tuple[-1][0])
        percent = format((len(addchain) - low)/(up - low))
        # print("percentage of result =  {:.2%}".percent)
        
        asp_record[str(times)].extend([
        float(percent), # 6
        len(addchain) - 1, # 7
        addchain, # 8
        result_tuple]) # 9

        # if(check_the_result(result_tuple)):
        #     pass
            # print("wrong...")
            # print(jihe)
            # print("result_tuple = " + str(result_tuple)[0:1000])
        # else:
        #     pass
            # print("win...")

    # max_scores_key, max_scores = defaultdict_max(asp_record, 0)   # flag = 0 <score> ; flag = 1 <count>
    # min_count_key, min_count = defaultdict_min(asp_record, 1)   # flag = 0 <score> ; flag = 1 <count>

    min_percent_key, min_percent = defaultdict_min(asp_record, 6) 
    # print("max scores = " + str(max_scores) + " " + str(asp_record[max_scores_key]))
    # print("min count = " + str(min_count) + " " + str(asp_record[min_count_key]))
    print("min percent = " + str(min_percent) + " " + str(len(asp_record[min_percent_key][9])) + " " + str(asp_record[min_percent_key][9][0:30]))

    end = datetime.now() 
    datetime.strptime(str(end),"%Y-%m-%d %H:%M:%S.%f")
    return  asp_record[min_percent_key],asp_record[min_percent_key][8], asp_record[min_percent_key][9], (end - begin).seconds

def exp1(num):
    global count_total
    global data
    global scores
    global jihe

    begin = datetime.now() 
    print(datetime.strptime(str(begin),"%Y-%m-%d %H:%M:%S.%f"))
    scores = 0 
    asp_record = defaultdict(list)
    times = 0
    bin_num = bin(int(num))[2:]
    # print("binary of number = " + bin_num)
    up = math.floor(math.log(num,2)) + bin_num.count("1")
    low = math.floor(math.log(num,2)) + math.log(bin_num.count("1"),2)
    # print("the number's length = " + str(len(bin_num)))
    print("the number's Lower bound = " + str(low))
    print("the number's Upper Bound = " + str(up))

    print("calculating......")

    for times in xrange(0,1000):
        # init
        data = bin(int(num))[2:]
        scores = 0 
        count_total = 0
        jihe = []
        # bin_num_ = sub_continuous_one()
        jihe_tmp,tmp_TopN = Calc_TopN(10,3,5)
        jihe.extend(jihe_tmp)
        # logger.info("jihe = " + str(jihe))

        result_tuple = []
        # begin generate the initarry
        jihe = sort_array(jihe)[::-1]
        # print("jihe = " + str(jihe))
        # jihe = jihe[::-1]

        initarray = sort_array(jihe)
        # print("jihe = " + str(jihe))
        # print("initarray = " + str(initarray))
        max_len = len(initarray[-1])
        initarray.append(bin_num[0:max_len])
        initarray = sort_array(initarray)
        initchain, _ = sortest_chain_in_windows(int(initarray[-1],2))
        # print("initchain = " + str(initchain))
        
        initchain = combine_chain(initarray, initchain)
        # initchain = sort_array(initchain)
        # print("initchain = " + str(initchain))
        # print("initchain = " + str(len(initchain)))
        result_tuple = initarray2tuple(initchain, result_tuple)
        # print(result_tuple)

        addchain, result_tuple = generate_chain(bin_num, initchain, jihe, result_tuple)

        percent = format((len(addchain) - low)/(up - low))

        # print(percent)
        asp_record[str(times)].extend([
            float(percent), # 0 
            jihe, # 1
            addchain, # 2
            result_tuple,
            tmp_TopN]) # 3
        # print(len(result_tuple))
        
        if(times % 200 == 0):
            print(times)

    min_percent_key, min_percent = defaultdict_min(asp_record, 0) 
    # print("min_percent_key" + str(min_percent_key))
    # print(min_percent)
    print("min percent = " + str(min_percent) + " " + str(len(asp_record[min_percent_key][3])) + " " + str(asp_record[min_percent_key][3][0:30]) + "jihe =  " + str(asp_record[min_percent_key][1]) + "TopN =  " + str(asp_record[min_percent_key][4]))

    end = datetime.now() 
    datetime.strptime(str(end),"%Y-%m-%d %H:%M:%S.%f")

    return asp_record[min_percent_key],asp_record[min_percent_key][2], asp_record[min_percent_key][3], (end - begin).seconds

# num = 18476997032117414743068356
num = 1847699703211741474306835620200164403018549338663410171471785774910651696711161249859337684305435744585616061544571794052229717732524660960646946071249623720442022269756756687378427562389508764678440933285157496578843415088475528298186726451339863364931908084671990431874381283363502795470282653297802934916155811881049844908319545009848393775227257052578591944993870073695755688436933812779613089230392569695253261620823676490316036551371447913932347169566988069

# num = 255211775190703851000955237173238443091 - 3
num = num - 5
bin_num = bin(num)[2:]
up = math.floor(math.log(num,2)) + bin_num.count("1")
low = math.floor(math.log(num,2)) + math.log(bin_num.count("1"),2)
begin = datetime.now() 
# AspOfTen_record = defaultdict(list)
flag = 0
if(flag == 1):
    for i in xrange(5):
        child_begin = datetime.now() 
        print("=============== exp1 =====================")
        print(num + i)
        asp_record, addchain, result_tuple, subtime = exp1(num + i)
        print("num " + str(i) + " = " + str(subtime))
        child_end = datetime.now() 

        logger.info("child total time = " + str((child_end - child_begin)))

        
        # save result
        # print(AspOfTen_record[min_keys])
        filename = "third_" + str(len(addchain) - 1) + "_" + str(num+i)[-10:] + '.txt'
        result_filename = "third_" + str(len(addchain) - 1) + "_" + str(num+i)[-10:] + "_result " + '.txt'

        content = print_result(result_tuple)
        content_second = "up = " + str(up) + "low = " + str(low) + str(num)[-10:0] + "len = " + str(len(addchain) - 1) + "time = " + str((child_end - child_begin)) + " " + str(asp_record)

        if(check_the_result(result_tuple)):
            print("wrong...")
            print("result_tuple = " + str(result_tuple)[0:500])
        else:
            # pass
            print("win...")

        save_to_file(filename, content_second)
        print(filename)
        save_to_file(result_filename, content)

    end = datetime.now() 
    logger.info("total time = " + str((end - begin)))
else:
    for i in xrange(5, 10):
        child_begin = datetime.now() 
        print("====================================")
        print("i = " + str(i))
        print(num+i)
        asp_record, addchain, result_tuple, subtime = exp(num+i)
        print("num " + str(i) + " = " + str(subtime))
        # min_keys,min_value = defaultdict_min(AspOfTen_record, 1)
        
        child_end = datetime.now() 
        print("child total time = " + str((child_end - child_begin)))

        # save result
        # print(AspOfTen_record[min_keys])
        filename = "third_" + str(len(addchain) - 1) + "_" + str(num+i)[-10:] + '.txt'
        result_filename = "third_" + str(len(addchain) - 1) + "_" + str(num+i)[-10:] + "_result " + '.txt'

        content = print_result(result_tuple)
        content_second = "up = " + str(up) + "low = " + str(low) + str(num)[-10:0] + "len = " + str(len(addchain) - 1) + "time = " + str((child_end - child_begin)) + " " + str(asp_record)

        if(check_the_result(result_tuple)):
            print("wrong...")
            print("result_tuple = " + str(result_tuple)[0:500])
        else:
            # pass
            print("win...")

        save_to_file(filename, content_second)
        print(filename)
        save_to_file(result_filename, content)
        del addchain
        del result_tuple
        del content_second
        del content
    
    end = datetime.now()
    print("total time = " + str((end - begin)))













# print("data's '1' nums = " + str(data.count("1")))

# print("max count = " + str(asp_record))
# scores = 456
# init_array = ['11110', '111', '10110', '110', '10100', '1001', '100001000', '1000000010', '1000000100']
# scores = 462d
# init_array = ['1111', '1011', '111', '11', '1010', '1001', '1000000100', '100000100', '1000100000']


# max scores = 466[466, 266, ['1111', '1011', '10011', '101', '110', '100100', '1000100000', '100000100', '100001000']]