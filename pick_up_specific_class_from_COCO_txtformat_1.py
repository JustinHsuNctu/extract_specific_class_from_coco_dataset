#created by ChatGPT 20201108
import os
import re
import random
import shutil

# Set the paths to your COCO dataset and annotation files
dataDir = 'E:\\datasets\\COCO dataset\\Microsoft COCO.v2-raw.yolov8\\'
dataType = 'valid'  # Change this to 'val2017' or 'test2017' as needed

# Define the specific COCO classes you want to extract
specific_classes_names = ['person', 'bicycle', 'dog']  # Modify as needed

# Define the number of images you want to extract
num_images_to_extract = 600  # Modify as needed

# Create an output directory for YOLOv8 format data
output_dir_labels = './pick_up_coco_output/labels/'
output_dir_images = './pick_up_coco_output/images/'
os.makedirs(output_dir_labels, exist_ok=True)
os.makedirs(output_dir_images, exist_ok=True)

# List the specific COCO classes in the YOLO format
specific_classes_numbers = ['48', '9', '27']  # Modify these indices according to your specific class mapping
class_mapping = {       # old_class: new_class
    48: 0,  #person
    9: 1, #bicycle
    27: 2, #dog
    # Add more mappings as needed
}
# Initialize a list to store image file names
image_file_names = []
image_short_file_name = []

# Loop through the image files
image_dir = os.path.join(dataDir, dataType, 'images\\')
label_dir = os.path.join(dataDir, dataType, 'labels\\')
file_lists = os.listdir(image_dir)
sel_no = 0
while (sel_no < num_images_to_extract):
    image_file = random.choice(file_lists)
    # Check if the corresponding label file exists
    image_basename = basename_without_ext = os.path.splitext(os.path.basename(image_dir + image_file))[0]
    image_basename_split = re.split('_', image_basename)
    label_file = os.path.join(label_dir, image_basename) + '.txt'
    if os.path.exists(label_file):
        # Open the label file and check if it contains any of the specific classes
        with open(os.path.join(label_dir, label_file), 'r') as label_file:
            label_lines = label_file.readlines()
            contains_specific_class = any(any(line.split()[0] == specific_class_num for specific_class_num in specific_classes_numbers) for line in label_lines)
            if contains_specific_class:
                image_file_names.append(image_file)
                image_short_file_name.append(image_basename_split[0])
                # Extract lines containing specific classes
                specific_class_lines = [line for line in label_lines if line.split()[0] in specific_classes_numbers]
                if specific_class_lines:
                    modified_class_lines=[]
                    for spec_lin in specific_class_lines:
                        parts = spec_lin.split()
                        if len(parts) >= 5:
                            class_id = int(parts[0])
                            if class_id in class_mapping:
                                parts[0] = str(class_mapping[class_id])
                                new_class_num_line = ' '.join(parts)
                                modified_class_lines.append(new_class_num_line)
                    # Create a new label file with the extracted lines
                    output_label_file_path = os.path.join(output_dir_labels, image_basename_split[0])  + '.txt'
                    with open(output_label_file_path, 'w') as output_label_file:
                        for line in modified_class_lines:
                            output_label_file.writelines(line + '\n')
                sel_no = sel_no + 1

# Take the first 'num_images_to_extract' image file names
image_file_names = image_file_names[:num_images_to_extract]

# Copy the selected images and their corresponding label files to the YOLOv8 data directory
n = 0
for image_file in image_file_names:
    image_source_path = os.path.join(image_dir, image_file)
    image_destination_path = os.path.join(output_dir_images, image_short_file_name[n]) + '.jpg'
    n = n+1
    
    # label_file = os.path.splitext(image_file)[0] + '.txt'
    # label_source_path = os.path.join(label_dir, label_file)
    # label_destination_path = os.path.join(output_dir, 'labels', dataType, label_file)
    
    # os.makedirs(os.path.dirname(image_destination_path), exist_ok=True)
    # os.makedirs(os.path.dirname(label_destination_path), exist_ok=True)
    
    shutil.copy(image_source_path, image_destination_path)
    # os.system(f'cp {label_source_path} {label_destination_path}')

# # Create a train.txt file with the paths to training images
# with open(os.path.join(output_dir, 'train.txt'), 'w') as f:
#     for image_file in image_file_names:
#         f.write(f'{os.path.join(output_dir, image_file)}\n')