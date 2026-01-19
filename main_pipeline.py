import os
import numpy as np
import time
import sys
from spect import SPECTDataLoader, OSEMReconstructor, Evaluator

def main():
    try:
        print("--- SPECT Reconstruction Pipeline Started ---", flush=True)
        
        # 1. Load Data
        loader = SPECTDataLoader()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, "data")
        outputs_dir = os.path.join(base_dir, "outputs")
    
        print("Loading data...", flush=True)
        proj_data = loader.load_projection(os.path.join(data_dir, "input", "Proj.dat"))
        orbit_df = loader.load_orbit(os.path.join(data_dir, "input", "orbit.xlsx"))
        ref_recon = loader.load_volume(os.path.join(data_dir, "reference", "OSEMReconed.dat"))
        ref_filtered = loader.load_volume(os.path.join(data_dir, "reference", "Filtered.dat"))
        
        orbit_angles = orbit_df['angle'].values
        
        # 2. Reconstruction
        print("\nStarting OSEM Reconstruction...", flush=True)
        # Using 4 subsets and 10 iterations as a standard choice
        reconstructor = OSEMReconstructor(n_subsets=4, n_iterations=10)
        
        # Reconstruct volume
        my_recon = reconstructor.reconstruct_volume(proj_data, orbit_angles)
        
        # Save My Recon
        os.makedirs(outputs_dir, exist_ok=True)
        my_recon_path = os.path.join(outputs_dir, "MyRecon.dat")
        my_recon.tofile(my_recon_path)
        print(f"Saved reconstruction to {my_recon_path}", flush=True)
        
        # 3. Post-Processing
        print("\nApplying Gaussian Filter...", flush=True)
        my_filtered = Evaluator.apply_filter(my_recon, fwhm_mm=10.0, pixel_size_mm=3.3)
        
        # Save My Filtered
        my_filtered_path = os.path.join(outputs_dir, "MyFiltered.dat")
        my_filtered.tofile(my_filtered_path)
        print(f"Saved filtered result to {my_filtered_path}", flush=True)
        
        # 4. Evaluation
        print("\n--- Evaluation Results ---", flush=True)
        
        # Raw Recon Comparison
        rmse_recon = Evaluator.calculate_rmse(my_recon, ref_recon)
        ssim_recon = Evaluator.calculate_ssim(my_recon, ref_recon)
        
        print(f"My Recon vs Ref Recon:", flush=True)
        print(f"  RMSE: {rmse_recon:.6f}", flush=True)
        print(f"  SSIM: {ssim_recon:.6f}", flush=True)
        
        # Filtered Comparison
        rmse_filt = Evaluator.calculate_rmse(my_filtered, ref_filtered)
        ssim_filt = Evaluator.calculate_ssim(my_filtered, ref_filtered)
        
        print(f"My Filtered vs Ref Filtered:", flush=True)
        print(f"  RMSE: {rmse_filt:.6f}", flush=True)
        print(f"  SSIM: {ssim_filt:.6f}", flush=True)
        
        # Save results to text
        with open(os.path.join(outputs_dir, "evaluation_results.txt"), "w") as f:
            f.write("Evaluation Results\n")
            f.write("==================\n")
            f.write(f"My Recon vs Ref Recon:\n")
            f.write(f"  RMSE: {rmse_recon:.6f}\n")
            f.write(f"  SSIM: {ssim_recon:.6f}\n\n")
            f.write(f"My Filtered vs Ref Filtered:\n")
            f.write(f"  RMSE: {rmse_filt:.6f}\n")
            f.write(f"  SSIM: {ssim_filt:.6f}\n")
        
        print("Pipeline Completed Successfully.", flush=True)
        
    except Exception as e:
        print(f"PIPELINE ERROR: {e}", file=sys.stderr, flush=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
