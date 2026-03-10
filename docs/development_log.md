# Development Log

## Day 2 — Image Preprocessing & Line Segmentation

### Work Completed

Today the focus was building the **first stages of the OCR pipeline**.

Implemented modules:

* `preprocessing/image_cleaning.py`
* `preprocessing/line_segmentation.py`

The preprocessing pipeline currently performs:

Image →
Grayscale conversion →
Noise reduction (median blur) →
Adaptive thresholding

This prepares images for OCR by improving text visibility and contrast.

---

### Line Segmentation

Implemented a method to split document images into **individual text lines**.

Initial approach used **morphological dilation + contour detection** to detect horizontal text regions.

Pipeline:

Image → Preprocessing → Dilation → Contour Detection → Line Cropping

The system outputs a list of **separate line images** which will later be passed individually to the OCR engine.

---

### Observations & Debugging

Several issues were encountered during testing:

1. **Kernel Size Sensitivity**

   * Large dilation kernels caused multiple lines to merge into a single block.
   * Smaller kernels improved detection but required tuning.

2. **Font Size Dependency**

   * Large font text segmented correctly.
   * Small font text often merged or failed to segment properly.

3. **Paragraph Detection Issue**

   * For some paragraph images the algorithm detected the entire paragraph as a single contour.

This revealed that the current approach is **scale dependent**.

---

### Design Insight

Because the project aims to reconstruct **damaged manuscripts**, the segmentation method must be robust to:

* small text
* faded ink
* noise
* irregular spacing

Morphological segmentation alone may not be sufficient.

Future improvements may involve **projection profile based segmentation**, which detects line gaps using pixel density rather than shape dilation.

---

### Current Pipeline Status

The system currently supports:

Image
↓
Preprocessing
↓
Line Segmentation
↓
Line Images Extracted

This prepares the pipeline for the next stage: OCR processing.

---

### Next Step

Implement **OCR with confidence extraction** using:

pytesseract.image_to_data()

This will allow extraction of:

* recognized word
* confidence score
* bounding box coordinates

Low-confidence regions will later be marked as:

[CHAR_GAP]
[WORD_GAP]

These gaps will be reconstructed using a language model in later stages.

---

### Reflection

Today's work highlighted the challenges of **document segmentation** and the importance of algorithm robustness when dealing with noisy or damaged text.

Despite several debugging iterations, the pipeline is now capable of detecting and extracting text lines from images, which is a critical step for building the manuscript reconstruction system.
