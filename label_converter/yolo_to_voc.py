import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from PIL import Image


def _build_voc_xml(filename, width, height, depth, objects):
    root = ET.Element("annotation")
    ET.SubElement(root, "filename").text = filename
    size = ET.SubElement(root, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = str(depth)
    for cls_name, xmin, ymin, xmax, ymax in objects:
        obj = ET.SubElement(root, "object")
        ET.SubElement(obj, "name").text = cls_name
        ET.SubElement(obj, "difficult").text = "0"
        bndbox = ET.SubElement(obj, "bndbox")
        ET.SubElement(bndbox, "xmin").text = str(xmin)
        ET.SubElement(bndbox, "ymin").text = str(ymin)
        ET.SubElement(bndbox, "xmax").text = str(xmax)
        ET.SubElement(bndbox, "ymax").text = str(ymax)
    return minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")


def yolo_to_voc(images_dir: str, labels_dir: str, output_dir: str, class_names: list):
    """Convert YOLO .txt annotations to Pascal VOC XML format."""
    os.makedirs(output_dir, exist_ok=True)
    img_files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    count = 0

    for img_file in sorted(img_files):
        img_path = os.path.join(images_dir, img_file)
        with Image.open(img_path) as img:
            w, h = img.size
            depth = len(img.getbands())

        label_file = os.path.splitext(img_file)[0] + ".txt"
        label_path = os.path.join(labels_dir, label_file)
        if not os.path.exists(label_path):
            continue

        objects = []
        with open(label_path) as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) != 5:
                    continue
                cls, cx, cy, bw, bh = int(parts[0]), float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])
                xmin = int((cx - bw / 2) * w)
                ymin = int((cy - bh / 2) * h)
                xmax = int((cx + bw / 2) * w)
                ymax = int((cy + bh / 2) * h)
                cls_name = class_names[cls] if cls < len(class_names) else str(cls)
                objects.append((cls_name, xmin, ymin, xmax, ymax))
                count += 1

        xml_str = _build_voc_xml(img_file, w, h, depth, objects)
        out_file = os.path.splitext(img_file)[0] + ".xml"
        with open(os.path.join(output_dir, out_file), "w") as f:
            f.write(xml_str)

    print(f"\u2705 VOC XMLs saved to: {output_dir}  ({count} annotations)")
