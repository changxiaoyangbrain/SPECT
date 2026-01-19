import numpy as np
import pandas as pd
import os

class SPECTDataLoader:
    def __init__(self):
        self.proj_dim = (128, 128, 64)
        self.recon_dim = (128, 128, 128)
        self.dtype = np.float32

    def load_projection(self, file_path):
        """
        Load projection data from binary file.
        Expected size: 128 * 128 * 64 * 4 bytes
        Returns: numpy array of shape (128, 128, 64)
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        try:
            data = np.fromfile(file_path, dtype=self.dtype)
            expected_elements = np.prod(self.proj_dim)
            if data.size != expected_elements:
                raise ValueError(f"File size mismatch. Expected {expected_elements} elements, got {data.size}")
            
            # Reshape to (128, 128, 64)
            # Note: The report says "128*128*64", usually (u, v, angle)
            return data.reshape(self.proj_dim)
        except Exception as e:
            raise RuntimeError(f"Failed to load projection data: {e}")

    def load_orbit(self, file_path):
        """
        Load orbit data from Excel file.
        Returns: pandas DataFrame with standardized column names
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        try:
            df = pd.read_excel(file_path)
            # Rename columns for easier access
            df.columns = ['index', 'angle', 'radius', 'probe_idx']
            return df
        except Exception as e:
            raise RuntimeError(f"Failed to load orbit data: {e}")

    def load_volume(self, file_path):
        """
        Load reconstruction volume from binary file.
        Expected size: 128 * 128 * 128 * 4 bytes
        Returns: numpy array of shape (128, 128, 128)
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        try:
            data = np.fromfile(file_path, dtype=self.dtype)
            expected_elements = np.prod(self.recon_dim)
            if data.size != expected_elements:
                raise ValueError(f"File size mismatch. Expected {expected_elements} elements, got {data.size}")
            
            return data.reshape(self.recon_dim)
        except Exception as e:
            raise RuntimeError(f"Failed to load volume data: {e}")

if __name__ == "__main__":
    # Basic self-test
    loader = SPECTDataLoader()
    print("SPECTDataLoader initialized.")
