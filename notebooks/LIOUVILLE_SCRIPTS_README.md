# Liouville Function Analysis Scripts

Python scripts to analyze Liouville function training and test results (alternative to Jupyter notebooks).

## Scripts

### 1. `analyze_liouville.py` - Training Analysis

Analyzes training logs and generates plots showing:
- Validation accuracy over epochs
- Training loss curves
- XE loss over epochs
- Comparison between λ(n) and λ²(n)

**Usage:**
```bash
cd notebooks

# Auto-detect most recent Liouville model
python analyze_liouville.py

# Or specify model directory
python analyze_liouville.py ../models/model_interCRT100_natural_liouville
```

**Output:**
- Prints training statistics to console
- Displays matplotlib plots
- Saves `liouville_training_plots.png` to model directory

---

### 2. `test_liouville_performance.py` - Test Performance

Comprehensively tests a trained model on multiple datasets:
- **Natural**: Uniform random numbers [1, 10^13]
- **Cheat**: Numbers with prime factors only in first 100 primes
- **Non-cheat**: Numbers with factors outside first 100 primes

Reports:
- Overall accuracy per dataset
- Per-class accuracy (λ=-1, λ=1)
- Precision, Recall, F1 scores
- Confusion matrices

**Usage:**
```bash
cd notebooks

# Auto-detect most recent model
python test_liouville_performance.py

# Specify model and encoding
python test_liouville_performance.py ../models/model_CRT100_natural_liouville --encoding CRT100
```

**Requirements:**
- Test data must exist in `../input/input_dir_{ENCODING}_{dataset_type}/`
- Checkpoint must exist at `{MODEL_DIR}/lambda/1/checkpoint.pth`
- Int2Int installed at `../Int2Int/`

**Output:**
- Prints detailed performance metrics to console
- Saves JSON results to `test_results_liouville/test_results.json`
- Saves plots to `test_results_liouville/test_performance.png`

---

## Example Workflow

**After training a model:**

```bash
cd notebooks

# 1. Analyze training curves
python analyze_liouville.py

# 2. Test on all datasets
python test_liouville_performance.py

# 3. View results
cat test_results_liouville/test_results.json
```

---

## Dependencies

Both scripts require:
- `numpy`
- `matplotlib`
- `tqdm` (optional, for progress bars)
- Standard library: `sys`, `os`, `pathlib`, `re`, `subprocess`, `json`

The test script additionally requires:
- Access to Int2Int train.py
- Test data files generated with matching encoding

**Install optional dependencies:**
```bash
pip install tqdm
```

Scripts will work without tqdm but won't show progress bars.

---

## Compared to Notebooks

**Advantages of Python scripts:**
- Faster to run (no notebook overhead)
- Easier to automate and script
- Can run on servers without Jupyter
- Simpler to version control
- Direct command-line usage

**Advantages of notebooks:**
- Interactive exploration
- Can run cells independently
- Easier to visualize intermediate results
- Better for documentation/reports

---

## Notes

### Encoding Detection

The test script auto-detects encoding from the model directory name:
- `model_interCRT100_*` → uses `interCRT100`
- `model_CRT100_*` → uses `CRT100`
- Override with `--encoding` flag if needed

### Test Data Generation

If test data doesn't exist, generate it with:
```bash
cd ../src/scripts
make good_data ENCODING=interCRT100 DATASET_TYPE=natural FUNCTION=liouville
make good_data ENCODING=interCRT100 DATASET_TYPE=cheat FUNCTION=liouville
make good_data ENCODING=interCRT100 DATASET_TYPE=non_cheat FUNCTION=liouville
```

### Comparing Möbius vs Liouville

To compare performance:
1. Train both: `make run FUNCTION=mobius` and `make run FUNCTION=liouville`
2. Test both: Run test script on each model directory
3. Compare the JSON results files

---

## Troubleshooting

**"No Liouville models found"**
- Train a model first with `make run FUNCTION=liouville`
- Or specify model path explicitly

**"Test file not found"**
- Generate test data as shown above
- Check encoding matches between model and data

**"Checkpoint not found"**
- Training must complete at least 1 epoch
- Check `{MODEL_DIR}/lambda/1/checkpoint.pth` exists

**Evaluation timeout**
- Normal for large test sets (10k samples)
- Increase timeout in script if needed (default 20 min)
