import hardpotato as hp
import softpotato as sp
import hardpotato.batch.CP_sweep as cp_batch
import numpy as np

# --- 1. Laboratory Setup ---
model = 'chi1205b'
path = r'C:\CHI_Data\chi6273e.exe'
folder = r'C:\CHI_Data\GuoZhu'

# Initialization:
hp.potentiostat.Setup(model, path, folder)

# --- 2. Define Batch Sweep Parameters ---
# Sweep Cathodic Current (A)
ic_vals = np.array([1e-6, 5e-6, 1e-5])
ia_vals = np.array([0.0, 1e-6, 2e-6])      
segments = np.array([2, 5, 10])

# Shared parameters for all runs in the sweep
eh = 1.0        # High E Limit
el = -1.0       # Low E Limit
tc = 10         # s, Cathodic time
ta = 10         # s, Anodic time

# --- 3. Initialize and Run Batch Sweep ---
print("--- Starting CP Batch Sweep ---")
# Initialize CPSweep class with sweep arrays and shared parameters
cp_sweep = cp_batch.CPSweep(
    ic_array=ic_vals, 
    ia_array=ia_vals, 
    segments_array=segments,
    eh=eh, el=el, tc=tc, ta=ta
)

# Run the batch loop: for each k, generate CP_k.mcr -> run -> save -> load
results = cp_sweep.run()

# --- 4. Plot All Results ---
cp_sweep.plot_all()

print("Batch sweep finished.")
