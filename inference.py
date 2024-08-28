from ultralytics import YOLO
import os 
import numpy as np
from sklearn.linear_model import LinearRegression
import math

def pred_cls_dic(result):
    cls_dic = {}
    cls_dic['curb'] = []
    cls_dic['mov'] = []
    cls_dic['lane'] = []
    for idx, cls in enumerate(result[0].boxes.cls):
        if cls.item() == 0.0:
            cls_dic['curb'].append(idx)
        elif cls.item() == 1.0:
            cls_dic['mov'].append(idx)
        else:
            cls_dic['lane'].append(idx)
    return cls_dic

def LR(arr):
    list_x, list_y = [], []
    for pt in arr:
        list_x.append(pt[0])
        list_y.append(pt[1])
    X = np.array(list_x).reshape((-1, 1))
    y = np.array(list_y)
    reg = LinearRegression().fit(X, y)
    coef = reg.coef_
    intercept = reg.intercept_
    return coef, intercept

def shortest_distance(x1, y1, a, b, c): 
    d = abs((a * x1 + b * y1 + c)) / (math.sqrt(a * a + b * b))
    return d

def dis_to_lane(lst, lane_a, lane_c):
    dis = []
    for p in lst:
        d = shortest_distance(p[0], p[1], lane_a, 1, lane_c)
        dis.append(d)
    min_d = min(dis)*50/1280
    avg_dis_meter = (sum(dis) / len(dis))*50/1280
    return avg_dis_meter, min_d

def ramain_lst(result, idx, dir, lane_min_thr, lane_max_thr):
    lst = result[0][idx].masks.xy[0].tolist()
    remain_lst = []
    for pt in lst:
        if lane_min_thr <= pt[dir] <= lane_max_thr:
            remain_lst.append(pt)
    return remain_lst

def inf(trained_model, img_source, save, name):
    curb = trained_model.predict(img_source, save, imgsz=1280, conf=0.2, classes=0, max_det=2, name=f"{name}curb")
    mov = trained_model.predict(img_source, save, imgsz=1280, conf=0.05, classes=1, max_det=2, name=f"{name}mov")
    lane = trained_model.predict(img_source, save, imgsz=1280, conf=0.05, classes=2, max_det=2, name=f"{name}lane")
    return curb, mov, lane

trained_model = YOLO('model\ori_best.pt')
img_path = 'ori_yolo_dataset\images/val/6_2_25.jpg'
name = '6_2_25'
save = True
curb_result, mov_result, lane_result = inf(trained_model, img_path, save, name)

lane_lst_all = []
for idx in range(len(lane_result[0])):
    lane_lst = lane_result[0][idx].masks.xy[0].tolist()
    lane_lst_all += lane_lst

lane_coef, lane_interc = LR(lane_lst_all)
lane_a, lane_c = -lane_coef[0], -lane_interc 
x = [row[0] for row in lane_lst_all]
y = [row[1] for row in lane_lst_all]

if abs(max(x) - min(x)) > abs(max(y) - min(y)):    #horizontal
    dir = 0
    min_thr, max_thr = min(x), max(x)
else:                                              #vertcal
    dir = 1
    min_thr, max_thr = min(y), max(y)

curb_dis = []
for idx in range(len(curb_result[0])):
    curb_remain_lst = ramain_lst(curb_result, idx, dir, min_thr, max_thr)
    if curb_remain_lst != []:
        curb_dis_meter, _ = dis_to_lane(curb_remain_lst, lane_a, lane_c)
        curb_dis.append(curb_dis_meter)
if curb_dis == []:
    avg_curb_dis = 0
else:
    avg_curb_dis = sum(curb_dis)/len(curb_dis)

mov_dis, shortest_dis = [], []
for idx in range(len(mov_result[0])):
    mov_remain_lst = ramain_lst(mov_result, idx, dir, min_thr, max_thr)
    if mov_remain_lst == []:
        avg_mov_dis_meter, min_mov_d = 0, 0
    else:
        avg_mov_dis_meter, min_mov_d = dis_to_lane(mov_remain_lst, lane_a, lane_c)
        mov_dis.append(avg_mov_dis_meter)
        shortest_dis.append(min_mov_d)
try:
    avg_mov_dis_meter = min(mov_dis)
    mov_shortest_meter = min(shortest_dis)
except:
    avg_mov_dis_meter = 0
    mov_shortest_meter = 0

dis_json = {}
dis_json[name] = [avg_curb_dis, avg_mov_dis_meter, mov_shortest_meter]
print(dis_json)