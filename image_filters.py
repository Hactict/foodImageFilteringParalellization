"""
Image Processing Filters - OPTIMIZED VERSION
Uses vectorized operations for better performance
"""
import numpy as np
from PIL import Image
from scipy import signal

def load_image(image_path):
    """Load image and convert to numpy array"""
    img = Image.open(image_path)
    return np.array(img)

def save_image(image_array, output_path):
    """Save numpy array as image"""
    img = Image.fromarray(image_array.astype('uint8'))
    img.save(output_path)

def grayscale_conversion(image):
    """
    Convert RGB image to grayscale using luminance formula
    VECTORIZED: No loops, operates on entire array at once
    """
    if len(image.shape) == 2:
        return image
    
    # Vectorized operation - much faster!
    gray = (0.299 * image[:, :, 0] + 
            0.587 * image[:, :, 1] + 
            0.114 * image[:, :, 2])
    
    return gray.astype('uint8')

def gaussian_blur(image):
    """
    Apply 3x3 Gaussian blur using scipy.signal.convolve2d
    VECTORIZED: Uses optimized C code, no Python loops
    """
    kernel = np.array([[1, 2, 1],
                       [2, 4, 2],
                       [1, 2, 1]], dtype=np.float32) / 16.0
    
    if len(image.shape) == 2:
        # Single channel - use scipy convolution (FAST!)
        return signal.convolve2d(image, kernel, mode='same', boundary='symm').astype('uint8')
    else:
        # Multiple channels - apply to each
        result = np.zeros_like(image)
        for i in range(image.shape[2]):
            result[:, :, i] = signal.convolve2d(
                image[:, :, i], kernel, mode='same', boundary='symm'
            )
        return result.astype('uint8')

def edge_detection(image):
    """
    Apply Sobel filter using scipy.signal.convolve2d
    VECTORIZED + NORMALIZED (0–255) for good contrast
    """
    import numpy as np
    from scipy import signal

    # Convert to grayscale if needed
    if len(image.shape) == 3:
        image = grayscale_conversion(image)

    # Sobel kernels
    sobel_x = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]], dtype=np.float32)

    sobel_y = np.array([[-1, -2, -1],
                        [0,  0,  0],
                        [1,  2,  1]], dtype=np.float32)

    # Vectorized convolution (FAST)
    grad_x = signal.convolve2d(image, sobel_x, mode='same', boundary='symm')
    grad_y = signal.convolve2d(image, sobel_y, mode='same', boundary='symm')

    # Gradient magnitude
    edges = np.sqrt(grad_x**2 + grad_y**2)

    # ✅ Normalization for good contrast
    if edges.max() > 0:
        edges = (edges / edges.max()) * 255

    edges = np.clip(edges, 0, 255)

    return edges.astype(np.uint8)


def sharpen(image):
    """
    Apply sharpening filter using scipy.signal.convolve2d
    VECTORIZED: No loops!
    """
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]], dtype=np.float32)
    
    if len(image.shape) == 2:
        result = signal.convolve2d(image, kernel, mode='same', boundary='symm')
        return np.clip(result, 0, 255).astype('uint8')
    else:
        result = np.zeros_like(image, dtype=np.float32)
        for i in range(image.shape[2]):
            result[:, :, i] = signal.convolve2d(
                image[:, :, i], kernel, mode='same', boundary='symm'
            )
        return np.clip(result, 0, 255).astype('uint8')

def brightness_adjustment(image, factor=1.3):
    """
    Adjust image brightness
    VECTORIZED: Single operation on entire array
    """
    # Vectorized multiplication and clipping - FAST!
    adjusted = image.astype(np.float32) * factor
    adjusted = np.clip(adjusted, 0, 255)
    return adjusted.astype('uint8')

def process_image_all_filters(image_path, output_dir):
    """
    Apply all filters to a single image
    Returns dict with processing time and output paths
    """
    import os
    import time
    
    start_time = time.time()
    
    # Load image
    img = load_image(image_path)
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    
    results = {}
    
    # Apply each filter
    filters = {
        'grayscale': lambda x: grayscale_conversion(x),
        'blur': lambda x: gaussian_blur(x),
        'edges': lambda x: edge_detection(x),
        'sharpen': lambda x: sharpen(x),
        'brightness': lambda x: brightness_adjustment(x)
    }
    
    for filter_name, filter_func in filters.items():
        filtered = filter_func(img.copy())
        output_path = os.path.join(output_dir, f"{base_name}_{filter_name}.jpg")
        save_image(filtered, output_path)
        results[filter_name] = output_path
    
    duration = time.time() - start_time
    
    return {
        'image': image_path,
        'duration': duration,
        'outputs': results
    }
