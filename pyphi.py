import pyphi
import numpy as np
from multiprocessing import Process, freeze_support

pyphi.config.load_file('./config/pyphi_config_l1_bi.yml')
# The tpm or transitio probability matrices 
tpm = np.array([
    [0, 0, 0],
    [0, 0, 1],
    [1, 0, 1],
    [1, 0, 0],
    [1, 1, 0],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 0]
])
# cm or connectivity matrix
cm = np.array([
    [0, 0, 1],
    [1, 0, 1],
    [1, 1, 0]
])
# Labels for the network nodes
labels = ('A', 'B', 'C')
# Network with the arguments
network = pyphi.Network(tpm, node_labels=labels)
# Red status
state = (1, 0, 0)
# All red nodes
node_indices = (0, 1, 2)
# Subsystem for evaluate
subsystem = pyphi.Subsystem(network, state, node_indices)
# 
sia = pyphi.compute.sia(subsystem)

print("MIP: \n", sia.cut)
print("Phi: \n Φ = ", sia.phi)
print("Tiempo: \n", sia.time, "s")
