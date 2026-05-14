#!/usr/bin/env python3
"""
label-converter CLI
Usage examples in README.md
"""
import argparse
from label_converter.yolo_to_coco import yolo_to_coco
from label_converter.coco_to_yolo import coco_to_yolo
from label_converter.yolo_to_voc  import yolo_to_voc
from label_converter.voc_to_yolo  import voc_to_yolo


def main():
    parser = argparse.ArgumentParser(description="\U0001f3f7\ufe0f  label-converter \u2014 YOLO \u2194 COCO \u2194 VOC")
    sub = parser.add_subparsers(dest="command", required=True)

    p1 = sub.add_parser("yolo2coco", help="YOLO \u2192 COCO JSON")
    p1.add_argument("--images",  required=True)
    p1.add_argument("--labels",  required=True)
    p1.add_argument("--output",  required=True)
    p1.add_argument("--classes", required=True, nargs="+")

    p2 = sub.add_parser("coco2yolo", help="COCO JSON \u2192 YOLO")
    p2.add_argument("--json",    required=True)
    p2.add_argument("--output",  required=True)

    p3 = sub.add_parser("yolo2voc", help="YOLO \u2192 Pascal VOC XML")
    p3.add_argument("--images",  required=True)
    p3.add_argument("--labels",  required=True)
    p3.add_argument("--output",  required=True)
    p3.add_argument("--classes", required=True, nargs="+")

    p4 = sub.add_parser("voc2yolo", help="Pascal VOC XML \u2192 YOLO")
    p4.add_argument("--voc",     required=True)
    p4.add_argument("--output",  required=True)
    p4.add_argument("--classes", required=True, nargs="+")

    args = parser.parse_args()

    if args.command == "yolo2coco":
        yolo_to_coco(args.images, args.labels, args.output, args.classes)
    elif args.command == "coco2yolo":
        coco_to_yolo(args.json, args.output)
    elif args.command == "yolo2voc":
        yolo_to_voc(args.images, args.labels, args.output, args.classes)
    elif args.command == "voc2yolo":
        voc_to_yolo(args.voc, args.output, args.classes)


if __name__ == "__main__":
    main()
