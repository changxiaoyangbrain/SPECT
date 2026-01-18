import unittest
import numpy as np
import os
from data_loader import SPECTDataLoader

class TestSPECTDataLoader(unittest.TestCase):
    def setUp(self):
        self.loader = SPECTDataLoader()
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.proj_path = os.path.join(self.base_dir, "Proj.dat")
        self.orbit_path = os.path.join(self.base_dir, "orbit.xlsx")
        self.recon_path = os.path.join(self.base_dir, "OSEMReconed.dat")

    def test_load_projection(self):
        data = self.loader.load_projection(self.proj_path)
        self.assertEqual(data.shape, (128, 128, 64))
        self.assertEqual(data.dtype, np.float32)
        print(f"\nProjection Data Stats: Min={data.min()}, Max={data.max()}, Mean={data.mean()}")

    def test_load_orbit(self):
        df = self.loader.load_orbit(self.orbit_path)
        self.assertEqual(len(df), 64)
        self.assertIn('angle', df.columns)
        self.assertIn('radius', df.columns)
        print(f"\nOrbit Data: Angle Range=[{df['angle'].min()}, {df['angle'].max()}]")
        print(f"Orbit Data: Radius Range=[{df['radius'].min()}, {df['radius'].max()}]")

    def test_load_volume(self):
        data = self.loader.load_volume(self.recon_path)
        self.assertEqual(data.shape, (128, 128, 128))
        self.assertEqual(data.dtype, np.float32)
        print(f"\nRecon Data Stats: Min={data.min()}, Max={data.max()}, Mean={data.mean()}")

if __name__ == "__main__":
    unittest.main()
