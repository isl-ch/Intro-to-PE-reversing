# 5. Finding main()

The first major goal when reversing an unknown executable is usually finding `main()` (or `WinMain()` for GUI apps). As we've seen, you can't just look at the Entry Point and expect user code.

If you have symbols (PDBs), finding `main` is trivial. But in malware analysis or CTFs, binaries are almost always "stripped" (symbols removed).

Here are the most common methods for finding the start of user code.

## Method 1: The "Three Args and Exit" Pattern

In the previous chapter, we noted that the CRT calls `main` and then immediately calls `exit`. This is the most reliable static analysis method for MSVC binaries.

1.  Go to the Entry Point in Ghidra.
2.  Scroll down to the bottom of the function.
3.  Look for a `CALL` instruction, immediately followed by another `CALL`.
4.  If the second `CALL` looks like it terminates the program (it might eventually call `ExitProcess`), the first `CALL` is highly likely to be `main`.

In MSVC x64, you often see three registers being set up right before this call (for `argc`, `argv`, `envp`):

```assembly
mov ecx, dword ptr [argc]
mov rdx, qword ptr [argv]
mov r8, qword ptr [envp]
call FUN_00401500  ; <--- This is main()
call FUN_00402100  ; <--- This is exit()
```

## Method 2: Following Strings

Programs often print banners, usage instructions, or error messages early in their execution.

1.  In Ghidra, open the **Defined Strings** window (`Window -> Defined Strings`).
2.  Search for strings that look like they belong in user code (e.g., "Usage: program.exe -f file", "Welcome to the crackme", "Invalid license").
3.  Double-click the string to go to its location in the `.rdata` or `.data` section.
4.  Find **Cross References (XREFs)** to that string. In Ghidra, right-click the string address -> `References -> Show References to Address`.
5.  Follow the reference to the code that uses the string.
6.  If you trace the function calls backwards from there, you will often arrive at `main()`.

## Method 3: Dynamic Tracing (Stepping in x64dbg)

If static analysis is confusing (maybe the binary is packed or obfuscated), use a debugger.

1.  Open the binary in x64dbg. You will start at the Entry Point.
2.  Use **Step Over** (F8) to execute instructions one by one.
3.  Pay attention to calls. If you step over a call and the program does something visible (prints to console, opens a window, creates a file), you know `main` is somewhere inside that call!
4.  Restart the program (Ctrl+F2). This time, when you reach that same call, use **Step Into** (F7) to go inside it.
5.  Repeat this process, drilling down until you find the core logic.

## Why main() Might Not Be Obvious

*   **GUI Applications (`WinMain`):** GUI apps don't use `argc` and `argv` in the same way. Their startup code looks slightly different, often involving a call to `GetModuleHandleA` before `WinMain`.
*   **Go and Rust Binaries:** These languages do not use the C Runtime. They have massive, complex runtimes of their own. Finding the true user entry point in Go or Rust binaries requires specific techniques (often relying on runtime-specific signatures).
*   **Packers/Crypters:** If the binary is packed (e.g., UPX), the Entry Point points to the unpacking stub, not the CRT or user code. The unpacker will run, decrypt the real program into memory, and then perform a "Tail Jump" (JMP) to the real Original Entry Point (OEP).

---

## Challenges and Tasks

### Task 1: Finding main() in a Stripped Binary
1. Open `challenges/ch05_task.exe` in Ghidra. This binary has been stripped of symbols.
2. Use the "Three Args and Exit" pattern to find the true `main()`. Rename the function in Ghidra once you find it.

### Challenge 1: The String Trace
1. Open `challenges/ch05_chal.exe` in Ghidra.
2. Find the string "Error: No arguments!".
3. Use Cross References to locate the function containing this string. Verify this is `main()`.
