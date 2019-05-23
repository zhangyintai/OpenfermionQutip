# Coding by Yintai Zhang @ School of Physical Sciences,
# University of Science and Techology of China

# COMMERCIAL USES ARE STRICTLY PROHIBITED.

import qutip
import openfermion

# Generate certain Pauli Operator according to the input
def to_pauli(s):

    # Input format:
        # s: take value from 'X', 'Y', 'Z', '+' and '-'
    # Return:
        # Pauli-X, Pauli-Y, Pauli-Z, flip-up or flip-down, according to the input

    if s == 'X':
        return qutip.sigmax()
    elif s == 'Y':
        return qutip.sigmay()
    elif s == 'Z':
        return qutip.sigmaz()
    elif s == '+':
        return qutip.sigmap()
    elif s == '-':
        return qutip.sigmam()
    else:
        return qutip.qeye(2) # For unidentified input, return identity

# Transform an operator calculated by OpenFermion after applying a certian tranform (J-W or B-K) to the operator for QuTiP
# The operator should have a form of the sum of some multiplications
def to_qutip(Opt, n_qubit):

    # Input format:
        # Opt: the operator calculated by OpenFermion, with certain format
        # n_qubit: the number of qubits that are used to encode the orbits
    # Return:
        # The operator of QuTiP
    n_max = n_qubit - 1 # index start with zero

    Opt_string = str(Opt) # Transform the operator in OpenFermion to string
    opt_list = Opt_string.split(sep = ' +\n') # separate multiplications from the sum

    s = 0

    for opts in opt_list:

        temp = opts.split(' ', 1)
        coef = complex(temp[0]) # Acquire coefficients from the multiplication

        ss = coef # ss is used to store the operator for QuTiP of the multiplication
        pauli_opts = temp[1][1 : len(temp[1]) - 1].split(' ')  #Acquire Pauli operators from the multiplication

        pauli_opt_list = [] # Store Pauli operators for each qubits.
        
        for i in range(0, n_qubit):
            pauli_opt_list.append([])
        
        if pauli_opts != ['']:
            for pauli_opt in pauli_opts:
                pauli_index = int(pauli_opt[1:])
                pauli_opt_list[pauli_index].append(to_pauli(pauli_opt[0]))
        
        
        for i in range(0, n_qubit):
            if pauli_opt_list[i] == []: # If there is no Pauli operator for such qubit, set the operator in this Hilbert subspace to identity
                try:
                    ss = qutip.tensor(ss, qutip.qeye(2))
                except:
                    ss = ss * qutip.qeye(2)
            else:
                for pauli_opt in pauli_opt_list[i]:
                    try:
                        ss = qutip.tensor(ss, pauli_opt)
                    except:
                        ss = ss * pauli_opt
        
        s = s + ss # Sum up the operator
    
    return s