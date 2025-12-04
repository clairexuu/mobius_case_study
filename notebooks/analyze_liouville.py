#!/usr/bin/env python3
"""
Analyze Liouville function training results

Usage:
    python analyze_liouville.py [model_dir]

Example:
    python analyze_liouville.py ../models/model_interCRT100_natural_liouville
"""

import os
import sys
import re
import matplotlib.pyplot as plt
from pathlib import Path

def parse_train_log(log_path):
    """Parse train.log file and extract metrics"""
    metrics = {
        'epochs': [],
        'train_loss': [],
        'valid_acc': [],
        'valid_xe_loss': [],
    }

    if not os.path.exists(log_path):
        print(f"Warning: {log_path} not found")
        return metrics

    with open(log_path, 'r') as f:
        for line in f:
            if '__log__:' in line:
                # Parse the dictionary at end of line
                log_str = line.split('__log__:')[1].strip()
                try:
                    log_dict = eval(log_str)

                    if 'epoch' in log_dict:
                        metrics['epochs'].append(log_dict['epoch'])

                    if 'valid_arithmetic_acc' in log_dict:
                        metrics['valid_acc'].append(log_dict['valid_arithmetic_acc'])

                    if 'valid_arithmetic_xe_loss' in log_dict:
                        metrics['valid_xe_loss'].append(log_dict['valid_arithmetic_xe_loss'])

                except:
                    continue

            elif '- LR:' in line and 'model LR' not in line:
                # Extract training loss
                parts = line.split()
                try:
                    loss_idx = parts.index('-') + 2
                    loss = float(parts[loss_idx])
                    metrics['train_loss'].append(loss)
                except:
                    continue

    return metrics


def print_summary(metrics, exp_name):
    """Print summary statistics"""
    if not metrics['valid_acc']:
        print(f"\n{exp_name}: No validation data found")
        return

    best_acc = max(metrics['valid_acc'])
    best_epoch = metrics['epochs'][metrics['valid_acc'].index(best_acc)]
    final_acc = metrics['valid_acc'][-1]
    final_epoch = metrics['epochs'][-1]

    print(f"\n{'='*60}")
    print(f"  {exp_name.upper()} RESULTS")
    print(f"{'='*60}")
    print(f"  Total Epochs:        {final_epoch + 1}")
    print(f"  Best Accuracy:       {best_acc:.2f}% (epoch {best_epoch})")
    print(f"  Final Accuracy:      {final_acc:.2f}% (epoch {final_epoch})")

    if metrics['valid_xe_loss']:
        best_loss = min(metrics['valid_xe_loss'])
        final_loss = metrics['valid_xe_loss'][-1]
        print(f"  Best XE Loss:        {best_loss:.4f}")
        print(f"  Final XE Loss:       {final_loss:.4f}")
    print(f"{'='*60}\n")


def plot_metrics(lambda_metrics, lambdasq_metrics, save_dir=None):
    """Generate plots for training metrics"""

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Liouville Function Training Results', fontsize=16, fontweight='bold')

    # Plot 1: Accuracy comparison
    ax = axes[0, 0]
    if lambda_metrics['valid_acc']:
        ax.plot(lambda_metrics['epochs'], lambda_metrics['valid_acc'],
                label='λ(n)', linewidth=2, color='blue')
    if lambdasq_metrics['valid_acc']:
        ax.plot(lambdasq_metrics['epochs'], lambdasq_metrics['valid_acc'],
                label='λ²(n)', linewidth=2, color='red')
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Validation Accuracy (%)')
    ax.set_title('Validation Accuracy Over Epochs')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 2: XE Loss comparison
    ax = axes[0, 1]
    if lambda_metrics['valid_xe_loss']:
        ax.plot(lambda_metrics['epochs'], lambda_metrics['valid_xe_loss'],
                label='λ(n)', linewidth=2, color='blue')
    if lambdasq_metrics['valid_xe_loss']:
        ax.plot(lambdasq_metrics['epochs'], lambdasq_metrics['valid_xe_loss'],
                label='λ²(n)', linewidth=2, color='red')
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Cross-Entropy Loss')
    ax.set_title('Validation Loss Over Epochs')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 3: Training loss (lambda)
    ax = axes[1, 0]
    if lambda_metrics['train_loss']:
        # Smooth by taking every 10th point to reduce noise
        train_loss = lambda_metrics['train_loss']
        step = max(1, len(train_loss) // 200)
        ax.plot(train_loss[::step], linewidth=1, color='blue', alpha=0.7)
    ax.set_xlabel('Training Steps')
    ax.set_ylabel('Training Loss')
    ax.set_title('λ(n) Training Loss')
    ax.set_ylim(0, 2)
    ax.grid(True, alpha=0.3)

    # Plot 4: Training loss (lambdasq)
    ax = axes[1, 1]
    if lambdasq_metrics['train_loss']:
        train_loss = lambdasq_metrics['train_loss']
        step = max(1, len(train_loss) // 200)
        ax.plot(train_loss[::step], linewidth=1, color='red', alpha=0.7)
    ax.set_xlabel('Training Steps')
    ax.set_ylabel('Training Loss')
    ax.set_title('λ²(n) Training Loss')
    ax.set_ylim(0, 2)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_dir:
        save_path = Path(save_dir) / 'liouville_training_plots.png'
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved plots to: {save_path}")

    plt.show()


def main():
    """Main analysis function"""

    # Parse command line arguments
    if len(sys.argv) > 1:
        model_dir = sys.argv[1]
    else:
        # Default to most recent Liouville model
        models_dir = Path(__file__).parent.parent / 'models'
        liouville_models = sorted(models_dir.glob('model_*_liouville'))
        if not liouville_models:
            print("No Liouville models found in ../models/")
            print("Usage: python analyze_liouville.py <model_dir>")
            sys.exit(1)
        model_dir = str(liouville_models[-1])

    model_path = Path(model_dir)
    print(f"\nAnalyzing model: {model_path.name}")
    print(f"Path: {model_path.absolute()}\n")

    # Find experiment directories
    lambda_log = model_path / 'lambda' / '1' / 'train.log'
    lambdasq_log = model_path / 'lambdasq' / '1' / 'train.log'

    # Parse logs
    print("Parsing training logs...")
    lambda_metrics = parse_train_log(lambda_log)
    lambdasq_metrics = parse_train_log(lambdasq_log)

    # Print summaries
    print_summary(lambda_metrics, 'λ(n)')
    print_summary(lambdasq_metrics, 'λ²(n)')

    # Generate plots
    if lambda_metrics['valid_acc'] or lambdasq_metrics['valid_acc']:
        print("Generating plots...")
        plot_metrics(lambda_metrics, lambdasq_metrics, save_dir=model_path)
    else:
        print("No validation data found. Skipping plots.")

    print("\nAnalysis complete!")


if __name__ == '__main__':
    main()
