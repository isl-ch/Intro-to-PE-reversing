# 6. Symbols and Debug Information

We briefly touched on symbols in the setup chapter, but understanding them deeply is vital for effective reverse engineering on Windows.

## What Are Symbols?

When a compiler translates C/C++ to machine code, the CPU doesn't care if a variable was named `user_password` or `x`. It only cares about memory addresses (e.g., `[RBP - 0x10]`).

**Debug Information** (Symbols) is the map that translates those raw addresses back into human-readable concepts. It contains:
*   Function names.
*   Global and local variable names.
*   Type information (e.g., "This address is a `struct Person` containing an `int` and a `char*`").
*   Source file and line number mappings (so the debugger knows which assembly instruction corresponds to line 42 of `main.c`).

## PDB Files (Program Database)

On Windows, debug information is stored separately from the `.exe` or `.dll` in a `.pdb` file.

*Why separate?* It keeps the executable small for users while allowing developers to debug crashes later. If an app crashes, the user sends a "dump file," and the developer loads it alongside their private PDB to see exactly where the crash happened.

### Public vs. Private Symbols

*   **Private Symbols:** Contain everything: local variables, private functions, source line numbers. Developers keep these secret.
*   **Public Symbols:** Stripped down. They typically only contain the names of exported functions and major global variables. Microsoft's public symbol server provides public PDBs. They won't tell you the names of local variables inside `ntdll.dll`, but they will tell you the names of all the internal API functions.

## How Tools Use Symbols

### In x64dbg
When x64dbg loads an executable or DLL, it checks the PE headers for a debug directory. This directory contains a GUID and the original path of the PDB file. x64dbg uses this GUID to request the matching PDB from the configured symbol server.
*   Once loaded, the disassembly will replace raw addresses with function names (e.g., `CALL ntdll.ZwAllocateVirtualMemory`).

### In Ghidra
Ghidra also supports downloading and applying PDBs (`File -> Download PDB`). When applied, Ghidra uses the type information in the PDB to dramatically improve its decompilation, automatically creating structures and naming variables.

## Working Without Symbols

In malware analysis and CTFs, you almost never have PDBs for the target binary. You only have symbols for the OS DLLs it calls.

When symbols are missing, you must rely on:
1.  **API Calls:** "This function calls `InternetOpenUrl`, it's probably related to networking."
2.  **Strings:** "This function references 'Admin Rights Required', it's probably an access check."
3.  **Constants:** "This function uses the constant `0xEDB88320`. A quick Google search shows that's the polynomial for CRC32 hashing." (Ghidra's FindCrypt plugin automates this).

---

## Challenges and Tasks

### Task 1: Examining the Debug Directory
1. Open `challenges/ch06_task.exe` in a PE editor.
2. Locate the "Debug Directory". This binary was compiled with DWARF symbols.

### Challenge 1: Ghidra with Symbols
1. Open `challenges/ch06_chal.exe` in Ghidra.
2. Because it was compiled with debug symbols, notice how Ghidra automatically creates the `Data` struct and names the variables correctly in the decompilation.
