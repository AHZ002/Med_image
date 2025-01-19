import numpy as np
from skimage.transform import rescale, rotate

def normalize_image(image):
    """
    Normalizes an image to the range [0, 255].
    Args:
        image (numpy.ndarray): Input image array.
    Returns:
        numpy.ndarray: Normalized image.
    """
    if image is None or np.max(image) == np.min(image):
        raise ValueError("Invalid image for normalization.")
    normalized = ((image - np.min(image)) / (np.max(image) - np.min(image)) * 255).astype(np.uint8)
    return normalized

def adjust_contrast(image, factor):
    """
    Adjusts the contrast of an image.
    Args:
        image (numpy.ndarray): Input image array.
        factor (float): Contrast adjustment factor.
    Returns:
        numpy.ndarray: Contrast-adjusted image.
    """
    contrast_image = image * factor
    return np.clip(contrast_image, 0, 255).astype(np.uint8)

def rotate_image(image, angle):
    """
    Rotates an image by the specified angle.
    Args:
        image (numpy.ndarray): Input image array.
        angle (float): Rotation angle in degrees.
    Returns:
        numpy.ndarray: Rotated image.
    """
    return rotate(image, angle=angle, resize=True, preserve_range=True).astype(image.dtype)

def flip_image(image):
    """
    Flips an image vertically.
    Args:
        image (numpy.ndarray): Input image array.
    Returns:
        numpy.ndarray: Flipped image.
    """
    return np.flipud(image)

def zoom_image(image, factor):
    """
    Zooms an image by the specified factor.
    Args:
        image (numpy.ndarray): Input image array.
        factor (float): Zoom factor.
    Returns:
        numpy.ndarray: Zoomed image.
    """
    return rescale(image, factor, preserve_range=True, anti_aliasing=True).astype(image.dtype)
