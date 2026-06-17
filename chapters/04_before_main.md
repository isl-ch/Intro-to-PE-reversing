# 4. What Happens Before main()

As we learned in the previous chapter, the `AddressOfEntryPoint` in the PE header does not point to the developer's `main()` function. It points to compiler-generated boilerplate code.

If you don't recognize this boilerplate, you will waste hours reverse engineering code you didn't need to look at.

## The CRT Startup Code

When you write a C/C++ program in Visual Studio, MSVC (Microsoft Visual C++) links a library called the C Runtime (CRT). The CRT provides the true entry point.

Depending on the subsystem and character set, the entry point is usually named:
*   `mainCRTStartup` (Console, ASCII)
*   `wmainCRTStartup` (Console, Unicode)
*   `WinMainCRTStartup` (GUI, ASCII)
*   `wWinMainCRTStartup` (GUI, Unicode)

*(Note: MinGW and Clang have their own variations of startup functions, usually just called `start` or `__tmainCRTStartup`)*.

### Key Operations Before main()

When you look at the disassembly of the Entry Point, you will typically see the following operations, in roughly this order:

#### 1. Security Cookie Initialization (`__security_init_cookie`)
To prevent stack buffer overflows, compilers insert a random value (a "canary" or "cookie") onto the stack before local variables. If an overflow occurs, it corrupts the cookie. Before returning, the function checks the cookie. If it changed, the program crashes instead of executing injected shellcode.
*   **What it looks like:** A call to a function that uses `GetSystemTimeAsFileTime`, `GetCurrentProcessId`, `GetCurrentThreadId`, and `QueryPerformanceCounter` to generate a random seed.

#### 2. Exception Handling Setup
Windows uses Structured Exception Handling (SEH). The startup code registers default exception handlers so that if the program crashes, the OS knows what to do.

#### 3. C Runtime Initialization (`_cinit`)
This initializes floating-point math support, memory allocation heaps (`malloc`/`free`), and other C standard library features.

#### 4. Global Constructors (`_initterm`)
In C++, if you declare an object globally:
```cpp
class MyClass { public: MyClass() { printf("Hello!"); } };
MyClass globalObj;
int main() { return 0; }
```
`"Hello!"` prints *before* `main()` runs. The CRT maintains an array of function pointers to all global constructors and iterates through them, calling each one.
*   **What it looks like:** A loop iterating over an array of pointers, `CALL`ing each valid pointer.

#### 5. Command Line and Environment
The CRT calls `GetCommandLineA/W` and parses the arguments into the `argc` and `argv` format that `main()` expects.

#### 6. Calling main()
Finally, the CRT calls the user's code.

```assembly
; Typical MSVC x64 call to main
mov rcx, [argc]        ; Arg 1: argc
mov rdx, [argv]        ; Arg 2: argv
mov r8, [envp]         ; Arg 3: envp
call main              ; <--- The good stuff
```

#### 7. Exit (`exit` / `ExitProcess`)
When `main()` returns, the CRT takes the return value and passes it to `exit()`, which runs global destructors and then terminates the process.

## Distinguishing User Code from Compiler Code

How do you know what to ignore?
1.  **Symbols:** If you have PDBs, the debugger tells you `mainCRTStartup`. Ignore it.
2.  **API Usage:** Code calling `GetSystemTimeAsFileTime` at the very start is usually the security cookie.
3.  **Pattern Recognition:** Once you see MSVC's startup code a few times, you'll recognize the shape of it visually in Ghidra or x64dbg.
4.  **The "Call to Exit" trick:** The call to `main()` is almost always immediately followed by a call to `exit()` or `ExitProcess()`.

---

## Challenges and Tasks

### Task 1: Exploring Startup Code
1. Open `challenges/ch04_task.exe` in Ghidra.
2. Go to the Entry Point.
3. Trace through the MinGW startup functions to find the call to your `main()`.

### Challenge 1: Global Constructor Hunt
1. Open `challenges/ch04_chal.exe` in x64dbg.
2. Break on the string "Global constructor!".
3. Notice this happens before you ever reach `main()`.
