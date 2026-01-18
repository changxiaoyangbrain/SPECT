import unittest
import numpy as np
import matplotlib.pyplot as plt
from system_matrix import SystemMatrix

class TestSystemMatrix(unittest.TestCase):
    def test_point_source_projection(self):
        sm = SystemMatrix(image_size=128, detector_size=128)
        angles = np.linspace(0, 360, 64, endpoint=False)
        H = sm.compute_matrix(angles)
        
        # Create a point source image
        image = np.zeros((128, 128), dtype=np.float32)
        # Place point off-center to see sine wave
        image[64+20, 64+10] = 1.0 
        
        # Forward project: p = H * f
        projection = H.dot(image.flatten())
        
        # Reshape to sinogram (Angles x Bins)
        sinogram = projection.reshape((64, 128))
        
        print("\nTest Point Source Projection:")
        print(f"Sinogram Shape: {sinogram.shape}")
        print(f"Sum of Image: {image.sum()}")
        print(f"Sum of Projection: {projection.sum()} (Should be close to Image Sum * n_angles?)")
        # Actually sum of projection approx sum of image * number of angles? 
        # No, Radon transform integral.
        # But here we distribute weight 1.0 to bins. So for each angle, sum should be 1.0 (if not out of bounds).
        # Total sum should be ~64.
        print(f"Actual Sum: {projection.sum()}")
        
        # Visual check (save plot)
        plt.figure(figsize=(10, 5))
        plt.subplot(121)
        plt.imshow(image, cmap='gray')
        plt.title('Point Source')
        plt.subplot(122)
        plt.imshow(sinogram, cmap='gray', aspect='auto')
        plt.title('Sinogram (Sine Wave?)')
        plt.savefig('test_system_matrix_result.png')
        print("Saved visualization to test_system_matrix_result.png")
        
        # Verify it's not empty
        self.assertGreater(projection.sum(), 0)

if __name__ == "__main__":
    unittest.main()
