# 9. Exception Handling

When a program tries to read invalid memory (Access Violation), divide by zero, or hits a breakpoint, the CPU generates an "Exception".

If the program doesn't handle the exception, the OS steps in, kills the process, and shows a crash dialog. Exception handling allows a program to catch these errors and recover gracefully.

## Structured Exception Handling (SEH)

SEH is Windows' native exception handling mechanism. It forms the backbone of C++ `try/catch` blocks and C `__try/__except` blocks.

### The 32-bit Way (Stack-based)
In x86 (32-bit) Windows, SEH was implemented by pushing exception handlers onto the stack. Malware used to love overwriting these stack pointers to hijack execution during a crash.

### The 64-bit Way (Table-based)
In x64 Windows, SEH was completely redesigned to be far more secure and efficient.

Exception handlers are *no longer stored on the stack*. Instead, they are stored in a read-only table in the PE file itself, within a section called `.pdata` (Procedure Data) and `.xdata` (Exception Data).

#### Unwind Information (`.pdata` and `.xdata`)
For an exception handler to work, the OS needs to be able to "unwind" the stack—that is, walk backwards through the call stack to find a function that registered a `catch` block for that specific error.

To make unwinding possible (especially since Frame Pointer Omission removes the standard `RBP` chain), the compiler generates **Unwind Codes** for every single function that modifies the stack pointer or saves non-volatile registers.

*   `.pdata` contains an array of `RUNTIME_FUNCTION` structures. Each structure maps a function's start and end addresses to its unwind data.
*   `.xdata` contains the actual unwind codes ("At offset +0x5, RSP was decreased by 0x20. At offset +0x9, RBX was pushed").

When an exception occurs, Windows searches `.pdata` to find the function where the crash happened, reads `.xdata` to reverse the prologue, moves up to the caller, and repeats until it finds a handler.

## C++ `try/catch`

When you write:
```cpp
try {
    DangerousFunction();
} catch (const std::exception& e) {
    printf("Caught it!");
}
```
The compiler translates this into underlying SEH structures.

**What you see in Ghidra:**
If you see a lot of complex, compiler-generated code referencing `CxxFrameHandler3` or `CxxFrameHandler4`, you are looking at the boilerplate implementation of a C++ `try/catch` block.

*Reverse Engineering Tip:* Don't waste time analyzing the internals of `CxxFrameHandler`. Recognize it as an exception handler and focus on the code *inside* the `try` block.

## Vectored Exception Handling (VEH)

VEH is an alternative to SEH. Instead of being tied to specific functions (like `try/catch`), VEH handlers are registered globally for the entire process using `AddVectoredExceptionHandler`.

When an exception occurs, Windows calls VEH handlers *before* SEH handlers.
Malware and game cheats frequently use VEH for anti-debugging or to hook functions silently by intentionally causing exceptions (like hardware breakpoints) and handling them.

---

## Challenges and Tasks

### Task 1: Locating .pdata
1. Open `challenges/ch09_task.exe` in a PE editor.
2. Find the `.pdata` section. This table proves the executable uses table-based exception handling.

### Challenge 1: The VEH Breakpoint
1. Open `challenges/ch09_chal.exe` in Ghidra.
2. Notice the call to `AddVectoredExceptionHandler`. This allows the program to catch exceptions globally before standard `try/catch` blocks.
