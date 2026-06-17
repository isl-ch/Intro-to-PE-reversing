# 13. Common Compiler Patterns

Different compilers generate different assembly code. Recognizing whether a binary was compiled with MSVC, MinGW (GCC), or Clang can give you huge hints about where to look for `main` and how strings or exceptions are handled.

## MSVC (Microsoft Visual C++)

This is the standard compiler for Windows. Most commercial software and a lot of malware are compiled with MSVC.

### Signatures
*   **Startup Code:** Uses `mainCRTStartup` / `WinMainCRTStartup`. The "Three Args and Exit" pattern (discussed in Chapter 5) is highly reliable.
*   **Security Cookie:** Very prominent use of `__security_init_cookie` and `__security_check_cookie`.
*   **Exception Handling:** `.pdata` and `.xdata` are standard. C++ uses `CxxFrameHandler`.
*   **String Implementation:** Uses Small String Optimization (SSO) with a threshold of 16 characters.

## MinGW (Minimalist GNU for Windows)

MinGW is essentially GCC ported to Windows. It is extremely popular in the open-source community, cross-platform development, and among malware authors who write code on Linux but target Windows.

### Signatures
*   **Startup Code:** The entry point is usually called `__tmainCRTStartup`. It looks very different from MSVC. It often has a massive, complex setup routine involving pseudo-relocations. Finding `main()` requires looking past a lot of MinGW-specific initialization (e.g., `__main` is often called *inside* the user's `main()` to initialize global constructors).
*   **Sections:** MinGW binaries often have `.eh_frame` and `.gcc_except_table` sections alongside the standard PE sections, as it relies on DWARF exception handling logic ported from Linux.
*   **Function Prologues:** Tends to rely more heavily on standard `push rbp; mov rbp, rsp` prologues compared to heavily optimized MSVC FPO.
*   **Strings:** GCC's `std::string` implementation historically uses a threshold of 15 characters for SSO.

## Clang / LLVM

Clang is becoming increasingly popular on Windows (even Microsoft supports it now). It generates highly optimized code that sometimes resembles MSVC (when compiling with MSVC compatibility) or GCC (when targeting MinGW).

### Signatures
*   **Optimizations:** Clang is aggressive with optimizations. It will inline functions relentlessly.
*   **Control Flow:** Clang sometimes generates more convoluted control flow graphs (CFGs) for simple loops compared to MSVC, attempting to optimize for branch prediction.
*   **Vectorization:** If you compile math-heavy code, Clang will almost certainly try to vectorize it using SIMD (XMM/YMM) registers, making the assembly look incredibly complex.

## Recognizing Go and Rust

While technically not C/C++ compilers, you will encounter them constantly.

### Go (Golang)
*   **Massive Binaries:** Even a "Hello World" is several megabytes because Go statically links its entire massive runtime (Garbage Collector, Scheduler, networking).
*   **Custom Calling Convention:** Older Go binaries use a stack-based calling convention (even on x64). Newer ones use a register-based convention, but it is *not* the standard Windows x64 ABI.
*   **Strings:** Go strings are not null-terminated. They are structs containing a pointer to the string data and an integer length.

### Rust
*   **Similar to C++:** Rust uses LLVM as its backend, so the assembly looks similar to Clang-compiled C++.
*   **Panics:** You will see a lot of checks leading to a "panic" handler (e.g., bounds checking on arrays).
*   **Name Mangling:** Rust function names are heavily mangled (e.g., `_ZN3std2io5stdio6_print17h...`).

---

## Challenges and Tasks

### Task 1: Identify the Compiler
1. Open `challenges/ch13_task.exe` in Ghidra or a PE viewer.
2. Look at the sections. You will see MinGW/GCC specific sections (like `.eh_frame`).

### Challenge 1: Inlining Optimization
1. Open `challenges/ch13_chal.exe` in Ghidra. This was compiled with `-O3`.
2. Notice that the `inline_me()` function doesn't actually exist as a separate callable function; the math (`* 42`) is done directly inside `main()`.
