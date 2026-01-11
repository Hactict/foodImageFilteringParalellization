"""
Parallel Image Processing using multiprocessing
Processes multiple images concurrently using separate processes
"""
import os
import time
import multiprocessing
from pathlib import Path
from image_filters import process_image_all_filters

def process_single_image(args):
    """
    Wrapper function for processing a single image
    Args: tuple of (image_path, output_dir)
    """
    image_path, output_dir = args
    
    # Get process info
    pid = os.getpid()
    
    print(f"🔄 [Process {pid}] Processing: {os.path.basename(image_path)}")
    
    start_time = time.time()
    result = process_image_all_filters(image_path, output_dir)
    duration = time.time() - start_time
    
    print(f"✅ [Process {pid}] Completed: {os.path.basename(image_path)} in {duration:.2f}s")
    
    return {
        'image': image_path,
        'duration': duration,
        'pid': pid
    }

def run_multiprocessing(image_paths, output_dir, num_processes=4):
    """
    Process images using multiprocessing.Pool
    
    Args:
        image_paths: List of image file paths
        output_dir: Directory to save processed images
        num_processes: Number of parallel processes
    
    Returns:
        dict with timing information and results
    """
    print(f"\n{'='*60}")
    print(f"🚀 MULTIPROCESSING MODE - Using {num_processes} processes")
    print(f"{'='*60}")
    
    # Prepare arguments for each image
    args_list = [(img_path, output_dir) for img_path in image_paths]
    
    start_time = time.time()
    
    # Create process pool and map work
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(process_single_image, args_list)
    
    total_time = time.time() - start_time
    
    # Calculate statistics
    individual_times = [r['duration'] for r in results]
    avg_time = sum(individual_times) / len(individual_times)
    
    print(f"\n📊 MULTIPROCESSING SUMMARY:")
    print(f"   Total images processed: {len(results)}")
    print(f"   Number of processes: {num_processes}")
    print(f"   Total execution time: {total_time:.2f}s")
    print(f"   Average time per image: {avg_time:.2f}s")
    
    # Show unique PIDs used
    unique_pids = set(r['pid'] for r in results)
    print(f"   Unique Process IDs used: {len(unique_pids)} -> {unique_pids}")
    
    return {
        'method': 'multiprocessing',
        'num_workers': num_processes,
        'total_time': total_time,
        'avg_time_per_image': avg_time,
        'images_processed': len(results),
        'unique_pids': len(unique_pids),
        'results': results
    }

def benchmark_multiprocessing(image_paths, output_dir):
    """
    Run benchmark tests with different numbers of processes
    Tests: 1, 2, 4, 8 processes
    """
    print("\n" + "="*60)
    print("🔬 BENCHMARKING MULTIPROCESSING")
    print("="*60)
    
    process_counts = [1, 2, 4, 8]
    benchmark_results = []
    
    for num_proc in process_counts:
        result = run_multiprocessing(image_paths, output_dir, num_proc)
        benchmark_results.append(result)
        time.sleep(1)  # Brief pause between runs
    
    # Calculate speedup and efficiency
    sequential_time = benchmark_results[0]['total_time']
    
    print("\n" + "="*60)
    print("📈 PERFORMANCE METRICS")
    print("="*60)
    print(f"{'Processes':<12} {'Time (s)':<12} {'Speedup':<12} {'Efficiency':<12}")
    print("-" * 60)
    
    for result in benchmark_results:
        num_workers = result['num_workers']
        total_time = result['total_time']
        speedup = sequential_time / total_time
        efficiency = (speedup / num_workers) * 100
        
        print(f"{num_workers:<12} {total_time:<12.2f} {speedup:<12.2f} {efficiency:<12.1f}%")
    
    return benchmark_results

if __name__ == "__main__":
    # Configuration
    INPUT_DIR = "food_images/input"
    OUTPUT_DIR = "food_images/output_multiprocessing"
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Get all image files
    image_extensions = ['.jpg', '.jpeg', '.png']
    image_paths = []
    
    for ext in image_extensions:
        image_paths.extend(Path(INPUT_DIR).glob(f"*{ext}"))
    
    image_paths = [str(p) for p in image_paths]
    
    if not image_paths:
        print(f"❌ No images found in {INPUT_DIR}")
        exit(1)
    
    print(f"Found {len(image_paths)} images to process")
    
    # Run benchmark
    results = benchmark_multiprocessing(image_paths, OUTPUT_DIR)
    
    print("\n✅ Processing complete! Check output directory for results.")
