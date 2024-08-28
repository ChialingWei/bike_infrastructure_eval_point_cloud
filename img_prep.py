import cv2
import os
import tqdm
from ply_to_jpg import*
from SAM import*

def find_start_idx(ply):
    f1 = open(ply, 'r')
    contents1 = f1.readlines()
    for idx, line in enumerate(contents1):
        if line == 'end_header\n':
            start_idx = idx + 1
    return start_idx

def mod_ply(nor_ply, bw_ply, start_idx):
    f1 = open(nor_ply, 'r')
    f2 = open(bw_ply, 'w')
    contents1 = f1.readlines()
    for idx, line in enumerate(contents1):
        if idx < start_idx:
            f2.write(line)
        else:
            c = line.split(' ')
            if float(c[3]) > 200:
                line1 = line.replace(c[3]+' '+c[4]+' '+c[5], '255 255 255')
                f2.write(line1)
            elif float(c[3]) < 120:
                line1 = line.replace(c[3]+' '+c[4]+' '+c[5], '255 255 255')
                f2.write(line1)
            else:    
                line1 = line.replace(c[3]+' '+c[4]+' '+c[5], '0 0 0')
                f2.write(line1)
    f1.close()
    f2.close()

def lane_mark(ref_ply, lane_ply, start_idx):
    f1 = open(ref_ply, 'r')
    f2 = open(lane_ply, 'w')
    contents1 = f1.readlines()
    for idx, line in enumerate(contents1):
        if idx < start_idx:
            f2.write(line)
        else:
            c = line.split(' ')
            if float(c[3]) > 210:
                line1 = line.replace(c[3]+' '+c[4]+' '+c[5], '255 255 255')  
                f2.write(line1)          
            else:    
                line1 = line.replace(c[3]+' '+c[4]+' '+c[5], '0 0 0')  
                f2.write(line1)
    f1.close()
    f2.close()

## moving car & road curb
## thresholding nor ply
# for ply in tqdm.tqdm(os.listdir('E:/code/custom_intensity_all')):
#     if 'nor' in ply:
#         nor = os.path.join('E:/code/custom_intensity_all', ply)
#         mod_nor = ply.replace('.ply', '_mod.ply')
#         mod_nor_path = os.path.join('E:/code/bw_ply', mod_nor)
#         st_idx = find_start_idx(nor)
#         mod_ply(nor, mod_nor_path, st_idx)

## black white nor ply file to image
# ori_path = 'E:/code/bw_ply'
# saved_path = 'E:/code/bw_img'
# for ply in tqdm.tqdm(os.listdir(ori_path)):
#     ply_path = os.path.join(ori_path, ply)
#     img_path = ply_to_jpg(ply_path)
#     img_name = ply.replace('_mod.ply', '.jpg')
#     save_img = os.path.join(saved_path, img_name)
#     cv2.imwrite(save_img, img_path)

## SAM on black white nor image
# ori_path = 'E:/code/bw_img'
# saved_path = 'E:/code/SAM'
# for img_name in tqdm.tqdm(os.listdir(ori_path)):
#     img_path = os.path.join(ori_path, img_name)
#     image = cv2.imread(img_path)  
#     img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     masks = segment_anything(img)
#     image_name = img_name.replace('nor', 'rgb')
#     save_img = os.path.join(saved_path, image_name)
#     plt.figure(figsize=(10,10))
#     plt.imshow(img)
#     show_anns(masks)
#     plt.axis('off')
#     plt.savefig(save_img)
#     plt.close()

# # lane markings
## thresholding 3dref ply
# for ply in tqdm.tqdm(os.listdir('E:/code/custom_intensity_all')):
#     if 'ref' in ply:
#         ref = os.path.join('E:/code/custom_intensity_all', ply)
#         mod_ref = ply.replace('3dref', 'rgb')
#         mod_lane = mod_ref.replace('.ply', '_lane.ply')
#         mod_lane_path = os.path.join('E:/code/lane_ply', mod_lane)
#         try:
#             st_idx = find_start_idx(ref)
#             lane_mark(ref, mod_lane_path, st_idx)
#         except:
#             print(ply)

## black white 3dref ply file to image
# ori_path = 'E:/code/lane_ply'
# saved_path = 'E:/code/bw_lane_img'
# for ply in tqdm.tqdm(os.listdir(ori_path)):
#     ply_path = os.path.join(ori_path, ply)
#     img_path = ply_to_jpg(ply_path)
#     img_name = ply.replace('.ply', '.jpg')
#     save_img = os.path.join(saved_path, img_name)
#     cv2.imwrite(save_img, img_path)

## SAM on black white 3dref image
# ori_path = 'E:/code/bw_lane_img'
# saved_path = 'E:/code/SAM_lane'
# for img_name in tqdm.tqdm(os.listdir(ori_path)):
#     img_path = os.path.join(ori_path, img_name)
#     image = cv2.imread(img_path)  
#     img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     masks = segment_anything(img)
#     save_img = os.path.join(saved_path, img_name)
#     plt.figure(figsize=(10,10))
#     plt.imshow(img)
#     show_anns(masks)
#     plt.axis('off')
#     plt.savefig(save_img)
#     plt.close()
