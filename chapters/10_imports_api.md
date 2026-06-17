# 10. Imports and API Calls

No Windows program is an island. To do anything useful—read a file, show a window, allocate memory—a program must ask the Operating System for help. It does this by calling Windows APIs exported by standard DLLs.

Identifying which APIs a program calls is the fastest way to understand what it does.

## The Holy Trinity of Windows DLLs

Almost every Windows executable imports from one or more of these three core libraries:

1.  **`kernel32.dll`**: The foundation. It provides core functionality: memory management (`VirtualAlloc`), file I/O (`CreateFile`, `ReadFile`), process/thread creation (`CreateProcess`), and synchronization.
    *   *Note:* `kernel32.dll` actually passes most of its work down to `ntdll.dll`.
2.  **`user32.dll`**: The User Interface. Handles windows, menus, buttons, cursors, and user input (mouse/keyboard). If you see a GUI, this is involved. (`MessageBoxA`, `CreateWindowEx`).
3.  **`advapi32.dll`**: Advanced APIs. Handles the Registry (`RegOpenKeyEx`), Service Manager, and Security/Cryptography.

### `ntdll.dll` (The Native API)
This is the lowest user-mode layer. It translates user-mode API calls into system calls (syscalls) that transition into the Windows Kernel.
*   Functions here usually start with `Nt` or `Zw` (e.g., `NtAllocateVirtualMemory`).
*   Malware often calls `ntdll.dll` directly to bypass hooks that security software places on `kernel32.dll`.

## Static vs Dynamic Imports

### Static Imports (The Import Address Table)
This is the standard method described in Chapter 2. The executable's header lists the DLLs and functions it needs. When the program starts, the Windows Loader fills the IAT with the memory addresses of these functions.
*   **In Ghidra:** Look at the "Symbol Tree" -> "Imports". You will see a clear list of every function the program requested.

### Dynamic Imports (`LoadLibrary` & `GetProcAddress`)
Malware authors know analysts look at the Import Table. To hide their intentions, they leave the Import Table empty.

Instead, they resolve APIs dynamically while the program is running:
1.  They call `LoadLibraryA("wininet.dll")` to load the networking DLL into memory.
2.  They call `GetProcAddress(handle, "InternetOpenUrlA")` to find the address of the specific function they want.
3.  They call the function via a function pointer.

*   **In Ghidra:** If an executable has almost no imports, but you see `LoadLibrary` and `GetProcAddress`, it is dynamically resolving its APIs.

## API Naming Conventions (A vs W)

You will frequently see two versions of the same API:
*   `MessageBoxA`: The **A** stands for ANSI (ASCII). It expects strings where each character is 1 byte.
*   `MessageBoxW`: The **W** stands for Wide (Unicode/UTF-16). It expects strings where each character is 2 bytes.

Modern Windows uses Unicode natively. Calling `MessageBoxA` just forces Windows to convert your ASCII string to Unicode before passing it to `MessageBoxW` under the hood.

## Delayed Imports

Sometimes, a program doesn't want to load a heavy DLL when it starts because it might not even use it.
A **Delay-Loaded Import** is an import that isn't resolved by the Loader at startup. Instead, the compiler inserts a small "stub". The *first time* the program calls the function, the stub pauses execution, calls `LoadLibrary`/`GetProcAddress`, updates the function pointer, and then executes the function.

---

## Challenges and Tasks

### Task 1: Analyzing Imports
1. Open `challenges/ch10_task.exe` in Ghidra.
2. Look at its Import Table. Identify the cryptography API (`CryptAcquireContext`).

### Challenge 1: The Hidden Import
1. Open `challenges/ch10_chal.exe` in Ghidra.
2. Verify that `MessageBoxA` does *not* appear in the Import Table.
3. Observe how `LoadLibraryA` and `GetProcAddress` are used dynamically.
