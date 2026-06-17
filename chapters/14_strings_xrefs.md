# 14. Strings and Cross References

When reverse engineering an unknown binary, you rarely read it from the Entry Point all the way to the end. That would take years. Instead, you hunt for "anchors"—points of interest that immediately tell you what a specific piece of code does.

The most powerful anchors are **Strings**.

If you find the string "License Key Valid!", you don't need to read the entire program; you just need to find the code that references that string and analyze the `if/else` condition right above it.

## Types of Strings

1.  **ASCII Strings (C-Strings):**
    *   1 byte per character.
    *   Ends with a Null byte (`0x00`).
    *   Example "Hello": `48 65 6C 6C 6F 00`
2.  **Unicode Strings (Wide Strings / UTF-16LE):**
    *   Used extensively by the Windows OS.
    *   2 bytes per character.
    *   Ends with two Null bytes (`0x00 0x00`).
    *   Example "Hello": `48 00 65 00 6C 00 6C 00 6F 00 00 00`
3.  **Delphi/Pascal Strings:**
    *   The first byte (or word) indicates the length of the string, followed by the characters. Usually not null-terminated.

## Finding Strings in Tools

### Static Analysis (Ghidra)
1.  **Defined Strings:** Ghidra automatically searches the `.rdata` and `.data` sections for valid string sequences during its initial auto-analysis. Go to `Window -> Defined Strings`.
2.  **Search Memory:** If a string is obfuscated or packed, Ghidra might not find it automatically. Use `Search -> Memory` and search for byte patterns or specific text.
3.  **Create String manually:** If you see bytes in the memory view that look like a string but Ghidra missed it, select the bytes, right-click, `Data -> String` (or `TerminatedCString`).

### Dynamic Analysis (x64dbg)
1.  Right-click anywhere in the CPU view -> `Search for -> Current Module -> String references`.
2.  x64dbg scans the loaded memory for strings and shows you the assembly instructions that use them.

## The Power of Cross References (XREFs)

Finding a string is useless if you don't know where it's used. A **Cross Reference (XREF)** tells you "This memory address is referenced by that instruction."

If a string "File not found" is located at address `0x40A000`:
1.  In Ghidra, click on the string.
2.  Look at the "References" window (or press `Ctrl+Shift+F`).
3.  Ghidra will show you every `LEA` or `MOV` instruction in the `.text` section that points to `0x40A000`.
4.  Double-click the reference. You are now looking at the code that prints that error message!

## Obfuscated / Stack Strings

Malware authors know analysts look for strings. To hide them, they don't store the strings in the `.rdata` section.

Instead, they build the string character-by-character on the stack at runtime.
**Assembly Example:**
```assembly
mov byte ptr [rbp-0x10], 'm'
mov byte ptr [rbp-0xF], 'a'
mov byte ptr [rbp-0xE], 'l'
mov byte ptr [rbp-0xD], 'w'
mov byte ptr [rbp-0xC], 'a'
mov byte ptr [rbp-0xB], 'r'
mov byte ptr [rbp-0xA], 'e'
mov byte ptr [rbp-0x9], 0
```
*   **Static tools (like `strings.exe`)** will not see this because the string doesn't exist as a contiguous block in the file.
*   **Ghidra** will show you the individual `mov` instructions.
*   **Dynamic analysis** is the easiest way to defeat this. Put a breakpoint *after* this block of code, and just look at the stack memory. The string will be fully formed and readable.

---

## Challenges and Tasks

### Task 1: Wide Strings
1. Open `challenges/ch14_task.exe` in Ghidra.
2. Search for the string "Secret Unicode String". Ensure you are searching for UTF-16, not ASCII.

### Challenge 1: Defeating Stack Strings
1. Open `challenges/ch14_chal.exe` in Ghidra.
2. Look at `main()`. You will see individual byte assignments (`'h'`, `'t'`, `'t'`, `'p'`). This defeats standard string search tools.
