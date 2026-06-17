# Windows RE Tutorial: 32 Challenge Solutions Guide

This guide provides the answers and walkthroughs for all 32 custom challenges (2 per chapter) provided in the `challenges/` directory.

## Chapter 1: Environment Setup
*   **Task 1:** Open `ch01_task.exe` in x64dbg. It will pause at the system breakpoint. Go to the "Memory Map", find the `.rdata` section, right-click and search for strings. You will find `x64dbg_is_awesome`.
*   **Challenge 1:** Open `ch01_chal.exe`. Go to the Symbols tab. If configured correctly, you will see `kernel32.pdb` loaded, allowing you to easily find the `Sleep` API call.

## Chapter 2: PE Fundamentals
*   **Task 1:** Open `ch02_task.exe` in PE-Bear. The `.data` section's Virtual Size is 5MB, but its Raw Size on disk is almost 0. The compiler knows the array is initialized to zeros, so it doesn't waste disk space, it just tells the Loader to allocate the memory.
*   **Challenge 1:** In `ch02_chal.exe`, the ImageBase is `0x00800000`. If `.text` is at RVA `0x1000`, the expected VA is `0x00801000`.

## Chapter 3: The Loading Process
*   **Task 1:** Open `ch03_task.exe` in Ghidra. You will see `wininet.dll` in the Imports tree, used for `InternetOpenA`.
*   **Challenge 1:** Run `ch03_chal.exe`. It prints "I ran before main!" due to the `TlsCallback` function pointer stored in the `.CRT$XLB` section.

## Chapter 4: What Happens Before main()
*   **Task 1:** Open `ch04_task.exe` in Ghidra. You will see MinGW's `__tmainCRTStartup` which eventually calls your `main()`.
*   **Challenge 1:** Open `ch04_chal.exe` in x64dbg. Place a breakpoint on `printf`. You will hit it inside `init()` before `main()` is ever executed.

## Chapter 5: Finding main()
*   **Task 1:** `ch05_task.exe` is stripped (`-s`). Find the call to `exit()` at the bottom of the entry point to locate `main()`.
*   **Challenge 1:** Open `ch05_chal.exe` in Ghidra. Search for "Error: No arguments!" and use `XREF` to jump to `main()`.

## Chapter 6: Symbols and Debug Information
*   **Task 1:** `ch06_task.exe` has debug info. Use a PE editor to inspect the Debug Directory.
*   **Challenge 1:** `ch06_chal.exe` contains a `Data` struct. Ghidra parses the DWARF info and automatically types the local variables.

## Chapter 7: x64 Calling Convention
*   **Task 1:** In `ch07_task.exe`, args 1-4 are in RCX, RDX, R8, R9. Args 5 and 6 are pushed to the stack (at `[rsp+0x20]` and `[rsp+0x28]`).
*   **Challenge 1:** In `ch07_chal.exe`, floats are passed via `XMM0` and `XMM1`.

## Chapter 8: Stack Frames and Functions
*   **Task 1:** `ch08_task.exe` allocates a massive 4096-byte array. The prologue is `sub rsp, 0x1000`.
*   **Challenge 1:** `ch08_chal.exe` is compiled without optimizations (`-O0`). You will see it explicitly push `RBP`, move `RSP` to `RBP`, and use `[rbp+X]` offsets.

## Chapter 9: Exception Handling
*   **Task 1:** `ch09_task.exe` modifies the stack, so the compiler generated a `.pdata` section. View it in PE-Bear.
*   **Challenge 1:** `ch09_chal.exe` registers a VEH. Notice the call to `AddVectoredExceptionHandler`.

## Chapter 10: Imports and API Calls
*   **Task 1:** `ch10_task.exe` imports `advapi32.dll` for `CryptAcquireContext`.
*   **Challenge 1:** `ch10_chal.exe` does not import `MessageBoxA`. It resolves it dynamically using `LoadLibrary` and `GetProcAddress`.

## Chapter 11: Debugging Basics
*   **Task 1:** In `ch11_task.exe`, step through the `for` loop in x64dbg using `F8`. Watch `EAX` increment.
*   **Challenge 1:** In `ch11_chal.exe`, type a fake password. Patch the `je` instruction after `strcmp` to `jne` to bypass the check.

## Chapter 12: Recognizing Compiler Artifacts
*   **Task 1:** `ch12_task.exe` uses a massive `switch`. Ghidra shows the jump table calculation (`jmp qword ptr [rdx*8 + table_addr]`).
*   **Challenge 1:** `ch12_chal.exe` initializes a 1024-byte buffer using `memset`. Ghidra often decompiles this as a `rep stosb` loop.

## Chapter 13: Common Compiler Patterns
*   **Task 1:** `ch13_task.exe` is compiled with MinGW. Note the `.eh_frame` section and MinGW entry point.
*   **Challenge 1:** `ch13_chal.exe` is heavily optimized (`-O3`). The `inline_me()` function is missing; its logic was injected straight into `main()`.

## Chapter 14: Strings and Cross References
*   **Task 1:** In `ch14_task.exe`, search for the Unicode string "Secret Unicode String".
*   **Challenge 1:** In `ch14_chal.exe`, the "http" string is built byte-by-byte (`'h'`, `'t'`, `'t'`, `'p'`). It will not appear in a normal string search.

## Chapter 15: Practical Workflow
*   **Task 1:** `ch15_task.exe` is empty. Triage it in PE-Bear to see standard headers.
*   **Challenge 1:** In `ch15_chal.exe`, reverse the PIN check. Look for `cmp eax, 0x539`. `0x539` is `1337` in decimal.

## Chapter 16: Advanced Topics
*   **Task 1:** `ch16_task.exe` calls `IsDebuggerPresent()`. Break on the return, and change `RAX` from `1` to `0` to bypass the detection.
*   **Challenge 1:** `ch16_chal.exe` calls `VirtualProtect` on a global array to make it executable, then calls it. This is a classic shellcode runner.
