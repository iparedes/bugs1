__author__ = 'nacho'

import copy

# Index of memory blocks and pointer registers
HEAP=0
STACK=1
CODE=2
# Index of other registers
COMM=3
ENER=4
OFFS=5


# Number of registers. The three registers are block pointers (stack, code, heap)
NREGS=10
# Number of memory blocks
NBLOCKS=3
# Size of memory blocks
MAX_MEM=1000

# Max Energy
ENERGY=100
# Number of descendants
OFFSPRING=2



OPS=['RST', # Resets the PC
     'NOP',  # NO Operation
     'PUSH', # PUSH n ; Pushes n into the STACK
     'MOV', # Sets the COMM register to MOV
     'ADD', # Adds the two numbers in the stack. Stores the result in the stack
     'JMF', # JMF n ; Jumps the PC forward n memory addresses
     'JMB', # JMB n ; Jumps the PC backward n memory addresses
]

class bug:
    def __init__(self):
        self._memory=[None]*NBLOCKS
        # Init the memory blocks
        self._memory[STACK]=[0]*MAX_MEM
        self._memory[CODE]=[0]*MAX_MEM
        self._memory[HEAP]=[0]*MAX_MEM
        # Init the registers
        self._registers=[0]*NREGS
        # 1-Stack pointer. Points to the head (top empty position) of the stack
        # 2-Program pointer. Points to the next instruction to be executed (or parameter to be read)
        self._registers[ENER]=ENERGY
        self._registers[OFFS]=OFFSPRING



    def copy(self,energy):
        b=copy.deepcopy(self)
        self._registers[ENER]=energy
        b._registers[ENER]=energy
        return b

    def _incPC(self,value=1):
        pc=self._registers[CODE]
        pc+=value
        if pc>=MAX_MEM:
            pc-=MAX_MEM
        elif pc<0:
            pc+=MAX_MEM

    def PC(self):
        return self._registers[CODE]

    def _push(self,S,value):
        """
        Pushes value (int) in the stack S

        :return:
        """
        id=self._registers[S]
        self._memory[S][id]=value
        id+=1
        if id==MAX_MEM:
            id=0
        self._registers[S]=id

    def _pop(self,S):
        """
        Pops the value from the stack S
        :return:
        The popped value (int)
        """
        id=self._registers[S]
        if id==0:
            id=MAX_MEM
        id-=1
        v=self._memory[S][id]
        self._registers[S]=id

        return v

    def pop(self):
        v=self._pop(STACK)
        return v


    def _set(self,address,value):
        """
        Sets a memory address to the given value
        :param address: The memory address.
        The memory block index is address/MAX_MEM. The cell index is address%MAX_MEM
        :param value: The value to set (int)
        :return:
        """
        (block,cell)=self._decode_address(address)
        self._memory[block][cell]=value


    def _get(self,address):
        """
        Gets the value in a memory address
        :param address: The memory address to get.
        The memory block index is address/MAX_MEM. The cell index is address%MAX_MEM
        :return: The value (int)
        """
        (block,cell)=self._decode_address(address)
        v=self._memory[block][cell]
        return v

    def _getp(self,address):
        """
        Gets the value of the memory address stored in address (pointer)
        :param address:
        :return: The value of the memory address pointed by the content of address
        """
        (block,cell)=self._decode_address(address)
        p=self._memory[block][cell]
        (block,cell)=self._decode_address(p)
        v=self._memory[block][cell]
        return v


    def _dump_memory(self,index):
        """
        Dumps to stdout a memory block
        :param index: The index of the memory block
        :return:
        """
        cont=0
        while cont<MAX_MEM:
            v=self._memory[index][cont]
            if v!=None:
                print cont,': ',self._memory[index][cont]
            cont+=1


    def _decode_address(self,address):
        """
        Decodes a memory address in block_index and cell
        :param address:
        :return:
        """
        if address<(NBLOCKS*MAX_MEM):
            return (address/MAX_MEM,address%MAX_MEM)
        else:
            return 0


    def _opcode_NOP(self):
        pass

    def _opcode_PUSH(self):
        pc=self._registers[CODE]
        v=self._memory[CODE][pc]
        self._incPC()
        self._push(STACK,v)

    def _opcode_JMF(self):
        pc=self._registers[CODE]
        v=self._memory[CODE][pc]
        self._incPC(v)

    def _opcode_JMB(self):
        pc=self._registers[CODE]
        v=self._memory[CODE][pc]
        self._incPC(-v)

    def _opcode_RST(self):
        self._registers[CODE]=0

    def _opcode_MOV(self):
        self._registers[COMM]=OPS.index('MOV')

    def _opcode_ADD(self):
        v1=self._pop(STACK)
        v2=self._pop(STACK)
        self._push(STACK,v1+v2)

    def compile(self,list):
        id=0
        for i in list:
            try:
                v=int(i)
            except:
                try:
                    v=OPS.index(i)
                except:
                    v=OPS.index('NOP')
            self._memory[CODE][id]=v
            id+=1


    def step(self):
        pc=self._registers[CODE]
        op=self._memory[CODE][pc]
        op=OPS[op]
        self._incPC()

        oper={
            'RST':    self._opcode_RST,
            'NOP':    self._opcode_NOP,
            'PUSH':   self._opcode_PUSH,
            'MOV':    self._opcode_MOV,
            'ADD':    self._opcode_ADD,
            'JMF':    self._opcode_JMF,
            'JMB':    self._opcode_JMB,
        }[op]
        oper()

        self._registers[ENER]-=1



    def readcomm(self):
        """
        Reads the content of the communications register
        After reading, sets it to zero
        :return: the value of the communications register
        """
        v=self._registers[COMM]
        self._registers[COMM]=0
        return v

    def dead(self):
        return self._registers[ENER]==0

    def mature(self):
        return self._registers[ENER]>=ENERGY

    def offspring(self):
        return self._registers[OFFS]

    def energy(self):
        return self._registers[ENER]




