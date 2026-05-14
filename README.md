# 🏷️ label-converter

> **Convert object detection annotations between YOLO, COCO, and Pascal VOC — in one command.**

Switching datasets or model frameworks shouldn’t mean rewriting your annotations from scratch.
`label-converter` handles the most common format conversions with a clean CLI and importable Python API.

---

## 🔁 Supported Conversions

| From → To | Command |
|---|---|
| YOLO → COCO JSON | `yolo2coco` |
| COCO JSON → YOLO | `coco2yolo` |
| YOLO → Pascal VOC XML | `yolo2voc` |
| Pascal VOC XML → YOLO | `voc2yolo` |

> COCO ↔ VOC coming in v0.2.0

---

## 📦 Installation

```bash
git clone https://github.com/sharvinvarghese/label-converter.git
cd label-converter
pip install -r requirements.txt
```

Requires **Python 3.7+** and **Pillow** for image dimension reading.

---

## 🛠️ Usage

### YOLO → COCO JSON

```bash
python convert.py yolo2coco \
  --images ./dataset/images \
  --labels ./dataset/labels \
  --output ./output/coco.json \
  --classes person car bike
```

### COCO JSON → YOLO

```bash
python convert.py coco2yolo \
  --json ./annotations/instances_train.json \
  --output ./output/yolo_labels/
```

### YOLO → Pascal VOC XML

```bash
python convert.py yolo2voc \
  --images ./dataset/images \
  --labels ./dataset/labels \
  --output ./output/voc/ \
  --classes person car bike
```

### Pascal VOC → YOLO

```bash
python convert.py voc2yolo \
  --voc ./dataset/Annotations/ \
  --output ./output/yolo_labels/ \
  --classes person car bike
```

---

## 🐍 Python API

```python
from label_converter.yolo_to_coco import yolo_to_coco
from label_converter.coco_to_yolo import coco_to_yolo
from label_converter.yolo_to_voc  import yolo_to_voc
from label_converter.voc_to_yolo  import voc_to_yolo

# YOLO → COCO
yolo_to_coco(
    images_dir="./images",
    labels_dir="./labels",
    output_path="./coco.json",
    class_names=["person", "car", "bike"]
)

# COCO → YOLO
coco_to_yolo(
    coco_json_path="./coco.json",
    output_dir="./yolo_out/"
)
```

---

## 📂 Format Reference

### YOLO `.txt`
One file per image. Each line: `class_id cx cy width height` (all normalized 0–1).
```
0 0.512 0.433 0.210 0.345
1 0.780 0.210 0.150 0.280
```

### COCO JSON
Single JSON file for the entire dataset. Bounding boxes in `[x, y, width, height]` (absolute pixels).
```json
{
  "images": [{"id": 1, "file_name": "img1.jpg", "width": 640, "height": 480}],
  "annotations": [{"id": 1, "image_id": 1, "category_id": 0, "bbox": [100, 80, 134, 165]}],
  "categories": [{"id": 0, "name": "person"}]
}
```

### Pascal VOC XML
One XML file per image. Bounding boxes in absolute pixel coordinates `xmin, ymin, xmax, ymax`.
```xml
<annotation>
  <filename>img1.jpg</filename>
  <size><width>640</width><height>480</height><depth>3</depth></size>
  <object>
    <name>person</name>
    <bndbox><xmin>100</xmin><ymin>80</ymin><xmax>234</xmax><ymax>245</ymax></bndbox>
  </object>
</annotation>
```

---

## 📁 Project Structure

```
label-converter/
├── convert.py                  # CLI entry point
├── requirements.txt
├── README.md
└── label_converter/
    ├── __init__.py
    ├── yolo_to_coco.py
    ├── coco_to_yolo.py
    ├── yolo_to_voc.py
    └── voc_to_yolo.py
```

---

## 🗺️ Roadmap

- [x] YOLO ↔ COCO
- [x] YOLO ↔ Pascal VOC
- [ ] COCO ↔ Pascal VOC
- [ ] CSV / custom format support
- [ ] Validation mode — check for missing/corrupt labels
- [ ] `pip install label-converter` PyPI package

---

## 📜 License

MIT — free for personal and commercial use.

---

## 🙋 Author

**Sharvin Varghese** — [@sharvinvarghese](https://github.com/sharvinvarghese)

> Built to stop copy-pasting annotation conversion scripts. 🏷️
