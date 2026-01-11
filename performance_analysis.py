"""
Performance Analysis and Visualization
Generates comparison charts for parallel implementations
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import os

def generate_performance_charts(cf_results, mp_results, output_dir="performance_charts"):
    """
    Generate comparison charts between threading (concurrent.futures) and multiprocessing
    
    Args:
        cf_results: List of benchmark results from concurrent.futures (threading)
        mp_results: List of benchmark results from multiprocessing
        output_dir: Directory to save chart images
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract data
    worker_counts = [r['num_workers'] for r in cf_results]
    cf_times = [r['total_time'] for r in cf_results]
    mp_times = [r['total_time'] for r in mp_results]
    
    # Calculate speedup (relative to sequential - 1 worker)
    cf_speedup = [cf_results[0]['total_time'] / t for t in cf_times]
    mp_speedup = [mp_results[0]['total_time'] / t for t in mp_times]
    
    # Calculate efficiency
    cf_efficiency = [(s / w) * 100 for s, w in zip(cf_speedup, worker_counts)]
    mp_efficiency = [(s / w) * 100 for s, w in zip(mp_speedup, worker_counts)]
    
    # Chart 1: Execution Time Comparison
    plt.figure(figsize=(10, 6))
    x = np.arange(len(worker_counts))
    width = 0.35
    
    plt.bar(x - width/2, cf_times, width, label='Threading (concurrent.futures)', alpha=0.8, color='skyblue')
    plt.bar(x + width/2, mp_times, width, label='Multiprocessing', alpha=0.8, color='lightcoral')
    
    plt.xlabel('Number of Threads/Processes', fontsize=12)
    plt.ylabel('Execution Time (seconds)', fontsize=12)
    plt.title('Execution Time: Threading vs Multiprocessing', fontsize=14, fontweight='bold')
    plt.xticks(x, worker_counts)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/execution_time_comparison.png", dpi=300)
    print(f"✅ Saved: {output_dir}/execution_time_comparison.png")
    plt.close()
    
    # Chart 2: Speedup Comparison
    plt.figure(figsize=(10, 6))
    plt.plot(worker_counts, cf_speedup, marker='o', linewidth=2, markersize=8, 
             label='Threading', color='blue')
    plt.plot(worker_counts, mp_speedup, marker='s', linewidth=2, markersize=8, 
             label='Multiprocessing', color='red')
    plt.plot(worker_counts, worker_counts, '--', linewidth=1, 
             label='Ideal (Linear)', color='gray', alpha=0.7)
    
    plt.xlabel('Number of Threads/Processes', fontsize=12)
    plt.ylabel('Speedup', fontsize=12)
    plt.title('Speedup: Threading vs Multiprocessing', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/speedup_comparison.png", dpi=300)
    print(f"✅ Saved: {output_dir}/speedup_comparison.png")
    plt.close()
    
    # Chart 3: Efficiency Comparison
    plt.figure(figsize=(10, 6))
    plt.plot(worker_counts, cf_efficiency, marker='o', linewidth=2, markersize=8, 
             label='Threading', color='green')
    plt.plot(worker_counts, mp_efficiency, marker='s', linewidth=2, markersize=8, 
             label='Multiprocessing', color='orange')
    plt.axhline(y=100, linestyle='--', color='gray', alpha=0.7, label='100% Efficiency')
    
    plt.xlabel('Number of Threads/Processes', fontsize=12)
    plt.ylabel('Efficiency (%)', fontsize=12)
    plt.title('Efficiency: Threading vs Multiprocessing', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.ylim(0, 110)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/efficiency_comparison.png", dpi=300)
    print(f"✅ Saved: {output_dir}/efficiency_comparison.png")
    plt.close()
    
    # Chart 4: Combined Bar Chart
    fig, ax = plt.subplots(1, 3, figsize=(15, 5))
    
    # Execution Time
    x = np.arange(len(worker_counts))
    width = 0.35
    ax[0].bar(x - width/2, cf_times, width, label='Threading', alpha=0.8)
    ax[0].bar(x + width/2, mp_times, width, label='Multiprocessing', alpha=0.8)
    ax[0].set_xlabel('Threads/Processes')
    ax[0].set_ylabel('Time (s)')
    ax[0].set_title('Execution Time')
    ax[0].set_xticks(x)
    ax[0].set_xticklabels(worker_counts)
    ax[0].legend()
    ax[0].grid(axis='y', alpha=0.3)
    
    # Speedup
    ax[1].bar(x - width/2, cf_speedup, width, label='Threading', alpha=0.8)
    ax[1].bar(x + width/2, mp_speedup, width, label='Multiprocessing', alpha=0.8)
    ax[1].set_xlabel('Threads/Processes')
    ax[1].set_ylabel('Speedup')
    ax[1].set_title('Speedup')
    ax[1].set_xticks(x)
    ax[1].set_xticklabels(worker_counts)
    ax[1].legend()
    ax[1].grid(axis='y', alpha=0.3)
    
    # Efficiency
    ax[2].bar(x - width/2, cf_efficiency, width, label='Threading', alpha=0.8)
    ax[2].bar(x + width/2, mp_efficiency, width, label='Multiprocessing', alpha=0.8)
    ax[2].set_xlabel('Threads/Processes')
    ax[2].set_ylabel('Efficiency (%)')
    ax[2].set_title('Efficiency')
    ax[2].set_xticks(x)
    ax[2].set_xticklabels(worker_counts)
    ax[2].legend()
    ax[2].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/combined_metrics.png", dpi=300)
    print(f"✅ Saved: {output_dir}/combined_metrics.png")
    plt.close()
    
    # Generate summary table
    generate_summary_table(cf_results, mp_results, worker_counts, output_dir)

def generate_summary_table(cf_results, mp_results, worker_counts, output_dir):
    """Generate a summary table in text format"""
    
    with open(f"{output_dir}/performance_summary.txt", "w") as f:
        f.write("="*80 + "\n")
        f.write("PERFORMANCE ANALYSIS SUMMARY\n")
        f.write("Comparison: Threading (concurrent.futures) vs Multiprocessing\n")
        f.write("="*80 + "\n\n")
        
        # Threading results
        f.write("THREADING (CONCURRENT.FUTURES) RESULTS\n")
        f.write("-"*80 + "\n")
        f.write(f"{'Threads':<10} {'Time (s)':<12} {'Speedup':<12} {'Efficiency (%)':<15}\n")
        f.write("-"*80 + "\n")
        
        sequential_cf = cf_results[0]['total_time']
        for i, result in enumerate(cf_results):
            workers = result['num_workers']
            time_val = result['total_time']
            speedup = sequential_cf / time_val
            efficiency = (speedup / workers) * 100
            f.write(f"{workers:<10} {time_val:<12.2f} {speedup:<12.2f} {efficiency:<15.1f}\n")
        
        f.write("\n")
        
        # Multiprocessing results
        f.write("MULTIPROCESSING RESULTS\n")
        f.write("-"*80 + "\n")
        f.write(f"{'Processes':<10} {'Time (s)':<12} {'Speedup':<12} {'Efficiency (%)':<15}\n")
        f.write("-"*80 + "\n")
        
        sequential_mp = mp_results[0]['total_time']
        for i, result in enumerate(mp_results):
            processes = result['num_workers']
            time_val = result['total_time']
            speedup = sequential_mp / time_val
            efficiency = (speedup / processes) * 100
            f.write(f"{processes:<10} {time_val:<12.2f} {speedup:<12.2f} {efficiency:<15.1f}\n")
        
        f.write("\n")
        f.write("="*80 + "\n")
        f.write("KEY INSIGHTS\n")
        f.write("="*80 + "\n")
        
        # Best performance
        best_cf_idx = cf_results.index(min(cf_results, key=lambda x: x['total_time']))
        best_mp_idx = mp_results.index(min(mp_results, key=lambda x: x['total_time']))
        
        f.write(f"\nBest threading performance: {worker_counts[best_cf_idx]} threads "
                f"({cf_results[best_cf_idx]['total_time']:.2f}s)\n")
        f.write(f"Best multiprocessing performance: {worker_counts[best_mp_idx]} processes "
                f"({mp_results[best_mp_idx]['total_time']:.2f}s)\n")
        
        # Overall winner
        if cf_results[best_cf_idx]['total_time'] < mp_results[best_mp_idx]['total_time']:
            winner = "Threading"
            diff = ((mp_results[best_mp_idx]['total_time'] - cf_results[best_cf_idx]['total_time']) 
                    / mp_results[best_mp_idx]['total_time'] * 100)
        else:
            winner = "Multiprocessing"
            diff = ((cf_results[best_cf_idx]['total_time'] - mp_results[best_mp_idx]['total_time']) 
                    / cf_results[best_cf_idx]['total_time'] * 100)
        
        f.write(f"\nOverall winner: {winner} (faster by {diff:.1f}%)\n")
        
        f.write("\nKEY INSIGHT:\n")
        if winner == "Multiprocessing":
            f.write("Multiprocessing outperforms threading for CPU-bound image processing tasks\n")
            f.write("because it bypasses Python's Global Interpreter Lock (GIL), enabling true\n")
            f.write("parallel execution across multiple CPU cores.\n")
        else:
            f.write("Results show similar performance, though multiprocessing typically\n")
            f.write("outperforms threading for CPU-intensive tasks due to GIL bypass.\n")
    
    print(f"✅ Saved: {output_dir}/performance_summary.txt")

if __name__ == "__main__":
    # This script should be called after running benchmarks
    print("Run parallel_multiprocessing.py and parallel_concurrent.py first to generate data")
    print("Then import this module to generate charts")
