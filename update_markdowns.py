import glob
import re

new_challenges = {
    "01": """## Challenges and Tasks

### Task 1: Setting up the Lab
1. Take a base "Clean State" VM snapshot.
2. Open `challenges/ch01_task.exe` in x64dbg. Ensure it pauses at the system breakpoint.
3. Look in the memory dump or string references for the hidden string `x64dbg_is_awesome` to confirm your setup.

### Challenge 1: The First Trace
1. Open `challenges/ch01_chal.exe` in x64dbg.
2. Find the call to `Sleep()`.
3. Use the "Symbols" tab to verify that `kernel32.dll` symbols are loaded correctly.
""",
    "02": """## Challenges and Tasks

### Task 1: Exploring Headers
1. Open `challenges/ch02_task.exe` in a PE editor like PE-Bear.
2. Look at the Section Table. Notice the enormous Virtual Size of the `.data` section compared to its Raw Size. Why did the compiler do this?

### Challenge 1: Manual RVA Calculation
1. Open `challenges/ch02_chal.exe` in a PE editor.
2. Look at the Optional Header. Notice that the `ImageBase` is set to `0x00800000` (non-standard).
3. If the `.text` section starts at RVA `0x1000`, what is its expected Virtual Address in memory?
""",
    "03": """## Challenges and Tasks

### Task 1: Locating the True Entry Point
1. Open `challenges/ch03_task.exe` in Ghidra.
2. Let auto-analysis finish. Look at the Imports tree and note `wininet.dll`.
3. Find the Entry Point and see the compiler-generated boilerplate.

### Challenge 1: TLS Callback Hunting
1. Open `challenges/ch03_chal.exe` in Ghidra or a PE editor.
2. Check the "Data Directories" in the Optional Header. Look for the "TLS Table" entry.
3. Run the binary in a normal terminal. Notice that it prints "I ran before main!" before "I am main!".
""",
    "04": """## Challenges and Tasks

### Task 1: Exploring Startup Code
1. Open `challenges/ch04_task.exe` in Ghidra.
2. Go to the Entry Point.
3. Trace through the MinGW startup functions to find the call to your `main()`.

### Challenge 1: Global Constructor Hunt
1. Open `challenges/ch04_chal.exe` in x64dbg.
2. Break on the string "Global constructor!".
3. Notice this happens before you ever reach `main()`.
""",
    "05": """## Challenges and Tasks

### Task 1: Finding main() in a Stripped Binary
1. Open `challenges/ch05_task.exe` in Ghidra. This binary has been stripped of symbols.
2. Use the "Three Args and Exit" pattern to find the true `main()`. Rename the function in Ghidra once you find it.

### Challenge 1: The String Trace
1. Open `challenges/ch05_chal.exe` in Ghidra.
2. Find the string "Error: No arguments!".
3. Use Cross References to locate the function containing this string. Verify this is `main()`.
""",
    "06": """## Challenges and Tasks

### Task 1: Examining the Debug Directory
1. Open `challenges/ch06_task.exe` in a PE editor.
2. Locate the "Debug Directory". This binary was compiled with DWARF symbols.

### Challenge 1: Ghidra with Symbols
1. Open `challenges/ch06_chal.exe` in Ghidra.
2. Because it was compiled with debug symbols, notice how Ghidra automatically creates the `Data` struct and names the variables correctly in the decompilation.
""",
    "07": """## Challenges and Tasks

### Task 1: Identifying Arguments
1. Open `challenges/ch07_task.exe` in x64dbg or Ghidra.
2. Find the function that adds 6 numbers together.
3. Identify how the 5th and 6th arguments are passed on the stack.

### Challenge 1: Floating Point Arguments
1. Open `challenges/ch07_chal.exe` in Ghidra.
2. Look at the function that takes floats. Notice that `RCX` and `RDX` are not used; instead, `XMM0` and `XMM1` are used.
""",
    "08": """## Challenges and Tasks

### Task 1: Prologue Identification
1. Open `challenges/ch08_task.exe` in Ghidra.
2. Look at `main()`. Notice the massive `sub rsp, 0x1000` prologue used to allocate the 4096-byte local array.

### Challenge 1: Manual Stack Reversal
1. Open `challenges/ch08_chal.exe` in Ghidra.
2. Look at the unoptimized assembly for `calc()`. Observe how it uses `RBP` to store the argument and retrieve the local variable.
""",
    "09": """## Challenges and Tasks

### Task 1: Locating .pdata
1. Open `challenges/ch09_task.exe` in a PE editor.
2. Find the `.pdata` section. This table proves the executable uses table-based exception handling.

### Challenge 1: The VEH Breakpoint
1. Open `challenges/ch09_chal.exe` in Ghidra.
2. Notice the call to `AddVectoredExceptionHandler`. This allows the program to catch exceptions globally before standard `try/catch` blocks.
""",
    "10": """## Challenges and Tasks

### Task 1: Analyzing Imports
1. Open `challenges/ch10_task.exe` in Ghidra.
2. Look at its Import Table. Identify the cryptography API (`CryptAcquireContext`).

### Challenge 1: The Hidden Import
1. Open `challenges/ch10_chal.exe` in Ghidra.
2. Verify that `MessageBoxA` does *not* appear in the Import Table.
3. Observe how `LoadLibraryA` and `GetProcAddress` are used dynamically.
""",
    "11": """## Challenges and Tasks

### Task 1: The First Trace
1. Open `challenges/ch11_task.exe` in x64dbg.
2. Hit `F9` to reach `main()`.
3. Use `F8` to step through the loop that counts to 100. Watch the registers update.

### Challenge 1: The "Always True" Patch
1. Open `challenges/ch11_chal.exe` in x64dbg.
2. Find the comparison instruction (`strcmp`).
3. Patch the jump instruction so that it always prints "Access Granted". Export the patched binary.
""",
    "12": """## Challenges and Tasks

### Task 1: The Switch Statement
1. Open `challenges/ch12_task.exe` in Ghidra.
2. Locate the `JMP` instruction that uses the jump table for the massive switch statement.

### Challenge 1: Recognizing `memset`
1. Open `challenges/ch12_chal.exe` in Ghidra.
2. Search for the `rep stosq` or `rep stosb` instruction used to quickly zero out or initialize the large buffer.
""",
    "13": """## Challenges and Tasks

### Task 1: Identify the Compiler
1. Open `challenges/ch13_task.exe` in Ghidra or a PE viewer.
2. Look at the sections. You will see MinGW/GCC specific sections (like `.eh_frame`).

### Challenge 1: Inlining Optimization
1. Open `challenges/ch13_chal.exe` in Ghidra. This was compiled with `-O3`.
2. Notice that the `inline_me()` function doesn't actually exist as a separate callable function; the math (`* 42`) is done directly inside `main()`.
""",
    "14": """## Challenges and Tasks

### Task 1: Wide Strings
1. Open `challenges/ch14_task.exe` in Ghidra.
2. Search for the string "Secret Unicode String". Ensure you are searching for UTF-16, not ASCII.

### Challenge 1: Defeating Stack Strings
1. Open `challenges/ch14_chal.exe` in Ghidra.
2. Look at `main()`. You will see individual byte assignments (`'h'`, `'t'`, `'t'`, `'p'`). This defeats standard string search tools.
""",
    "15": """## Challenges and Tasks

### Task 1: The Full Triage
1. Open `challenges/ch15_task.exe` in a PE viewer and string extractor (do not use Ghidra).
2. Perform Phase 1 (Triage) to identify its architecture and imports.

### Challenge 1: The Crackme Simulation
1. Open `challenges/ch15_chal.exe` in x64dbg.
2. Find the logic comparing your input to `1337`.
3. Patch the binary so that entering the *wrong* PIN prints "Success!".
""",
    "16": """## Challenges and Tasks

### Task 1: Anti-Debugging
1. Open `challenges/ch16_task.exe` in x64dbg.
2. Notice how it calls `IsDebuggerPresent()`. Step over it and modify the return value in `RAX` to spoof the check.

### Challenge 1: Shellcode Execution
1. Open `challenges/ch16_chal.exe` in Ghidra.
2. Notice how it changes memory protections (`VirtualProtect`) on a global byte array and then casts it to a function pointer to execute it (this is how shellcode runners operate).
"""
}

for i in range(1, 17):
    prefix = f"{i:02d}"
    
    # Find the corresponding file
    files = glob.glob(f"chapters/{prefix}_*.md")
    if not files:
        continue
        
    filepath = files[0]
    
    with open(filepath, "r") as f:
        content = f.read()
        
    # Replace everything from "## Challenges and Tasks" onwards
    new_content = re.sub(r"## Challenges and Tasks.*", new_challenges[prefix], content, flags=re.DOTALL)
    
    with open(filepath, "w") as f:
        f.write(new_content)

print("Updated all markdown files.")
