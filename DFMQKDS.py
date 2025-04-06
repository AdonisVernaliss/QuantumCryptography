import numpy as np
import random
from itertools import combinations
import string


# PRNG for rotation angles
def prng(seed=None):
    if seed is not None:
        random.seed(seed)
    return random.randint(0, 720)


# Set min key length to 5b
def exchange_key_length():
    key_length = prng() % 6 + 5  # key length 5-10 bits
    return key_length


# Pre-set qubit states
def pre_set_qubits(num_qubits):
    states = ['|-⟩', '|+⟩']
    return [(prng(), random.choice(states)) for _ in range(num_qubits)]


# Generate qubits with random angles and states
def generate_qubits(num_qubits):
    states = pre_set_qubits(num_qubits)
    return states


# Process qubits by formatting and applying rotations
def process_qubits(angles_states):
    processed_states = []
    for angle, state in angles_states:
        formatted_state = format_state(angle, state)
        rotated_state = apply_rotation(angle, state)
        processed_states.append({"formatted": formatted_state, "rotated_array": rotated_state})
    return processed_states

# Extract the key by comparing processed states of two nodes
def extract_key(node1_states, node2_states):
    key_bits = []
    for i in range(len(node1_states)):
        p1_formatted, p1_rotated_state = node1_states[i]["formatted"], node1_states[i]["rotated_array"]
        p2_formatted, p2_rotated_state = node2_states[i]["formatted"], node2_states[i]["rotated_array"]

        _, _, _, _, key_bit = calculate_key_bit(p1_rotated_state, p2_rotated_state)
        key_bits.append(key_bit)

    key = ''.join(map(str, key_bits))
    return key


# Apply rotation to a given qubit state based on angle
def apply_rotation(theta_degrees, state):
    theta = np.deg2rad(theta_degrees)

    if state == '|-⟩':
        R = np.array([
            [np.cos(theta / 2), -np.sin(theta / 2)],
            [np.sin(theta / 2), np.cos(theta / 2)]
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


# Format the state representation for readability
def format_state(theta_degrees, state):
    rotated_state = apply_rotation(theta_degrees, state)
    return (
        f"{rotated_state[0]:.4f}|0⟩ + {rotated_state[1]:.4f}|1⟩"
        if rotated_state[1] >= 0
        else f"{rotated_state[0]:.4f}|0⟩ - {abs(rotated_state[1]):.4f}|1⟩"
    )


# Calculate key bit based on qubit states of two nodes
def calculate_key_bit(person1_state, person2_state):
    p1_coeffs = np.abs(person1_state) ** 2
    p2_coeffs = np.abs(person2_state) ** 2

    p1_bit = 1 if p1_coeffs[1] > p1_coeffs[0] else 0
    p2_bit = 1 if p2_coeffs[1] > p2_coeffs[0] else 0

    key_bit = p1_bit ^ p2_bit
    print(f"node1's bit: {p1_bit}, node2's bit: {p2_bit} -> XOR result (Key bit): {key_bit}\n")

    return p1_coeffs[0], p1_coeffs[1], p2_coeffs[0], p2_coeffs[1], key_bit


# Get names for nodes based on alphabet
def get_node_names(num_people):
    alphabet = list(string.ascii_uppercase)
    if num_people <= 26:
        return alphabet[:num_people]
    else:
        names = alphabet[:]
        names += [f"{letter}{i}" for i in range(2, num_people // 26 + 2) for letter in alphabet]
        return names[:num_people]


# Execute QKD protocol for full mesh network
def execute_qkd_protocol_for_full_mesh():
    # Prompt user for number of nodes
    num_people = int(input("Enter the number of nodes in the network (e.g., 5): "))

    # Key lengths output
    key_length = exchange_key_length()
    print(f"Key length: {key_length}")

    # Generate node names
    nodes = get_node_names(num_people)

    # Dictionary to store generated keys for each pair
    keys = {}

    # Iterate through all pairs in a full mesh network
    for p1, p2 in combinations(nodes, 2):
        print(f"\n--- Exchange between {p1} and {p2} ---")

        # Generate key length and qubits for each node
        p1_qubits = generate_qubits(key_length)
        p2_qubits = generate_qubits(key_length)

        # Process qubits
        p1_processed = process_qubits(p1_qubits)
        p2_processed = process_qubits(p2_qubits)

        # Display processed information with improved readability
        print(f"{p1}'s qubits and states: {p1_qubits}")
        print(f"{p1} processed: {p1_processed}\n")

        print(f"{p2}'s qubits and states: {p2_qubits}")
        print(f"{p2} processed: {p2_processed}\n")

        # Extract key for this pair
        key = extract_key(p1_processed, p2_processed)
        keys[(p1, p2)] = key
        print(f"Generated key for {p1} and {p2}: {key}\n")

    # Output of all keys for each pair
    print("\n--- Keys for all node pairs ---")
    for (p1, p2), key in keys.items():
        print(f"Key between {p1} and {p2}: {key}")


# Run full mesh QKD protocol
execute_qkd_protocol_for_full_mesh()