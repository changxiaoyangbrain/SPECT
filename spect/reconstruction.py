import numpy as np
from .system_matrix import SystemMatrix
import time

class OSEMReconstructor:
    def __init__(self, n_subsets=8, n_iterations=4):
        self.n_subsets = n_subsets
        self.n_iterations = n_iterations
        self.sm = SystemMatrix()
        
    def reconstruct_slice(self, sinogram, angles_deg, initial_image=None):
        """
        Reconstruct a single 2D slice using OSEM.
        sinogram: shape (n_angles, n_detector_bins) -> (64, 128)
        angles_deg: array of angles in degrees
        """
        n_angles, n_bins = sinogram.shape
        n_pixels = self.sm.image_size * self.sm.image_size
        
        # Flatten sinogram to (n_angles * n_bins)
        # Note: Our SystemMatrix produces rows ordered by angle: 
        # [Angle0_Bin0...Angle0_Bin127, Angle1_Bin0...]
        # So we must flatten row-major (default in numpy)
        measured_data = sinogram.flatten()
        
        # Compute full system matrix once
        # (Optimisation: Could compute subset matrices on the fly to save memory, 
        # but for 2D slice, memory is small enough)
        H_full = self.sm.compute_matrix(angles_deg)
        
        # Prepare Subsets
        subset_indices = []
        for s in range(self.n_subsets):
            # Select every n_subsets-th angle
            # Indices into the rows of H. 
            # H has (n_angles * n_bins) rows.
            # We need to select blocks of rows corresponding to specific angles.
            
            # Angles in this subset
            angle_indices = np.arange(s, n_angles, self.n_subsets)
            
            # Row indices in H
            # For each angle index 'a', rows are [a*128 : (a+1)*128]
            rows = []
            for a in angle_indices:
                rows.extend(range(a * n_bins, (a + 1) * n_bins))
            subset_indices.append(rows)
            
        # Initialize Image
        if initial_image is None:
            recon = np.ones(n_pixels, dtype=np.float32)
        else:
            recon = initial_image.flatten().astype(np.float32)
            
        epsilon = 1e-10
        
        # Precompute sensitivity images (normalization terms) for each subset
        sensitivity_images = []
        subset_matrices = []
        
        for s in range(self.n_subsets):
            H_sub = H_full[subset_indices[s], :]
            subset_matrices.append(H_sub)
            
            # Backproject ones
            ones_sub = np.ones(H_sub.shape[0], dtype=np.float32)
            sens = H_sub.transpose().dot(ones_sub)
            sensitivity_images.append(sens)

        # OSEM Loop
        for it in range(self.n_iterations):
            for s in range(self.n_subsets):
                H_sub = subset_matrices[s]
                sens = sensitivity_images[s]
                
                # Get measured data for this subset
                measured_sub = measured_data[subset_indices[s]]
                
                # Forward project
                expected_sub = H_sub.dot(recon)
                
                # Ratio
                ratio = measured_sub / (expected_sub + epsilon)
                
                # Backproject Ratio
                correction = H_sub.transpose().dot(ratio)
                
                # Update
                # recon = recon * (correction / (sens + epsilon))
                # Handle division by zero in sens (if any pixel is not seen by any ray)
                normalization = sens + epsilon
                recon *= (correction / normalization)
                
                # Enforce non-negativity
                recon[recon < 0] = 0
                
        return recon.reshape((self.sm.image_size, self.sm.image_size))

    def reconstruct_volume(self, projection_data, orbit_angles):
        """
        Reconstruct full volume slice by slice.
        projection_data: (128, 128, 64) -> (u, v, angle)
        orbit_angles: (64,) array of angles
        Returns: volume (128, 128, 128) -> (x, y, z)
        """
        # Input shape check
        u_dim, v_dim, n_angles = projection_data.shape
        # projection_data: u (detector bin), v (axial slice), angle
        
        volume = np.zeros((u_dim, u_dim, v_dim), dtype=np.float32)
        
        print(f"Starting reconstruction of {v_dim} slices...", flush=True)
        start_time = time.time()
        
        for z in range(v_dim):
            if z % 10 == 0:
                print(f"Reconstructing slice {z}/{v_dim}...", flush=True)
                
            # Extract sinogram for slice z
            # shape: (u, angle) -> (128, 64)
            sinogram_slice = projection_data[:, z, :]
            
            # Transpose to (angle, bin) for my reconstruct_slice method
            sinogram_slice = sinogram_slice.T # Now (64, 128)
            
            recon_slice = self.reconstruct_slice(sinogram_slice, orbit_angles)
            
            # Store
            # Standard orientation: usually z is the axial axis.
            # We map z index of projection to z index of volume.
            volume[:, :, z] = recon_slice
            
        end_time = time.time()
        print(f"Reconstruction complete in {end_time - start_time:.2f} seconds.")
        
        # Rotate volume if necessary to match reference orientation
        # (Will check orientation in Evaluation step)
        return volume
