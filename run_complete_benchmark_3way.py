"""
Complete Benchmark Runner - Compare ALL 3 Approaches
1. multiprocessing.Pool
2. concurrent.futures.ProcessPoolExecutor
3. concurrent.futures.ThreadPoolExecutor
"""
import os
import sys
from pathlib import Path
import time

def setup_directories():
    """Create necessary directories"""
    dirs = [
        "food_images/input",
        "food_images/output_multiprocessing",
        "food_images/output_concurrent_processes",
        "food_images/output_concurrent_threads",
        "performance_charts"
    ]
    
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"✅ Created directory: {d}")

def check_images(input_dir="food_images/input"):
    """Check if images exist"""
    image_extensions = ['.jpg', '.jpeg', '.png']
    image_paths = []
    
    for ext in image_extensions:
        image_paths.extend(Path(input_dir).glob(f"*{ext}"))
    
    if not image_paths:
        print(f"\n❌ ERROR: No images found in {input_dir}")
        print("\nPlease add images to the input directory:")
        print(f"  1. Download sample images from Food-101 dataset")
        print(f"  2. Place 20-50 images in: {input_dir}")
        print(f"  3. Run this script again")
        return None
    
    print(f"\n✅ Found {len(image_paths)} images")
    return [str(p) for p in image_paths]

def run_full_benchmark():
    """Run complete benchmark suite for all 3 methods"""
    
    print("\n" + "="*80)
    print("🚀 STARTING COMPLETE 3-WAY BENCHMARK SUITE")
    print("="*80)
    print("Comparing:")
    print("  1. multiprocessing.Pool (processes)")
    print("  2. concurrent.futures.ProcessPoolExecutor (processes)")
    print("  3. concurrent.futures.ThreadPoolExecutor (threads)")
    print("="*80)
    
    # Setup
    print("\n📁 Setting up directories...")
    setup_directories()
    
    # Check images
    print("\n🖼️  Checking for images...")
    image_paths = check_images()
    
    if not image_paths:
        return
    
    # Import modules
    print("\n📦 Loading modules...")
    try:
        from parallel_multiprocessing import benchmark_multiprocessing
        from parallel_concurrent_processes import benchmark_concurrent_processes
        from parallel_concurrent_threads import benchmark_concurrent_threads
        print("✅ All modules loaded successfully")
    except ImportError as e:
        print(f"❌ Error importing modules: {e}")
        print("Make sure all files are in the same directory")
        return
    
    # Run benchmarks
    print("\n" + "="*80)
    print("📊 PHASE 1: MULTIPROCESSING.POOL BENCHMARK")
    print("="*80)
    time.sleep(2)
    mp_results = benchmark_multiprocessing(
        image_paths, 
        "food_images/output_multiprocessing"
    )
    
    print("\n" + "="*80)
    print("📊 PHASE 2: CONCURRENT.FUTURES (PROCESSES) BENCHMARK")
    print("="*80)
    time.sleep(2)
    cfp_results = benchmark_concurrent_processes(
        image_paths, 
        "food_images/output_concurrent_processes"
    )
    
    print("\n" + "="*80)
    print("📊 PHASE 3: CONCURRENT.FUTURES (THREADS) BENCHMARK")
    print("="*80)
    time.sleep(2)
    cft_results = benchmark_concurrent_threads(
        image_paths, 
        "food_images/output_concurrent_threads"
    )
    
    # Final summary
    print("\n" + "="*80)
    print("🎉 BENCHMARK COMPLETE!")
    print("="*80)
    
    print("\n📂 Results saved to:")
    print("   • Processed images: food_images/output_*")
    
    # Complete comparison for all worker counts
    worker_counts = [1, 2, 4, 8]
    
    print("\n" + "="*80)
    print("⚡ 3-WAY COMPARISON - ALL WORKER COUNTS")
    print("="*80)
    print(f"{'Workers':<10} {'MP.Pool (s)':<18} {'CF.Process (s)':<18} {'CF.Thread (s)':<18}")
    print("-" * 80)
    
    for i, wc in enumerate(worker_counts):
        mp_time = mp_results[i]['total_time']
        cfp_time = cfp_results[i]['total_time']
        cft_time = cft_results[i]['total_time']
        print(f"{wc:<10} {mp_time:<18.2f} {cfp_time:<18.2f} {cft_time:<18.2f}")
    
    # Rankings for each worker count
    print("\n" + "="*80)
    print("🏆 RANKINGS BY WORKER COUNT")
    print("="*80)
    
    medals = ['🥇', '🥈', '🥉']
    
    for i, wc in enumerate(worker_counts):
        mp_time = mp_results[i]['total_time']
        cfp_time = cfp_results[i]['total_time']
        cft_time = cft_results[i]['total_time']
        
        results = [
            ('multiprocessing.Pool', mp_time),
            ('concurrent.futures (processes)', cfp_time),
            ('concurrent.futures (threads)', cft_time)
        ]
        results.sort(key=lambda x: x[1])
        
        print(f"\n{wc} Worker(s):")
        for rank, (method, time_val) in enumerate(results, 1):
            medal = medals[rank-1] if rank <= 3 else '  '
            print(f"  {rank}. {medal} {method:<40} {time_val:.2f}s")
    
    # Overall best performance (at 4 workers)
    mp_4 = mp_results[2]['total_time']
    cfp_4 = cfp_results[2]['total_time']
    cft_4 = cft_results[2]['total_time']
    
    print("\n" + "="*80)
    print("💡 KEY INSIGHTS")
    print("="*80)
    
    process_avg = (mp_4 + cfp_4) / 2
    thread_time = cft_4
    
    print(f"\n1. PROCESS-BASED METHODS (4 workers avg: {process_avg:.2f}s)")
    print(f"   • multiprocessing.Pool: {mp_4:.2f}s")
    print(f"   • concurrent.futures (processes): {cfp_4:.2f}s")
    print(f"   → Similar performance (both bypass GIL)")
    
    print(f"\n2. THREAD-BASED METHOD (4 workers): {thread_time:.2f}s")
    print(f"   • concurrent.futures (threads)")
    
    if thread_time > process_avg:
        slowdown = ((thread_time - process_avg) / process_avg) * 100
        print(f"   → {slowdown:.1f}% slower than process-based methods")
        print(f"   → Limited by Python's Global Interpreter Lock (GIL)")
    else:
        print(f"   → Comparable to process-based methods")
    
    # Speedup analysis
    print(f"\n3. SPEEDUP ANALYSIS (vs 1 worker)")
    mp_speedup_4 = mp_results[0]['total_time'] / mp_4
    cfp_speedup_4 = cfp_results[0]['total_time'] / cfp_4
    cft_speedup_4 = cft_results[0]['total_time'] / cft_4
    
    print(f"   • multiprocessing.Pool: {mp_speedup_4:.2f}x")
    print(f"   • concurrent.futures (processes): {cfp_speedup_4:.2f}x")
    print(f"   • concurrent.futures (threads): {cft_speedup_4:.2f}x")
    
    print(f"\n4. RECOMMENDATION")
    print(f"   For CPU-bound tasks (image processing):")
    print(f"   ✅ Use multiprocessing or concurrent.futures with processes")
    print(f"   ✅ 4 workers optimal for 4-core VM")
    print(f"   ❌ Avoid threading (GIL limits parallel execution)")
    
    # Generate summary file
    generate_summary(mp_results, cfp_results, cft_results)
    
    print("\n✅ All done! Check performance_charts/3way_comparison.txt for detailed analysis.")

def generate_summary(mp_results, cfp_results, cft_results):
    """Generate text summary of all results with rankings"""
    
    with open("performance_charts/3way_comparison.txt", "w") as f:
        f.write("="*80 + "\n")
        f.write("3-WAY PERFORMANCE COMPARISON\n")
        f.write("Image Processing: Threading vs Multiprocessing\n")
        f.write("="*80 + "\n\n")
        
        worker_counts = [1, 2, 4, 8]
        
        # Table header
        f.write("EXECUTION TIME COMPARISON\n")
        f.write("-"*80 + "\n")
        f.write(f"{'Workers':<12} {'MP.Pool':<15} {'CF.Process':<15} {'CF.Thread':<15}\n")
        f.write("-"*80 + "\n")
        
        for i, wc in enumerate(worker_counts):
            mp_time = mp_results[i]['total_time']
            cfp_time = cfp_results[i]['total_time']
            cft_time = cft_results[i]['total_time']
            
            f.write(f"{wc:<12} {mp_time:<15.2f} {cfp_time:<15.2f} {cft_time:<15.2f}\n")
        
        # Rankings for each worker count
        f.write("\n" + "="*80 + "\n")
        f.write("RANKINGS BY WORKER COUNT\n")
        f.write("="*80 + "\n\n")
        
        for i, wc in enumerate(worker_counts):
            mp_time = mp_results[i]['total_time']
            cfp_time = cfp_results[i]['total_time']
            cft_time = cft_results[i]['total_time']
            
            results = [
                ('multiprocessing.Pool', mp_time),
                ('concurrent.futures (processes)', cfp_time),
                ('concurrent.futures (threads)', cft_time)
            ]
            results.sort(key=lambda x: x[1])
            
            f.write(f"{wc} Worker(s):\n")
            for rank, (method, time_val) in enumerate(results, 1):
                if rank == 1:
                    medal = "1st"
                elif rank == 2:
                    medal = "2nd"
                else:
                    medal = "3rd"
                f.write(f"  {medal}: {method:<40} {time_val:.2f}s\n")
            f.write("\n")
        
        f.write("="*80 + "\n")
        f.write("SPEEDUP ANALYSIS (vs sequential - 1 worker)\n")
        f.write("="*80 + "\n\n")
        
        mp_seq = mp_results[0]['total_time']
        cfp_seq = cfp_results[0]['total_time']
        cft_seq = cft_results[0]['total_time']
        
        f.write(f"{'Workers':<12} {'MP.Pool':<15} {'CF.Process':<15} {'CF.Thread':<15}\n")
        f.write("-"*80 + "\n")
        
        for i, wc in enumerate(worker_counts):
            mp_speedup = mp_seq / mp_results[i]['total_time']
            cfp_speedup = cfp_seq / cfp_results[i]['total_time']
            cft_speedup = cft_seq / cft_results[i]['total_time']
            
            f.write(f"{wc:<12} {mp_speedup:<15.2f} {cfp_speedup:<15.2f} {cft_speedup:<15.2f}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("EFFICIENCY ANALYSIS (Speedup / Workers * 100%)\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"{'Workers':<12} {'MP.Pool':<15} {'CF.Process':<15} {'CF.Thread':<15}\n")
        f.write("-"*80 + "\n")
        
        for i, wc in enumerate(worker_counts):
            mp_speedup = mp_seq / mp_results[i]['total_time']
            cfp_speedup = cfp_seq / cfp_results[i]['total_time']
            cft_speedup = cft_seq / cft_results[i]['total_time']
            
            mp_eff = (mp_speedup / wc) * 100
            cfp_eff = (cfp_speedup / wc) * 100
            cft_eff = (cft_speedup / wc) * 100
            
            f.write(f"{wc:<12} {mp_eff:<15.1f} {cfp_eff:<15.1f} {cft_eff:<15.1f}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("KEY FINDINGS\n")
        f.write("="*80 + "\n\n")
        
        mp_4 = mp_results[2]['total_time']
        cfp_4 = cfp_results[2]['total_time']
        cft_4 = cft_results[2]['total_time']
        
        f.write(f"1. PROCESS-BASED METHODS (4 workers)\n")
        f.write(f"   - multiprocessing.Pool: {mp_4:.2f}s\n")
        f.write(f"   - concurrent.futures (processes): {cfp_4:.2f}s\n")
        avg_process = (mp_4 + cfp_4) / 2
        f.write(f"   - Average: {avg_process:.2f}s\n")
        f.write(f"   - Both bypass GIL and enable true parallelism\n")
        f.write(f"   - Performance difference: {abs(mp_4 - cfp_4):.2f}s ({abs(mp_4-cfp_4)/avg_process*100:.1f}%)\n\n")
        
        f.write(f"2. THREAD-BASED METHOD (4 workers)\n")
        f.write(f"   - concurrent.futures (threads): {cft_4:.2f}s\n")
        
        if cft_4 > avg_process:
            slowdown = ((cft_4 - avg_process) / avg_process) * 100
            f.write(f"   - {slowdown:.1f}% slower than process-based methods\n")
            f.write(f"   - Limited by Global Interpreter Lock (GIL)\n")
            f.write(f"   - Threads cannot execute Python code in parallel\n\n")
        else:
            f.write(f"   - Comparable to process-based methods\n\n")
        
        f.write(f"3. OPTIMAL CONFIGURATION\n")
        # Find best overall
        all_results = []
        for i, wc in enumerate(worker_counts):
            all_results.extend([
                (f'MP.Pool ({wc}w)', mp_results[i]['total_time']),
                (f'CF.Process ({wc}w)', cfp_results[i]['total_time']),
                (f'CF.Thread ({wc}w)', cft_results[i]['total_time'])
            ])
        all_results.sort(key=lambda x: x[1])
        
        best_config = all_results[0]
        f.write(f"   - Fastest configuration: {best_config[0]} at {best_config[1]:.2f}s\n")
        
        # Best for each method
        mp_best_idx = mp_results.index(min(mp_results, key=lambda x: x['total_time']))
        cfp_best_idx = cfp_results.index(min(cfp_results, key=lambda x: x['total_time']))
        cft_best_idx = cft_results.index(min(cft_results, key=lambda x: x['total_time']))
        
        f.write(f"   - Best MP.Pool: {worker_counts[mp_best_idx]} workers ({mp_results[mp_best_idx]['total_time']:.2f}s)\n")
        f.write(f"   - Best CF.Process: {worker_counts[cfp_best_idx]} workers ({cfp_results[cfp_best_idx]['total_time']:.2f}s)\n")
        f.write(f"   - Best CF.Thread: {worker_counts[cft_best_idx]} workers ({cft_results[cft_best_idx]['total_time']:.2f}s)\n\n")
        
        f.write(f"4. RECOMMENDATIONS\n")
        f.write(f"   - For CPU-intensive tasks: Use process-based parallelism\n")
        f.write(f"   - concurrent.futures provides cleaner, more modern API\n")
        f.write(f"   - Match worker count to available CPU cores (4 optimal for 4-core VM)\n")
        f.write(f"   - Threading suitable only for I/O-bound tasks\n")
        f.write(f"   - Beyond 4 workers on 4-core system: diminishing returns due to overhead\n\n")
        
        f.write(f"5. PERFORMANCE INSIGHTS\n")
        mp_speedup_4 = mp_seq / mp_4
        cfp_speedup_4 = cfp_seq / cfp_4
        cft_speedup_4 = cft_seq / cft_4
        
        f.write(f"   - MP.Pool 4-worker speedup: {mp_speedup_4:.2f}x\n")
        f.write(f"   - CF.Process 4-worker speedup: {cfp_speedup_4:.2f}x\n")
        f.write(f"   - CF.Thread 4-worker speedup: {cft_speedup_4:.2f}x\n")
        f.write(f"   - Process-based methods achieve near-optimal speedup\n")
        f.write(f"   - Threading limited by GIL for CPU-bound operations\n")
    
    print(f"✅ Saved: performance_charts/3way_comparison.txt")

def quick_test():
    """Run a quick test with limited images"""
    print("\n" + "="*80)
    print("🧪 QUICK TEST MODE (3-WAY)")
    print("="*80)
    
    setup_directories()
    image_paths = check_images()
    
    if not image_paths:
        return
    
    # Limit to first 10 images for quick test
    test_images = image_paths[:10]
    print(f"\n📸 Using {len(test_images)} images for quick test")
    
    from parallel_multiprocessing import run_multiprocessing
    from parallel_concurrent_processes import run_concurrent_processes
    from parallel_concurrent_threads import run_concurrent_threads
    
    print("\n🔹 Testing multiprocessing.Pool (4 processes)...")
    mp_result = run_multiprocessing(
        test_images, 
        "food_images/output_multiprocessing", 
        4
    )
    
    print("\n🔹 Testing concurrent.futures with PROCESSES (4 processes)...")
    cfp_result = run_concurrent_processes(
        test_images, 
        "food_images/output_concurrent_processes", 
        4
    )
    
    print("\n🔹 Testing concurrent.futures with THREADS (4 threads)...")
    cft_result = run_concurrent_threads(
        test_images, 
        "food_images/output_concurrent_threads", 
        4
    )
    
    print("\n✅ Quick test complete!")
    print(f"\n{'Method':<40} {'Time (s)':<15}")
    print("-" * 55)
    print(f"{'multiprocessing.Pool':<40} {mp_result['total_time']:<15.2f}")
    print(f"{'concurrent.futures (processes)':<40} {cfp_result['total_time']:<15.2f}")
    print(f"{'concurrent.futures (threads)':<40} {cft_result['total_time']:<15.2f}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        quick_test()
    else:
        run_full_benchmark()
