# 1. Environment Setup

Before diving into the assembly code and memory layouts of Windows executables, you need a safe and capable laboratory. Reverse engineering often involves analyzing potentially malicious or simply broken code. Running this on your host machine is a recipe for disaster.

This chapter covers building your analysis environment and setting up the core tools.

## The Analysis Virtual Machine

**Why a VM?** 
*   **Safety:** Malware is contained.
*   **Snapshotting:** You can save a state before running a suspect executable and revert back to a clean state instantly.
*   **Control:** You can disconnect it from the network or monitor its traffic.

**Setting it up:**
1.  **Hypervisor:** Install VirtualBox, VMware Workstation Player, or Hyper-V on your host OS.
2.  **OS:** Install a 64-bit Windows 10 or Windows 11 VM.
3.  **Guest Additions:** Install VMware Tools or VirtualBox Guest Additions for better resolution and clipboard sharing.
4.  **Disable Defender (Carefully):** For analyzing crackmes and certain tools, Windows Defender might intervene. You can disable real-time protection, but remember the risks. Use specific exclusion folders for your tools.

> [!CAUTION]
> Always assume malware can escape a VM. If analyzing sophisticated malware, ensure the VM is strictly isolated from your host network (Host-Only networking or fully disabled network adapter).

## Core Reversing Tools

### 1. Ghidra (Static Analysis)

Ghidra is a powerful, open-source software reverse engineering (SRE) suite developed by the NSA. We use it for **static analysis**—analyzing the code without running it.

*   **Installation:** Requires Java (JDK 17+). Download the release zip, extract it, and run `ghidraRun.bat`.
*   **Why Ghidra?** It has an excellent decompiler that translates assembly back into a C-like approximation.
*   **Useful Extensions:** 
    *   FindCrypt: Helps locate cryptographic constants.

### 2. x64dbg (Dynamic Analysis)

x64dbg (and its 32-bit counterpart, x32dbg) is the standard open-source user-mode debugger for Windows. We use it for **dynamic analysis**—running the program and watching what happens.

*   **Installation:** Download the latest snapshot, extract, and you're good to go.
*   **Why x64dbg?** It's highly visual, intuitive, and modern compared to older tools like OllyDbg.
*   **Linux Comparison:** It's like GDB but with a full GUI, memory maps, and visual call stacks out-of-the-box.

### 3. WinDbg (System/Kernel Debugging)

WinDbg is Microsoft's official debugger. While x64dbg is great for user-mode applications, WinDbg is the king of kernel debugging and analyzing crashes (dump files).

*   **Installation:** Available via the Microsoft Store ("WinDbg Preview" or just "WinDbg") or the Windows SDK.
*   **Usage:** It relies heavily on command-line inputs (e.g., `!peb`, `k`, `lm`). It has a steeper learning curve than x64dbg.

## Symbols and Debug Information

When a developer compiles code (e.g., in Visual Studio), the compiler translates readable C/C++ into machine code. In the process, variable names, function names, and line numbers are often stripped away to make the executable smaller and faster.

*   **Release Build:** Highly optimized. Stripped of most human-readable information.
*   **Debug Build:** Less optimized. Contains or points to debug information, allowing the debugger to show exactly which line of C code corresponds to the current assembly instruction.

### Symbol Servers

To make debugging its own OS easier, Microsoft hosts a public **Symbol Server**. This server provides `.pdb` (Program Database) files containing the names of functions and variables for Windows system DLLs (like `kernel32.dll` and `ntdll.dll`).

Without symbols, a call into the OS looks like:
`CALL 0x00007FFD81A42100`

With symbols, the debugger resolves it to:
`CALL kernel32.CreateFileW`

**Configuring the Microsoft Symbol Server:**

In **x64dbg**:
1.  Go to `Options -> Preferences`.
2.  Go to the `Symbol` tab.
3.  Ensure the "Symbol Path" includes: `srv*C:\Symbols*https://msdl.microsoft.com/download/symbols`.

In **Ghidra**:
1.  When analyzing a file, Ghidra will often prompt or allow you to download PDBs via `File -> Download PDB`.

## Chapter Summary

Your workflow usually starts by dropping an executable into Ghidra to get a sense of its structure (static), and then loading it into x64dbg to watch its execution flow and inspect memory live (dynamic).

---

## Challenges and Tasks

### Task 1: Setting up the Lab
1. Take a base "Clean State" VM snapshot.
2. Open `challenges/ch01_task.exe` in x64dbg. Ensure it pauses at the system breakpoint.
3. Look in the memory dump or string references for the hidden string `x64dbg_is_awesome` to confirm your setup.

### Challenge 1: The First Trace
1. Open `challenges/ch01_chal.exe` in x64dbg.
2. Find the call to `Sleep()`.
3. Use the "Symbols" tab to verify that `kernel32.dll` symbols are loaded correctly.
