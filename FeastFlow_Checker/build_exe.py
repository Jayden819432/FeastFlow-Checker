import os
import sys
import subprocess
import platform

def build_exe():
    print("=" * 60)
    print("FeastFlow Checker - Windows Executable Builder")
    print("=" * 60)
    print()
    
    system = platform.system()
    print(f"Current OS: {system}")
    
    if system != "Windows":
        print()
        print("⚠️  WARNING: You are not on Windows!")
        print("This build script is designed to run on Windows 10-11.")
        print("To build the .exe file, please run this on a Windows machine.")
        print()
        print("However, you can still test the application by running:")
        print("  python main.py")
        print()
        return
    
    print()
    print("Building FeastFlow Checker executable...")
    print()
    
    try:
        subprocess.run([
            sys.executable, '-m', 'PyInstaller',
            'FeastFlow_Checker.spec',
            '--clean',
            '--noconfirm'
        ], check=True)
        
        print()
        print("=" * 60)
        print("✓ Build completed successfully!")
        print("=" * 60)
        print()
        print("Your executable is located at:")
        print("  dist/FeastFlow_Checker.exe")
        print()
        print("You can now distribute this .exe file to run on Windows 10-11")
        print("=" * 60)
        
    except subprocess.CalledProcessError as e:
        print()
        print("✗ Build failed!")
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print()
        print("✗ An error occurred during the build process!")
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()
