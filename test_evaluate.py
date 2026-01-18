import unittest
import numpy as np
from evaluate import Evaluator

class TestEvaluator(unittest.TestCase):
    def test_metrics(self):
        # Create dummy images
        img1 = np.random.rand(128, 128, 128).astype(np.float32)
        img2 = img1.copy()
        
        # Test Perfect Match
        rmse = Evaluator.calculate_rmse(img1, img2)
        self.assertAlmostEqual(rmse, 0.0)
        
        score_ssim = Evaluator.calculate_ssim(img1, img2)
        self.assertAlmostEqual(score_ssim, 1.0)
        
        # Test Mismatch
        img3 = img1 + 0.1
        rmse_diff = Evaluator.calculate_rmse(img1, img3)
        self.assertAlmostEqual(rmse_diff, 0.1, places=5)
        
        score_ssim_diff = Evaluator.calculate_ssim(img1, img3)
        self.assertLess(score_ssim_diff, 1.0)
        
        print("\nTest Metrics:")
        print(f"RMSE (Same): {rmse}")
        print(f"SSIM (Same): {score_ssim}")
        print(f"RMSE (Diff): {rmse_diff}")
        print(f"SSIM (Diff): {score_ssim_diff}")

    def test_filter(self):
        img = np.zeros((20, 20, 20), dtype=np.float32)
        img[10, 10, 10] = 100.0 # Impulse
        
        filtered = Evaluator.apply_filter(img, fwhm_mm=10.0, pixel_size_mm=3.3)
        
        print("\nTest Filter:")
        print(f"Impulse Max: {img.max()}")
        print(f"Filtered Max: {filtered.max()}")
        # Filtered max should be lower
        self.assertLess(filtered.max(), img.max())
        
        # Check spread
        self.assertGreater(filtered[10, 10, 11], 0.0)

if __name__ == "__main__":
    unittest.main()
