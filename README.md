# Reverse Engineering Windows Executables: A Practical Guide

Welcome to this comprehensive, beginner-friendly introduction to reverse engineering Windows executables. If you have some basic C/C++ and assembly knowledge, but lack Windows internals experience, this tutorial is designed for you.

Instead of a dry reference manual, this guide is structured as a progressive learning path. You'll build your intuition layer by layer, starting from the environment setup, delving into how Windows loads binaries, navigating the initial execution sequence, and finally practical debugging and reversing. 

Whether your goal is malware analysis, cracking crackmes, CTFs, or general curiosity, this guide will provide the foundation you need.

## Table of Contents

1.  **[Environment Setup](chapters/01_environment_setup.md)**
2.  **[Windows Executable Fundamentals](chapters/02_pe_fundamentals.md)**
3.  **[The Loading Process](chapters/03_loading_process.md)**
4.  **[What Happens Before main()](chapters/04_before_main.md)**
5.  **[Finding main()](chapters/05_finding_main.md)**
6.  **[Symbols and Debug Information](chapters/06_symbols_debug.md)**
7.  **[x64 Calling Convention](chapters/07_x64_calling_convention.md)**
8.  **[Stack Frames and Functions](chapters/08_stack_frames.md)**
9.  **[Exception Handling](chapters/09_exception_handling.md)**
10. **[Imports and API Calls](chapters/10_imports_api.md)**
11. **[Debugging Basics](chapters/11_debugging_basics.md)**
12. **[Recognizing Compiler Artifacts](chapters/12_recognizing_compiler_artifacts.md)**
13. **[Common Compiler Patterns](chapters/13_common_compiler_patterns.md)**
14. **[Strings and Cross References](chapters/14_strings_xrefs.md)**
15. **[Practical Reverse Engineering Workflow](chapters/15_practical_re_workflow.md)**
16. **[Advanced Topics Overview](chapters/16_advanced_topics.md)**

## How to use this guide

*   **Read sequentially**: Chapters build upon previous knowledge.
*   **Do the exercises**: At the end of each chapter, you'll find challenges and tasks. Don't skip them!
*   **Get hands-on**: Have your virtual machine, Ghidra, and x64dbg open while reading.

Let's get started!
