#lien kết với googledrive
from google.colab import drive
drive.mount('/content/gdrive')

#tai darknet
cd /content/gdrive/MyDrive/Machine Learing/Demo-final/YOLO
!git clone https://github.com/AlexeyAB/darknet
!gdown --id 1JKF-bdIklxOOVy-2Cr5qdvjgGpmGfcbp

#copy và thay the ten
!cp cfg/yolov4-custom.cfg  cfg/yolo-obj.cfg

#
import os
def create_txt(path, file_out):
  lst_files = os.listdir(path)
  lst_images = []
  for file in lst_files:
    if ".jpg" in file:
      lst_images.append(file) 
  with open(file_out,"w") as f:
    for img in lst_images:
      x= path+"/"+img+"\n"
      f.write(x)

# Chuyen file .xml thanh file .txt 
import xml.etree.ElementTree as ET
import os
import glob
def Convert2List(file_xml):
  tree = ET.parse(file_xml)
  root = tree.getroot() 
  all_lst = []
  size = root.find('size')
  height = int(size.find('height').text)
  width = float(size.find('width').text) 
  for object in root.findall('object'):
    name = object.find('name').text
    lst = [name]
    for bdb in object.findall('bndbox'):
      xmin = int(bdb.find('xmin').text)
      xmax = int(bdb.find('xmax').text)
      ymin = int(bdb.find('ymin').text)
      ymax = int(bdb.find('ymax').text)
      
      x = round(((xmin + xmax)/2)/width, 6)
      y = round(((ymin + ymax)/2)/height, 6)
      w = round((xmax - xmin)/width,6)
      h = round((ymax - ymin)/height,6)

      lst.append(x)
      lst.append(y)
      lst.append(w)
      lst.append(h)
    all_lst.append(lst)
  return all_lst

cd /content/gdrive
#chuyen train.xml thanh train.txt 
path = "/content/gdrive/MyDrive/Machine Learing/Demo-final/UIT-VD/Train"
path_out = '/content/gdrive/MyDrive/Machine Learing/Demo-final/UIT-VD/Train-txt'
for filename in glob.glob(os.path.join(path, '*.xml')):
    with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
      name = filename.replace(path,'')
      filename_out = path_out + name.replace('.xml','.txt')
      print(filename_out)
      lst = Convert2List(filename) 
      with open(filename_out, 'w') as file:
        for row in lst:
          s = " ".join(map(str, row))
          file.write(s+'\n')

#chuyen test.xml thanh test.txt 
path = "/content/gdrive/MyDrive/Machine Learing/Demo-final/UIT-VD/Test"
path_out = '/content/gdrive/MyDrive/Machine Learing/Demo-final/UIT-VD/Test-txt'
for filename in glob.glob(os.path.join(path, '*.xml')):
    with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
      name = filename.replace(path,'')
      filename_out = path_out + name.replace('.xml','.txt')
      print(filename_out)
      lst = Convert2List(filename) 
      with open(filename_out, 'w') as file:
        for row in lst:
          s = " ".join(map(str, row))
          file.write(s+'\n')

!rm -rf "/content/drive/MyDrive/Data/DONE"

cd /content/drive/MyDrive/Machine Learing/Demo-final/YOLO/darknet
# change makefile to have GPU and OPENCV enabled
!sed -i 's/OPENCV=0/OPENCV=1/' Makefile
!sed -i 's/GPU=0/GPU=1/' Makefile
!sed -i 's/CUDNN=0/CUDNN=1/' Makefile
!sed -i 's/LIBSO=0/LIBSO=1/' Makefile
!sed -i 's/CUDNN_HALF=0/CUDNN_HALF=1/' Makefile
!make

#train
!./darknet detector train data/obj.data cfg/yolo-obj.cfg yolov4.conv.137 -dont_show -map

#test
!./darknet detector test data/obj.data cfg/yolo-obj.cfg yolov-obj_best.weights -thresh 0.5 #-thresh 0.5