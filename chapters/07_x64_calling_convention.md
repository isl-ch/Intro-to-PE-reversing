# 7. x64 Calling Convention

When one function calls another, they need an agreed-upon way to pass arguments and return values. This agreement is the **Calling Convention** or **ABI** (Application Binary Interface).

If you don't memorize the calling convention, reading assembly will feel like reading a foreign language without a dictionary.

## The Microsoft x64 Calling Convention

Unlike x86 (32-bit), which had many confusing calling conventions (`__cdecl`, `__stdcall`, `__fastcall`), Windows x64 unified everything into a single, mandatory convention.

### The Core Rules

1.  **The First Four Arguments:** Passed in registers.
    *   Argument 1: **RCX**
    *   Argument 2: **RDX**
    *   Argument 3: **R8**
    *   Argument 4: **R9**
    *(Mnemonic: "Reverse Crazies Destroy 8 9")*
2.  **Arguments 5 and Beyond:** Passed on the stack, pushed right-to-left.
3.  **Return Value:** Placed in the **RAX** register.

If arguments are floating-point numbers, they go in XMM0, XMM1, XMM2, XMM3 instead.

### The Shadow Space

This is a unique quirk of the Windows x64 ABI.

Even though the first four arguments are passed in registers, the calling function *must* reserve 32 bytes (4 slots of 8 bytes) on the stack right before the `CALL` instruction.

This is called the **Shadow Space** (or Home Space).
*   **Why?** It gives the called function a guaranteed safe place to dump those four registers onto the stack if it needs to use them for something else, or if the code is compiled in Debug mode (where variables are kept on the stack for easier viewing).
*   **Rule:** The caller allocates it, the callee can use it.

### Example in Assembly

C Code:
```c
int result = MyFunction(10, 20, 30, 40, 50);
```

Assembly:
```assembly
; Prepare Argument 5 on the stack
push 50              ; Arg 5 on stack

; Prepare Arguments 1-4 in registers
mov r9, 40           ; Arg 4
mov r8, 30           ; Arg 3
mov rdx, 20          ; Arg 2
mov rcx, 10          ; Arg 1

; Allocate Shadow Space (32 bytes)
sub rsp, 32          ; Make room on the stack

; Call the function
call MyFunction      

; Clean up the stack (Shadow Space + 1 stack argument)
add rsp, 40          ; 32 (Shadow) + 8 (Arg 5)

; The result is now in RAX
mov [local_result], rax 
```

### Volatile vs. Non-Volatile Registers

When calling a function, what happens to the values you stored in registers?

*   **Volatile (Caller-Saved):** `RAX`, `RCX`, `RDX`, `R8`, `R9`, `R10`, `R11`.
    *   If you call a function, you must assume it destroyed the contents of these registers. If you need their values later, *you* must save them to the stack before the call.
*   **Non-Volatile (Callee-Saved):** `RBX`, `RBP`, `RDI`, `RSI`, `R12`, `R13`, `R14`, `R15`.
    *   If a function wants to use these, it must back them up (usually `PUSH` them at the start of the function) and restore them (`POP` them) before returning. You can trust their values will survive a function call.

## Comparison with Linux (System V ABI)

If you have Linux reversing experience, pay close attention. The Linux x64 calling convention is different!

*   **Linux Registers:** `RDI`, `RSI`, `RDX`, `RCX`, `R8`, `R9`. (First 6 passed in registers).
*   **Linux Shadow Space:** Does not exist. Instead, Linux has a "Red Zone" (128 bytes *below* the stack pointer) that functions can use for local variables without allocating stack space. Windows does not use a Red Zone.

---

## Challenges and Tasks

### Task 1: Identifying Arguments
1. Open `challenges/ch07_task.exe` in x64dbg or Ghidra.
2. Find the function that adds 6 numbers together.
3. Identify how the 5th and 6th arguments are passed on the stack.

### Challenge 1: Floating Point Arguments
1. Open `challenges/ch07_chal.exe` in Ghidra.
2. Look at the function that takes floats. Notice that `RCX` and `RDX` are not used; instead, `XMM0` and `XMM1` are used.
