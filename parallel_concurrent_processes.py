"""
Parallel Image Processing using concurrent.futures
Uses ProcessPoolExecutor for process-based parallelism
"""
import os
import time
import concurrent.futures
from pathlib import Path
from image_filters import process_image_all_filters

def process_single_image(args):
    """
    Wrapper function for processing a single image
    Args: tuple of (image_path, output_dir)
    """
    image_path, output_dir = args
    
    pid = os.getpid()
    
    print(f"🔄 [Worker {pid}] Processing: {os.path.basename(image_path)}")
    
    start_time = time.time()
    result = process_image_all_filters(image_path, output_dir)
    duration = time.time() - start_time
    
    print(f"✅ [Worker {pid}] Completed: {os.path.basename(image_path)} in {duration:.2f}s")
    
    return {
        'image': image_path,
        'duration': duration,
        'pid': pid
    }

def run_concurrent_processes(image_paths, output_dir, num_workers=4):
    """
    Process images using concurrent.futures.ProcessPoolExecutor
    
    Args:
        image_paths: List of image file paths
        output_dir: Directory to save processed images
        num_workers: Number of parallel processes
    
    Returns:
        dict with timing information and results
    """
    print(f"\n{'='*60}")
    print(f"🚀 CONCURRENT.FUTURES (PROCESSES) MODE - Using {num_workers} processes")
    print(f"{'='*60}")
    
    args_list = [(img_path, output_dir) for img_path in image_paths]
    
    start_time = time.time()
    results = []
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        future_to_image = {executor.submit(process_single_image, args): args[0] for args in args_list}
        
        for future in concurrent.futures.as_completed(future_to_image):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                image_path = future_to_image[future]
                print(f"❌ Error processing {image_path}: {e}")
    
    total_time = time.time() - start_time
    individual_times = [r['duration'] for r in results]
    avg_time = sum(individual_times) / len(individual_times) if individual_times else 0
    
    print(f"\n📊 CONCURRENT.FUTURES (PROCESSES) SUMMARY:")
    print(f"   Total images processed: {len(results)}")
    print(f"   Number of processes: {num_workers}")
    print(f"   Total execution time: {total_time:.2f}s")
    print(f"   Average time per image: {avg_time:.2f}s")
    
    unique_pids = set(r['pid'] for r in results)
    print(f"   Unique Process IDs used: {len(unique_pids)} -> {unique_pids}")
    
    return {
        'method': 'concurrent.futures (processes)',
        'num_workers': num_workers,
        'total_time': total_time,
        'avg_time_per_image': avg_time,
        'images_processed': len(results),
        'unique_pids': len(unique_pids),
        'results': results
    }

def benchmark_concurrent_processes(image_paths, output_dir):
    """
    Run benchmark tests with different numbers of processes
    Tests: 1, 2, 4, 8 processes
    """
    print("\n" + "="*60)
    print("🔬 BENCHMARKING CONCURRENT.FUTURES (PROCESSES)")
    print("="*60)
    
    process_counts = [1, 2, 4, 8]
    benchmark_results = []
    
    for num_proc in process_counts:
        result = run_concurrent_processes(image_paths, output_dir, num_proc)
        benchmark_results.append(result)
        time.sleep(1)
    
    sequential_time = benchmark_results[0]['total_time']
    
    print("\n" + "="*60)
    print("📈 PERFORMANCE METRICS")
    print("="*60)
    print(f"{'Processes':<12} {'Time (s)':<12} {'Speedup':<12} {'Efficiency':<12}")
    print("-" * 60)
    
    for result in benchmark_results:
        num_workers = result['num_workers']
        total_time = result['total_time']
        speedup = sequential_time / total_time if total_time > 0 else 0
        efficiency = (speedup / num_workers) * 100 if num_workers > 0 else 0
        
        print(f"{num_workers:<12} {total_time:<12.2f} {speedup:<12.2f} {efficiency:<12.1f}%")
    
    return benchmark_results

if __name__ == "__main__":
    INPUT_DIR = "food_images/input"
    OUTPUT_DIR = "food_images/output_concurrent_processes"
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    image_extensions = ['.jpg', '.jpeg', '.png']
    image_paths = []
    for ext in image_extensions:
        image_paths.extend(Path(INPUT_DIR).glob(f"*{ext}"))
    
    image_paths = [str(p) for p in image_paths]
    
    if not image_paths:
        print(f"❌ No images found in {INPUT_DIR}")
        exit(1)
    
    print(f"Found {len(image_paths)} images to process")
    
    results = benchmark_concurrent_processes(image_paths, OUTPUT_DIR)
    
    print("\n✅ Processing complete! Check output directory for results.")
