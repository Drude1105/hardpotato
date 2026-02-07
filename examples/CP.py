import hardpotato as hp
import softpotato as sp
import numpy as np

# --- 1. Laboratory Setup ---
# Select your potentiostat model
model = 'chi1205b'

# Path to the CHI software executable
path = r'C:\CHI_Data\chi6273e.exe'

# Folder where to save the data (ensure this directory exists)
folder = r'C:\CHI_Data\GuoZhu'

# Initialization:
hp.potentiostat.Setup(model, path, folder)

# --- 2. Chronopotentiometry (CP) Parameters ---
# Cathodic/Anodic Current and Time
ic = 1e-6       # A, Cathodic current
ia = 0          # A, Anodic current
he = 1
het = 0 
le = -1
let = 0
ct = 10
at = 10
ip = 'p'
ds = 0.1
segment = 1

fileName = 'CP_Test'
header = 'Lab CP Measurement'

# --- 3. Run Experiment ---
# Initialize CP
cp = hp.potentiostat.CP(ic, ia, he, het, le, let, ct, at, ip, fileName, header)

# One-click execution: generates macro -> calls CHI -> runs -> saves
cp.run()

# --- 4. Load and Plot ---
# Load acquired data
data = hp.load_data.CP(fileName + '.txt', folder, model)

# Plot Time vs Potential
sp.plotting.plot(data.t, data.E, xlab='$t$ / s', ylab='$E$ / V', show=1)

print(f"Experiment finished. Data saved in {folder}/{fileName}.txt")
