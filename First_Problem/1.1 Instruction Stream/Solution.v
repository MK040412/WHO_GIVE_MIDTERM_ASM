    .text
    .globl process_array

process_array:
    # Function Prologue
    addi    sp, sp, -16         # Allocate stack space (16 bytes)
    sw      ra, 12(sp)          # Save return address
    sw      s0, 8(sp)           # Save s0 (used for base address of arr)

    # Initialize variables
    addi    s0, a0, 0           # s0 = arr (base address of the array)
    li      t0, 0               # i = 0
    li      t1, 0               # sum = 0
    li      t2, 10              # Constant 10 for loop comparison
    li      t3, 50              # Constant 50 for sum comparison

loop_start:
    # Check if i >= 10
    bge     t0, t2, loop_end    # if (i >= 10) goto loop_end

    # Calculate address of arr[i]
    slli    t4, t0, 2           # t4 = i * 4 (word size)
    add     t4, s0, t4          # t4 = arr + i*4 (address of arr[i])

    # Load arr[i]
    lw      t5, 0(t4)           # t5 = arr[i]

    # Check if arr[i] is even (arr[i] % 2 == 0)
    andi    t6, t5, 1           # t6 = arr[i] & 1
    beq     t6, x0, is_even     # if (t6 == 0) goto is_even

    # Else branch: arr[i] is odd
    sub     t1, t1, t5          # sum = sum - arr[i]
    jal     x0, check_sum       # Jump to check_sum

is_even:
    # If branch: arr[i] is even
    add     t1, t1, t5          # sum = sum + arr[i]

check_sum:
    # Check if sum > 50
    ble     t1, t3, continue_loop # if (sum <= 50) goto continue_loop

    # If sum > 50, exit the program
    li      a7, 10              # syscall number for exit
    ecall                         # Make syscall to exit

continue_loop:
    # Increment i
    addi    t0, t0, 1           # i = i + 1
    jal     x0, loop_start      # Jump back to the start of the loop

loop_end:
    # Function Epilogue
    lw      ra, 12(sp)          # Restore return address
    lw      s0, 8(sp)           # Restore s0
    addi    sp, sp, 16          # Deallocate stack space
    jalr    x0, ra, 0           # Return to caller

#|
      /* Thanks https://github.com/darklife/darkriscv */
  __heap_size    = 0x200;  /* required amount of heap */
  __stack_size  = 0x800;  /* required amount of stack */

  MEMORY
  {
    ROM (rwx) : ORIGIN = 0x00000000, LENGTH = 0x10000
    RAM (rwx) : ORIGIN = 0x00010000, LENGTH = 0x08000
  }
  SECTIONS
  {
    .text :
    {
      *(.boot)
      *(.text)
      *(.text)
      *(.rodata*)
    } > ROM
    .data :
    {
      *(.sbss)
      *(.data)
      *(.bss)
      *(.rela*)
      *(COMMON)
    } > RAM

    .heap :
    {
      . = ALIGN(4);
      PROVIDE ( end = . );
      _sheap = .;
      . = . + __heap_size;
      . = ALIGN(4);
      _eheap = .;
    } >RAM

    .stack :
    {
      . = ALIGN(4);
      _estack = .;
      . = . + __stack_size;
      . = ALIGN(4);
      _sstack = .;
    } >RAM
  }
                        
      |#
