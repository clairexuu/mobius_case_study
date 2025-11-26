# Exploring Möbius and Liouville Functions with Deep Learning

## Project Motivation

This project extends the work from [Studying number theory with deep learning: a case study with the Möbius and squarefree indicator functions](https://arxiv.org/abs/2502.10335) by David Lowry-Duda. We investigate whether transformer models can genuinely learn number-theoretic properties beyond simple pattern matching, focusing on:

1. **Encoding effectiveness**: Do different input encodings (CRT vs. interleaved CRT) affect model performance?
2. **CRT utility verification**: Is the Chinese Remainder Theorem (CRT) representation truly useful for learning number-theoretic functions?
3. **Learning function values**: Can models learn that the Möbius function takes values {-1, 0, 1} and distinguish between them?
4. **Generalization testing**: How do models trained on different data distributions (natural, cheat, non-cheat) perform across test sets?
5. **Multi-task learning**: Can models simultaneously learn both the Möbius function μ(n) and the Liouville function λ(n)?

### Key Findings

- Models achieve ~53% accuracy on natural test sets but struggle to predict μ(n) = 1
- Training on "cheat" data (numbers with only small prime factors) vs. "non-cheat" data (numbers with large prime factors) reveals different generalization patterns
- Interleaved CRT encoding shows comparable performance to standard CRT encoding
- Models show strong bias toward predicting μ(n) = 0, achieving >90% accuracy on this class but near-zero accuracy on μ(n) = 1

## Technical Highlights

### Architecture
- **Model**: Small transformer based on [Int2Int](https://github.com/f-charton/Int2Int)
- **Input**: Chinese Remainder Theorem (CRT) encoding with first 100 primes
- **Output**: Möbius function μ(n) ∈ {-1, 0, 1} and Liouville function λ(n)
- **Training**: PyTorch with GPU acceleration support

### Data Encodings

We explore three encoding formats (detailed in [ENCODING_FORMATS.md](ENCODING_FORMATS.md)):

1. **`interCRT100`** (Default): Interleaved `[n mod p₁, p₁, n mod p₂, p₂, ...]` (length 200)
2. **`CRT100`**: Standard `[n mod p₁, n mod p₂, ..., n mod p₁₀₀]` (length 100)
3. **`interCRT100_with_n`**: Interleaved CRT with original number appended (length 201)

### Dataset Types

Three training/test dataset configurations:

- **Natural**: Uniformly random samples from [1, 10¹³]
- **Cheat**: Numbers with prime factors only within the first 100 primes
- **Non-cheat**: Numbers with at least one prime factor outside the first 100 primes

## Getting Started

### Prerequisites

- Python 3.7+
- PyTorch 1.7.0+
- NumPy 1.19.0+
- G++ compiler (for data generation, optional)

### Installation

1. Clone the repository with submodules:
```bash
git clone https://github.com/yourusername/mobius_case_study.git
cd mobius_case_study
git submodule init
git submodule update
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Demo

### Generate Training Data

Generate data with different encodings and dataset types:

```bash
# Generate natural dataset with interCRT100 encoding
cd src/scripts
python generate_datafiles.py --encoding interCRT100 --dataset_type natural --n_samples 1000000

# Generate cheat dataset
python generate_datafiles.py --encoding interCRT100 --dataset_type cheat --n_samples 1000000

# Generate non-cheat dataset
python generate_datafiles.py --encoding interCRT100 --dataset_type non_cheat --n_samples 1000000
```

This will create training and test files in the `input/` directory.

### Train a Model

Train on different dataset types:

```bash
# Train on natural data
cd src/run_int2int_scripts
make train_natural

# Train on cheat data
make train_cheat

# Train on non-cheat data
make train_non_cheat

# Or train all at once
make train_all
```

Models will be saved to `models/model_{encoding}_{dataset_type}/`.


### Evaluate Model Performance


```bash
cd notebooks
jupyter notebook test_performance_report.ipynb
```

This notebook will:
- Test your model on natural, cheat, and non-cheat datasets
- Generate confusion matrices
- Compute precision, recall, and F1-scores per class
- Visualize per-class performance
- Save results to `test_results/`

## Project Structure

```
mobius_case_study/
├── README.md                          # This file
├── ENCODING_FORMATS.md                # Detailed encoding documentation
├── LICENSE                            # MIT License
├── requirements.txt                   # Python dependencies
│
├── Int2Int/                           # Submodule: transformer library
│   └── train.py                       # Main training script
│
├── src/
│   ├── scripts/
│   │   ├── generate_datafiles.py      # Generate training/test data
│   │   ├── shuffle_datafiles.py       # Shuffle data files
│   │   └── utils.py                   # Helper functions
│   ├── mobius_code/
│   │   └── mobius_test.py             # Möbius function implementation
│   └── run_int2int_scripts/
│       └── Makefile                   # Training commands
│
├── input/                             # Generated training/test data
│   ├── input_dir_interCRT100_natural/
│   ├── input_dir_interCRT100_cheat/
│   └── input_dir_interCRT100_non_cheat/
│
├── models/                            # Trained models
│   ├── model_interCRT100_natural/
│   ├── model_interCRT100_cheat/
│   └── model_interCRT100_non_cheat/
│
├── notebooks/                         # Analysis notebooks
│   ├── test_performance_report.ipynb  # Comprehensive evaluation
│   ├── make_model_plots.ipynb         # Training curve visualization
│   └── study_corrupted_inputs.ipynb   # Robustness analysis
│
└── test_results/                      # Evaluation results
    └── {encoding}_{task}/
        ├── overall_summary.csv
        ├── per_class_metrics_*.csv
        ├── confusion_matrices.png
        └── predictions_*.npz
```

## Visualization & Results

### Performance Metrics

After training and evaluation, the following visualizations are automatically generated:

1. **Confusion Matrices**: Shows prediction patterns across μ(n) = {-1, 0, 1}
2. **Per-Class Accuracy**: Compares performance on each Möbius value
3. **Cross-Dataset Performance**: How models trained on one dataset type perform on others
4. **Training Curves**: Accuracy and loss over training epochs

### Example Results

| Dataset    | Overall Accuracy | Acc μ=0 | Acc μ=1 | Acc μ=-1 | Precision (Macro) | Recall (Macro) |
|------------|------------------|---------|---------|----------|-------------------|----------------|
| Natural    | 53.40%          | 91.38%  | 0.03%   | 56.33%   | 68.10%           | 49.25%         |
| Non-Cheat  | 51.38%          | 89.57%  | 0.00%   | 53.30%   | 33.26%           | 47.62%         |

See [notebooks/test_performance_report.ipynb](notebooks/test_performance_report.ipynb)

## Key Experiments

### 1. Encoding Comparison
Compare `interCRT100` vs. `CRT100` vs. `interCRT100_with_stat`:
```bash
make train_all_encodings
```

### 2. Cross-Dataset Testing
Train on one dataset type, test on all three:
```bash
# Train on natural, test on all
make train_natural
cd ../notebooks
# Run test_performance_report.ipynb with MODEL_DIR pointing to natural model
```

### 3. Multi-Task Learning
Train on both μ(n) and λ(n) simultaneously:
```bash
# Modify train.py parameters to include both tasks
python train.py --tasks mu,liouville ...
```

## Citation

If you use this code, please cite the original paper:

```bibtex
@article{lowryduda2025studying,
  title={Studying number theory with deep learning: a case study with the M{\"o}bius and squarefree indicator functions},
  author={Lowry-Duda, David},
  journal={arXiv preprint arXiv:2502.10335},
  year={2025}
}
```

## Additional Resources

- [Original paper](https://arxiv.org/abs/2502.10335)
- [David Lowry-Duda's general report](https://davidlowryduda.com/ml-mobius-general/)
- [Technical report](https://davidlowryduda.com/ml-mobius-technical/)
- [Int2Int GitHub](https://github.com/f-charton/Int2Int)
