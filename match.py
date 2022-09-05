import pyfirmata
import time

board = pyfirmata.Arduino('/dev/ttyAMC0')

it = pyfirmata.util.Iterator(board)
it.start()

# Get pin handles
left_pins = [ board.get_pin(f'd:{i}:i') for i in range(0, 4) ]
right_pins = [ board.get_pin(f'd:{i}:i') for i in range(4, 8) ]
out_pin = [ board.get_pin(f'd:{i}:o') for i in range(12, 14) ]
out_cached = [0, 0]

# Match table
ans = { 0:3, 1:0, 2:1, 3:2 }

def write_output(out_list):
    for i, (a, b) in enumerate(zip(out_list, out_cached)):
        if a != b:
            out_pin[i].write(a)
            out_cached[i] = a

while True:
    # Get left, right and out pins values
    left = [ left_pins[i].read() for i in range(0, 4) ]
    right = [ right_pins[i].read() for i in range(4, 8) ]
    print(f'Left pin values: {left}')
    print(f'Right pin values: {right}')

    if not any(left) and not any(right):
        write_output([0, 0])
        time.sleep(0.1)
        continue
        
    # Get the pressed pin index
    a = [ i for i, v in enumerate(left) if v == True ]
    b = [ i for i, v in enumerate(right) if v == True ]
    a = a[0]
    b = b[0]

    match = True if b == ans[a] else False

    if match is True:
        print(f'Match: True {a}:{b}')
    else:
        print(f'Match: False {a}:{b}')

    out_list = [1, 0] if match is True else [0, 1]

    time.sleep(0.1)
