import os
import xml.etree.ElementTree as ET


def voc_to_yolo(voc_dir: str, output_dir: str, class_names: list):
    """Convert Pascal VOC XML annotations to YOLO .txt format."""
    os.makedirs(output_dir, exist_ok=True)
    xml_files = [f for f in os.listdir(voc_dir) if f.endswith(".xml")]
    count = 0

    for xml_file in sorted(xml_files):
        tree = ET.parse(os.path.join(voc_dir, xml_file))
        root = tree.getroot()
        size = root.find("size")
        w = int(size.find("width").text)
        h = int(size.find("height").text)
        lines = []

        for obj in root.findall("object"):
            cls_name = obj.find("name").text
            if cls_name not in class_names:
                continue
            cls_id = class_names.index(cls_name)
            bb = obj.find("bndbox")
            xmin = float(bb.find("xmin").text)
            ymin = float(bb.find("ymin").text)
            xmax = float(bb.find("xmax").text)
            ymax = float(bb.find("ymax").text)
            cx = ((xmin + xmax) / 2) / w
            cy = ((ymin + ymax) / 2) / h
            bw = (xmax - xmin) / w
            bh = (ymax - ymin) / h
            lines.append(f"{cls_id} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}")
            count += 1

        out_file = os.path.splitext(xml_file)[0] + ".txt"
        with open(os.path.join(output_dir, out_file), "w") as f:
            f.write("\n".join(lines))

    print(f"\u2705 YOLO labels saved to: {output_dir}  ({count} annotations)")
