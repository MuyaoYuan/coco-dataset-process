import os
import random
import json
from shutil import copyfile

def create_mini_coco_dataset(train_annotations_file, val_annotations_file, train_images_dir, val_images_dir, output_dir, sample_percentage):
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    mini_train_dir = os.path.join(output_dir, 'train2017')
    mini_val_dir = os.path.join(output_dir, 'val2017')
    mini_annotations_dir = os.path.join(output_dir, 'annotations')
    os.makedirs(mini_train_dir, exist_ok=True)
    os.makedirs(mini_val_dir, exist_ok=True)
    os.makedirs(mini_annotations_dir, exist_ok=True)

    # 复制训练集图像
    train_image_files = os.listdir(train_images_dir)
    sample_size = int(len(train_image_files) * sample_percentage)
    sampled_train_image_files = random.sample(train_image_files, sample_size)
    for image_file in sampled_train_image_files:
        src_image_path = os.path.join(train_images_dir, image_file)
        dst_image_path = os.path.join(mini_train_dir, image_file)
        copyfile(src_image_path, dst_image_path)

    # 复制验证集图像
    val_image_files = os.listdir(val_images_dir)
    sample_size = int(len(val_image_files) * sample_percentage)
    sampled_val_image_files = random.sample(val_image_files, sample_size)
    for image_file in sampled_val_image_files:
        src_image_path = os.path.join(val_images_dir, image_file)
        dst_image_path = os.path.join(mini_val_dir, image_file)
        copyfile(src_image_path, dst_image_path)

    # 更新训练集标注
    with open(train_annotations_file, 'r') as f:
        train_annotations = json.load(f)
    mini_train_annotations = {'images': [], 'annotations': [], 'categories': train_annotations['categories']}
    for image in train_annotations['images']:
        if image['file_name'] in sampled_train_image_files:
            mini_train_annotations['images'].append(image)
    for annotation in train_annotations['annotations']:
        if annotation['image_id'] in [image['id'] for image in mini_train_annotations['images']]:
            mini_train_annotations['annotations'].append(annotation)
    mini_train_annotations_file = os.path.join(mini_annotations_dir, 'instances_train2017.json')
    with open(mini_train_annotations_file, 'w') as f:
        json.dump(mini_train_annotations, f)

    # 更新验证集标注
    with open(val_annotations_file, 'r') as f:
        val_annotations = json.load(f)
    mini_val_annotations = {'images': [], 'annotations': [], 'categories': val_annotations['categories']}
    for image in val_annotations['images']:
        if image['file_name'] in sampled_val_image_files:
            mini_val_annotations['images'].append(image)
    for annotation in val_annotations['annotations']:
        if annotation['image_id'] in [image['id'] for image in mini_val_annotations['images']]:
            mini_val_annotations['annotations'].append(annotation)
    mini_val_annotations_file = os.path.join(mini_annotations_dir, 'instances_val2017.json')
    with open(mini_val_annotations_file, 'w') as f:
        json.dump(mini_val_annotations, f)

    print(f"Mini COCO dataset created successfully in {output_dir}.")

# 示例用法
train_annotations_file = './coco/annotations/instances_train2017.json'
val_annotations_file = './coco/annotations/instances_val2017.json'
train_images_dir = './coco/train2017'
val_images_dir = './coco/val2017'
output_dir = './mini_coco'
sample_percentage = 0.1

create_mini_coco_dataset(train_annotations_file, val_annotations_file, train_images_dir, val_images_dir, output_dir, sample_percentage)
