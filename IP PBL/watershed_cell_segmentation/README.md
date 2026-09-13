# Watershed-Based Cell Segmentation & Image Processing

A complete educational web application implementing the PRD pipeline:
upload -> grayscale -> noise -> filtering -> thresholding -> morphology ->
distance transform -> markers -> watershed -> boundaries -> metrics/dashboard.

## Stack
- Frontend: HTML, CSS, vanilla JavaScript
- Backend: Python + Flask
- Image processing: OpenCV, NumPy, scikit-image
- Charts: Chart.js (loaded from CDN)

## Run
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```
Open http://127.0.0.1:5000

## Sample dataset
Run:
```bash
python generate_samples.py
```
This creates 5 synthetic microscope-like images and masks for demonstration. Replace them with real cell images for the final academic experiment.

## Notes
- PSNR/MSE/SSIM compare the processed grayscale image with the original grayscale image unless a reference image is supplied.
- IoU/Dice/Precision/Recall/F1/Accuracy are computed when a ground-truth mask is supplied.
- The kernel experiment runs 3x3, 5x5, 7x7 and 9x9 and returns calculated values; no hard-coded metrics are used.
