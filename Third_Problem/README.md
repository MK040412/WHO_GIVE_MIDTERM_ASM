# 3. Designing and Implementing FP8 Matrix Multiplication

FP8 (8-bit Floating Point) is a compact floating-point representation that offers significant memory and computational efficiency benefits, especially in applications like machine learning where reduced precision is acceptable. This section outlines the design and implementation of matrix multiplication using the FP8 format, focusing on extending the instruction set and designing the necessary datapath and functional units.

---

## 3.1. Instruction Set Extension for FP8 Operations (5 pts)

To perform matrix multiplication using FP8 values, we need to extend the existing RISC-V instruction set with specialized instructions that handle FP8 operations. Below are the proposed instructions along with their syntax, functionality, and usage in the matrix multiplication process.

### **Proposed FP8 Instructions**

1. **`fl8s` - Load FP8 Single**
    - **Syntax:** `fl8s rd, offset(rs1)`
    - **Functionality:** Loads an FP8 value from memory into a floating-point register.
    - **Operands:**
        - `rd`: Destination floating-point register.
        - `rs1`: Base address register.
        - `offset`: Memory offset.
    - **Usage in Matrix Multiplication:**
        - Fetches elements from matrices A and B into registers for computation.
    - **Example:**
        ```assembly
        fl8s f1, 0(a0)    # Load A[i][k] into f1
        fl8s f2, 4(a1)    # Load B[k][j] into f2
        ```

2. **`fst8` - Store FP8 Single**
    - **Syntax:** `fst8 rs2, offset(rs1)`
    - **Functionality:** Stores an FP8 value from a floating-point register into memory.
    - **Operands:**
        - `rs2`: Source floating-point register.
        - `rs1`: Base address register.
        - `offset`: Memory offset.
    - **Usage in Matrix Multiplication:**
        - Stores the computed sum into matrix C.
    - **Example:**
        ```assembly
        fst8 f3, 0(a2)    # Store sum into C[i][j]
        ```

3. **`fadd8` - FP8 Add**
    - **Syntax:** `fadd8 rd, rs1, rs2`
    - **Functionality:** Adds two FP8 values from floating-point registers and stores the result in a destination register.
    - **Operands:**
        - `rd`: Destination floating-point register.
        - `rs1`: Source floating-point register 1.
        - `rs2`: Source floating-point register 2.
    - **Usage in Matrix Multiplication:**
        - Accumulates the sum of products.
    - **Example:**
        ```assembly
        fadd8 f3, f3, f4   # sum += (A[i][k] * B[k][j])
        ```

4. **`fmul8` - FP8 Multiply**
    - **Syntax:** `fmul8 rd, rs1, rs2`
    - **Functionality:** Multiplies two FP8 values from floating-point registers and stores the result in a destination register.
    - **Operands:**
        - `rd`: Destination floating-point register.
        - `rs1`: Source floating-point register 1.
        - `rs2`: Source floating-point register 2.
    - **Usage in Matrix Multiplication:**
        - Computes the product of A[i][k] and B[k][j].
    - **Example:**
        ```assembly
        fmul8 f4, f1, f2   # f4 = A[i][k] * B[k][j]
        ```

### **Instruction Usage in Matrix Multiplication**

Here's how these instructions integrate into the matrix multiplication process:

```assembly
fp8_matrix_mult:
    # Initialize loop counters i, j, k and sum
    li      t0, 0              # i = 0
loop_i:
    bge     t0, 2, end_mult    # if (i >= 2) goto end_mult
    li      t1, 0              # j = 0
loop_j:
    bge     t1, 2, next_i      # if (j >= 2) goto next_i
    li      t2, 0              # k = 0
    li      t3, 0x00           # sum = 0x00 (FP8 zero)
loop_k:
    bge     t2, 2, store_sum    # if (k >= 2) goto store_sum
    # Load A[i][k] and B[k][j]
    add     a0, base_A, t0      # base_A + i
    add     a1, base_B, t1      # base_B + j
    fl8s    f1, 0(a0)           # Load A[i][k] into f1
    fl8s    f2, 0(a1)           # Load B[k][j] into f2
    fmul8   f4, f1, f2          # f4 = A[i][k] * B[k][j]
    fadd8   f3, f3, f4          # sum += f4
    addi    t2, t2, 1           # k++
    j       loop_k
store_sum:
    # Store the sum into C[i][j]
    add     a2, base_C, t0      # base_C + i
    fst8    f3, 0(a2)           # Store sum into C[i][j]
    addi    t1, t1, 1           # j++
    j       loop_j
next_i:
    addi    t0, t0, 1           # i++
    j       loop_i
end_mult:
    jr      ra                  # Return
```

### **Summary of FP8 Instructions**

- **`fl8s`** and **`fst8`** handle loading and storing FP8 values between memory and floating-point registers.
- **`fadd8`** and **`fmul8`** perform arithmetic operations directly on FP8 values, facilitating efficient matrix multiplication without converting to higher precision formats.

These instructions extend the RISC-V architecture to natively support FP8 operations, enabling efficient computation required for applications like matrix multiplication in machine learning.

---

## 3.2. Datapath and Functional Unit Design (10 pts)

Designing the datapath and functional units for FP8 matrix multiplication involves integrating FP8 arithmetic capabilities into a single-cycle RISC-V CPU. The design must support loading, storing, addition, and multiplication of FP8 values. Below is a detailed explanation of the datapath modifications and the FP8 arithmetic unit design.

### **1. Overview of the Modified Datapath**

The datapath of a single-cycle RISC-V CPU typically includes the following components:

- **Program Counter (PC)**
- **Instruction Memory**
- **Register File**
- **ALU (Arithmetic Logic Unit)**
- **Data Memory**
- **Control Unit**

To support FP8 operations, the datapath requires additional components and modifications:

- **FP8 Arithmetic Unit**: Handles FP8 addition and multiplication.
- **FP8 Register File**: Stores FP8 values separately from integer registers.
- **Control Signals**: Extended to manage FP8 instructions and operations.

### **2. FP8 Arithmetic Unit Design**

The FP8 Arithmetic Unit is responsible for performing FP8-specific operations, namely addition and multiplication. Below is the design of the FP8 Arithmetic Unit.

#### **Components of the FP8 Arithmetic Unit**

1. **FP8 Adder (`fadd8`)**
    - **Inputs**: Two FP8 operands.
    - **Output**: FP8 sum.
    - **Functionality**:
        - Align exponents.
        - Perform mantissa addition.
        - Normalize the result.
        - Handle overflow and underflow.
  
2. **FP8 Multiplier (`fmul8`)**
    - **Inputs**: Two FP8 operands.
    - **Output**: FP8 product.
    - **Functionality**:
        - Add exponents (subtract bias).
        - Multiply mantissas.
        - Normalize the result.
        - Handle overflow and underflow.

#### **FP8 Arithmetic Unit Block Diagram**

```plaintext
+---------------------+
|     FP8 Adder       |
| +-----------------+ |
| | Operand A (FP8) | |
| | Operand B (FP8) | |
| +--------+--------+ |
|          |          |
|          v          |
|     FP8 Sum (FP8)   |
+---------------------+
          |
          v
+---------------------+
|     FP8 Multiplier  |
| +-----------------+ |
| | Operand A (FP8) | |
| | Operand B (FP8) | |
| +--------+--------+ |
|          |          |
|          v          |
|    FP8 Product (FP8)|
+---------------------+
```

### **3. Modified Datapath Diagram**

Below is a simplified block diagram illustrating the integration of the FP8 Arithmetic Unit into the existing RISC-V single-cycle CPU datapath.

```plaintext
+---------------------+
|      Program        |
|      Counter (PC)   |
+----------+----------+
           |
           v
+----------+----------+
|   Instruction       |
|     Memory          |
+----------+----------+
           |
           v
+----------+----------+
|  Register File      |
| +-------+-------+   |
| | Int Regs | FP8 Regs|
| +-------+-------+   |
+----------+----------+
           |
           v
+----------+----------+       +-----------------------+
|         ALU         | <---- |    FP8 Arithmetic     |
| (Integer Operations)|       |        Unit           |
+----------+----------+       +-----------------------+
           |                          |
           v                          v
+----------+----------+       +-----------------------+
|      Data Memory    |       |        Control        |
+----------+----------+       +-----------------------+
           |
           v
        [Other Components]
```

### **4. Detailed Functional Description**

#### **a. Register File Enhancements**

- **Separate FP8 Registers**: Introduce a separate set of floating-point registers (`f0`-`f31`) dedicated to FP8 operations. This allows parallel handling of integer and FP8 data.
- **Read and Write Ports**: Extend the register file to support additional read/write ports for floating-point operations.

#### **b. FP8 Arithmetic Unit Integration**

- **Control Signals**: Modify the Control Unit to recognize FP8 instructions (`fadd8`, `fmul8`, `fl8s`, `fst8`) and generate appropriate control signals.
- **Data Path Connections**: Connect the FP8 Arithmetic Unit to the floating-point register file and ensure data flows correctly between components.

#### **c. Control Unit Modifications**

- **Instruction Decoding**: Update the Instruction Decoder to identify FP8 instructions based on opcode and function fields.
- **Operation Selection**: Generate control signals to select between integer ALU operations and FP8 Arithmetic Unit operations.

### **5. Control Logic Enhancements**

The Control Unit must be extended to handle the new FP8 instructions. Here's how the control signals are managed:

1. **Instruction Decoding**:
    - **Opcode Field**: Assign unique opcodes for FP8 instructions to differentiate them from existing integer and standard floating-point instructions.
  
2. **Control Signal Generation**:
    - **FP8 Operation Select**: Determine whether to route data through the integer ALU or the FP8 Arithmetic Unit based on the instruction.
    - **Memory Operations**: Ensure that load and store operations correctly handle FP8 data widths and alignments.
    - **Register Write-Back**: Direct the results from the FP8 Arithmetic Unit to the appropriate floating-point registers.

### **6. Example Control Flow for `fp8_matrix_mult`**

```plaintext
1. Load A[i][k] and B[k][j] using `fl8s`
    - Control signals: 
        - Select FP8 Load operation
        - Read from memory and write to FP8 registers

2. Multiply A[i][k] * B[k][j] using `fmul8`
    - Control signals:
        - Select FP8 Multiply operation
        - Operands from FP8 registers
        - Output to FP8 Arithmetic Unit

3. Add the product to sum using `fadd8`
    - Control signals:
        - Select FP8 Add operation
        - Operands from FP8 registers
        - Output to FP8 Arithmetic Unit

4. Store the sum into C[i][j] using `fst8`
    - Control signals:
        - Select FP8 Store operation
        - Read from FP8 register and write to memory
```

### **7. Summary of Datapath and Functional Unit Design**

- **FP8 Arithmetic Unit**: Integrates FP8-specific addition and multiplication, handling exponent alignment and mantissa operations.
- **FP8 Register File**: Stores FP8 operands and results, facilitating parallel data handling with integer registers.
- **Control Unit**: Extended to decode FP8 instructions and generate necessary control signals to manage data flow between integer and FP8 units.
- **Data Path**: Enhanced to support loading, storing, and performing arithmetic operations on FP8 data without converting to higher precision formats.

### **8. Visual Representation**

While a detailed block diagram would ideally be created using a graphical tool, here's a simplified textual representation:

```plaintext
+---------------------+
|      Program        |
|      Counter (PC)   |
+----------+----------+
           |
           v
+----------+----------+
|   Instruction       |
|     Memory          |
+----------+----------+
           |
           v
+----------+----------+
|  Register File      |
| +-------+-------+   |
| | Int Regs | FP8 Regs|
| +-------+-------+   |
+----------+----------+
           |
           v
+----------+----------+       +-----------------------+
|         ALU         | <---- |    FP8 Arithmetic     |
| (Integer Operations)|       |        Unit           |
+----------+----------+       +-----------------------+
           |                          |
           v                          v
+----------+----------+       +-----------------------+
|      Data Memory    |       |        Control        |
+----------+----------+       +-----------------------+
           |
           v
        [Other Components]
```

---

## Conclusion

Implementing FP8 matrix multiplication in a single-cycle RISC-V CPU involves extending the instruction set with FP8-specific operations and redesigning the datapath to incorporate FP8 arithmetic units and registers. The proposed instructions (`fl8s`, `fst8`, `fadd8`, `fmul8`) enable efficient loading, storing, and arithmetic operations on FP8 data. The modified datapath ensures seamless integration of these operations alongside existing integer computations, facilitating optimized performance for applications requiring reduced precision.

By carefully designing the control logic and ensuring proper data flow between components, the CPU can efficiently execute FP8 matrix multiplication, leveraging the benefits of lower memory usage and faster computation times inherent to the FP8 format.

---

# Appendix: Example Verilog Implementation

To complement the theoretical design, here's an example of how you might implement the FP8 Arithmetic Unit and integrate it into a simple single-cycle RISC-V CPU using Verilog.

### **FP8 Arithmetic Unit in Verilog**

```verilog
// FP8_Arithmetic_Unit.v
module FP8_Arithmetic_Unit (
    input  wire [7:0] A,        // Operand A (FP8)
    input  wire [7:0] B,        // Operand B (FP8)
    input  wire        Op,       // Operation: 0 = Add, 1 = Multiply
    output wire [7:0] Result     // Result (FP8)
);

    // Internal signals
    wire [7:0] Add_Result;
    wire [7:0] Mul_Result;

    // FP8 Adder
    FP8_Adder adder (
        .A(A),
        .B(B),
        .Sum(Add_Result)
    );

    // FP8 Multiplier
    FP8_Multiplier multiplier (
        .A(A),
        .B(B),
        .Product(Mul_Result)
    );

    // Select operation
    assign Result = Op ? Mul_Result : Add_Result;

endmodule
```

### **FP8 Adder Module**

```verilog
// FP8_Adder.v
module FP8_Adder (
    input  wire [7:0] A,        // Operand A (FP8)
    input  wire [7:0] B,        // Operand B (FP8)
    output wire [7:0] Sum        // Sum (FP8)
);

    // Implementation details would include:
    // - Extracting sign, exponent, and mantissa
    // - Aligning exponents
    // - Adding mantissas
    // - Normalizing the result
    // - Handling special cases (overflow, underflow)

    // Placeholder for actual FP8 addition logic
    assign Sum = A + B; // Simplified; replace with actual FP8 addition logic

endmodule
```

### **FP8 Multiplier Module**

```verilog
// FP8_Multiplier.v
module FP8_Multiplier (
    input  wire [7:0] A,        // Operand A (FP8)
    input  wire [7:0] B,        // Operand B (FP8)
    output wire [7:0] Product    // Product (FP8)
);

    // Implementation details would include:
    // - Extracting sign, exponent, and mantissa
    // - Adding exponents (subtract bias)
    // - Multiplying mantissas
    // - Normalizing the result
    // - Handling special cases (overflow, underflow)

    // Placeholder for actual FP8 multiplication logic
    assign Product = A * B; // Simplified; replace with actual FP8 multiplication logic

endmodule
```

### **Integrating FP8 Arithmetic Unit into CPU Datapath**

```verilog
// CPU.v
module CPU (
    input  wire        clk,
    input  wire        reset
);

    // Program Counter
    reg [31:0] PC;

    // Instruction Memory Signals
    wire [31:0] instruction;

    // Register File Signals
    wire [31:0] reg_data1, reg_data2;
    wire [31:0] reg_write_data;
    wire [4:0]  reg_write_addr;
    wire        reg_write_enable;

    // FP8 Arithmetic Unit Signals
    wire [7:0] FP8_A, FP8_B;
    wire       FP8_Op; // 0 = Add, 1 = Multiply
    wire [7:0] FP8_Result;

    // Instantiate Instruction Memory
    InstructionMemory IM (
        .addr(PC),
        .instr(instruction)
    );

    // Instantiate Register File
    RegisterFile RF (
        .clk(clk),
        .we(reg_write_enable),
        .ra1(instruction[19:15]),
        .ra2(instruction[24:20]),
        .wa(reg_write_addr),
        .wd(reg_write_data),
        .rd1(reg_data1),
        .rd2(reg_data2)
    );

    //
