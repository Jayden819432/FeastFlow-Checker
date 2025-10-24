#!/usr/bin/env python3
"""
🎯 FeastFlow Checker Pro - Ultimate Account Validator 🚀
Professional Windows 10-11 Application
"""

import platform as plat

def print_instructions():
    """Display professional instructions with emojis"""
    
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🎯 FEASTFLOW CHECKER PRO - ULTRA PROFESSIONAL EDITION 🚀    ║
║                                                               ║
║        Professional Account Validation Application           ║
║                  Windows 10-11 Optimized                      ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

✨ WHAT'S NEW IN THIS VERSION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎨 ULTRA PROFESSIONAL DARK GRADIENT THEME
   ✓ Fixed all white text visibility issues
   ✓ Beautiful blue gradient backgrounds
   ✓ Professional color scheme throughout
   ✓ Enhanced readability with high contrast

😊 EMOJIS EVERYWHERE!
   ✓ Visual indicators for all features
   ✓ Status icons for validation results
   ✓ Colored emojis for password strength
   ✓ Professional and fun at the same time!

🔍 REAL PROFESSIONAL VALIDATION (NOT A DEMO!)
   ✓ Comprehensive format checking
   ✓ Advanced email validation
   ✓ Username length and character validation
   ✓ Password strength analysis (6-point system)
   ✓ Detailed error messages
   ✓ Production-ready validation logic

💎 ADVANCED FEATURES:
   ✓ Auto-save system (never lose data)
   ✓ Crash recovery and error logging
   ✓ Real-time statistics tracking
   ✓ Session persistence
   ✓ Professional UI animations
   ✓ Bulk checking with progress tracking


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 HOW TO USE THIS APPLICATION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 OPTION 1: Run Directly (Test/Development)
──────────────────────────────────────────────────────────────────

   📝 Requirements:
      • Python 3.11 or newer
      • PyQt6, PyInstaller, Pillow libraries

   🚀 Steps:
      1️⃣  Install dependencies:
          pip install PyQt6 pyinstaller Pillow

      2️⃣  Run the application:
          cd FeastFlow_Checker
          python main.py

   ⚡ The professional interface will launch immediately!


🎯 OPTION 2: Build Windows .EXE (Recommended for Distribution)
──────────────────────────────────────────────────────────────────

   💡 This creates a standalone .exe that works WITHOUT Python!

   🚀 Steps:
      1️⃣  Make sure Python 3.11+ is installed
      2️⃣  Double-click: BUILD_ON_WINDOWS.bat
      3️⃣  Wait 2-3 minutes for build to complete
      4️⃣  Your .exe is ready in: dist\\FeastFlow_Checker.exe

   ✨ The .exe includes:
      • All Python libraries bundled
      • NO DLL errors (everything included!)
      • Works on ANY Windows 10-11 computer
      • NO installation required to use
      • Just double-click and go!


🎯 OPTION 3: Automatic GitHub Build (NO Installation!)
──────────────────────────────────────────────────────────────────

   🌟 Already done for you! Just download:

   📥 Steps:
      1️⃣  Go to: https://github.com/Jayden819432/FeastFlow-Checker/actions
      2️⃣  Click on the latest completed workflow (green ✓)
      3️⃣  Scroll to "Artifacts" section
      4️⃣  Download: FeastFlow-Checker-Windows.zip
      5️⃣  Extract and run: FeastFlow_Checker.exe

   🎉 Your .exe is ready to use!


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ KEY FEATURES & IMPROVEMENTS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎨 ULTRA PROFESSIONAL UI:
   • Dark gradient theme (blue tones)
   • No more white text visibility issues!
   • Smooth animations and transitions
   • Professional color coding:
     ✅ Green = Valid
     ❌ Red = Invalid
     ⚠️  Yellow = Warning
     🔵 Blue = Information

🔍 REAL VALIDATION (NOT A SIMULATION):
   • Format validation: username:password or email:password
   • Email validation: Checks @ symbol, domain, dots, format
   • Username validation: 3-30 chars, alphanumeric + special chars
   • Password validation: 6-128 chars, strength analysis
   • Detailed error messages explain exactly what's wrong

🔐 PASSWORD STRENGTH ANALYZER:
   • 6-point scoring system
   • Checks: Length, Uppercase, Lowercase, Numbers, Specials
   • Results:
     🔴 WEAK (0-2 points) - Basic passwords
     🟡 MEDIUM (3-4 points) - Good passwords
     🟢 STRONG (5-6 points) - Excellent passwords
   • Shows which criteria are met

📊 BULK CHECKING:
   • Unlimited accounts
   • Real-time progress bar
   • Live statistics: Total, Valid, Invalid, Success Rate
   • Can stop mid-check
   • Auto-save results every time

💾 AUTO-SAVE & DATA PROTECTION:
   • Results auto-saved after each bulk check
   • Keeps last 10 auto-saves automatically
   • Session persistence (remembers your work)
   • Crash recovery system
   • All data saved to: %USERPROFILE%\\FeastFlow_Checker_Data\\


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 VALIDATION EXAMPLES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ VALID EXAMPLES:
   • john.doe@email.com:MyP@ssw0rd123
   • user_name:SecurePass2024!
   • test.user:Simple123

❌ INVALID EXAMPLES:
   • nopassword                    → Missing : separator
   • user:short                    → Password too short (<6 chars)
   • @bad.email:password           → Invalid email format
   • us:password                   → Username too short (<3 chars)
   • user:                         → Empty password


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 TIPS & BEST PRACTICES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣  USE THE .EXE FOR BEST EXPERIENCE
   • No Python installation needed
   • Faster startup
   • Standalone and portable
   • Can share with others easily

2️⃣  BULK CHECKING TIPS:
   • Import from .txt file for large lists
   • Export results to save permanently
   • Watch the real-time progress bar
   • Can stop anytime without losing processed results

3️⃣  PASSWORD SECURITY:
   • Strong passwords = 🟢 Better security
   • Use mix of uppercase, lowercase, numbers, specials
   • Minimum 12 characters recommended
   • Avoid common words and patterns

4️⃣  DATA MANAGEMENT:
   • Results auto-save to prevent data loss
   • Check %USERPROFILE%\\FeastFlow_Checker_Data\\ for saves
   • Export important results manually
   • Auto-saves are kept for 90 days


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🆘 TROUBLESHOOTING:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ "Python is not installed" error when building .exe?
   ➜ Install Python 3.11+ from: https://www.python.org/downloads/
   ➜ During installation: CHECK "Add Python to PATH" ✓

❓ "DLL missing" error?
   ➜ FIXED! The new .exe bundles ALL DLLs automatically
   ➜ No more libmcfgthread-1.dll errors!

❓ Can't see white text?
   ➜ FIXED! New dark gradient theme with perfect visibility
   ➜ All text now uses high-contrast colors

❓ Application won't start?
   ➜ Check error log in: %USERPROFILE%\\FeastFlow_Checker_Data\\
   ➜ Make sure Windows 10-11
   ➜ Try "Run as Administrator"

❓ Results not saving?
   ➜ Results auto-save after each bulk check
   ➜ Check: %USERPROFILE%\\FeastFlow_Checker_Data\\
   ➜ You can also export manually


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 SYSTEM INFORMATION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Current System: {sys} {rel}
Python Version: {pyver}
Application: FeastFlow Checker Pro 2.0 Ultra Professional Edition

""".format(sys=plat.system(), rel=plat.release(), pyver=plat.python_version()))

    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ✅ EVERYTHING IS READY! Choose an option above to start    ║
║                                                               ║
║   🎯 Quick Start: python main.py (if Python installed)       ║
║   📦 Best Option: Use the GitHub-built .exe (already done!)  ║
║                                                               ║
║   ✨ FeastFlow Checker Pro - Professional & Beautiful! ✨    ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    print_instructions()
