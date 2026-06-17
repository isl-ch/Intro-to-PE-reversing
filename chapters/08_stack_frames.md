# 8. Stack Frames and Functions

The stack is a contiguous block of memory allocated for a thread. It grows downwards (from higher memory addresses to lower memory addresses). It is managed primarily by two registers:
*   **RSP (Stack Pointer):** Points to the very "top" (lowest address) of the stack.
*   **RBP (Base Pointer):** Traditionally used as an anchor point to access local variables.

Every time a function is called, a new chunk of the stack is allocated for it. This chunk is called a **Stack Frame**.

## The Anatomy of a Function

A typical function in assembly is divided into three parts: the Prologue, the Body, and the Epilogue.

### 1. The Prologue (Setup)

The prologue prepares the stack frame for the function.

```assembly
; Typical x64 Prologue
push rbp             ; 1. Save the caller's RBP
mov rbp, rsp         ; 2. Set our own RBP as the base of our frame
sub rsp, 0x40        ; 3. Allocate 64 bytes for local variables
                     ;    (RSP moves down, making room)
```

If the function needs to use non-volatile registers (like `rbx` or `rdi`), it will `push` them to the stack right after this.

### 2. The Body (Execution)

This is where the actual logic happens.
*   **Accessing Locals:** Variables stored on the stack are accessed via negative offsets from RBP or positive offsets from RSP. E.g., `mov dword ptr [rbp-0x10], 5` (Store the number 5 into a local variable).
*   **Accessing Arguments:** In x64, remember the first four args are in registers. If the function was compiled in Debug mode, the body will often start by moving RCX, RDX, R8, R9 into the Shadow Space that the caller allocated just above the current frame.

### 3. The Epilogue (Cleanup)

Before returning to the caller, the function must clean up its stack frame. The stack pointer (`RSP`) must be exactly where it was before the prologue started.

```assembly
; Typical x64 Epilogue
add rsp, 0x40        ; 1. Deallocate local variables
pop rbp              ; 2. Restore the caller's RBP
ret                  ; 3. Return to caller (pops the return address into RIP)
```

*(Alternatively, you often see `leave` instead of `mov rsp, rbp` / `pop rbp`, though modern x64 compilers prefer `add rsp, X` followed by `pop rbp` for speed).*

## Stack Canaries (Security Cookies)

If a local buffer on the stack (e.g., an array of characters) is overflowed, the attacker can overwrite the saved Return Address. When the function executes `ret`, it jumps to the attacker's code instead of the caller.

To prevent this, compilers insert a random value between the local variables and the saved return address. This is the **Security Cookie** (or Canary).

**Prologue with Canary:**
```assembly
sub rsp, 0x40
mov rax, qword ptr [__security_cookie]
xor rax, rbp         ; XOR it with RBP for extra randomness
mov [rbp-0x8], rax   ; Place the cookie right above the local variables
```

**Epilogue with Canary:**
```assembly
mov rcx, [rbp-0x8]   ; Retrieve the cookie
xor rcx, rbp         ; Un-XOR it
call __security_check_cookie ; Checks if it matches the original. If not, CRASH!
add rsp, 0x40
ret
```
*Takeaway:* When you see XORing with a global variable near the start and end of a function, you are looking at stack protection.

## Frame Pointer Omission (FPO)

In optimized Release builds, compilers often realize that tying up the `RBP` register just to keep track of the stack frame is a waste. They can keep track of everything using just `RSP`.

This is called Frame Pointer Omission.
*   The prologue will just be `sub rsp, 0x40`. (No `push rbp`).
*   Local variables are accessed relative to `RSP` (e.g., `[rsp+0x10]`).
*   This makes reading assembly harder for humans because `RSP` changes whenever there's a `push` or `pop`, meaning the offset to a local variable might change halfway through the function.
*   Ghidra handles FPO automatically, showing you clean variables in the decompiler.

---

## Challenges and Tasks

### Task 1: Prologue Identification
1. Open `challenges/ch08_task.exe` in Ghidra.
2. Look at `main()`. Notice the massive `sub rsp, 0x1000` prologue used to allocate the 4096-byte local array.

### Challenge 1: Manual Stack Reversal
1. Open `challenges/ch08_chal.exe` in Ghidra.
2. Look at the unoptimized assembly for `calc()`. Observe how it uses `RBP` to store the argument and retrieve the local variable.
