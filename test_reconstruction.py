import unittest
import numpy as np
from reconstruction import OSEMReconstructor
from data_loader import SPECTDataLoader

class TestOSEM(unittest.TestCase):
    def test_reconstruct_slice(self):
        # Create a simple phantom
        sm = OSEMReconstructor(n_subsets=4, n_iterations=2).sm
        phantom = np.zeros((128, 128), dtype=np.float32)
        phantom[64-10:64+10, 64-10:64+10] = 10.0 # Central square
        
        # Forward project to create synthetic data
        angles = np.linspace(0, 180, 64, endpoint=False)
        H = sm.compute_matrix(angles)
        sinogram_flat = H.dot(phantom.flatten())
        sinogram = sinogram_flat.reshape((64, 128))
        
        # Add noise?
        # sinogram = np.random.poisson(sinogram).astype(np.float32)
        
        # Reconstruct
        recon = OSEMReconstructor(n_subsets=4, n_iterations=2)
        result = recon.reconstruct_slice(sinogram, angles)
        
        print("\nTest Slice Reconstruction:")
        print(f"Phantom Max: {phantom.max()}")
        print(f"Result Max: {result.max()}")
        print(f"Phantom Mean: {phantom.mean()}")
        print(f"Result Mean: {result.mean()}")
        
        # Check conservation of counts
        self.assertAlmostEqual(result.sum(), phantom.sum(), delta=phantom.sum()*0.1) # 10% tolerance
        
        # Check basic shape recovery (center should be high)
        center_val = result[64, 64]
        edge_val = result[10, 10]
        self.assertGreater(center_val, edge_val)

if __name__ == "__main__":
    unittest.main()
