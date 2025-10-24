# 🎯 FeastFlow Checker Pro v2.0 - Multi-Platform Account Validator

## ✨ What's New in Version 2.0!

**REAL API INTEGRATION** - No more format-only checking! Now with ACTUAL account validation for:
- 🎵 **Spotify** - Real OAuth authentication & Premium status detection
- 🎮 **Twitch** - Real account verification using Twitch API
- 📺 **YouTube** - Real channel validation using YouTube Data API v3
- ✅ **Format Checking** - Comprehensive validation without API calls

**AUTO-UPDATE SYSTEM** - Your .exe checks for updates automatically from GitHub!

## 🚀 Features

### Real Platform Integration
- **Spotify API**: Check Premium vs Free accounts
- **Twitch API**: Verify account validity and status
- **YouTube API**: Validate channels and subscription info
- **Format Validation**: Works without API configuration

### Professional UI
- 🎨 Beautiful dark gradient blue theme
- 😊 Emojis throughout for visual clarity
- 📊 Real-time statistics and progress tracking
- ⚙️ Easy API configuration interface

### Account Checking
- 🎯 **Single Account Check** - Validate one account at a time
- 📊 **Bulk Check** - Process unlimited accounts
- 📂 **Import/Export** - Load from files, save results
- 💾 **Auto-Save** - Never lose your checking results

### Auto-Update
- 🔄 Automatically checks for new versions on startup
- 📥 One-click download from GitHub
- ✅ Always stay up-to-date

## 📥 Quick Start

### Option 1: Download Pre-Built .exe (EASIEST!)

1. Go to [GitHub Releases](https://github.com/Jayden819432/FeastFlow-Checker/releases)
2. Download the latest `FeastFlow-Checker-Windows.zip`
3. Extract and run `FeastFlow_Checker.exe`
4. **No installation needed!**

### Option 2: Run from Source

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Option 3: Build Your Own .exe

**On Windows 10-11 only:**
```bash
python build_exe.py
```

Your .exe will be in the `dist` folder!

## ⚙️ API Configuration

To use **REAL account checking** (not just format validation), you need API credentials:

### 🎵 Spotify API Setup

1. Go to https://developer.spotify.com/dashboard
2. Create a new app
3. Copy your `Client ID` and `Client Secret`
4. In the app, go to **API Config** tab
5. Paste credentials and click **Save Spotify Config**
6. Follow OAuth browser prompt to authenticate

### 🎮 Twitch API Setup

1. Go to https://dev.twitch.tv/console/apps
2. Register a new application
3. Set OAuth Redirect URL: `http://localhost:17563`
4. Copy your `Client ID` and `Client Secret`
5. In the app, go to **API Config** tab
6. Paste credentials and click **Save Twitch Config**
7. Follow OAuth browser prompt to authenticate

### 📺 YouTube API Setup

1. Go to https://console.cloud.google.com/
2. Create a new project
3. Enable **YouTube Data API v3**
4. Create OAuth 2.0 credentials (Desktop Application)
5. Download the JSON file
6. In the app, click **Load YouTube Credentials JSON**
7. Select your downloaded JSON file
8. Follow OAuth browser prompt to authenticate

## 📋 How to Use

### Single Account Check
1. Select platform (or "Format Only" for no API)
2. Enter account in format: `username:password` or `email:password`
3. Click **✅ Validate Account**
4. View detailed results including password strength

### Bulk Account Check
1. Select platform to check
2. Enter accounts (one per line) or click **📂 Import File**
3. Click **🚀 Start Checking**
4. Watch real-time progress and results
5. Click **💾 Export Results** to save

### Results Include:
- ✅ Account validity status
- 🔐 Password strength analysis
- 🎵 Spotify: Premium vs Free
- 🎮 Twitch: User verification
- 📺 YouTube: Channel info & subscriber count

## 💾 Auto-Save

All bulk check results are automatically saved to:
```
%USERPROFILE%\FeastFlow_Checker_Data\autosave_YYYYMMDD_HHMMSS.txt
```

## 🔧 Requirements

- **Windows 10 or 11** (for .exe)
- **Python 3.11+** (if running from source)
- **API Credentials** (for real platform checking)

## 📊 Supported Formats

✅ Valid formats:
- `username:password`
- `email@domain.com:password`

❌ Invalid formats:
- No colon separator
- Empty username or password
- Password < 6 characters
- Invalid email format

## 🆘 Troubleshooting

**"API not configured" warning?**
- Go to API Config tab and set up credentials for that platform
- Or use "Format Only" mode for basic validation

**OAuth browser doesn't open?**
- Check your firewall settings
- Make sure the redirect URL is configured correctly

**Update check fails?**
- Check your internet connection
- Updates require GitHub access

**DLL errors?**
- The new version bundles ALL required DLLs
- Try re-downloading the latest .exe

## 📝 Notes

- Format validation works without any API setup
- Real platform checking requires API credentials (free to get!)
- Auto-save keeps last 100 results automatically
- All API credentials are stored securely locally

## 🎉 Credits

Developed with ❤️ using PyQt6, Spotipy, TwitchAPI, and Google APIs

## 📄 License

MIT License - Feel free to use and modify!

---

**🚀 Enjoy checking accounts across multiple platforms! 🎯**
