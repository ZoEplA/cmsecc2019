import math
from datetime import datetime 


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

def IntegrationList(result):
    tmp = []
    for i in result:
        tmp.append(i[0])
    return tmp

def findadd(number, initarray):
    for i in range(len(initarray)):
        for j in range(len(initarray)):
            if(int(initarray[i],2) + int(initarray[j],2) == number):
                return i+1, j+1
    return False

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

def generate_begin_chain(bin_num, addchain):
    addchain_int = map(int, addchain)
    print(addchain)
    # print("===================================")
    max_len = len(str(max(addchain_int)))
    for i in range(0,max_len):
        tmp = bin_num[0:max_len - i]
        if(tmp in addchain):
            # if(len(tmp) == max_len):
            return addchain, len(tmp)

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
    if(int(bin_num, 2) - int(cur_bin,2)):
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
    return addchain, result_tuple

def check_the_result(result_tuple):
    result_tuple_re = result_tuple[::-1]
    for i in result_tuple_re:
        if(i == (1,) or i == (2,)):
            continue
        if(result_tuple[i[2]][0] + result_tuple[i[3]][0] == i[0]):
            pass
        else:
            print(i)
            print(result_tuple[i[2]])
            print(result_tuple[i[3]])
            return True
    return False
    
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

begin = datetime.now() 
data = "11000000000000000000000000000000000000000000000000000000101110001000000000000000000000000000000000000000000000000010110001010000"

up = math.floor(math.log(int(data, 2),2)) + data.count("1")
low = math.floor(math.log(int(data, 2),2)) + math.log(data.count("1"),2)
'''
11000000000000000000000000000000000000000000000000000000101
00000100000000000000000000000000000000000000000000000000110
11000100000000000000000000000000000000000000000000000001011
0001010000

11000000000000000000000000000000000000000000000000000000101
11000100000000000000000000000000000000000000000000000001011
0001010000
'''
initchain = ['101','11']
addchain = ['1','10','11','101']
result_tuple = []
result_tuple = initarray2tuple(addchain, result_tuple)
print(result_tuple)
data1 = "11000000000000000000000000000000000000000000000000000000101"
_, result_ = generate_chain(data1, addchain, initchain,result_tuple)
data1_result_num = result_[-1][1]
data2 = "1100000000000000000000000000000000000000000000000000000010100000100000000000000000000000000000000000000000000000000110"
addchain, result_tuple = generate_chain(data2, addchain, initchain,result_tuple)
print(len(addchain))
print(result_tuple)

data3 = int(data1,2) + int(data2,2)
print(result_tuple[data1_result_num])
# print(bin(data3)[2:])
result_tuple.append((data3, len(result_tuple), len(result_tuple) - 1 , data1_result_num))
data3_bin = bin(data3)[2:]
addchain.append(data3_bin)

result_tuple.append((int(data3_bin + "0", 2), len(result_tuple), len(result_tuple) - 1, len(result_tuple) - 1))
addchain.append(data3_bin + "0")
result_tuple.append((int(data3_bin + 2*"0", 2), len(result_tuple), len(result_tuple) - 1, len(result_tuple) - 1))
addchain.append(data3_bin + "0"*2)
result_tuple.append((int(data3_bin + 3*"0", 2), len(result_tuple), len(result_tuple) - 1, len(result_tuple) - 1))
addchain.append(data3_bin + "0"*3)
result_tuple.append((int(data3_bin + 4*"0", 2), len(result_tuple), len(result_tuple) - 1, len(result_tuple) - 1))
addchain.append(data3_bin + "0"*4)
result_tuple.append((int(data3_bin + 5*"0", 2), len(result_tuple), len(result_tuple) - 1, len(result_tuple) - 1))
addchain.append(data3_bin + "0"*5)
result_tuple.append((int(data3_bin + 6*"0", 2), len(result_tuple), len(result_tuple) - 1, len(result_tuple) - 1))
addchain.append(data3_bin + "0"*6)

result_tuple.append((int(data3_bin + "000101", 2), len(result_tuple), len(result_tuple) - 1, 3))
addchain.append(data3_bin + "000101")

data3_bin = data3_bin + "000101"
result_tuple.append((int(data3_bin + "0", 2), len(result_tuple), len(result_tuple) - 1, len(result_tuple) - 1))
addchain.append(data3_bin + "0")
result_tuple.append((int(data3_bin + 2*"0", 2), len(result_tuple), len(result_tuple) - 1, len(result_tuple) - 1))
addchain.append(data3_bin + "0"*2)
result_tuple.append((int(data3_bin + 3*"0", 2), len(result_tuple), len(result_tuple) - 1, len(result_tuple) - 1))
addchain.append(data3_bin + "0"*3)
result_tuple.append((int(data3_bin + 4*"0", 2), len(result_tuple), len(result_tuple) - 1, len(result_tuple) - 1))
addchain.append(data3_bin + "0"*4)

if(check_the_result(result_tuple)):
    print("wrong...")
else:
    print("win...")

end = datetime.now() 
print("total time = " + str((end - begin)))

filename = "four_" + str(int(data,2))[-10:] + '.txt'
content = "up = " + str(up) + "low = " + str(low)  + " time = " + str((end - begin)) + " " +  print_result(result_tuple) 
content = content.replace("L","")
save_to_file(filename, content)

print(addchain)
print(len(addchain) - 1)
print(len(result_tuple))
print(result_tuple[-1])