# Construction Defects Classification

A small research/demo repository for detecting and classifying surface defects on building façades using convolutional neural networks. The project aims to automate defect detection from images, improve site safety, and reduce inspection cost by providing an image inference API (planned AWS deployment).

Short summary
- Model type: convolutional neural network (CNN) for image classification
- Deployment target: an API served on AWS (work in progress)
- Input: still images (single or batched)
- Goal: detect defect type and return a label/confidence

Dataset
- Source: BD3 – Building Defects Detection Dataset (referenced in `main.ipynb`)
- Example classes: Algae, Major Crack, Minor Crack, Peeling, Spalling, Stain, Normal

Quick start (development)
1. Create and activate a Python environment (venv or conda)
2. Install dependencies:
	python -m pip install --upgrade pip; python -m pip install -r requirements.txt
4. Open `test_model.ipynb` and run the cells interactively in Jupyter / VS Code.

How to collaborate
- When working on code, create a branch named `feat/<short-description>` or `fix/<short-description>` from `master`.
- Submit a pull request with a short description and link to any relevant issue. Keep changes small and focused.

Notes and next steps
- This repository is an early-stage prototype. The API deployment, CI, and more robust dataset handling are not yet implemented.
