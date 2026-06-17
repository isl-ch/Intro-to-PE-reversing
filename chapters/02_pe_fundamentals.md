# 2. Windows Executable Fundamentals

Before we look at code, we must understand the container that holds the code. On Linux, executables are typically ELF (Executable and Linkable Format) files. On Windows, they are **PE (Portable Executable)** files.

Every `.exe`, `.dll`, `.sys` (driver), and even `.scr` (screensaver) on Windows uses the PE format.

## What is a PE file?

A PE file is essentially a data structure that tells the Windows Loader how to map the file into memory and start executing it. It contains not just code, but metadata, imported functions, icons, and text strings.

### The Big Picture Structure

```text
+-------------------------+
| MS-DOS Header           | Starts with 'MZ' (0x5A4D)
+-------------------------+
| DOS Stub                | "This program cannot be run in DOS mode"
+-------------------------+
| NT Headers              | Starts with 'PE\0\0' (0x00004550)
|  - File Header          | Architecture, Number of Sections
|  - Optional Header      | Entry Point, Image Base, Subsystem
+-------------------------+
| Section Table (Headers) | Describes .text, .data, etc.
+-------------------------+
| Section 1 (.text)       | Executable Code
+-------------------------+
| Section 2 (.rdata)      | Read-only Data / Imports
+-------------------------+
| Section 3 (.data)       | Writable Data (Variables)
+-------------------------+
| Section 4 (.rsrc)       | Resources (Icons, Version Info)
+-------------------------+
```

### 1. MS-DOS Header and the MZ Signature

Historically, Windows ran on top of MS-DOS. For backward compatibility, every PE file starts with an MS-DOS header.
*   **The Signature:** The first two bytes of every valid PE file are always `MZ` (in hex: `4D 5A`), the initials of Mark Zbikowski, an early MS-DOS architect.
*   **The Pointer:** The most critical part of this header is the final 4 bytes (`e_lfanew`). This is an offset pointing to where the *real* PE header (NT Headers) begins.

### 2. NT Headers and PE Signature

This is the core of the format.
*   **The Signature:** It starts with the letters `PE` followed by two null bytes (`50 45 00 00`).
*   **File Header:** Contains basic info like the architecture (x86 vs x64) and the number of sections.
*   **Optional Header:** (It's not actually optional for executables). Crucial fields include:
    *   `AddressOfEntryPoint`: Where execution starts (not necessarily `main()`).
    *   `ImageBase`: The preferred memory address where the application wants to be loaded (e.g., `0x00400000`).
    *   `Subsystem`: Tells Windows if this is a GUI app (Windows Subsystem) or a terminal app (Console Subsystem).

### 3. The Section Table

A PE file is divided into blocks called **sections**. The section table is an array of headers describing these blocks. Common sections include:

*   `.text`: Contains the actual executable CPU instructions (your code). Marked as Read + Execute (RX).
*   `.data`: Contains initialized global and static variables. Marked as Read + Write (RW).
*   `.rdata` or `.rodata`: Read-only data. Holds string literals (e.g., `"Hello World"`) and constant values. Marked as Read (R).
*   `.idata`: Import tables (information about functions needed from other DLLs).
*   `.edata`: Export tables (functions this DLL provides to others).
*   `.rsrc`: Resources like icons, menus, dialogue layouts, and version information.
*   `.reloc`: Relocation information (explained below).
*   `.tls`: Thread Local Storage. Data specific to individual threads.

## Memory Terminology: RVA vs VA vs File Offset

This is the most common stumbling block for beginners.

When a PE file is sitting on your hard drive, it's just bytes on disk. When you run it, Windows loads those bytes into RAM (memory).

1.  **File Offset (Raw Address):** The physical location of a byte within the file on your hard drive. (e.g., "Byte 0x400 in notepad.exe").
2.  **Virtual Address (VA):** The absolute address of a byte in the process's memory after it's loaded. (e.g., "Address `0x00401000` in memory").
3.  **Relative Virtual Address (RVA):** The distance (offset) from the starting memory address of the loaded module.

**Formula:** `VA = ImageBase + RVA`

*Why RVAs?* If `notepad.exe` is loaded at `ImageBase` `0x10000000`, an RVA of `0x1000` means the VA is `0x10001000`. If ASLR (Address Space Layout Randomization) forces notepad to load at `0x50000000`, the RVA is *still* `0x1000`, but the new VA is `0x50001000`. RVAs make the executable position-independent.

### Alignment

Files on disk and mapped memory differ in alignment to optimize for disk space vs CPU efficiency.
*   **FileAlignment:** Usually 0x200 (512 bytes). Sections in the file are padded to multiples of 512.
*   **SectionAlignment (Memory):** Usually 0x1000 (4096 bytes - one page). Sections in memory are padded to multiples of 4KB.
*   *Consequence:* A byte's File Offset is rarely the same as its RVA. Reverse engineering tools handle this translation for you, but understanding it is critical.

## Crucial PE Mechanisms

### The Import Address Table (IAT)

Your program doesn't know how to print to the console or open a network socket; the OS does. Your program must call functions in Windows DLLs (like `kernel32.dll`).
The IAT is a table in your executable. The Windows Loader fills this table with the actual memory addresses of those DLL functions when your program starts.

### Relocations (`.reloc`)

If a program asks to be loaded at `0x00400000`, but that space is already taken, the Loader moves it somewhere else. If the code contains absolute memory addresses (e.g., `CALL 0x00401500`), those addresses will be wrong. The `.reloc` section contains a list of every place in the code where an absolute address needs to be "patched" or "relocated" by the Loader.

### TLS Callbacks

Thread Local Storage (TLS) has a feature called "callbacks". These are functions executed by the OS *before* the main Entry Point. Malware authors love TLS callbacks because they can run anti-debugging checks before the analyst's debugger hits the official starting point.

## Security Mitigations

*   **ASLR (Address Space Layout Randomization):** Randomizes the `ImageBase` every time the program runs, making exploit development (like Return Oriented Programming) harder because memory locations are unpredictable.
*   **DEP (Data Execution Prevention) / NX (No-eXecute):** Ensures that memory regions marked as data (like the stack or `.data` section) cannot be executed as code. This stops basic buffer overflow exploits that try to run shellcode injected into data areas.

---

## Challenges and Tasks

### Task 1: Exploring Headers
1. Open `challenges/ch02_task.exe` in a PE editor like PE-Bear.
2. Look at the Section Table. Notice the enormous Virtual Size of the `.data` section compared to its Raw Size. Why did the compiler do this?

### Challenge 1: Manual RVA Calculation
1. Open `challenges/ch02_chal.exe` in a PE editor.
2. Look at the Optional Header. Notice that the `ImageBase` is set to `0x00800000` (non-standard).
3. If the `.text` section starts at RVA `0x1000`, what is its expected Virtual Address in memory?
