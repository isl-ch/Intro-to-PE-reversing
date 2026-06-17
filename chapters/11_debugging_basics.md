# 11. Debugging Basics (x64dbg)

Static analysis (Ghidra) is like reading a map. Dynamic analysis (x64dbg) is like driving the car. Both are necessary, but dynamic analysis lets you see exactly what happens in memory without having to mentally simulate complex CPU instructions.

x64dbg is the standard user-mode debugger for Windows reverse engineering. Let's cover the essential controls.

## The Interface

When you open an executable in x64dbg, you'll see a few main panels:
1.  **CPU (Disassembly):** The top-left. Shows the assembly instructions.
2.  **Registers:** The top-right. Shows the current value of RAX, RCX, RSP, RIP, etc.
3.  **Memory Dump:** The bottom-left. Lets you view raw hex values of memory addresses.
4.  **Stack:** The bottom-right. Shows the current stack frame.

## Essential Shortcuts

Memorize these. You will use them constantly.

*   `F9` (Run): Continue execution until the program exits, crashes, or hits a breakpoint.
*   `F2` (Toggle Breakpoint): Sets a software breakpoint on the currently selected instruction.
*   `F7` (Step Into): Execute one single instruction. If the instruction is a `CALL`, the debugger will go *inside* the called function.
*   `F8` (Step Over): Execute one single instruction. If the instruction is a `CALL`, the debugger will execute the *entire function* and pause on the instruction immediately after the call.
*   `Ctrl+F2` (Restart): Reloads the executable from the beginning.
*   `Ctrl+G` (Go to Expression): Jump to a specific memory address or API function (e.g., type `MessageBoxA`).

## Breakpoints

Breakpoints are how you force the debugger to pause execution at a location you care about.

### 1. Software Breakpoints (`F2` / `INT 3`)
When you press F2, x64dbg overwrites the first byte of the target instruction in memory with `0xCC` (the `INT 3` instruction). When the CPU hits `0xCC`, it throws an exception that x64dbg catches and pauses.
*   **Pros:** You can have unlimited software breakpoints.
*   **Cons:** Malware can easily detect them by scanning its own memory for `0xCC` bytes.

### 2. Hardware Breakpoints
Instead of modifying memory, hardware breakpoints use special debug registers built into the CPU (DR0, DR1, DR2, DR3).
*   **Pros:** Invisible to memory scans. They don't modify the code.
*   **Cons:** You can only have a maximum of 4 hardware breakpoints active at a time.
*   **How to set:** Right-click an instruction -> Breakpoint -> Hardware -> Execute.

### 3. Memory Breakpoints
You can tell the debugger to pause whenever a specific block of memory is Read from, Written to, or Executed.
*   **How:** In the Memory Dump, right-click a byte -> Breakpoint -> Hardware, Access/Write.

## Practical Debugging Maneuvers

### "Run to User Code"
When you start x64dbg, it usually pauses at the "System Breakpoint" deep inside `ntdll.dll` before the program has even loaded. Press `F9` once. It will then pause at the actual Entry Point of the executable.

### Inspecting Arguments
Right before you step over (`F8`) a `CALL` to a Windows API, look at the Registers panel. Remember the x64 calling convention:
*   RCX = Arg 1
*   RDX = Arg 2
*   R8 = Arg 3
*   R9 = Arg 4
You can right-click any register and choose "Follow in Dump" to see what string or data it points to.

### Changing Execution Flow (Patching)
If a program has a check like:
```assembly
cmp eax, 1         ; Did they enter the correct serial?
je good_boy        ; Jump if equal (ZF=1)
call bad_boy       ; Print "Wrong serial!"
```
You can force it to take the jump even if the serial is wrong!
1. Set a breakpoint on the `je` instruction.
2. Run until it hits.
3. Look at the Registers panel. Double-click the `ZF` (Zero Flag) and toggle it from 0 to 1.
4. Press F8. The CPU will now take the jump.

Alternatively, you can patch the assembly:
1. Select the `je` instruction.
2. Press Spacebar.
3. Change it to `jmp` (unconditional jump) or `nop` (do nothing).

---

## Challenges and Tasks

### Task 1: The First Trace
1. Open `challenges/ch11_task.exe` in x64dbg.
2. Hit `F9` to reach `main()`.
3. Use `F8` to step through the loop that counts to 100. Watch the registers update.

### Challenge 1: The "Always True" Patch
1. Open `challenges/ch11_chal.exe` in x64dbg.
2. Find the comparison instruction (`strcmp`).
3. Patch the jump instruction so that it always prints "Access Granted". Export the patched binary.
