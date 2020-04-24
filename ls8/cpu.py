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
JMP = 0b01010100
CMP = 0b10100111
JNE = 0b01010110
JEQ = 0b01010101
AND = 0b10101000
OR = 0b10101010
XOR =0b10101011
NOT =0b01101001
SHL = 0b10101100
SHR = 0b10101101
MOD = 0b10100100
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
        self.branchtable[CMP] = self.handle_CMP
        self.branchtable[JMP] = self.handle_JMP
        self.branchtable[JNE] = self.handle_JNE
        self.branchtable[JEQ] = self.handle_JEQ
        #stretch
        self.branchtable[AND] = self.handle_AND
        self.branchtable[OR] = self.handle_OR
        self.branchtable[XOR] = self.handle_XOR
        self.branchtable[NOT] = self.handle_NOT
        self.branchtable[SHL] = self.handle_SHL
        self.branchtable[SHR] = self.handle_SHR
        self.branchtable[MOD] = self.handle_MOD
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
        if value_a < value_b:
            self.flag_L == 1
        else:
            self.flag_L == 0
        # If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.
    
        if value_a > value_b:
            self.flag_G== 1
        else:
            self.flag_G == 0
         #increment
        self.pc +=3

    def handle_JMP(self, a):

        # Jump to the address stored in the given register.
         
        # Set the PC to the address stored in the given register.
        self.pc = self.reg[a]

    def handle_JEQ(self,a):
        if self.flag_E == 1:
        # If equal flag is set (true), jump to the address stored in the given register.
            self.pc = self.reg[a]
        else: 
            self.pc += 2
    def handle_JNE(self, a):
        # If E flag is clear (false, 0), jump to the address stored in the given register.
        if self.flag_E == 0:
            self.pc = self.reg[a]
        else: 
            self.pc += 2
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

    def handle_AND(self, a, b):
        # Bitwise-AND the values in registerA and registerB, then store the result in registerA.
        value_a = self.reg[a]
        value_b = self.reg[b]
            
        if value_a & value_b == 1:
            self.reg[a] = 1

        else:
            self.reg[a] = 0
        
        self.pc +=3

    def handle_OR(self, a , b):
     # Perform a bitwise-OR between the values in registerA and registerB, storing the result in registerA.
        value_a = self.reg[a]
        value_b = self.reg[b]

        if value_a | value_b == 1:
            self.reg[a] = 1

        else:
            self.reg[a] = 0
        
        self.pc +=3
    
    def handle_XOR(self, a,b):
        
        value_a = self.reg[a]
        value_b = self.reg[b]
        if value_a & value_b == 1:
            self.reg[a] = 0
        
        elif value_a | value_b == 1:
            self.reg[a] = 1

        else:
            self.reg[a] = 0

        self.pc +=3

    def handle_NOT(self,a):
    
    #set true to false and false to true?
        value_a = self.reg[a]

        if value_a == 1:
            self.reg[a] = 0
        else: 
            self.reg[a] = 1

        self.pc +=2

    def handle_SHL(self, a, b):
        value_a = self.reg[a]
        value_b = self.reg[b]

        self.reg[a] = value_a << value_b
        self.pc +=3

    def handle_SHR(self, a, b):
        value_a = self.reg[a]
        value_b = self.reg[b]

        self.reg[a] = value_a >> value_b
        self.pc +=3

    def handle_MOD(self, a , b):
        # Divide the value in the first register by the value in the second, storing the remainder of the result in registerA.

        # If the value in the second register is 0, the system should print an error message and halt.

        value_a = self.reg[a]
        value_b = self.reg[b]

        value_c = value_a % value_b
        if value_c == 0:
            print("The value is 0 err")
            self.running = False
        else:
            self.reg[a] = value_c
            self.pc +=3
    
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

