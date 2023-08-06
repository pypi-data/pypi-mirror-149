import sys

sys.path.insert(0, "../")

import numpy as np
import tensorcircuit as tc

print(tc.gates.x().tensor)

# or an equivalent way
n = 1  # single qubit gate
c = tc.Circuit(n, inputs=np.eye(2**n))
c.x(0)
print(c.state().reshape([2**n, 2**n]))  # get the circuit unitary
n = 2  # two-qubit gate
c = tc.Circuit(n, inputs=np.eye(2**n))
c.cnot(0, 1)
print(c.state().reshape([2**n, 2**n]))  # get the circuit unitary
