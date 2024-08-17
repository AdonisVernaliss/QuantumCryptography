import numpy as np

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
    alice_coeffs = np.abs(alice_state)**2
    bob_coeffs = np.abs(bob_state)**2
    
    global alice_bit, bob_bit
    
    alice_bit = 1 if alice_coeffs[1] > alice_coeffs[0] else 0
    bob_bit = 1 if bob_coeffs[1] > bob_coeffs[0] else 0
    
    key_bit = alice_bit ^ bob_bit
    return alice_coeffs[0], alice_coeffs[1], bob_coeffs[0], bob_coeffs[1], key_bit

def print_grouped_states_and_key(angles_states):
    alice_bits = angles_states[:5]
    bob_bits = angles_states[5:]
    
    key_bits = []
    outputs = []

    for i in range(len(alice_bits)):
        alice_angle, alice_state = alice_bits[i]
        bob_angle, bob_state = bob_bits[i]
        
        alice_formatted = format_state(alice_angle, alice_state)
        bob_formatted = format_state(bob_angle, bob_state)
        
        alice_rotated_state = apply_rotation(alice_angle, alice_state)
        bob_rotated_state = apply_rotation(bob_angle, bob_state)
        
        alice_coeffs_0, alice_coeffs_1, bob_coeffs_0, bob_coeffs_1, key_bit = calculate_key_bit(
            alice_rotated_state, bob_rotated_state)
        
        output = (
            f"(Alice's bits) - {alice_angle}°{alice_state}: {alice_formatted}   |   "
            f"(Bob's bits) - {bob_angle}°{bob_state}: {bob_formatted}\n"
            f"{alice_coeffs_0:.4f}^2 vs {alice_coeffs_1:.4f}^2 = {alice_coeffs_1:.4f}^2 > {alice_coeffs_0:.4f}^2 -> {alice_bit}   |   "
            f"{bob_coeffs_0:.4f}^2 vs {bob_coeffs_1:.4f}^2 = {bob_coeffs_0:.4f}^2 > {bob_coeffs_1:.4f}^2 -> {bob_bit}\n"
            f"{alice_bit}^ {bob_bit} = {key_bit}"
        )
        outputs.append(output)
        key_bits.append(key_bit)
    
    for output in outputs:
        print(output)
    
    key = ''.join(map(str, key_bits))
    print(f"Generated key: {key}")

angles_states = [
    (571, '|-⟩'),
    (496, '|+⟩'),
    (705, '|+⟩'),
    (54, '|-⟩'),
    (114, '|-⟩'),
    (624, '|+⟩'),
    (324, '|-⟩'),
    (669, '|+⟩'),
    (517, '|-⟩'),
    (568, '|+⟩')
]

print_grouped_states_and_key(angles_states)