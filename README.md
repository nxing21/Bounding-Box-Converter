# COCO to YOLO Converter

Converts COCO-format annotations into YOLO format, for bounding boxes or segmentation polygons.

## Why this isn't trivial

The two formats differ in more than layout, and each difference fails quietly rather than loudly:

| | COCO | YOLO |
|---|---|---|
| Box format | `[x_min, y_min, width, height]` | `[x_center, y_center, width, height]` |
| Units | absolute pixels | normalized to `[0, 1]` |
| Class IDs | arbitrary, non-contiguous | contiguous `0..N-1` |

A wrong normalization or an unmapped class ID produces label files that parse cleanly and train badly — the model quietly learns the wrong thing.

## What it handles

- Corner-origin to center-origin conversion, normalized by image dimensions
- Category ID remapping from COCO's sparse IDs to contiguous indices
- Segmentation polygons, normalizing x by width and y by height
- Skips RLE-encoded masks and degenerate (zero-area) boxes
- Optionally copies matched images into a parallel directory, for building train/val/test splits in one pass

## Usage

```bash
python coco2yolo.py \
  --coco-json labels/val.json \
  --label-out labels/val \
  --image-src images/all_images \
  --image-out images/val \
  --mode bbox
```

Use `--mode segmentation` to emit normalized polygons instead of boxes.

## Example

COCO input, for a 640 x 480 image:

```json
{"image_id": 12, "category_id": 3, "bbox": [100.0, 60.0, 200.0, 120.0]}
```

With COCO categories `[1, 3, 90]` remapping to indices `[0, 1, 2]`, category 3 becomes class 1:

```
1 0.312500 0.250000 0.312500 0.250000
```

Checking the arithmetic: `(100 + 200/2) / 640 = 0.3125` and `(60 + 120/2) / 480 = 0.25`.

---

## Format reference

### COCO bounding box

`'bbox': [x_min, y_min, width, height]` — floats, absolute pixel coordinates, not relative to image size.

- `x_min` is the corner on the X axis closest to the left border, in pixels
- `y_min` is the corner on the Y axis closest to the top border, in pixels
- `width` and `height` are the box dimensions in pixels

### COCO segmentation

A list of polygons. Each polygon is a flat list of points: `[x0, y0, x1, y1, ..., xn, yn]`. The image below shows 17 polygons inside a single bounding box.

![COCO segmentation polygons](https://github.com/user-attachments/assets/24f73cad-bfd3-4fa8-a8a4-af7ad33064b0)

Conversion between bbox and segmentation format, as implemented in `cocoapi/PythonAPI/pycocotools/coco.py`:

![bbox and segmentation conversion](https://github.com/user-attachments/assets/378f0103-1af5-45e2-b245-f8472586f952)

### YOLO bounding box

`label: [x_center, y_center, width, height]` — normalized to `[0, 1]`.

![YOLO format](https://github.com/user-attachments/assets/98552206-4e36-4bfe-ae02-61f2b0c56aee)

![YOLO format detail](https://github.com/user-attachments/assets/5bf9897c-af2c-426f-aaf3-c10fce09f6bd)

Reference: [cocodataset.org](https://cocodataset.org)
