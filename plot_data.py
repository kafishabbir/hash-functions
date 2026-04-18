import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil

def create_plots(df, figures_subdir, title_suffix=""):
    """Create individual and combined plots for a given dataframe"""
    
    # Get unique values
    lengths = sorted(df['length_string'].unique())
    hash_names = sorted(df['hash_name'].unique())
    
    # Use default matplotlib color cycle
    default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    color_dict = {hash_name: default_colors[i % len(default_colors)] 
                  for i, hash_name in enumerate(hash_names)}
    
    # Different line thicknesses for different lengths
    thickness_dict = {length: 1.5 + (i * 0.3) for i, length in enumerate(lengths)}
    
    # Different alpha (transparency) values for different lengths
    alpha_dict = {length: 0.6 + (i * 0.1) for i, length in enumerate(lengths)}
    
    # ========== PART 1: Individual plots for each length ==========
    print(f"  Generating individual plots for each string length...")
    for length in lengths:
        # Filter data for current length
        df_length = df[df['length_string'] == length]
        
        # Find appropriate y-axis scale for this specific plot
        y_max_local = df_length['collision_proportion'].max()
        y_min_local = df_length['collision_proportion'].min()
        # Add 10% padding at the top, start from 0 or slightly below min if needed
        y_top = y_max_local + (y_max_local * 0.1) if y_max_local > 0 else 0.1
        y_bottom = 0  # Start from 0
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 7))
        
        # Plot each hash function as a separate line (no points)
        for hash_name in hash_names:
            df_hash = df_length[df_length['hash_name'] == hash_name]
            if not df_hash.empty:
                ax.plot(df_hash['number_strings'], 
                       df_hash['collision_proportion'], 
                       linewidth=2.5,
                       label=hash_name,
                       color=color_dict[hash_name])
        
        # Customize the plot
        ax.set_xlabel('Number of Strings', fontsize=12, fontweight='bold')
        ax.set_ylabel('Collision Proportion', fontsize=12, fontweight='bold')
        ax.set_title(f'Hash Function Collision Performance\nString Length = {length}{title_suffix}', 
                    fontsize=14, fontweight='bold')
        
        # Add grid
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # Set appropriate axes limits for this specific plot
        x_max = df_length['number_strings'].max()
        ax.set_xlim(0, x_max + (x_max * 0.05) if x_max > 0 else 5)
        ax.set_ylim(y_bottom, y_top)
        
        # Add legend
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10, 
                 framealpha=0.9, edgecolor='black')
        
        # Visual enhancements
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Adjust layout
        plt.tight_layout()
        
        # Save the plot
        plt.savefig(os.path.join(figures_subdir, f'collision_plot_length_{length}.png'), 
                    dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"    ✓ Saved: collision_plot_length_{length}.png (y-axis: 0 to {y_top:.4f})")
    
    # ========== PART 2: Combined plot with all lengths ==========
    print(f"  Generating combined plot with all lengths...")
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Find appropriate y-axis scale for combined plot
    y_max_combined = df['collision_proportion'].max()
    y_top_combined = y_max_combined + (y_max_combined * 0.1) if y_max_combined > 0 else 0.1
    
    # Plot each hash function with different thickness/alpha for each length (no points)
    for hash_name in hash_names:
        for length in lengths:
            # Filter data for current hash and length
            df_subset = df[(df['hash_name'] == hash_name) & (df['length_string'] == length)]
            
            if not df_subset.empty:
                # Create label for legend
                label = f"{hash_name} (len={length})"
                
                # Plot with continuous line, varying thickness and alpha (no markers)
                ax.plot(df_subset['number_strings'], 
                       df_subset['collision_proportion'], 
                       linewidth=thickness_dict[length],
                       alpha=alpha_dict[length],
                       color=color_dict[hash_name],
                       label=label)
    
    # Customize the combined plot
    ax.set_xlabel('Number of Strings', fontsize=12, fontweight='bold')
    ax.set_ylabel('Collision Proportion', fontsize=12, fontweight='bold')
    ax.set_title(f'Hash Function Collision Performance Across All String Lengths\n(Same color = same hash, thickness/darkness = string length){title_suffix}', 
                fontsize=14, fontweight='bold')
    
    # Add grid
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Set appropriate axes limits for combined plot
    x_max_combined = df['number_strings'].max()
    ax.set_xlim(0, x_max_combined + (x_max_combined * 0.05))
    ax.set_ylim(0, y_top_combined)
    
    # Place legend outside the plot with 2 columns
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9, 
             framealpha=0.9, edgecolor='black', ncol=2)
    
    # Visual enhancements
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the combined plot
    plt.savefig(os.path.join(figures_subdir, 'collision_plot_all_lengths_combined.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"    ✓ Saved: collision_plot_all_lengths_combined.png (y-axis: 0 to {y_top_combined:.4f})")
    
    return len(lengths)

# ========== MAIN PROGRAM ==========

# Create main figures directory and clear it
main_figures_dir = 'figures'
if os.path.exists(main_figures_dir):
    shutil.rmtree(main_figures_dir)
os.makedirs(main_figures_dir)
print(f"Created fresh directory: {main_figures_dir}/\n")

# Read the data
df = pd.read_csv('data.txt', sep='\t')

# ========== SET 1: All hash functions ==========
print("="*60)
print("SET 1: Generating plots with ALL hash functions")
print("="*60)

# Create subdirectory for set 1
set1_dir = os.path.join(main_figures_dir, 'with_all_hash_functions')
os.makedirs(set1_dir)
print(f"Created: {set1_dir}/")

# Generate plots for all hash functions
create_plots(df, set1_dir, " (All Hash Functions)")

# ========== SET 2: Without PJW and ELF ==========
print("\n" + "="*60)
print("SET 2: Generating plots WITHOUT PJW and ELF hash functions")
print("="*60)

# Remove PJW and ELF from the dataset
df_without_pjw_elf = df[~df['hash_name'].isin(['PJW', 'ELF'])].copy()

# Create subdirectory for set 2
set2_dir = os.path.join(main_figures_dir, 'without_pjw_elf')
os.makedirs(set2_dir)
print(f"Created: {set2_dir}/")

# Generate plots without PJW and ELF
create_plots(df_without_pjw_elf, set2_dir, " (Without PJW & ELF)")

# ========== Summary ==========
print("\n" + "="*60)
print("FINAL SUMMARY")
print("="*60)
print(f"✓ All plots saved in: {main_figures_dir}/")
print(f"  ├── with_all_hash_functions/  (all hash functions including PJW & ELF)")
print(f"  └── without_pjw_elf/          (all hash functions except PJW & ELF)")
print(f"\nEach subfolder contains:")
print(f"  • Individual plots per string length (each with its own appropriate y-axis scale)")
print(f"  • One combined plot with all lengths")
print(f"\nKey features:")
print(f"  • NO points - just clean lines")
print(f"  • Default matplotlib colors (orange, blue, red, green, etc.)")
print(f"  • Different lengths have slightly different line thickness")
print(f"  • Different lengths have different transparency/darkness")
print(f"  • Same hash function has same color across all plots")
print(f"  • Y-axis starts at 0 for all plots")
print(f"  • Each plot has its OWN appropriate y-axis scale (not forced global max)")
