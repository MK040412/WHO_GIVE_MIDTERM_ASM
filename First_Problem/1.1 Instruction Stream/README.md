### 1.1. Instruction Stream Creation (3 pts): Convert the given C code into a minimized RISC-V instruction stream.

#### What is the problem 
------------------------

The problem says that convert C code into a minimized RISC-V instruction stream.
---
```c
void process_array(int arr[10])
```
---
It talk me make process_array function.  

For making array, we need knowlegde about stack and register.  
Each of stack has the address for each word (eg. stack memory).  
In this function, we initialize array size is 10 (eg. 40 bit).  


#### Concise Instruction about the problem 
------------------------

---
```c
void process_array(int arr[10]){
    int i, sum = 0;
// For loop
    for (i = 0; i < 10; i++) {
  // Branch IF it is even 
        if (arr[i] % 2 == 0) { 
            sum += arr[i]; 
        }
  // Branch IF it is odd
          else { 
            sum -= arr[i]; 
        }
  // Branch If it exceed 50
        if (sum > 50) { 
            exit(0); 
        } 
    } 
}
```
---

We need to see the logic about this code.  

  I made briefly annotation on this code. But it doesn't give us concise understanding.  
  I'll show pseudo code about this problem.  

     Pseudocode for `process_array` Function

```plaintext
Function process_array(arr[10])
    // Initialize variables
    Initialize sum to 0

    // Iterate over each element in the array
    For i from 0 to 9 do
        // Check if the current element is even
        If (arr[i] modulo 2 equals 0) then
            // If even, add the element to sum
            sum = sum + arr[i]
        Else
            // If odd, subtract the element from sum
            sum = sum - arr[i]
        End If

        // Check if the sum exceeds 50
        If (sum > 50) then
            // If sum is greater than 50, terminate the program
            Terminate program
        End If
    End For
End Function
```



