import hardpotato as hp
import softpotato as sp
import numpy as np

# --- 1. Laboratory Setup ---
# Select your potentiostat model
model = 'chi1205b'

# Path to the CHI software executable
path = 'C:/CHI/chi1205b.exe'

# Folder where to save the data (ensure this directory exists)
folder = 'C:/hardpotato_data'

# Initialization:
hp.potentiostat.Setup(model, path, folder)

# --- 2. Chronopotentiometry (CP) Parameters ---
# Cathodic/Anodic Current and Time
ic = 1e-6       # A, Cathodic current
ia = 0          # A, Anodic current
tc = 10         # s, Cathodic time
ta = 10         # s, Anodic time

# Potential Limits
eh = 1.0        # V, High E Limit
el = -1.0       # V, Low E Limit

# Cycles and Interval
cl = 2          # Number of segments
si = 0.1        # s, Data storage interval
sens = 1e-6     # Current sensitivity

fileName = 'CP_Test'
header = 'Lab CP Measurement'

# --- 3. Run Experiment ---
# Initialize CP
cp = hp.potentiostat.CP(ic, ia, eh, el, tc, ta, cl, si, sens, fileName, header)

# One-click execution: generates macro -> calls CHI -> runs -> saves
cp.run()

# --- 4. Load and Plot ---
# Load acquired data
data = hp.load_data.CP(fileName + '.txt', folder, model)

# Plot Time vs Potential
sp.plotting.plot(data.t, data.E, xlab='$t$ / s', ylab='$E$ / V', show=1)

print(f"Experiment finished. Data saved in {folder}/{fileName}.txt")
