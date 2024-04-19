import random

# Variables
qubit_states = ['|+>', '|->', '|0>', '|1>']
bit_values = ['0', '1']
measurements = ['X', 'Z']
x_basis_measurements = ['|+>', '|->']
z_basis_measurements = ['|0>', '|1>']

def generate_qubit_sequence(length):
    return [random.choice(qubit_states) for _ in range(length)]

def generate_measurement_sequence(length):
    return [random.choice(measurements) for _ in range(length)]

def convert_qubit_to_bit(qubit_seq):
    return ['1' if qubit in ['|+>', '|1>'] else '0' for qubit in qubit_seq]

def measure_qubits(qubit_seq, measurement_seq):
    result_qubit_seq = []

    for qubit, measurement in zip(qubit_seq, measurement_seq):
        if (qubit == '|->' and measurement == 'X') or (qubit == '|+>' and measurement == 'X') or \
           (qubit == '|0>' and measurement == 'Z') or (qubit == '|1>' and measurement == 'Z'):
            result_qubit_seq.append(qubit)
        else:
            result_qubit_seq.append(random.choice(x_basis_measurements if measurement == 'X' else z_basis_measurements))

    return result_qubit_seq

def alice_determine_correct_measurements(alice_qubit_seq, bob_measurement_seq):
    correct_indices = []

    for i, (alice_qubit, bob_measurement) in enumerate(zip(alice_qubit_seq, bob_measurement_seq)):
        if (alice_qubit in x_basis_measurements and bob_measurement == 'X') or \
           (alice_qubit in z_basis_measurements and bob_measurement == 'Z'):
            correct_indices.append(i)

    return correct_indices

def extract_key(correct_indices, bit_seq):
    return ''.join([bit_seq[i] for i in correct_indices])

def calculate_error_rate(key1, key2):
    return sum(1 for k1, k2 in zip(key1, key2) if k1 != k2) / len(key1)

def simulate_eve():
    choice = input("Would you like to simulate Eve's actions? (yes/no): ").lower()
    return choice == 'yes'

# Simulation
def intercept_qubits(qubit_seq, simulate_eve):
    intercepted_seq = []
    if simulate_eve:
        for qubit in qubit_seq:
            if random.random() < 0.5:  # 50%
                new_state = '|1>' if qubit in ['|0>', '|1>'] else '|0>'
                intercepted_seq.append(new_state)
                print("Eve has altered a qubit.")
            else:
                intercepted_seq.append(qubit)
        print("Eve has intercepted the qubits.")
    else:
        intercepted_seq = qubit_seq
    return intercepted_seq

def run_bb84_protocol(qubit_length):
    alice_qubit_seq = generate_qubit_sequence(qubit_length)
    alice_bit_seq = convert_qubit_to_bit(alice_qubit_seq)

    simulate_eve_flag = simulate_eve()
    eve_qubit_seq = intercept_qubits(alice_qubit_seq, simulate_eve_flag)

    bob_measurement_seq = generate_measurement_sequence(qubit_length)
    bob_qubit_seq = measure_qubits(eve_qubit_seq, bob_measurement_seq)
    bob_bit_seq = convert_qubit_to_bit(bob_qubit_seq)

    correct_measurements = alice_determine_correct_measurements(alice_qubit_seq, bob_measurement_seq)

    bob_key = extract_key(correct_measurements, bob_bit_seq)
    alice_key = extract_key(correct_measurements, alice_bit_seq)

    if len(bob_key) == 0 or len(alice_key) == 0:
        error_rate = 1.0
    else:
        error_rate = calculate_error_rate(bob_key, alice_key)

    print('Alice\'s prepared qubit sequence:', alice_qubit_seq)
    print('Alice\'s bit sequence:', alice_bit_seq)
    print('Eve\'s intercepted qubit sequence:', eve_qubit_seq)
    print('Bob\'s measurement basis sequence:', bob_measurement_seq)
    print('Bob\'s measured qubit sequence:', bob_qubit_seq)
    print('Correct indices:', correct_measurements)
    print('Bob\'s key:', bob_key)
    print('Alice\'s key:', alice_key)
    print('Error rate:', error_rate)

    return error_rate

if __name__ == '__main__':
    qubit_length = int(input('Please enter the length of the set of polarized photons prepared by Alice: '))
    error_rate = run_bb84_protocol(qubit_length)