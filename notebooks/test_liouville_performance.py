#!/usr/bin/env python3
"""
Test Liouville Model Performance

Evaluates a trained Liouville model on multiple test datasets:
- Natural: Uniformly random samples
- Cheat: Numbers with prime factors only within first 100 primes
- Non-cheat: Numbers with at least one prime factor outside first 100 primes

Reports per-class performance, confusion matrices, precision/recall/F1.

Usage:
    python test_liouville_performance.py [model_dir] [--encoding ENCODING]

Example:
    python test_liouville_performance.py ../models/model_interCRT100_natural_liouville
    python test_liouville_performance.py ../models/model_CRT100_natural_liouville --encoding CRT100
"""

import sys
import os
import subprocess
import json
import re
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt



# Encoding configurations
ENCODING_MAP = {
    "interCRT100": "int[200]:range(-1,2)",
    "CRT100": "int[100]:range(-1,2)",
    "interCRT100_with_n": "int[201]:range(-1,2)",
    "CRT100_with_stats": "int[103]:range(-1,2)"
}


def get_test_data_path(encoding, dataset_type, function='liouville'):
    """Construct path to test data file"""
    if function == 'liouville':
        base_name = f"lambda_{encoding}"
    else:
        base_name = f"mu_{encoding}"

    input_dir = Path("../input") / f"input_dir_{encoding}_{dataset_type}"
    test_file = input_dir / f"{base_name}_{dataset_type}.txt.test"
    return test_file


def run_evaluation(checkpoint_path, test_data_path, encoding, results_dir):
    """Run Int2Int evaluation on test data"""
    data_types = ENCODING_MAP.get(encoding, "int[200]:range(-1,2)")

    eval_dump_path = results_dir / "eval_dump"
    eval_dump_path.mkdir(parents=True, exist_ok=True)

    cmd = [
        "python", "../Int2Int/train.py",
        "--eval_only", "True",
        "--reload_model", str(checkpoint_path.absolute()),
        "--eval_data", str(test_data_path.absolute()),
        "--eval_size", "10000",
        "--data_types", data_types,
        "--operation", "data",
        "--cpu", "True",
        "--num_workers", "0",
        "--dump_path", str(eval_dump_path.absolute()),
        "--eval_verbose", "2",
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1200)

        # Parse metrics
        log_match = re.search(r'__log__:({.+})', result.stdout)
        if not log_match:
            log_match = re.search(r'__log__:({.+})', result.stderr)

        metrics = None
        if log_match:
            try:
                metrics = json.loads(log_match.group(1))
            except:
                pass

        # Find eval file with predictions
        eval_files = sorted(eval_dump_path.glob("eval.valid.arithmetic.*"))
        eval_file = eval_files[-1] if eval_files else None

        return metrics, eval_file, result

    except subprocess.TimeoutExpired:
        print("  ✗ Evaluation timed out")
        return None, None, None
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return None, None, None


def parse_eval_file(eval_file):
    """Parse eval file to extract predictions and ground truth"""
    y_true = []
    y_pred = []

    if not eval_file or not Path(eval_file).exists():
        return None, None

    with open(eval_file, 'r') as f:
        lines = f.readlines()

    for i in range(len(lines)):
        line = lines[i].strip()

        if line.startswith('tgt='):
            tgt_match = re.search(r"tgt=\['?(-?\d+)'?\]", line)
            if tgt_match:
                true_val = int(tgt_match.group(1))

                if i + 1 < len(lines):
                    pred_line = lines[i + 1].strip()
                    pred_match = re.search(r"^[01]\s+\[?'?(-?\d+)'?\]?", pred_line)
                    if pred_match:
                        pred_val = int(pred_match.group(1))
                        y_true.append(true_val)
                        y_pred.append(pred_val)

    if len(y_true) == 0:
        return None, None

    return np.array(y_true), np.array(y_pred)


def compute_metrics(y_true, y_pred):
    """Compute classification metrics"""
    if y_true is None or len(y_true) == 0:
        return None

    labels = [-1, 1]  # Liouville only returns -1 or 1

    # Filter valid predictions
    valid_mask = np.isin(y_pred, labels)
    y_true_valid = y_true[valid_mask]
    y_pred_valid = y_pred[valid_mask]

    if len(y_true_valid) == 0:
        return None

    # Compute confusion matrix
    cm = np.zeros((len(labels), len(labels)), dtype=int)
    for i, true_label in enumerate(labels):
        for j, pred_label in enumerate(labels):
            cm[i, j] = np.sum((y_true_valid == true_label) & (y_pred_valid == pred_label))

    # Compute per-class metrics
    metrics = {}
    for i, label in enumerate(labels):
        tp = cm[i, i]
        fp = cm[:, i].sum() - tp
        fn = cm[i, :].sum() - tp

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

        metrics[f'precision_{label}'] = precision
        metrics[f'recall_{label}'] = recall
        metrics[f'f1_{label}'] = f1

    # Macro and weighted averages
    precisions = [metrics[f'precision_{l}'] for l in labels]
    recalls = [metrics[f'recall_{l}'] for l in labels]
    f1s = [metrics[f'f1_{l}'] for l in labels]

    metrics['precision_macro'] = np.mean(precisions)
    metrics['recall_macro'] = np.mean(recalls)
    metrics['f1_macro'] = np.mean(f1s)

    # Weighted by support
    support = cm.sum(axis=1)
    total = support.sum()
    weights = support / total if total > 0 else np.zeros(len(labels))

    metrics['precision_weighted'] = np.sum(np.array(precisions) * weights)
    metrics['recall_weighted'] = np.sum(np.array(recalls) * weights)
    metrics['f1_weighted'] = np.sum(np.array(f1s) * weights)

    metrics['confusion_matrix'] = cm
    metrics['labels'] = labels
    metrics['accuracy'] = np.sum(np.diag(cm)) / np.sum(cm) if np.sum(cm) > 0 else 0
    metrics['n_samples'] = len(y_true_valid)

    return metrics


def print_summary(dataset_type, basic_metrics, detailed_metrics):
    """Print performance summary for a dataset"""
    print(f"\n{'='*80}")
    print(f"  {dataset_type.upper()} DATASET")
    print(f"{'='*80}")

    if basic_metrics:
        print(f"  Overall Accuracy:    {basic_metrics.get('valid_arithmetic_acc', 0):.2f}%")
        print(f"  λ(n) = -1 Accuracy:  {basic_metrics.get('valid_arithmetic_acc_-1', 0):.2f}%")
        print(f"  λ(n) = 1 Accuracy:   {basic_metrics.get('valid_arithmetic_acc_1', 0):.2f}%")
        print(f"  XE Loss:             {basic_metrics.get('valid_arithmetic_xe_loss', 0):.4f}")

    if detailed_metrics:
        print(f"\n  Classification Metrics:")
        print(f"    Precision (macro):   {detailed_metrics['precision_macro']:.4f}")
        print(f"    Recall (macro):      {detailed_metrics['recall_macro']:.4f}")
        print(f"    F1 (macro):          {detailed_metrics['f1_macro']:.4f}")
        print(f"\n  Per-Class Metrics:")
        print(f"    λ=-1: P={detailed_metrics['precision_-1']:.3f}, R={detailed_metrics['recall_-1']:.3f}, F1={detailed_metrics['f1_-1']:.3f}")
        print(f"    λ=1:  P={detailed_metrics['precision_1']:.3f}, R={detailed_metrics['recall_1']:.3f}, F1={detailed_metrics['f1_1']:.3f}")

        cm = detailed_metrics['confusion_matrix']
        print(f"\n  Confusion Matrix:")
        print(f"              Pred λ=-1  Pred λ=1")
        print(f"    True λ=-1     {cm[0,0]:6d}     {cm[0,1]:6d}")
        print(f"    True λ=1      {cm[1,0]:6d}     {cm[1,1]:6d}")

    print(f"{'='*80}")


def plot_results(results, results_dir):
    """Generate visualization plots"""
    dataset_types = list(results.keys())
    if not dataset_types:
        return

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Liouville Function Test Performance', fontsize=16, fontweight='bold')

    # Plot 1: Overall accuracy comparison
    ax = axes[0, 0]
    accuracies = [results[dt]['basic'].get('valid_arithmetic_acc', 0) for dt in dataset_types]
    colors = ['#2ecc71', '#e74c3c', '#3498db']
    bars = ax.bar(dataset_types, accuracies, color=colors[:len(dataset_types)], alpha=0.8)
    for bar, acc in zip(bars, accuracies):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f'{acc:.1f}%', ha='center', va='bottom', fontweight='bold')
    ax.set_ylabel('Accuracy (%)')
    ax.set_title('Overall Accuracy by Dataset')
    ax.set_ylim([0, 105])
    ax.grid(True, alpha=0.3, axis='y')

    # Plot 2: Per-class accuracy
    ax = axes[0, 1]
    x = np.arange(len(dataset_types))
    width = 0.35
    acc_neg1 = [results[dt]['basic'].get('valid_arithmetic_acc_100', 0) for dt in dataset_types]
    acc_pos1 = [results[dt]['basic'].get('valid_arithmetic_acc_1', 0) for dt in dataset_types]

    bars1 = ax.bar(x - width/2, acc_neg1, width, label='λ=-1', color='#3498db')
    bars2 = ax.bar(x + width/2, acc_pos1, width, label='λ=1', color='#e74c3c')

    ax.set_ylabel('Accuracy (%)')
    ax.set_title('Per-Class Accuracy')
    ax.set_xticks(x)
    ax.set_xticklabels(dataset_types)
    ax.legend()
    ax.set_ylim([0, 105])
    ax.grid(True, alpha=0.3, axis='y')

    # Plot 3: F1 scores
    ax = axes[1, 0]
    if all('detailed' in results[dt] for dt in dataset_types):
        f1_macro = [results[dt]['detailed']['f1_macro'] for dt in dataset_types]
        bars = ax.bar(dataset_types, f1_macro, color=colors[:len(dataset_types)], alpha=0.8)
        for bar, f1 in zip(bars, f1_macro):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                    f'{f1:.3f}', ha='center', va='bottom', fontweight='bold')
        ax.set_ylabel('F1 Score (Macro)')
        ax.set_title('F1 Score by Dataset')
        ax.set_ylim([0, 1.1])
        ax.grid(True, alpha=0.3, axis='y')

    # Plot 4: Confusion matrix for first dataset
    ax = axes[1, 1]
    if 'detailed' in results[dataset_types[0]]:
        cm = results[dataset_types[0]]['detailed']['confusion_matrix']
        im = ax.imshow(cm, cmap='Blues', aspect='auto')

        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(['λ=-1', 'λ=1'])
        ax.set_yticklabels(['λ=-1', 'λ=1'])
        ax.set_xlabel('Predicted')
        ax.set_ylabel('Actual')
        ax.set_title(f'Confusion Matrix ({dataset_types[0]})')

        # Add text annotations
        for i in range(2):
            for j in range(2):
                text = ax.text(j, i, cm[i, j], ha="center", va="center",
                             color="white" if cm[i, j] > cm.max()/2 else "black",
                             fontsize=14, fontweight='bold')

        plt.colorbar(im, ax=ax)

    plt.tight_layout()

    save_path = results_dir / 'test_performance.png'
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"\nPlots saved to: {save_path}")
    plt.show()


def main():
    """Main function"""
    # Parse arguments
    if len(sys.argv) > 1:
        model_dir = Path(sys.argv[1])
    else:
        models_dir = Path(__file__).parent.parent / 'models'
        liouville_models = sorted(models_dir.glob('model_*_liouville'))
        if not liouville_models:
            print("No Liouville models found. Specify model directory.")
            sys.exit(1)
        model_dir = liouville_models[-1]

    # Extract encoding from model directory name
    encoding = "interCRT100"  # default
    for enc in ENCODING_MAP.keys():
        if enc in model_dir.name:
            encoding = enc
            break

    # Override encoding if specified
    if '--encoding' in sys.argv:
        idx = sys.argv.index('--encoding')
        if idx + 1 < len(sys.argv):
            encoding = sys.argv[idx + 1]

    print(f"\n{'='*80}")
    print(f"  TESTING LIOUVILLE MODEL PERFORMANCE")
    print(f"{'='*80}")
    print(f"  Model: {model_dir.name}")
    print(f"  Encoding: {encoding}")
    print(f"{'='*80}\n")

    # Setup paths
    lambda_checkpoint = model_dir / 'lambda' / '1' / 'checkpoint.pth'
    results_dir = Path(__file__).parent / 'test_results_liouville'
    results_dir.mkdir(exist_ok=True)

    if not lambda_checkpoint.exists():
        print(f"✗ Checkpoint not found: {lambda_checkpoint}")
        sys.exit(1)

    print(f"✓ Checkpoint found: {lambda_checkpoint}\n")

    # Test on all datasets
    dataset_types = ['natural', 'cheat', 'non_cheat']
    results = {}

    for dataset_type in dataset_types:
        print(f"\nTesting on {dataset_type} dataset...")

        test_file = get_test_data_path(encoding, dataset_type, 'liouville')

        if not test_file.exists():
            print(f"  ✗ Test file not found: {test_file}")
            continue

        print(f"  ✓ Test file: {test_file}")
        print(f"  Running evaluation...")

        # Run evaluation
        basic_metrics, eval_file, _ = run_evaluation(lambda_checkpoint, test_file, encoding, results_dir)

        if not basic_metrics:
            print(f"  ✗ Evaluation failed")
            continue

        # Parse detailed predictions
        y_true, y_pred = parse_eval_file(eval_file)
        detailed_metrics = None

        if y_true is not None:
            detailed_metrics = compute_metrics(y_true, y_pred)

        results[dataset_type] = {
            'basic': basic_metrics,
            'detailed': detailed_metrics
        }

        # Print summary
        print_summary(dataset_type, basic_metrics, detailed_metrics)

    # Save results
    if results:
        results_json = results_dir / 'test_results.json'
        save_results = {}
        for dt, data in results.items():
            save_results[dt] = {'basic': data['basic']}
            if data['detailed']:
                detailed = data['detailed'].copy()
                detailed['confusion_matrix'] = detailed['confusion_matrix'].tolist()
                save_results[dt]['detailed'] = detailed

        with open(results_json, 'w') as f:
            json.dump(save_results, f, indent=2)
        print(f"\n✓ Results saved to: {results_json}")

        # Generate plots
        print("\nGenerating plots...")
        plot_results(results, results_dir)

    print("\n✓ Testing complete!")


if __name__ == '__main__':
    main()
