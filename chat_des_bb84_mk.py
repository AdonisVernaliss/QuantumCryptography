import asyncio, random
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import run_async, run_js

# Initial Permutation Table
initial_perm = [58, 50, 42, 34, 26, 18, 10, 2,
                60, 52, 44, 36, 28, 20, 12, 4,
                62, 54, 46, 38, 30, 22, 14, 6,
                64, 56, 48, 40, 32, 24, 16, 8,
                57, 49, 41, 33, 25, 17, 9, 1,
                59, 51, 43, 35, 27, 19, 11, 3,
                61, 53, 45, 37, 29, 21, 13, 5,
                63, 55, 47, 39, 31, 23, 15, 7]

# Expansion D-box Table
exp_d = [32, 1, 2, 3, 4, 5, 4, 5,
         6, 7, 8, 9, 8, 9, 10, 11,
         12, 13, 12, 13, 14, 15, 16, 17,
         16, 17, 18, 19, 20, 21, 20, 21,
         22, 23, 24, 25, 24, 25, 26, 27,
         28, 29, 28, 29, 30, 31, 32, 1]

# Straight Permutation Table
per = [16, 7, 20, 21,
       29, 12, 28, 17,
       1, 15, 23, 26,
       5, 18, 31, 10,
       2, 8, 24, 14,
       32, 27, 3, 9,
       19, 13, 30, 6,
       22, 11, 4, 25]

# S-box Table
sbox = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

# Final Permutation Table
final_perm = [40, 8, 48, 16, 56, 24, 64, 32,
              39, 7, 47, 15, 55, 23, 63, 31,
              38, 6, 46, 14, 54, 22, 62, 30,
              37, 5, 45, 13, 53, 21, 61, 29,
              36, 4, 44, 12, 52, 20, 60, 28,
              35, 3, 43, 11, 51, 19, 59, 27,
              34, 2, 42, 10, 50, 18, 58, 26,
              33, 1, 41, 9, 49, 17, 57, 25]

# Keys table

# Bit drop table
keyp = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4]

# Number of bit shifts
shift_table = [1, 1, 2, 2,
               2, 2, 2, 2,
               1, 2, 2, 2,
               2, 2, 2, 1]

# Compression Table
key_comp = [14, 17, 11, 24, 1, 5,
            3, 28, 15, 6, 21, 10,
            23, 19, 12, 4, 26, 8,
            16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55,
            30, 40, 51, 45, 33, 48,
            44, 49, 39, 56, 34, 53,
            46, 42, 50, 36, 29, 32]

chat_msgs = []
online_users = set()

qubit_states = ['|+>', '|->', '|0>', '|1>']
bit_values = ['0', '1']
measurements = ['X', 'Z']
x_basis_measurements = ['|+>', '|->']
z_basis_measurements = ['|0>', '|1>']

MAX_MESSAGES_COUNT = 150

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
    if len(key1) == 0 or len(key2) == 0:
        return 1.0
    else:
        return sum(1 for k1, k2 in zip(key1, key2) if k1 != k2) / max(len(key1), len(key2))


def simulate_eve():
    pass

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

    if bob_key == alice_key:
        master_key = bob_key
        error_rate = calculate_error_rate(bob_key, alice_key)
    else:
        master_key = None
        error_rate = 1.0
        print("Eavesdropping detected. Key discarded.")

    print('Alice\'s prepared qubit sequence:', alice_qubit_seq)
    print('Alice\'s bit sequence:', alice_bit_seq)
    print('Eve\'s intercepted qubit sequence:', eve_qubit_seq)
    print('Bob\'s measurement basis sequence:', bob_measurement_seq)
    print('Bob\'s measured qubit sequence:', bob_qubit_seq)
    print('Correct indices:', correct_measurements)
    print('Bob\'s key:', bob_key)
    print('Alice\'s key:', alice_key)
    print('Master key:', master_key)
    print('Error rate:', error_rate)

    return error_rate, master_key

############################################################################################################

def hex2bin(s):
    if not s:
        return ""  # Return an empty string if s is empty
    return bin(int(s, 16))[2:].zfill(len(s) * 4)


def bin2hex(s):
    if not s:
        return ""  # Return an empty string if s is empty
    return hex(int(s, 2))[2:]


def bin2dec(binary):
    return int(str(binary), 2)


def dec2bin(num):
    return bin(num)[2:].zfill(4)


def permute(k, arr, n):
    permutation = ""
    for i in range(0, n):
        permutation = permutation + k[arr[i] - 1]
    return permutation


def shift_left(k, nth_shifts):
    return k[nth_shifts:] + k[:nth_shifts]


def xor(a, b):
    ans = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            ans = ans + "0"
        else:
            ans = ans + "1"
    return ans


def encrypt(pt, rkb, rk):
    pt = hex2bin(pt)

    while len(pt) % 64 != 0:
        pt += '0'

    cipher_text = ''
    for block_start in range(0, len(pt), 64):
        block = pt[block_start:block_start + 64]

        block = permute(block, initial_perm, 64)
        print("IP:", bin2hex(block))

        left = block[0:32]
        right = block[32:64]
        for i in range(0, 16):
            right_expanded = permute(right, exp_d, 48)

            xor_x = xor(right_expanded, rkb[i])

            sbox_str = ""
            for j in range(0, 8):
                row = bin2dec(int(xor_x[j * 6] + xor_x[j * 6 + 5]))
                col = bin2dec(
                    int(xor_x[j * 6 + 1] + xor_x[j * 6 + 2] + xor_x[j * 6 + 3] + xor_x[j * 6 + 4]))
                val = sbox[j][row][col]
                sbox_str = sbox_str + dec2bin(val)

            sbox_str = permute(sbox_str, per, 32)

            result = xor(left, sbox_str)
            left = result

            if (i != 15):
                left, right = right, left
            print("Round ", i + 1, " ", bin2hex(left),
                  " ", bin2hex(right), " ", rk[i])

        combine = left + right

        cipher_block = permute(combine, final_perm, 64)
        cipher_text += cipher_block

    return cipher_text


async def main():
    global chat_msgs

    msg_box = output()
    put_scrollable(msg_box, height=300, keep_bottom=True)

    nickname = await input(required=True, placeholder="Your name:",
                           validate=lambda
                               n: "Nickname's already in use." if n in online_users or n == '[INFO]' else None)
    online_users.add(nickname)

    chat_msgs.append(('[INFO]', f'`{nickname}` joined.'))
    msg_box.append(put_markdown(f'[INFO] `{nickname}` join the chat'))

    refresh_task = run_async(refresh_msg(nickname, msg_box))

    while True:
        data = await input_group("| Internet Relay Chat |", [
            file_upload(accept='.txt,.pdf,.doc', name='file', help_text='Choose a file (txt, pdf, doc)'),
            input(placeholder="...", name="msg"),
            actions(name="cmd", buttons=["Send", {'label': "Log out", 'type': 'cancel'}])
        ], validate=lambda m: ('msg', "Enter the message") if m["cmd"] == "Send" and not m['msg'] and not m[
            'file'] else None)

        if data is None:
            break

        # Process file if uploaded
        file_content = ""
        if 'file' in data and data['file']:
            file_content = data['file']['content'].decode('latin-1')
            encrypted_file = bin2hex(encrypt(file_content.encode().hex(), rkb, rk))
            msg_box.append(put_markdown(f"`{nickname}` (Encrypted File): {encrypted_file}"))
            chat_msgs.append((nickname, encrypted_file))

        # Process text message if provided
        if 'msg' in data:
            encrypted_msg = bin2hex(encrypt(data['msg'].encode().hex(), rkb, rk))
            msg_box.append(put_markdown(f"`{nickname}` (Encrypted): {encrypted_msg} ({data['msg']})"))
            chat_msgs.append((nickname, encrypted_msg))

    refresh_task.close()

    online_users.remove(nickname)
    toast("You have logged out of the chat.")
    msg_box.append(put_markdown(f'[INFO] User `{nickname}` left the chat.'))
    chat_msgs.append(('[INFO]', f'User `{nickname}` left the chat.'))

    put_buttons(['Re-visit'], onclick=lambda btn: run_js('window.location.reload()'))


async def refresh_msg(nickname, msg_box):
    global chat_msgs
    last_idx = len(chat_msgs)

    while True:
        await asyncio.sleep(1)

        for m in chat_msgs[last_idx:]:
            if m[0] != nickname:  # if not a message from the current user
                if all(c in "0123456789ABCDEFabcdef" for c in m[1]):
                    decrypted_msg = bytes.fromhex(bin2hex(encrypt(m[1], rkb[::-1], rk[::-1]))).decode('latin-1')
                    msg_box.append(put_markdown(f"`{m[0]}` (Decrypted): {decrypted_msg}"))
                else:
                    msg_box.append(put_markdown(f"`{m[0]}`: {m[1]}"))

        # remove expired
        if len(chat_msgs) > MAX_MESSAGES_COUNT:
            chat_msgs = chat_msgs[len(chat_msgs) // 2:]

        last_idx = len(chat_msgs)


if __name__ == "__main__":
    key = str(run_bb84_protocol(50)[1])
    key = key.ljust(64, '0') if len(key) < 64 else key[:64]
    key = permute(key, keyp, 56)

    left = key[0:28]
    right = key[28:56]

    rkb = []
    rk = []
    for i in range(0, 16):
        left = shift_left(left, shift_table[i])
        right = shift_left(right, shift_table[i])

        combine_str = left + right
        round_key = permute(combine_str, key_comp, 48)

        rkb.append(round_key)
        rk.append(bin2hex(round_key))

    start_server(main, debug=True, port=8080, cdn=False)