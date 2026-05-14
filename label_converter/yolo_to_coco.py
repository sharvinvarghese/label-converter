import os
import json
from PIL import Image


def yolo_to_coco(images_dir: str, labels_dir: str, output_path: str, class_names: list):
    """Convert YOLO .txt annotations to COCO JSON format."""
    coco = {"images": [], "annotations": [], "categories": []}
    for i, name in enumerate(class_names):
        coco["categories"].append({"id": i, "name": name, "supercategory": "object"})

    ann_id = 1
    img_files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    for img_id, img_file in enumerate(sorted(img_files), 1):
        img_path = os.path.join(images_dir, img_file)
        with Image.open(img_path) as img:
            w, h = img.size

        coco["images"].append({"id": img_id, "file_name": img_file, "width": w, "height": h})

        label_file = os.path.splitext(img_file)[0] + ".txt"
        label_path = os.path.join(labels_dir, label_file)
        if not os.path.exists(label_path):
            continue

        with open(label_path) as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) != 5:
                    continue
                cls, cx, cy, bw, bh = int(parts[0]), float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])
                x = (cx - bw / 2) * w
                y = (cy - bh / 2) * h
                abs_w = bw * w
                abs_h = bh * h
                coco["annotations"].append({
                    "id": ann_id, "image_id": img_id, "category_id": cls,
                    "bbox": [round(x, 2), round(y, 2), round(abs_w, 2), round(abs_h, 2)],
                    "area": round(abs_w * abs_h, 2), "iscrowd": 0
                })
                ann_id += 1

    with open(output_path, "w") as f:
        json.dump(coco, f, indent=2)
    print(f"\u2705 COCO JSON saved to: {output_path}  ({ann_id-1} annotations)")
    return coco
