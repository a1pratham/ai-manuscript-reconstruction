## Day 3 — OCR Integration

Today I focused on integrating the OCR stage into the pipeline. The preprocessing module was connected to Tesseract using `pytesseract.image_to_data()`, which allows the system to extract recognized text along with confidence scores and line information.

Initial tests produced inconsistent results. Some OCR outputs were empty or contained random text. After debugging, it became clear that the issue was related to how the image regions were being passed to the OCR engine rather than a problem with Tesseract itself.

While experimenting with segmentation, I noticed that Tesseract already performs internal line detection. Instead of relying entirely on custom line segmentation, I decided to use the `line_num` field returned by Tesseract to group words by line. This simplified the pipeline and improved reliability.

With these adjustments, the system can now successfully convert paragraph images into structured OCR output containing words and confidence scores.

Current pipeline:

Image → preprocessing → OCR → text + confidence extraction

The next step is to implement gap detection, which will mark low-confidence words using tags such as `[CHAR_GAP]` and `[WORD_GAP]` for later reconstruction.
