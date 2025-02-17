# Bounding-Box-Converter
Convert COCO bounding box to YOLO

COCO (https://cocodataset.org)
1. COCO bounding box (BBOX)

   'bbox': [x_min, y_min, width, height]
   float, not int; absolute coordinates, not relative to image size
   - x_min is the point (corner) in the X axis (from left to right) closer to the left border, in pixels.
   - y_min is the point (corner) in the Y axis (from top to bottom) closer to the top border, in pixels.
   - width is the width of the bounding box (rectangle) in pixels.
   - height is the height of the bounding box (rectangle) in pixels.
2. COCO segmentation format

   A list contains multiple polygons. Each item in the list should be a separate polygon. Each polygon consists of multiple points, which are stored in the following format of [x0, y0, x1, y1, ..., xn, yn].
   17 polygons inside a bbox below (using matplotlib.patches.Polygon).

   ![Picture1](https://github.com/user-attachments/assets/24f73cad-bfd3-4fa8-a8a4-af7ad33064b0)
   000000080659.jpg

BBox and segmentation format conversion (cocoapi/PythonAPI/pycocotools/coco.py Lines 331 to 359 in 8c9bcc3)

![image](https://github.com/user-attachments/assets/378f0103-1af5-45e2-b245-f8472586f952)

YOLO BBOX format
label: [Xcenter Ycenter ObjectWidth ObjectHeight]
Normalized values in [0, 1]

![image](https://github.com/user-attachments/assets/98552206-4e36-4bfe-ae02-61f2b0c56aee)
![image](https://github.com/user-attachments/assets/5bf9897c-af2c-426f-aaf3-c10fce09f6bd)

Please modify the directory to your local directory before using the code!!!
![image](https://github.com/user-attachments/assets/d31ac43d-a658-435e-a6df-0555264f0789)
