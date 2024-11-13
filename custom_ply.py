import os
import tqdm
import math

def vertex_amount(ply):
    f1 = open(ply, 'r')
    contents1 = f1.readlines()
    return contents1[5]

def find_start_idx(ply):
    f1 = open(ply, 'r')
    contents1 = f1.readlines()
    for idx, line in enumerate(contents1):
        if line == 'end_header\n':
            start_idx = idx + 1
    return start_idx

def rgb_array(ply, start_idx, col):
    arr = []
    with open(ply, 'r') as fr:
        contents = fr.readlines()[start_idx:]
        for i in contents:
            c = i.split(' ')
            arr.append(c[col])
            # arr.append(float(c[col]))
    return arr

def xyz_array(ply, i):
    dic = {}
    with open(ply, 'r') as fr:
        contents = fr.readlines()[i:]
        for i in contents:
            xyz = []
            c = i.split(' ')
            xyz.append(math.floor(float(c[0])*100)/100)
            xyz.append(math.floor(float(c[1])*100)/100)
            xyz.append(math.floor(float(c[2])*100)/100)
            dic[str(xyz)] = c[3]
    return dic

def xyz_arr_temp(ply, i):
    s = set()
    with open(ply, 'r') as fr:
        contents = fr.readlines()[i:]
        for i in contents:
            xyz = []
            c = i.split(' ')
            xyz.append(c[0])
            xyz.append(c[1])
            xyz.append(c[2])
            s.add(xyz) 
    return s
 
ori_path = '21_2'
save_path = 'ref_low'
file_lst = []
for f in os.listdir(ori_path):
    file_lst.append(f)
d = {}
# iterating over each string in the list
for s in file_lst:
    # extracting the substring before the underscore
    key = s.split('_')[0]+s.split('_')[1]+s.split('_')[3]
    # adding the string to the dictionary under the key
    if key in d:
        d[key].append(s)
    else:
        d[key] = [s]
res = list(d.values())

prob_set = set()
for ch in tqdm.tqdm(res):
    ref_start = find_start_idx(f"{ori_path}/{ch[0]}")
    nor_start = find_start_idx(f"{ori_path}/{ch[2]}")
    ref_ch = rgb_array(f"{ori_path}/{ch[0]}", ref_start, 3)
    nor_ch = rgb_array(f"{ori_path}/{ch[2]}", nor_start, 3)
    file_name = f"{ch[0].split('_')[0]}_{ch[0].split('_')[1]}_{ch[0].split('_')[3]}"
    f1 = open(f"{ori_path}/{ch[1]}", 'r')
    f2 = open(f"{save_path}/{file_name}", 'w')
    contents1 = f1.readlines()
    grey_start = find_start_idx(f"{ori_path}/{ch[1]}")
    for idx, line in enumerate(contents1):
        if idx < grey_start:
            f2.write(line)
        else:
            c = line.split(' ')
            try:
                line1 = line.replace(c[3]+' '+ c[4]+' '+c[5], c[3]+' '+ref_ch[idx-grey_start]+' '+nor_ch[idx-grey_start])  
                f2.write(line1) 
            except:
                prob_set.add(file_name)
    f1.close()
    f2.close()
print(prob_set)







