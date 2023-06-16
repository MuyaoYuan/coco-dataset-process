import os
import random
import json
from shutil import copyfile

def create_vis_coco_dataset(val_annotations_file, val_images_dir, output_dir, num_images):
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    vis_images_dir = os.path.join(output_dir, 'img')
    vis_annotations_dir = os.path.join(output_dir, 'ann')
    os.makedirs(vis_images_dir, exist_ok=True)
    os.makedirs(vis_annotations_dir, exist_ok=True)

    # 复制验证集图像
    val_image_files = os.listdir(val_images_dir)
    sampled_val_image_files = random.sample(val_image_files, num_images)
    for image_file in sampled_val_image_files:
        src_image_path = os.path.join(val_images_dir, image_file)
        dst_image_path = os.path.join(vis_images_dir, image_file)
        copyfile(src_image_path, dst_image_path)

    # 更新验证集标注
    with open(val_annotations_file, 'r') as f:
        val_annotations = json.load(f)
    vis_annotations = {'images': [], 'annotations': [], 'categories': val_annotations['categories']}
    for image in val_annotations['images']:
        if image['file_name'] in sampled_val_image_files:
            vis_annotations['images'].append(image)
    for annotation in val_annotations['annotations']:
        if annotation['image_id'] in [image['id'] for image in vis_annotations['images']]:
            vis_annotations['annotations'].append(annotation)
    vis_annotations_file = os.path.join(vis_annotations_dir, 'instances_val2017.json')
    with open(vis_annotations_file, 'w') as f:
        json.dump(vis_annotations, f)

    print(f"vis_coco dataset created successfully in {output_dir}.")

# 示例用法
val_annotations_file = './coco/annotations/instances_val2017.json'
val_images_dir = './coco/val2017'
output_dir = './vis_coco'
num_images = 10

create_vis_coco_dataset(val_annotations_file, val_images_dir, output_dir, num_images)
