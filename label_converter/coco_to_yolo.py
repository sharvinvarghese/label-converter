import os
import json


def coco_to_yolo(coco_json_path: str, output_dir: str):
    """Convert COCO JSON annotations to YOLO .txt format."""
    os.makedirs(output_dir, exist_ok=True)

    with open(coco_json_path) as f:
        coco = json.load(f)

    img_map = {img["id"]: img for img in coco["images"]}
    ann_map: dict = {}
    for ann in coco["annotations"]:
        ann_map.setdefault(ann["image_id"], []).append(ann)

    count = 0
    for img_id, img_info in img_map.items():
        w, h = img_info["width"], img_info["height"]
        lines = []
        for ann in ann_map.get(img_id, []):
            x, y, bw, bh = ann["bbox"]
            cx = (x + bw / 2) / w
            cy = (y + bh / 2) / h
            nw = bw / w
            nh = bh / h
            lines.append(f"{ann['category_id']} {cx:.6f} {cy:.6f} {nw:.6f} {nh:.6f}")
            count += 1
        fname = os.path.splitext(img_info["file_name"])[0] + ".txt"
        with open(os.path.join(output_dir, fname), "w") as f:
            f.write("\n".join(lines))

    print(f"\u2705 YOLO labels saved to: {output_dir}  ({count} annotations)")
