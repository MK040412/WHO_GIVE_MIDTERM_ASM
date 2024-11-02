# Converting C Code to RISC-V Instructions (Total: 10 Points)

The description are given a fragment of C code. Task is to convert this C code into a corresponding RISC-V instruction stream and ensure it runs correctly on a single-cycle RISC-V CPU. The following steps outline your work:

```c
void process_array(int arr[10]) { 
    int i, sum = 0; 
    for (i = 0; i < 10; i++) { 
        if (arr[i] % 2 == 0) { 
            sum += arr[i]; 
        } else { 
            sum -= arr[i]; 
        } 
        if (sum > 50) { 
            exit(0); 
        } 
    } 
}
```

## 1.1. Instruction Stream Creation (3 Points)

**Task:**  
Convert the given C code into a minimized RISC-V instruction stream.

## 1.2. Instruction Memory Implementation (3 Points)

**Task:**  
Implement the instruction memory such that the RISC-V processor can access and execute your instruction stream.

## 1.3. Single-Cycle CPU Modification (4 Points)

**Task:**  
Modify or create the single-cycle RISC-V CPU code to run your generated instruction stream. Make sure that the CPU correctly handles all the instructions needed to execute the given C code.

---

## Grading Criteria

### 1.1. Instruction Stream Creation (3 Points)

- **Full Points:**  
  - Works correctly.
  
- **Half Points:**  
  - Some functionality issues.
  
- **Zero Points:**  
  - Does not work.

# <span style="color: red"> !!Notice!! : I can't do below one, because I'm CSE student, Not a EE student</span>

### 1.2. Instruction Memory Implementation (3 Points)

- **Full Points:**  
  - Works correctly.
  
- **Half Points:**  
  - Some functionality issues.
  
- **Zero Points:**  
  - Does not work.

### 1.3. Single-Cycle CPU Modification (4 Points)

- **Full Points:**  
  - Works correctly.
  
- **Half Points:**  
  - Some functionality issues.
  
- **Zero Points:**  
  - Does not work.

---
