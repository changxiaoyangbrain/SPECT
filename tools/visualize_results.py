import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spect import SPECTDataLoader

def save_comparison_plot(my_vol, ref_vol, title_prefix, filename, slice_idx=None, axis=2):
    """
    Save a side-by-side comparison of a slice.
    axis: 0=Sagittal, 1=Coronal, 2=Axial (Transverse)
    """
    if slice_idx is None:
        # Find slice with max intensity in ref volume
        if axis == 0:
            proj = np.max(ref_vol, axis=(1, 2))
        elif axis == 1:
            proj = np.max(ref_vol, axis=(0, 2))
        else:
            proj = np.max(ref_vol, axis=(0, 1))
        slice_idx = np.argmax(proj)
        
    # Extract slices
    if axis == 0:
        sl_my = my_vol[slice_idx, :, :]
        sl_ref = ref_vol[slice_idx, :, :]
        axis_name = "Sagittal"
    elif axis == 1:
        sl_my = my_vol[:, slice_idx, :]
        sl_ref = ref_vol[:, slice_idx, :]
        axis_name = "Coronal"
    else:
        sl_my = my_vol[:, :, slice_idx]
        sl_ref = ref_vol[:, :, slice_idx]
        axis_name = "Axial"
        
    # Plot
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Common scaling
    vmin = 0
    vmax = max(sl_my.max(), sl_ref.max())
    
    im0 = axes[0].imshow(sl_ref, cmap='gray', vmin=vmin, vmax=vmax)
    axes[0].set_title(f"Reference ({axis_name} {slice_idx})")
    plt.colorbar(im0, ax=axes[0])
    
    im1 = axes[1].imshow(sl_my, cmap='gray', vmin=vmin, vmax=vmax)
    axes[1].set_title(f"My Recon ({axis_name} {slice_idx})")
    plt.colorbar(im1, ax=axes[1])
    
    # Difference
    diff = sl_my - sl_ref
    im2 = axes[2].imshow(diff, cmap='seismic', vmin=-vmax/2, vmax=vmax/2)
    axes[2].set_title("Difference")
    plt.colorbar(im2, ax=axes[2])
    
    plt.suptitle(f"{title_prefix} Comparison")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"Saved comparison to {filename}")

def main():
    loader = SPECTDataLoader()
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    outputs_dir = os.path.join(base_dir, "outputs")
    pictures_dir = os.path.join(base_dir, "pictures")
    
    print("Loading volumes for visualization...")
    my_recon = loader.load_volume(os.path.join(outputs_dir, "MyRecon.dat"))
    ref_recon = loader.load_volume(os.path.join(data_dir, "reference", "OSEMReconed.dat"))
    
    my_filt = loader.load_volume(os.path.join(outputs_dir, "MyFiltered.dat"))
    ref_filt = loader.load_volume(os.path.join(data_dir, "reference", "Filtered.dat"))
    
    # Find a good slice (center of mass or max intensity)
    # Usually heart is high intensity
    max_z = np.argmax(np.max(ref_recon, axis=(0, 1)))
    print(f"Detected max intensity slice at Z={max_z}")
    
    # 1. Raw Comparison (Axial)
    os.makedirs(pictures_dir, exist_ok=True)
    save_comparison_plot(my_recon, ref_recon, "Raw Reconstruction", 
                         os.path.join(pictures_dir, "viz_compare_raw_axial.png"), 
                         slice_idx=max_z, axis=2)
                         
    # 2. Filtered Comparison (Axial)
    save_comparison_plot(my_filt, ref_filt, "Filtered Reconstruction", 
                         os.path.join(pictures_dir, "viz_compare_filtered_axial.png"), 
                         slice_idx=max_z, axis=2)
    
    # 3. Orthogonal Views of My Result
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Axial
    axes[0].imshow(my_filt[:, :, max_z], cmap='gray')
    axes[0].set_title(f"Axial (Z={max_z})")
    
    # Coronal (Y)
    max_y = np.argmax(np.max(my_filt, axis=(0, 2)))
    axes[1].imshow(np.rot90(my_filt[:, max_y, :]), cmap='gray') # Rotate for display convention
    axes[1].set_title(f"Coronal (Y={max_y})")
    
    # Sagittal (X)
    max_x = np.argmax(np.max(my_filt, axis=(1, 2)))
    axes[2].imshow(np.rot90(my_filt[max_x, :, :]), cmap='gray')
    axes[2].set_title(f"Sagittal (X={max_x})")
    
    plt.suptitle("My Filtered Result - Orthogonal Views")
    plt.tight_layout()
    plt.savefig(os.path.join(pictures_dir, "viz_ortho_views.png"))
    plt.close()
    print(f"Saved orthogonal views to {os.path.join(pictures_dir, 'viz_ortho_views.png')}")

if __name__ == "__main__":
    main()
