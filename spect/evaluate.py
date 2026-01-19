import numpy as np
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
from scipy.ndimage import gaussian_filter

class Evaluator:
    @staticmethod
    def calculate_rmse(img1, img2):
        """
        Calculate Root Mean Square Error.
        """
        return np.sqrt(np.mean((img1 - img2) ** 2))

    @staticmethod
    def calculate_ssim(img1, img2, data_range=None):
        """
        Calculate Structural Similarity Index.
        img1, img2: 3D volumes
        """
        if data_range is None:
            data_range = max(img1.max(), img2.max()) - min(img1.min(), img2.min())
        
        # ssim in skimage supports 3D if channel_axis is None (default for 2D, but we have 3D volume)
        # Actually skimage ssim is typically 2D. For 3D we can compute per slice or use 3D support.
        # skimage 0.19+ supports nd-images.
        # We need to specify win_size smaller than 7 if any dimension is < 7? No, our dims are 128.
        return ssim(img1, img2, data_range=data_range)

    @staticmethod
    def calculate_snr(signal_image, noise_std=None):
        """
        Simple SNR calculation.
        If noise_std is not provided, estimate from background (assuming corners are background).
        """
        # This is tricky without knowing ROI.
        # We will use Peak SNR (PSNR) relative to reference instead.
        pass

    @staticmethod
    def apply_filter(volume, fwhm_mm=10.0, pixel_size_mm=3.3):
        """
        Apply 3D Gaussian Filter.
        FWHM = 2.355 * sigma
        """
        sigma_mm = fwhm_mm / 2.355
        sigma_pixel = sigma_mm / pixel_size_mm
        
        # Report says: "Kernel 7x7x7"
        # Scipy gaussian_filter automatically chooses kernel size based on sigma (usually 4*sigma)
        # sigma 1.28 -> radius ~5 -> size ~11. 
        # If strict 7x7x7 kernel is required, we might need truncate parameter.
        # truncate = radius / sigma. Radius = 3 (for 7x7). 
        # truncate = 3 / 1.28 = 2.34
        
        return gaussian_filter(volume, sigma=sigma_pixel, truncate=2.34)

if __name__ == "__main__":
    pass
