import argparse
import json
import os
import shutil
from pathlib import Path


def coco_to_yolo_bbox(bbox, img_w, img_h):
    """COCO [x_min, y_min, w, h] in pixels -> YOLO [xc, yc, w, h] normalised to [0, 1]."""
    x_min, y_min, w, h = bbox
    return (
        (x_min + w / 2) / img_w,
        (y_min + h / 2) / img_h,
        w / img_w,
        h / img_h,
    )


def coco_to_yolo_segmentation(polygon, img_w, img_h):
    """Flat [x0, y0, x1, y1, ...] in pixels -> same, normalised. x by width, y by height."""
    return [
        coord / (img_w if i % 2 == 0 else img_h)
        for i, coord in enumerate(polygon)
    ]


def main():
    ap = argparse.ArgumentParser(description="Convert COCO annotations to YOLO format.")
    ap.add_argument("--coco-json", required=True, help="path to COCO annotations json")
    ap.add_argument("--label-out", required=True, help="directory for YOLO .txt labels")
    ap.add_argument("--image-src", help="directory holding the source images")
    ap.add_argument("--image-out", help="directory to copy matched images into")
    ap.add_argument("--mode", choices=["bbox", "segmentation"], default="bbox")
    args = ap.parse_args()

    with open(args.coco_json) as f:
        coco = json.load(f)

    images = {img["id"]: img for img in coco["images"]}

    # COCO category ids are arbitrary and non-contiguous; YOLO wants 0..N-1.
    cat_ids = sorted(c["id"] for c in coco["categories"])
    cat_to_idx = {cid: i for i, cid in enumerate(cat_ids)}

    os.makedirs(args.label_out, exist_ok=True)
    if args.image_out:
        os.makedirs(args.image_out, exist_ok=True)

    available = set(os.listdir(args.image_src)) if args.image_src else None

    written, skipped = 0, 0
    seen_images = set()

    for ann in coco["annotations"]:
        image = images.get(ann["image_id"])
        if image is None:
            skipped += 1
            continue
        if available is not None and image["file_name"] not in available:
            continue

        img_w, img_h = image["width"], image["height"]
        cls = cat_to_idx[ann["category_id"]]
        label_path = Path(args.label_out) / (Path(image["file_name"]).stem + ".txt")

        lines = []
        if args.mode == "bbox":
            xc, yc, w, h = coco_to_yolo_bbox(ann["bbox"], img_w, img_h)
            if w <= 0 or h <= 0:                      # degenerate box
                skipped += 1
                continue
            lines.append(f"{cls} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}")
        else:
            for polygon in ann.get("segmentation", []):
                if not isinstance(polygon, list) or len(polygon) < 6:
                    continue                           # RLE masks or degenerate polygons
                if any(isinstance(p, str) for p in polygon):
                    continue
                pts = coco_to_yolo_segmentation(polygon, img_w, img_h)
                lines.append(f"{cls} " + " ".join(f"{p:.6f}" for p in pts))

        if lines:
            with open(label_path, "a") as f:
                f.write("\n".join(lines) + "\n")
            written += len(lines)

        if args.image_out and args.image_src and image["file_name"] not in seen_images:
            shutil.copy(os.path.join(args.image_src, image["file_name"]), args.image_out)
            seen_images.add(image["file_name"])

    print(f"wrote {written} labels across {len(seen_images) or '?'} images; skipped {skipped}")


if __name__ == "__main__":
    main()
