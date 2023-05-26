import json
import random

# 定义COCO标注文件的路径
annotations_file = "coco/annotations/instances_train2017.json"

# 读取COCO标注文件
with open(annotations_file, 'r') as f:
    coco_data = json.load(f)

# 从annotations列表中随机选择一个标注信息
annotations = coco_data['annotations']
random_annotation = random.choice(annotations)

# 获取相关信息
annotation_id = random_annotation['id']
image_id = random_annotation['image_id']
category_id = random_annotation['category_id']
bbox = random_annotation['bbox']
segmentation = random_annotation['segmentation']
area = random_annotation['area']
iscrowd = random_annotation['iscrowd']

# 获取图像信息
image_info = next((image for image in coco_data['images'] if image['id'] == image_id), None)
if image_info:
    image_file_name = image_info['file_name']
    image_width = image_info['width']
    image_height = image_info['height']
else:
    image_file_name = None
    image_width = None
    image_height = None

# 获取类别信息
category_info = next((category for category in coco_data['categories'] if category['id'] == category_id), None)
if category_info:
    category_name = category_info['name']
else:
    category_name = None

# 输出随机选择的标注信息
print("Random Annotation:")
print("Annotation ID:", annotation_id)
print("Image ID:", image_id)
print("Image File Name:", image_file_name)
print("Image Width:", image_width)
print("Image Height:", image_height)
print("Category ID:", category_id)
print("Category Name:", category_name)
print("Bounding Box (x, y, width, height):", bbox)
print("Segmentation:", segmentation)
print("Area:", area)
print("Is Crowd:", iscrowd)
