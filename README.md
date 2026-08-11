# Liquid Food Analyzer

## Research Objective

The objective of this project is to develop a computer-vision-based system capable of identifying Lactobacillus species and estimating the number of bacterial instances present in microscopic slide images.

The project is being developed as an initial research prototype, with the long-term goal of studying whether microscopic image analysis and machine learning can be used for automated liquid-food quality analysis.

---

## Current Progress

- Collected microscopic image data from Jagiellonian University, Krakow, Poland.
- Collected data covering 11 species of Lactobacillus.
- Initial objective: identify selected Lactobacillus species and count bacterial instances present in microscopic slide photographs.
- Currently experimenting with YOLO instance segmentation for bacterial detection and counting.
- Using the YOLO26 Nano segmentation model (`yolo26n-seg`).
- A preliminary test model has been trained using:
  - Lactobacillus delbrueckii
  - Lactobacillus salivarius
- Microscopic slides are divided into 640 × 640 pixel tiles with 20% overlap to process large slide images.

---

## Test Objectives

The current implementation is a preliminary test to determine whether YOLO26n-seg can be used to:

- Detect individual bacterial instances in microscopic slide images.
- Distinguish between selected Lactobacillus species.
- Estimate the number of bacterial instances present in a slide.
- Process large microscopic images by dividing them into smaller overlapping image tiles.

The current test is limited to two trained species:

- Lactobacillus delbrueckii
- Lactobacillus salivarius

This is only an initial proof-of-concept and is not intended to represent the final performance of the Liquid Food Analyzer.

---

## Preliminary Test Results

### Test 1 — Lactobacillus delbrueckii

**Input:** `Lactobacillus.delbrueckii_0001.tif`

**Detected instances:**

- L. delbrueckii: 2,109
- L. salivarius: 1
- Total: 2,110

Correct species classification among detected instances:

**99.95%**

The preliminary model strongly classified the detected instances as the expected species for this test image.

---

### Test 2 — Lactobacillus salivarius

**Input:** `Lactobacillus.salivarius_0001.tif`

**Detected instances:**

- L. delbrueckii: 8
- L. salivarius: 456
- Total: 464

Correct species classification among detected instances:

**98.28%**

The model again predominantly assigned the detected instances to the expected species.

---

### Test 3 — Unseen Lactobacillus Species

**Input:** Lactobacillus casei sample

This species was not included in the training classes of the preliminary model.

The model produced mixed predictions between the two known classes.

This result is expected because the current model only has two available classes:

```text
0 → L. delbrueckii
1 → L. salivarius
```

Therefore, the model currently has no explicit "unknown species" class.

This test highlights an important area for future research: determining how the system should handle bacterial species that were not present in its training data.

---

## Interpretation of Preliminary Results

The initial tests indicate that the approach is technically promising for the two species used during preliminary training.

The results should not yet be considered the final accuracy of the system. A proper evaluation will require an independent test dataset with verified ground-truth annotations and evaluation using appropriate metrics such as precision, recall, mAP, and segmentation/mask IoU.

The preliminary results are being used primarily to establish that the proposed computer-vision pipeline is feasible and worth developing further.

---

## Current Prototype Pipeline

```text
Microscopic Slide
       ↓
Image Tiling
(640 × 640, 20% overlap)
       ↓
Image Preprocessing
       ↓
YOLO26n Instance Segmentation
       ↓
Bacterial Instance Detection
       ↓
Species Classification
       ↓
Bacterial Counting
```

---

## Planned Work

The current implementation is only a preliminary prototype. The next stages of the project will include:

1. Study and understand the complete YOLO segmentation pipeline.
2. Learn image preprocessing and microscopy-image characteristics.
3. Improve and verify bacterial segmentation annotations.
4. Expand the training dataset to include the available Lactobacillus species.
5. Create proper training, validation, and independent test datasets.
6. Train and compare models using the expanded dataset.
7. Evaluate the model using appropriate metrics such as:
   - Precision
   - Recall
   - mAP
   - IoU / mask quality
8. Investigate duplicate detections and counting accuracy when processing overlapping image tiles.
9. Study how the system should respond to species that were not present in the training data.
10. Evaluate the feasibility of applying the approach to liquid-food quality analysis.

---

## Learning Plan

To ensure that the project is properly understood rather than treated only as a working prototype, the following areas will be studied:

- Python for machine learning
- NumPy and OpenCV
- Image preprocessing
- Computer vision fundamentals
- CNN fundamentals
- Object detection
- Instance segmentation
- YOLO architecture and training
- Dataset annotation and augmentation
- PyTorch
- GPU/CUDA-based model training
- Model evaluation and validation
- Microscopy image analysis
- Basic machine-learning research methodology

The current prototype provides a starting point for studying and improving each of these components systematically.

---

## Current Status

**Prototype:** Working  
**GPU Training:** Working  
**Initial Species:** 2 / 11  
**Dataset:** 11 Lactobacillus species collected  
**Model:** YOLO26n-seg  
**Image Processing:** 640 × 640 tiles with 20% overlap  
**Next Goal:** Build a properly validated multi-species prototype
