from computer import Computer

def test_day2_1():
    program = [1,0,0,0,99]

    computer = Computer(program)
    computer.run()
    assert computer.state.mem[:len(program)] == [2,0,0,0,99]

def test_day2_2():
    program = [2,3,0,3,99]

    computer = Computer(program)
    computer.run()
    assert computer.state.mem[:len(program)] == [2,3,0,6,99]

def test_day2_3():
    program = [2,4,4,5,99,0]

    computer = Computer(program)
    computer.run()
    assert computer.state.mem[:len(program)] == [2,4,4,5,99,9801]

def test_day2_4():
    program = [1,1,1,4,99,5,6,0,99]

    computer = Computer(program)
    computer.run()
    assert computer.state.mem[:len(program)] == [30,1,1,4,2,5,6,0,99]

def test_day2_5():
    program = [1,9,10,3,2,3,11,0,99,30,40,50]

    computer = Computer(program)
    computer.run()
    assert computer.state.mem[:len(program)] == [3500,9,10,70,2,3,11,0,99,30,40,50]

def test_day2_6():
    program = [3,9,8,9,10,9,4,9,99,-1,8]

    for i, out in [(7, 0), (8, 1), (9, 0)]:
        computer = Computer(program)
        computer.add_input(i)
        computer.run()
        assert computer.state.outputs[-1] == out

def test_day5_1():
    """Using position mode, consider whether the input is 
    equal to 8; output 1 (if it is) or 0 (if it is not)."""
    program = [3,9,8,9,10,9,4,9,99,-1,8]

    for i, out in [(7, 0), (8, 1), (9, 0)]:
        computer = Computer(program)
        computer.add_input(i)
        computer.run()
        assert computer.state.outputs[-1] == out

def test_day5_2():
    """Using position mode, consider whether the input is 
    less than 8; output 1 (if it is) or 0 (if it is not)."""
    program = [3,9,7,9,10,9,4,9,99,-1,8]

    for i, out in [(7, 1), (8, 0), (9, 0)]:
        computer = Computer(program)
        computer.add_input(i)
        computer.run()
        assert computer.state.outputs[-1] == out

def test_day5_3():
    """Using immediate mode, consider whether the input is 
    equal to 8; output 1 (if it is) or 0 (if it is not)."""
    program = [3,3,1108,-1,8,3,4,3,99] 

    for i, out in [(7, 0), (8, 1), (9, 0)]:
        computer = Computer(program)
        computer.add_input(i)
        computer.run()
        assert computer.state.outputs[-1] == out

def test_day5_4():
    """Using immediate mode, consider whether the input is 
    less than 8; output 1 (if it is) or 0 (if it is not)."""
    program = [3,3,1107,-1,8,3,4,3,99]

    for i, out in [(7, 1), (8, 0), (9, 0)]:
        computer = Computer(program)
        computer.add_input(i)
        computer.run()
        assert computer.state.outputs[-1] == out


def test_day5_5():
    """Here are some jump tests that take an input, then output 0 if 
    the input was zero or 1 if the input was non-zero"""
    program = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]

    for i, out in [(-1, 1), (0, 0), (1, 1)]:
        computer = Computer(program)
        computer.add_input(i)
        computer.run()
        assert computer.state.outputs[-1] == out

def test_day5_6():
    """Here are some jump tests that take an input, then output 0 if 
    the input was zero or 1 if the input was non-zero"""
    program = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]

    for i, out in [(-1, 1), (0, 0), (1, 1)]:
        computer = Computer(program)
        computer.add_input(i)
        computer.run()
        assert computer.state.outputs[-1] == out


def test_day5_7():
    """The above example program uses an input instruction to ask 
    for a single number. The program will then output 999 if the 
    input value is below 8, output 1000 if the input value is equal to 8, 
    or output 1001 if the input value is greater than 8."""

    program = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
        1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
        999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]

    for i, out in [(7, 999), (8, 1000), (9, 1001)]:
        computer = Computer(program)
        computer.add_input(i)
        computer.run()
        assert computer.state.outputs[-1] == out

