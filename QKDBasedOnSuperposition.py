import numpy as np
import random

# prng for corners
def prng(seed=None):
    if seed is not None:
        random.seed(seed)
    return random.randint(0, 720)


# classic channel
def exchange_key_length():
    key_length = prng() % 10 + 1  # key length 1-10
    print(f"Key length agreed upon by Alice and Bob: {key_length} bits")
    return key_length


# pre set qubits stations
def pre_set_qubits(num_qubits):
    states = ['|-⟩', '|+⟩']
    return [(prng(), random.choice(states)) for _ in range(num_qubits)]


# generation qubits
def generate_qubits(num_qubits):
    states = pre_set_qubits(num_qubits)
    return states


# qubit transmissions (qubit processing)
def process_qubits(angles_states):
    processed_states = []
    for angle, state in angles_states:
        formatted_state = format_state(angle, state)
        rotated_state = apply_rotation(angle, state)
        processed_states.append((formatted_state, rotated_state))
    return processed_states


# extracting key
def extract_key(alice_states, bob_states):
    key_bits = []
    for i in range(len(alice_states)):
        alice_formatted, alice_rotated_state = alice_states[i]
        bob_formatted, bob_rotated_state = bob_states[i]

        alice_coeffs_0, alice_coeffs_1, bob_coeffs_0, bob_coeffs_1, key_bit = calculate_key_bit(
            alice_rotated_state, bob_rotated_state)

        key_bits.append(key_bit)

    key = ''.join(map(str, key_bits))
    return key


# rotation
def apply_rotation(theta_degrees, state):
    theta = np.deg2rad(theta_degrees)

    if state == '|-⟩':
        R = np.array([
            [np.cos(theta / 2), -np.sin(theta / 2)],
            [-np.cos(theta / 2), -np.sin(theta / 2)],
            [np.cos(theta / 2), np.sin(theta / 2)]
        ])
        initial_state = np.array([1 / np.sqrt(2), 1 / np.sqrt(2)])
    elif state == '|+⟩':
        R = np.array([
            [np.cos(theta / 2), -np.sin(theta / 2)],
            [np.cos(theta / 2), np.sin(theta / 2)]
        ])
        initial_state = np.array([1 / np.sqrt(2), 1 / np.sqrt(2)])
    else:
        raise ValueError("Invalid state. Choose '|-⟩' or '|+⟩'.")

    rotated_state = np.dot(R, initial_state)
    return rotated_state


def format_state(theta_degrees, state):
    rotated_state = apply_rotation(theta_degrees, state)
    return (
        f"{rotated_state[0]:.4f}|0⟩ + {rotated_state[1]:.4f}|1⟩"
        if rotated_state[1] >= 0
        else f"{rotated_state[0]:.4f}|0⟩ - {abs(rotated_state[1]):.4f}|1⟩"
    )

def calculate_key_bit(alice_state, bob_state):
    alice_coeffs = np.abs(alice_state) ** 2
    bob_coeffs = np.abs(bob_state) ** 2

    global alice_bit, bob_bit

    alice_bit = 1 if alice_coeffs[1] > alice_coeffs[0] else 0
    bob_bit = 1 if bob_coeffs[1] > bob_coeffs[0] else 0

    key_bit = alice_bit ^ bob_bit
    print(f"Alice's bit: {alice_bit}, Bob's bit: {bob_bit} -> XOR result (Key bit): {key_bit}\n")

    return alice_coeffs[0], alice_coeffs[1], bob_coeffs[0], bob_coeffs[1], key_bit

def execute_qkd_protocol():
    # key exchange
    key_length = exchange_key_length()

    # generated own qubits
    alice_qubits = generate_qubits(key_length)
    bob_qubits = generate_qubits(key_length)

    # qubit transmission
    alice_processed = process_qubits(alice_qubits)
    bob_processed = process_qubits(bob_qubits)

    # oUTPUT
    print(f"Alice's qubits and states: {alice_qubits}")
    print(f"Alice processed: {alice_processed}\n")

    print(f"Bob's qubits and states: {bob_qubits}")
    print(f"Bob processed: {bob_processed}\n")



    # key extracting
    key = extract_key(alice_processed, bob_processed)


    print("Generated key:", key)

execute_qkd_protocol()
