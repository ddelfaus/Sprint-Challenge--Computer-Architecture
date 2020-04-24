"""CPU functionality."""

import sys
# commands
LDI = 0b10000010
HLT = 0b00000001
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
ADD = 0b10100000
RET = 0b00010001



class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.SP = 7
        self.reg[self.SP] = 0xF4
        self.IR = 0
        self.pc = 0  # counter
        self.flag_E = 0
        self.flag_G = 0
        self.flag_L = 0 
        self.running = True
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[ADD] = self.handle_ADD
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[POP] = self.handle_POP
        self.branchtable[CALL] = self.handle_CALL
        self.branchtable[RET] = self.handle_RET

    def handle_LDI(self, a, b):

        self.reg[a] = b
        self.pc += 3

    def handle_HLT(self):
        self.running = False
        # self.pc +=1

    def handle_PRN(self, a):
        print(self.reg[a], "print")
        self.pc += 2

    def handle_ADD(self, a, b):
        self.reg[a] = self.reg[a] + self.reg[b]

        self.pc += 3

    def handle_MUL(self, a, b):
       
        self.reg[a] = self.reg[a] * self.reg[b]

        self.pc += 3

    def handle_PUSH(self, a):

        self.reg[self.SP] -= 1
        self.ram[self.reg[self.SP]] = self.reg[a]
        self.pc += 2

    def handle_POP(self, a):
       
        self.reg[a] = self.ram[self.reg[self.SP]]
        self.reg[self.SP] += 1
        self.pc += 2

    def handle_CALL(self, a):
        return_address = self.pc +2
    
        self.pc -= 1
        self.ram[self.reg[self.SP]] = return_address
        self.pc = self.reg[a]
  

    def handle_RET(self):
      
        self.pc = self.ram[self.reg[self.SP]]
        self.reg[self.SP] += 1

    
    def handle_CMP(self, a, b):
        #get value
        value_a = self.reg[a]
        value_b = self.reg[b]


        #compare and set flag
        # If they are equal, set the Equal E flag to 1, otherwise set it to 0.
        if value_a == value_b:
            self.flag_E == 1
        else:
            self.flag_E == 0
        
        # If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.
        if value_A < value_b:
            self.flag_L == 1
        else:
            self.flag_L == 0
        # If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.
       

        if value_A > value_b:
            self.flag_L == 1
        else:
            self.flag_L == 0
         #increment
        self.pc +=3

    def handle_JUMP(self, a):

        # Jump to the address stored in the given register.

        # Set the PC to the address stored in the given register.
        
    def load(self, filename):
        """Load a program into memory."""

        address = 0
     
        count = 0
        with open(filename) as f:
            for line in f:
                line = line.split('#')
                line = line[0].strip()

                if line == '':
                    continue

                self.ram[address] = int(line, 2)

                count = count + 1
                # print(line)
                # print(count)
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

    def ram_read(self, mar):

        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def run(self):
        """Run the CPU."""

        while self.running is True:
            self.IR = self.ram_read(self.pc)

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            operands = self.IR >> 6

            if self.IR in self.branchtable:
               
                if operands == 0:
                    self.branchtable[self.IR]()

                elif operands == 1:

                    self.branchtable[self.IR](operand_a)

                elif operands == 2:

                    self.branchtable[self.IR](operand_a, operand_b)

            else:
                print("unknown instruction")

                break

