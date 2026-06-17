import os
import subprocess

# Ensure directories exist
os.makedirs("src", exist_ok=True)
os.makedirs("challenges", exist_ok=True)

challenges = {
    # Chapter 1
    "ch01_task.c": '#include <stdio.h>\nint main() { printf("Hello World!\\n"); /* Debug string: x64dbg_is_awesome */ return 0; }\n',
    "ch01_chal.c": '#include <windows.h>\nint main() { Sleep(100); return 0; }\n',

    # Chapter 2
    "ch02_task.c": 'char massive_data[1024*1024*5] = {1};\nint main() { return 0; }\n',
    "ch02_chal.c": 'int main() { return 0; }\n', # We will compile this with specific flags later

    # Chapter 3
    "ch03_task.c": '#include <windows.h>\n#include <wininet.h>\nint main() { InternetOpenA("Test", 0, NULL, NULL, 0); return 0; }\n',
    "ch03_chal.c": '#include <stdio.h>\n#include <windows.h>\nvoid NTAPI TlsCallback(PVOID DllHandle, DWORD Reason, PVOID Reserved) { if (Reason == DLL_PROCESS_ATTACH) { printf("I ran before main!\\n"); } }\nPIMAGE_TLS_CALLBACK pTlsCallback __attribute__((section(".CRT$XLB"))) = TlsCallback;\nint main() { printf("I am main!\\n"); return 0; }\n',

    # Chapter 4
    "ch04_task.c": '#include <stdio.h>\nint main() { printf("Trace me!\\n"); return 0; }\n',
    "ch04_chal.c": '#include <stdio.h>\nvoid __attribute__((constructor)) init() { printf("Global constructor!\\n"); }\nint main() { printf("Main!\\n"); return 0; }\n',

    # Chapter 5
    "ch05_task.c": '#include <stdio.h>\nint main(int argc, char** argv) { return 42; }\n',
    "ch05_chal.c": '#include <stdio.h>\nint main() { printf("Error: No arguments!\\n"); return 1; }\n',

    # Chapter 6
    "ch06_task.c": 'int global_secret = 1337;\nint main() { return global_secret; }\n',
    "ch06_chal.c": 'struct Data { int a; char b; };\nint main() { struct Data d = {1, \'a\'}; return d.a; }\n',

    # Chapter 7
    "ch07_task.c": 'int func(int a, int b, int c, int d, int e, int f) { return a+b+c+d+e+f; }\nint main() { return func(1,2,3,4,5,6); }\n',
    "ch07_chal.c": 'float func(float a, float b) { return a * b; }\nint main() { return (int)func(1.5f, 2.0f); }\n',

    # Chapter 8
    "ch08_task.c": 'int main() { volatile char buf[4096]; buf[0] = 1; return 0; }\n',
    "ch08_chal.c": 'int calc(int a) { int b = a + 5; return b; }\nint main() { return calc(10); }\n',

    # Chapter 9
    "ch09_task.c": '#include <stdio.h>\nvoid func() { volatile char buf[1024]; buf[0]=1; }\nint main() { func(); int* ptr = NULL; *ptr = 1; return 0; }\n',
    "ch09_chal.c": '#include <windows.h>\nLONG WINAPI Handler(EXCEPTION_POINTERS *ExceptionInfo) { return EXCEPTION_CONTINUE_SEARCH; }\nint main() { AddVectoredExceptionHandler(1, Handler); return 0; }\n',

    # Chapter 10
    "ch10_task.c": '#include <windows.h>\n#include <wincrypt.h>\nint main() { HCRYPTPROV hProv; CryptAcquireContext(&hProv, NULL, NULL, PROV_RSA_FULL, CRYPT_VERIFYCONTEXT); return 0; }\n',
    "ch10_chal.c": '#include <windows.h>\ntypedef int (WINAPI *MBox)(HWND, LPCSTR, LPCSTR, UINT);\nint main() { HMODULE h = LoadLibraryA("user32.dll"); MBox m = (MBox)GetProcAddress(h, "MessageBoxA"); if(m) m(0, "Hi", "Hi", 0); return 0; }\n',

    # Chapter 11
    "ch11_task.c": '#include <stdio.h>\nint main() { int sum = 0; for(int i=0; i<100; i++) sum += i; return sum; }\n',
    "ch11_chal.c": '#include <stdio.h>\n#include <string.h>\nint main() { char buf[32]; scanf("%31s", buf); if(strcmp(buf, "Secret123")==0) printf("Access Granted\\n"); else printf("Denied\\n"); return 0; }\n',

    # Chapter 12
    "ch12_task.c": '#include <stdio.h>\nint main() { int c = 5; switch(c) { case 1: return 1; case 2: return 2; case 3: return 3; case 4: return 4; case 5: return 5; case 6: return 6; default: return 0; } }\n',
    "ch12_chal.c": '#include <string.h>\nint main() { char buf[1024]; memset(buf, 0x41, sizeof(buf)); return 0; }\n',

    # Chapter 13
    "ch13_task.c": '#include <stdio.h>\nint main() { printf("Hello!\\n"); return 0; }\n', # We use GCC so std::string is tricky without g++, we'll just use printf for MinGW signature
    "ch13_chal.c": 'int inline_me(int a) { return a * 42; }\nint main() { return inline_me(5); }\n',

    # Chapter 14
    "ch14_task.c": '#include <windows.h>\nint main() { MessageBoxW(0, L"Secret Unicode String", L"Title", 0); return 0; }\n',
    "ch14_chal.c": 'int main() { volatile char str[5]; str[0]=\'h\'; str[1]=\'t\'; str[2]=\'t\'; str[3]=\'p\'; str[4]=0; return 0; }\n',

    # Chapter 15
    "ch15_task.c": '#include <windows.h>\nint main() { return 0; }\n',
    "ch15_chal.c": '#include <stdio.h>\nint main() { int p; scanf("%d", &p); if(p==1337) printf("Success!\\n"); return 0; }\n',

    # Chapter 16
    "ch16_task.c": '#include <windows.h>\n#include <stdio.h>\nint main() { if (IsDebuggerPresent()) printf("Debugger!\\n"); return 0; }\n',
    "ch16_chal.c": '#include <windows.h>\nunsigned char sc[] = {0x90, 0x90, 0xc3};\nint main() { DWORD old; VirtualProtect(sc, sizeof(sc), PAGE_EXECUTE_READWRITE, &old); void (*f)() = (void*)sc; f(); return 0; }\n'
}

for filename, content in challenges.items():
    with open(f"src/{filename}", "w") as f:
        f.write(content)

print("Source files created. Compiling...")

# Compilation commands
cmds = [
    # CH01
    "x86_64-w64-mingw32-gcc src/ch01_task.c -o challenges/ch01_task.exe",
    "x86_64-w64-mingw32-gcc src/ch01_chal.c -o challenges/ch01_chal.exe",
    # CH02
    "x86_64-w64-mingw32-gcc src/ch02_task.c -o challenges/ch02_task.exe",
    "x86_64-w64-mingw32-gcc src/ch02_chal.c -Wl,--image-base,0x00800000 -o challenges/ch02_chal.exe",
    # CH03
    "x86_64-w64-mingw32-gcc src/ch03_task.c -lwininet -o challenges/ch03_task.exe",
    "x86_64-w64-mingw32-gcc src/ch03_chal.c -o challenges/ch03_chal.exe",
    # CH04
    "x86_64-w64-mingw32-gcc src/ch04_task.c -o challenges/ch04_task.exe",
    "x86_64-w64-mingw32-gcc src/ch04_chal.c -o challenges/ch04_chal.exe",
    # CH05
    "x86_64-w64-mingw32-gcc src/ch05_task.c -s -o challenges/ch05_task.exe", # -s strips symbols
    "x86_64-w64-mingw32-gcc src/ch05_chal.c -o challenges/ch05_chal.exe",
    # CH06
    "x86_64-w64-mingw32-gcc -g src/ch06_task.c -o challenges/ch06_task.exe",
    "x86_64-w64-mingw32-gcc -g src/ch06_chal.c -o challenges/ch06_chal.exe",
    # CH07
    "x86_64-w64-mingw32-gcc src/ch07_task.c -o challenges/ch07_task.exe",
    "x86_64-w64-mingw32-gcc src/ch07_chal.c -o challenges/ch07_chal.exe",
    # CH08
    "x86_64-w64-mingw32-gcc src/ch08_task.c -o challenges/ch08_task.exe",
    "x86_64-w64-mingw32-gcc -O0 src/ch08_chal.c -o challenges/ch08_chal.exe",
    # CH09
    "x86_64-w64-mingw32-gcc src/ch09_task.c -o challenges/ch09_task.exe",
    "x86_64-w64-mingw32-gcc src/ch09_chal.c -o challenges/ch09_chal.exe",
    # CH10
    "x86_64-w64-mingw32-gcc src/ch10_task.c -o challenges/ch10_task.exe",
    "x86_64-w64-mingw32-gcc src/ch10_chal.c -o challenges/ch10_chal.exe",
    # CH11
    "x86_64-w64-mingw32-gcc src/ch11_task.c -o challenges/ch11_task.exe",
    "x86_64-w64-mingw32-gcc src/ch11_chal.c -o challenges/ch11_chal.exe",
    # CH12
    "x86_64-w64-mingw32-gcc src/ch12_task.c -o challenges/ch12_task.exe",
    "x86_64-w64-mingw32-gcc -O2 src/ch12_chal.c -o challenges/ch12_chal.exe",
    # CH13
    "x86_64-w64-mingw32-gcc src/ch13_task.c -o challenges/ch13_task.exe",
    "x86_64-w64-mingw32-gcc -O3 src/ch13_chal.c -o challenges/ch13_chal.exe",
    # CH14
    "x86_64-w64-mingw32-gcc src/ch14_task.c -o challenges/ch14_task.exe",
    "x86_64-w64-mingw32-gcc src/ch14_chal.c -o challenges/ch14_chal.exe",
    # CH15
    "x86_64-w64-mingw32-gcc src/ch15_task.c -o challenges/ch15_task.exe",
    "x86_64-w64-mingw32-gcc src/ch15_chal.c -o challenges/ch15_chal.exe",
    # CH16
    "x86_64-w64-mingw32-gcc src/ch16_task.c -o challenges/ch16_task.exe",
    "x86_64-w64-mingw32-gcc src/ch16_chal.c -o challenges/ch16_chal.exe"
]

for cmd in cmds:
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

print("All done!")
