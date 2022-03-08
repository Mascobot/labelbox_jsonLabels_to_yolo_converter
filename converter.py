#Labeling format comverter:
#Converter of Labelbox json format to Yolov5 format
import json
import os
import cv2


########Only inputs needed:
path = '' #Path to dataset folder
json_file_name = '.json' #Name of json file (ahouls be in the same dataset folder)
class_index = {'class1':0, 'class2': 1, 'class3': 2}#Fill class index
#########


with open(f"{os.path.join(path,json_file_name)}", "r") as f:
    image_annotations = json.load(f)
f.close()
lista = []
for idx, bbox in enumerate(image_annotation["Label"]["objects"]):
    lista.append(bbox['value'])
         
print ('Number of images with annotations: {}'.format(len(image_annotations)))
print ('Classes in whole dataset: {}'.format(str(set(lista))))

for image_annotation in image_annotations:#For each image file with annotations
    filename = image_annotation["External ID"].split(".jpg")[0]#Get the filename
    image_path = os.path.join(path, filename + '.jpg')
    img = cv2.imread(image_path)
    img_h, img_w, _ = img.shape#Get image size
    with open(os.path.join(path, filename + '.txt'),'w') as f:#Create new txt file
        for idx, bbox in enumerate(image_annotation["Label"]["objects"]):
            w = bbox["bbox"]["width"]
            new_w = w/img_w
            
            h = bbox["bbox"]["height"]
            new_h = h/img_h
            
            center_y = bbox["bbox"]["top"] + (h//2)
            new_y = center_y/img_h
            
            center_x = bbox["bbox"]["left"] + (w//2)
            new_x = center_x/img_w
            
            class_value = class_index[bbox['value']]
            f.write(f"{class_value} {new_x} {new_y} {new_w} {new_h}\n")
