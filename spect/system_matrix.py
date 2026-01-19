import numpy as np
from scipy.sparse import lil_matrix, csr_matrix

class SystemMatrix:
    def __init__(self, image_size=128, detector_size=128, pixel_size=3.3):
        self.image_size = image_size
        self.detector_size = detector_size
        self.pixel_size = pixel_size
        self.center_image = (image_size - 1) / 2.0
        self.center_detector = (detector_size - 1) / 2.0

    def compute_matrix(self, angles_deg):
        """
        Compute the system matrix H for a set of angles.
        H maps image (N*N) -> projections (M*A)
        Rows: A (angles) * M (detector bins)
        Cols: N * N (pixels)
        """
        n_angles = len(angles_deg)
        n_pixels = self.image_size * self.image_size
        n_bins = self.detector_size * n_angles
        
        H = lil_matrix((n_bins, n_pixels), dtype=np.float32)
        
        # Precompute coordinates for all pixels
        # Image coordinates: x (col), y (row). Center at (0,0)
        # Using meshgrid
        y_indices, x_indices = np.indices((self.image_size, self.image_size))
        
        # Flatten
        x_flat = (x_indices.flatten() - self.center_image) * self.pixel_size
        y_flat = (self.center_image - y_indices.flatten()) * self.pixel_size # y points up
        
        for i, angle in enumerate(angles_deg):
            theta = np.radians(angle)
            cos_t = np.cos(theta)
            sin_t = np.sin(theta)
            
            # Radon transform: t = x * cos(theta) + y * sin(theta)
            # This projects (x,y) onto the detector axis rotated by theta
            t_positions = x_flat * cos_t + y_flat * sin_t
            
            # Convert physical position t to detector bin index
            # Bin 0 is at -center * pixel_size
            # index = (t / pixel_size) + center_detector
            bin_indices_float = (t_positions / self.pixel_size) + self.center_detector
            
            # Linear Interpolation (distribute value to adjacent bins)
            bin_lower = np.floor(bin_indices_float).astype(int)
            bin_upper = bin_lower + 1
            weight_upper = bin_indices_float - bin_lower
            weight_lower = 1.0 - weight_upper
            
            # Valid bins
            valid_mask = (bin_lower >= 0) & (bin_upper < self.detector_size)
            
            # Current projection row offset
            row_offset = i * self.detector_size
            
            # We can vectorize the assignment to sparse matrix row-by-row or loop
            # Since lil_matrix is slow with random access, but we are filling it systematically
            # Actually, constructing COO format vectors directly is faster
            pass
            
        # Re-implement using COO construction for speed
        rows = []
        cols = []
        data = []
        
        for i, angle in enumerate(angles_deg):
            theta = np.radians(angle)
            cos_t = np.cos(theta)
            sin_t = np.sin(theta)
            
            t_positions = x_flat * cos_t + y_flat * sin_t
            bin_indices_float = (t_positions / self.pixel_size) + self.center_detector
            
            bin_lower = np.floor(bin_indices_float).astype(int)
            weight_upper = bin_indices_float - bin_lower
            weight_lower = 1.0 - weight_upper
            
            # Filter valid
            valid_lower = (bin_lower >= 0) & (bin_lower < self.detector_size)
            valid_upper = ((bin_lower + 1) >= 0) & ((bin_lower + 1) < self.detector_size)
            
            # Row index in H (projection bin index)
            # Base row for this angle is i * self.detector_size
            
            # Add lower bin contributions
            current_pixels = np.where(valid_lower)[0]
            if len(current_pixels) > 0:
                current_bins = bin_lower[current_pixels] + i * self.detector_size
                current_weights = weight_lower[current_pixels]
                
                rows.extend(current_bins)
                cols.extend(current_pixels)
                data.extend(current_weights)
                
            # Add upper bin contributions
            current_pixels_upper = np.where(valid_upper)[0]
            if len(current_pixels_upper) > 0:
                current_bins = (bin_lower[current_pixels_upper] + 1) + i * self.detector_size
                current_weights = weight_upper[current_pixels_upper]
                
                rows.extend(current_bins)
                cols.extend(current_pixels_upper)
                data.extend(current_weights)
                
        H = csr_matrix((data, (rows, cols)), shape=(n_bins, n_pixels), dtype=np.float32)
        return H

if __name__ == "__main__":
    # Basic Test
    sm = SystemMatrix()
    angles = np.linspace(0, 180, 64, endpoint=False)
    H = sm.compute_matrix(angles)
    print(f"System Matrix Shape: {H.shape}")
    print(f"Sparsity: {H.nnz / (H.shape[0]*H.shape[1]):.6f}")
