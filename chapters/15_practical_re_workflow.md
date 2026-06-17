# 15. Practical Reverse Engineering Workflow

You now have the puzzle pieces. This chapter puts them together into a standard, repeatable methodology for analyzing a completely unknown Windows PE file.

Whether you are facing a CTF crackme or a suspicious email attachment, the initial workflow is always the same.

## Phase 1: Triage (Static Analysis)

**Do not run the executable yet.**

1.  **Inspect the Headers:**
    *   Open the file in a PE editor (like PE-Bear).
    *   Check the Architecture (32-bit vs 64-bit). This dictates which version of Ghidra/x64dbg you will use.
    *   Look at the Sections. Are there weird section names (e.g., `.upx0`, `.vmp0`)? Are the virtual sizes vastly larger than the raw sizes? If so, the file is probably **packed**.
2.  **Examine Imports:**
    *   What DLLs does it load?
    *   `ws2_32.dll` or `wininet.dll` -> It talks to the internet.
    *   `advapi32.dll` (specifically `RegOpenKey`) -> It modifies the registry.
    *   If the import table is almost empty (only `LoadLibrary` and `GetProcAddress`), it's hiding its API usage dynamically.
3.  **Find the Strings:**
    *   Run `strings` or look at them in your PE viewer.
    *   Look for IP addresses, URLs, file paths, or telltale messages ("Access Denied", "Connecting to C2...").
4.  **Drop it into Ghidra:**
    *   Run the auto-analyzer.
    *   Identify the compiler (MSVC, MinGW, Go?).
    *   If it's MSVC, locate `main()` using the "Three Args and Exit" pattern.
    *   Rename the function to `main`.
    *   Look at the Cross References for the interesting strings you found in step 3.

## Phase 2: Hypothesis and Navigation

At this point, you should have a hypothesis. ("This is a keylogger that saves to `C:\temp\log.txt` and sends data to `http://evil.com`").

1.  **Find the Core Logic:** Navigate from `main()` down into the functions that do the heavy lifting.
2.  **Ignore the Noise:** Skip over CRT initialization, stack cookies, and obvious compiler boilerplate (`memset`, etc.).
3.  **Rename and Retype:** As you figure out what a function does, rename it in Ghidra (e.g., rename `FUN_00401500` to `EncryptData`). If you figure out a function's arguments, change its signature in Ghidra.

## Phase 3: Dynamic Verification (Debugging)

Static analysis only gets you so far. When the code gets too complex (e.g., heavy math, obfuscation, dynamic API resolution), it's time to run it.

1.  **Snapshot your VM.**
2.  **Open in x64dbg.**
3.  **Set Strategic Breakpoints:**
    *   Set a breakpoint on `main()` (you found the address in Ghidra!).
    *   Set breakpoints on interesting APIs (e.g., `Ctrl+G` -> type `CreateFileW` -> `F2`).
4.  **Run (`F9`) and Trace:**
    *   When a breakpoint hits, look at the Registers and Stack to inspect the arguments.
    *   Step Over (`F8`) complex functions. If the output of the function looks important, restart and Step Into (`F7`) it.
5.  **Modify Memory (If needed):**
    *   Force jumps to bypass anti-debugging checks or license verifications.

## Example Scenario: A Simple Crackme

Imagine a program that asks for a serial key.
1.  **Static:** Find the string "Invalid Key!". Follow its XREF to a function.
2.  **Static:** Look slightly above the string reference. You see a `strcmp` (or similar comparison) and a conditional jump (`JE` or `JNE`).
3.  **Dynamic:** Open x64dbg. Set a breakpoint on the `strcmp` instruction.
4.  **Dynamic:** Run the program. Type a fake key ("123456").
5.  **Dynamic:** When the breakpoint hits, look at the arguments to `strcmp` (RCX and RDX). One will be your fake key "123456". The other will be the *real* key sitting right there in memory!

---

## Challenges and Tasks

### Task 1: The Full Triage
1. Open `challenges/ch15_task.exe` in a PE viewer and string extractor (do not use Ghidra).
2. Perform Phase 1 (Triage) to identify its architecture and imports.

### Challenge 1: The Crackme Simulation
1. Open `challenges/ch15_chal.exe` in x64dbg.
2. Find the logic comparing your input to `1337`.
3. Patch the binary so that entering the *wrong* PIN prints "Success!".
