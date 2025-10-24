import sys
import os
import platform
import json
import traceback
import requests
import webbrowser
import asyncio
from pathlib import Path
from packaging import version as pkg_version
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                              QTextEdit, QTabWidget, QFileDialog, QMessageBox,
                              QProgressBar, QGroupBox, QSplitter, QComboBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QSettings, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QIcon, QPixmap, QColor, QPalette
import re
from datetime import datetime

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


APP_VERSION = "2.0.0"
GITHUB_REPO = "Jayden819432/FeastFlow-Checker"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"


class AutoUpdater:
    """Auto-update checker for GitHub releases"""
    
    @staticmethod
    def check_for_updates():
        """Check GitHub for latest release"""
        try:
            response = requests.get(GITHUB_API_URL, timeout=10)
            response.raise_for_status()
            
            release_data = response.json()
            latest_version = release_data['tag_name'].lstrip('v')
            download_url = None
            
            for asset in release_data['assets']:
                if 'FeastFlow' in asset['name'] and asset['name'].endswith('.zip'):
                    download_url = asset['browser_download_url']
                    break
            
            if pkg_version.parse(latest_version) > pkg_version.parse(APP_VERSION):
                return {
                    'available': True,
                    'version': latest_version,
                    'download_url': download_url or release_data['html_url'],
                    'notes': release_data.get('body', '')[:200]
                }
            return {'available': False}
        except Exception as e:
            print(f"Update check failed: {e}")
            return {'available': False}


class PlatformAuth:
    """Handle OAuth authentication for different platforms"""
    
    def __init__(self):
        self.spotify_client = None
        self.twitch_client = None
        self.youtube_client = None
        self.credentials = {}
        self.load_credentials()
    
    def load_credentials(self):
        """Load saved API credentials"""
        cred_file = Path.home() / "FeastFlow_Checker_Data" / "api_credentials.json"
        if cred_file.exists():
            try:
                with open(cred_file, 'r') as f:
                    self.credentials = json.load(f)
            except:
                pass
    
    def save_credentials(self):
        """Save API credentials"""
        data_dir = Path.home() / "FeastFlow_Checker_Data"
        data_dir.mkdir(exist_ok=True)
        cred_file = data_dir / "api_credentials.json"
        with open(cred_file, 'w') as f:
            json.dump(self.credentials, f)
    
    def setup_spotify(self, client_id, client_secret):
        """Set up Spotify OAuth"""
        try:
            self.credentials['spotify'] = {
                'client_id': client_id,
                'client_secret': client_secret
            }
            self.save_credentials()
            
            sp_oauth = SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri="http://localhost:8888/callback",
                scope="user-read-private user-read-email"
            )
            self.spotify_client = spotipy.Spotify(auth_manager=sp_oauth)
            return True
        except Exception as e:
            print(f"Spotify setup error: {e}")
            return False
    
    async def setup_twitch(self, client_id, client_secret):
        """Set up Twitch OAuth"""
        try:
            self.credentials['twitch'] = {
                'client_id': client_id,
                'client_secret': client_secret
            }
            self.save_credentials()
            
            self.twitch_client = await Twitch(client_id, client_secret)
            scopes = [AuthScope.USER_READ_EMAIL]
            auth = UserAuthenticator(self.twitch_client, scopes)
            token, refresh = await auth.authenticate()
            await self.twitch_client.set_user_authentication(token, scopes, refresh)
            return True
        except Exception as e:
            print(f"Twitch setup error: {e}")
            return False
    
    def setup_youtube(self, credentials_json):
        """Set up YouTube OAuth"""
        try:
            scopes = ['https://www.googleapis.com/auth/youtube.readonly']
            flow = InstalledAppFlow.from_client_secrets_file(credentials_json, scopes)
            creds = flow.run_local_server(port=8080)
            self.youtube_client = build('youtube', 'v3', credentials=creds)
            return True
        except Exception as e:
            print(f"YouTube setup error: {e}")
            return False


class MultiPlatformChecker(QThread):
    """Check accounts across multiple platforms"""
    progress_signal = pyqtSignal(int)
    result_signal = pyqtSignal(str, str, str)
    finished_signal = pyqtSignal(dict)
    
    def __init__(self, accounts, platform, auth_handler):
        super().__init__()
        self.accounts = accounts
        self.platform = platform.lower()
        self.auth = auth_handler
        self.is_running = True
        self.stats = {'total': 0, 'valid': 0, 'invalid': 0, 'processed': 0, 'stopped': False}
    
    def run(self):
        total = len(self.accounts)
        self.stats['total'] = total
        
        try:
            for i, account in enumerate(self.accounts):
                if not self.is_running:
                    self.stats['stopped'] = True
                    break
                
                try:
                    if self.platform == "format":
                        result, strength = self.check_format_only(account)
                    elif self.platform == "spotify":
                        result, strength = self.check_spotify(account)
                    elif self.platform == "twitch":
                        result, strength = self.check_twitch(account)
                    elif self.platform == "youtube":
                        result, strength = self.check_youtube(account)
                    else:
                        result, strength = self.check_format_only(account)
                    
                    if result.startswith("✅"):
                        self.stats['valid'] += 1
                    else:
                        self.stats['invalid'] += 1
                    
                    self.stats['processed'] += 1
                    self.result_signal.emit(account, result, strength)
                    progress = int((i + 1) / total * 100)
                    self.progress_signal.emit(progress)
                except Exception as e:
                    self.result_signal.emit(account, f"❌ ERROR - {str(e)}", "N/A")
                    self.stats['invalid'] += 1
                    self.stats['processed'] += 1
                
                self.msleep(100)
        except Exception as e:
            pass
        finally:
            self.finished_signal.emit(self.stats)
    
    def check_format_only(self, account):
        """Format validation only (no API calls)"""
        account = account.strip()
        if not account:
            return "❌ INVALID - Empty account", "N/A"
        
        if ':' not in account:
            return "❌ INVALID - Missing ':' separator (use username:password or email:password)", "N/A"
        
        parts = account.split(':', 1)
        if len(parts) != 2:
            return "❌ INVALID - Wrong format (use username:password)", "N/A"
        
        username, password = parts
        
        if not username or not password:
            return "❌ INVALID - Missing username or password", "N/A"
        
        if len(password) < 6:
            return f"❌ INVALID - Password too short ({len(password)} chars, min 6)", "🔴 WEAK"
        
        if '@' in username:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, username):
                return "❌ INVALID - Invalid email format", "N/A"
        else:
            if len(username) < 3:
                return f"❌ INVALID - Username too short (min 3 chars)", "N/A"
        
        weak_passwords = ['password', '123456', '12345678', 'qwerty', 'abc123', 'password123']
        if password.lower() in weak_passwords:
            return "❌ INVALID - Common weak password detected!", "🔴 WEAK"
        
        strength = self.calculate_password_strength(password)
        return f"✅ VALID - Format check passed (Platform: {self.platform.upper()})", strength
    
    def check_spotify(self, account):
        """Check Spotify account using real API"""
        if not self.auth.spotify_client:
            return "⚠️ WARNING - Spotify API not configured", "N/A"
        
        username, password = account.split(':', 1)
        
        try:
            user = self.auth.spotify_client.current_user()
            product = user.get('product', 'unknown')
            
            if product == 'premium':
                return f"✅ VALID - Spotify Premium Account ✨", "🟢 PREMIUM"
            elif product == 'free':
                return f"✅ VALID - Spotify Free Account", "🟡 FREE"
            else:
                return f"✅ VALID - Spotify Account ({product})", "🔵 ACTIVE"
        except Exception as e:
            return f"❌ INVALID - Spotify: {str(e)[:50]}", "N/A"
    
    def check_twitch(self, account):
        """Check Twitch account using real API"""
        if not self.auth.twitch_client:
            return "⚠️ WARNING - Twitch API not configured", "N/A"
        
        username, password = account.split(':', 1)
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            users = loop.run_until_complete(
                self.auth.twitch_client.get_users(logins=[username])
            )
            
            if users:
                user = users[0]
                return f"✅ VALID - Twitch User: {user.display_name}", "🟢 VERIFIED"
            else:
                return f"❌ INVALID - Twitch user not found", "N/A"
        except Exception as e:
            return f"❌ INVALID - Twitch: {str(e)[:50]}", "N/A"
    
    def check_youtube(self, account):
        """Check YouTube account using real API"""
        if not self.auth.youtube_client:
            return "⚠️ WARNING - YouTube API not configured", "N/A"
        
        try:
            response = self.auth.youtube_client.channels().list(
                part='snippet,statistics',
                mine=True
            ).execute()
            
            if response.get('items'):
                channel = response['items'][0]
                name = channel['snippet']['title']
                subs = channel['statistics'].get('subscriberCount', '0')
                return f"✅ VALID - YouTube: {name} ({subs} subs)", "🟢 VERIFIED"
            else:
                return f"❌ INVALID - No YouTube channel found", "N/A"
        except Exception as e:
            return f"❌ INVALID - YouTube: {str(e)[:50]}", "N/A"
    
    def calculate_password_strength(self, password):
        """Calculate password strength"""
        score = 0
        if len(password) >= 8: score += 1
        if len(password) >= 12: score += 1
        if re.search(r'[A-Z]', password): score += 1
        if re.search(r'[a-z]', password): score += 1
        if re.search(r'\d', password): score += 1
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password): score += 1
        
        if score <= 2:
            return "🔴 WEAK"
        elif score <= 4:
            return "🟡 MEDIUM"
        else:
            return "🟢 STRONG"
    
    def stop(self):
        self.is_running = False


class FeastFlowCheckerPro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.checker_thread = None
        self.auth_handler = PlatformAuth()
        self.init_ui()
        self.load_settings()
        self.check_for_updates_on_startup()
    
    def init_ui(self):
        self.setWindowTitle(f"🎯 FeastFlow Checker Pro v{APP_VERSION} - Multi-Platform Account Validator 🚀")
        self.setMinimumSize(1100, 700)
        
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1e3a8a, stop:0.5 #1e40af, stop:1 #2563eb);
            }
            QTabWidget::pane {
                border: 2px solid #3b82f6;
                border-radius: 10px;
                background: rgba(30, 41, 59, 0.95);
                padding: 15px;
            }
            QTabBar::tab {
                background: rgba(30, 64, 175, 0.8);
                color: #e0e7ff;
                padding: 12px 25px;
                margin: 2px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                min-width: 150px;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3b82f6, stop:1 #2563eb);
                color: #ffffff;
            }
            QTabBar::tab:hover {
                background: rgba(59, 130, 246, 0.9);
            }
            QGroupBox {
                border: 2px solid #3b82f6;
                border-radius: 10px;
                margin-top: 15px;
                padding: 20px;
                background: rgba(15, 23, 42, 0.8);
                color: #e0e7ff;
                font-weight: bold;
                font-size: 13px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
                color: #60a5fa;
                font-size: 14px;
            }
            QLineEdit, QTextEdit, QComboBox {
                background: rgba(30, 41, 59, 0.95);
                border: 2px solid #475569;
                border-radius: 8px;
                padding: 10px;
                color: #e0e7ff;
                font-size: 13px;
                selection-background-color: #3b82f6;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border-color: #3b82f6;
                background: rgba(30, 41, 59, 1);
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3b82f6, stop:1 #2563eb);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 25px;
                font-size: 13px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #60a5fa, stop:1 #3b82f6);
            }
            QPushButton:pressed {
                background: #1e40af;
            }
            QPushButton:disabled {
                background: #475569;
                color: #94a3b8;
            }
            QLabel {
                color: #e0e7ff;
                font-size: 13px;
            }
            QProgressBar {
                border: 2px solid #3b82f6;
                border-radius: 8px;
                text-align: center;
                background: rgba(30, 41, 59, 0.9);
                color: #e0e7ff;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #22c55e, stop:1 #16a34a);
                border-radius: 6px;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        header = QLabel(f"🎯 FeastFlow Checker Pro v{APP_VERSION} 🚀")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #ffffff;
            padding: 15px;
            background: rgba(59, 130, 246, 0.3);
            border-radius: 10px;
            margin-bottom: 10px;
        """)
        main_layout.addWidget(header)
        
        subtitle = QLabel("✨ Multi-Platform Account Validator (YouTube • Twitch • Spotify) ✨")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 14px; color: #93c5fd; padding: 5px;")
        main_layout.addWidget(subtitle)
        
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        self.setup_single_check_tab()
        self.setup_bulk_check_tab()
        self.setup_api_config_tab()
        self.setup_stats_tab()
    
    def setup_single_check_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        group = QGroupBox("🎯 Single Account Check")
        group_layout = QVBoxLayout()
        
        platform_layout = QHBoxLayout()
        platform_layout.addWidget(QLabel("🌐 Platform:"))
        self.single_platform = QComboBox()
        self.single_platform.addItems([
            "Format Only (No API)",
            "Spotify",
            "Twitch",
            "YouTube"
        ])
        platform_layout.addWidget(self.single_platform)
        group_layout.addLayout(platform_layout)
        
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("📧 Account:"))
        self.single_input = QLineEdit()
        self.single_input.setPlaceholderText("username:password or email:password")
        input_layout.addWidget(self.single_input)
        group_layout.addLayout(input_layout)
        
        btn_layout = QHBoxLayout()
        check_btn = QPushButton("✅ Validate Account")
        check_btn.clicked.connect(self.check_single_account)
        clear_btn = QPushButton("🗑️ Clear")
        clear_btn.clicked.connect(self.clear_single)
        btn_layout.addWidget(check_btn)
        btn_layout.addWidget(clear_btn)
        group_layout.addLayout(btn_layout)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        result_group = QGroupBox("📊 Validation Result")
        result_layout = QVBoxLayout()
        self.single_result = QTextEdit()
        self.single_result.setReadOnly(True)
        self.single_result.setMaximumHeight(250)
        result_layout.addWidget(self.single_result)
        result_group.setLayout(result_layout)
        layout.addWidget(result_group)
        
        layout.addStretch()
        self.tabs.addTab(tab, "🎯 Single Check")
    
    def setup_bulk_check_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        config_group = QGroupBox("⚙️ Bulk Check Configuration")
        config_layout = QVBoxLayout()
        
        platform_layout = QHBoxLayout()
        platform_layout.addWidget(QLabel("🌐 Platform:"))
        self.bulk_platform = QComboBox()
        self.bulk_platform.addItems([
            "Format Only (No API)",
            "Spotify",
            "Twitch",
            "YouTube"
        ])
        platform_layout.addWidget(self.bulk_platform)
        config_layout.addLayout(platform_layout)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        input_group = QGroupBox("📝 Account List (one per line)")
        input_layout = QVBoxLayout()
        self.bulk_input = QTextEdit()
        self.bulk_input.setPlaceholderText("username1:password1\nusername2:password2\nemail@example.com:password3")
        input_layout.addWidget(self.bulk_input)
        
        file_btn_layout = QHBoxLayout()
        import_btn = QPushButton("📂 Import File")
        import_btn.clicked.connect(self.import_accounts)
        export_btn = QPushButton("💾 Export Results")
        export_btn.clicked.connect(self.export_results)
        file_btn_layout.addWidget(import_btn)
        file_btn_layout.addWidget(export_btn)
        input_layout.addLayout(file_btn_layout)
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        control_layout = QHBoxLayout()
        self.start_btn = QPushButton("🚀 Start Checking")
        self.start_btn.clicked.connect(self.start_bulk_check)
        self.stop_btn = QPushButton("🛑 Stop")
        self.stop_btn.clicked.connect(self.stop_bulk_check)
        self.stop_btn.setEnabled(False)
        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.stop_btn)
        layout.addLayout(control_layout)
        
        self.bulk_progress = QProgressBar()
        layout.addWidget(self.bulk_progress)
        
        result_group = QGroupBox("📊 Results")
        result_layout = QVBoxLayout()
        self.bulk_result = QTextEdit()
        self.bulk_result.setReadOnly(True)
        result_layout.addWidget(self.bulk_result)
        result_group.setLayout(result_layout)
        layout.addWidget(result_group)
        
        self.tabs.addTab(tab, "📊 Bulk Check")
    
    def setup_api_config_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        info = QLabel("⚙️ Configure API credentials for real account checking")
        info.setStyleSheet("font-size: 14px; padding: 10px;")
        layout.addWidget(info)
        
        spotify_group = QGroupBox("🎵 Spotify API Configuration")
        spotify_layout = QVBoxLayout()
        spotify_layout.addWidget(QLabel("Get credentials from: https://developer.spotify.com/dashboard"))
        
        sp_id_layout = QHBoxLayout()
        sp_id_layout.addWidget(QLabel("Client ID:"))
        self.spotify_id_input = QLineEdit()
        sp_id_layout.addWidget(self.spotify_id_input)
        spotify_layout.addLayout(sp_id_layout)
        
        sp_secret_layout = QHBoxLayout()
        sp_secret_layout.addWidget(QLabel("Client Secret:"))
        self.spotify_secret_input = QLineEdit()
        self.spotify_secret_input.setEchoMode(QLineEdit.EchoMode.Password)
        sp_secret_layout.addWidget(self.spotify_secret_input)
        spotify_layout.addLayout(sp_secret_layout)
        
        sp_btn = QPushButton("💾 Save Spotify Config")
        sp_btn.clicked.connect(self.save_spotify_config)
        spotify_layout.addWidget(sp_btn)
        
        spotify_group.setLayout(spotify_layout)
        layout.addWidget(spotify_group)
        
        twitch_group = QGroupBox("🎮 Twitch API Configuration")
        twitch_layout = QVBoxLayout()
        twitch_layout.addWidget(QLabel("Get credentials from: https://dev.twitch.tv/console/apps"))
        
        tw_id_layout = QHBoxLayout()
        tw_id_layout.addWidget(QLabel("Client ID:"))
        self.twitch_id_input = QLineEdit()
        tw_id_layout.addWidget(self.twitch_id_input)
        twitch_layout.addLayout(tw_id_layout)
        
        tw_secret_layout = QHBoxLayout()
        tw_secret_layout.addWidget(QLabel("Client Secret:"))
        self.twitch_secret_input = QLineEdit()
        self.twitch_secret_input.setEchoMode(QLineEdit.EchoMode.Password)
        tw_secret_layout.addWidget(self.twitch_secret_input)
        twitch_layout.addLayout(tw_secret_layout)
        
        tw_btn = QPushButton("💾 Save Twitch Config")
        tw_btn.clicked.connect(self.save_twitch_config)
        twitch_layout.addWidget(tw_btn)
        
        twitch_group.setLayout(twitch_layout)
        layout.addWidget(twitch_group)
        
        youtube_group = QGroupBox("📺 YouTube API Configuration")
        youtube_layout = QVBoxLayout()
        youtube_layout.addWidget(QLabel("Get credentials from: https://console.cloud.google.com/"))
        youtube_layout.addWidget(QLabel("⚠️ Requires OAuth JSON file download"))
        
        yt_btn = QPushButton("📂 Load YouTube Credentials JSON")
        yt_btn.clicked.connect(self.load_youtube_credentials)
        youtube_layout.addWidget(yt_btn)
        
        youtube_group.setLayout(youtube_layout)
        layout.addWidget(youtube_group)
        
        layout.addStretch()
        self.tabs.addTab(tab, "⚙️ API Config")
    
    def setup_stats_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        group = QGroupBox("📈 Real-Time Statistics")
        group_layout = QVBoxLayout()
        
        self.stats_display = QTextEdit()
        self.stats_display.setReadOnly(True)
        self.stats_display.setMaximumHeight(400)
        self.stats_display.setHtml("""
            <div style='color: #e0e7ff; font-family: Arial; padding: 20px;'>
                <h2 style='color: #60a5fa;'>📊 FeastFlow Checker Pro Statistics</h2>
                <p style='font-size: 14px;'>No checking session yet. Start a bulk check to see statistics!</p>
                <hr style='border-color: #3b82f6;'>
                <p style='color: #93c5fd;'>✨ Ready to validate accounts across multiple platforms!</p>
            </div>
        """)
        group_layout.addWidget(self.stats_display)
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        layout.addStretch()
        self.tabs.addTab(tab, "📈 Stats")
    
    def check_for_updates_on_startup(self):
        """Check for updates when app starts"""
        QTimer.singleShot(2000, self.auto_update_check)
    
    def auto_update_check(self):
        """Background update check"""
        try:
            update_info = AutoUpdater.check_for_updates()
            if update_info.get('available'):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("🎉 Update Available!")
                msg.setText(f"Version {update_info['version']} is available!\n\nCurrent: v{APP_VERSION}")
                msg.setInformativeText("Would you like to download the update?")
                msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                
                if msg.exec() == QMessageBox.StandardButton.Yes:
                    url = update_info.get('download_url', '')
                    if url:
                        webbrowser.open(url)
        except:
            pass
    
    def check_single_account(self):
        """Check single account"""
        account = self.single_input.text().strip()
        if not account:
            self.single_result.setHtml("<div style='color: #ef4444;'>❌ Please enter an account</div>")
            return
        
        platform = self.single_platform.currentText().split()[0].lower()
        
        checker = MultiPlatformChecker([account], platform, self.auth_handler)
        checker.result_signal.connect(lambda acc, res, strength: self.display_single_result(res, strength))
        checker.start()
        checker.wait()
    
    def display_single_result(self, result, strength):
        """Display single check result"""
        color = "#22c55e" if result.startswith("✅") else "#ef4444" if result.startswith("❌") else "#eab308"
        html = f"""
            <div style='color: #e0e7ff; font-family: Arial; padding: 15px;'>
                <h3 style='color: {color};'>{result}</h3>
                <p><strong>Password Strength:</strong> {strength}</p>
                <p style='color: #94a3b8; font-size: 12px;'>Checked at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        """
        self.single_result.setHtml(html)
    
    def clear_single(self):
        """Clear single check inputs"""
        self.single_input.clear()
        self.single_result.clear()
    
    def start_bulk_check(self):
        """Start bulk checking"""
        accounts = [line.strip() for line in self.bulk_input.toPlainText().split('\n') if line.strip()]
        if not accounts:
            QMessageBox.warning(self, "No Accounts", "Please enter accounts to check!")
            return
        
        platform = self.bulk_platform.currentText().split()[0].lower()
        
        self.bulk_result.clear()
        self.bulk_progress.setValue(0)
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        
        self.checker_thread = MultiPlatformChecker(accounts, platform, self.auth_handler)
        self.checker_thread.progress_signal.connect(self.bulk_progress.setValue)
        self.checker_thread.result_signal.connect(self.append_bulk_result)
        self.checker_thread.finished_signal.connect(self.bulk_check_finished)
        self.checker_thread.start()
    
    def stop_bulk_check(self):
        """Stop bulk checking"""
        if self.checker_thread:
            self.checker_thread.stop()
    
    def append_bulk_result(self, account, result, strength):
        """Append result to bulk display"""
        color = "#22c55e" if result.startswith("✅") else "#ef4444" if result.startswith("❌") else "#eab308"
        html = f"<div style='color: {color}; margin: 5px 0;'><strong>{account}</strong> → {result} | {strength}</div>"
        self.bulk_result.append(html)
    
    def bulk_check_finished(self, stats):
        """Handle bulk check completion"""
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        success_rate = (stats['valid'] / stats['total'] * 100) if stats['total'] > 0 else 0
        
        summary_html = f"""
            <div style='color: #e0e7ff; background: rgba(59, 130, 246, 0.2); padding: 15px; border-radius: 8px; margin-top: 10px;'>
                <h3 style='color: #60a5fa;'>📊 Summary</h3>
                <p>✅ Valid: {stats['valid']}</p>
                <p>❌ Invalid: {stats['invalid']}</p>
                <p>📈 Success Rate: {success_rate:.1f}%</p>
            </div>
        """
        self.bulk_result.append(summary_html)
        
        self.update_stats_display(stats)
        self.auto_save_results()
    
    def update_stats_display(self, stats):
        """Update statistics tab"""
        success_rate = (stats['valid'] / stats['total'] * 100) if stats['total'] > 0 else 0
        
        html = f"""
            <div style='color: #e0e7ff; font-family: Arial; padding: 20px;'>
                <h2 style='color: #60a5fa;'>📊 Session Statistics</h2>
                <div style='background: rgba(59, 130, 246, 0.2); padding: 15px; border-radius: 10px; margin: 10px 0;'>
                    <h3 style='color: #93c5fd;'>📈 Results</h3>
                    <p style='font-size: 16px;'><strong>Total Checked:</strong> {stats['total']}</p>
                    <p style='font-size: 16px; color: #22c55e;'><strong>✅ Valid:</strong> {stats['valid']}</p>
                    <p style='font-size: 16px; color: #ef4444;'><strong>❌ Invalid:</strong> {stats['invalid']}</p>
                    <p style='font-size: 16px; color: #60a5fa;'><strong>📊 Success Rate:</strong> {success_rate:.1f}%</p>
                </div>
                <p style='color: #94a3b8; font-size: 12px;'>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        """
        self.stats_display.setHtml(html)
    
    def import_accounts(self):
        """Import accounts from file"""
        file_name, _ = QFileDialog.getOpenFileName(self, "Import Accounts", "", "Text Files (*.txt)")
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    self.bulk_input.setPlainText(f.read())
                QMessageBox.information(self, "Success", "Accounts imported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import: {str(e)}")
    
    def export_results(self):
        """Export results to file"""
        file_name, _ = QFileDialog.getSaveFileName(self, "Export Results", "", "Text Files (*.txt)")
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(self.bulk_result.toPlainText())
                QMessageBox.information(self, "Success", "Results exported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export: {str(e)}")
    
    def auto_save_results(self):
        """Auto-save results"""
        try:
            data_dir = Path.home() / "FeastFlow_Checker_Data"
            data_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            save_file = data_dir / f"autosave_{timestamp}.txt"
            with open(save_file, 'w', encoding='utf-8') as f:
                f.write(self.bulk_result.toPlainText())
        except:
            pass
    
    def save_spotify_config(self):
        """Save Spotify API configuration"""
        client_id = self.spotify_id_input.text().strip()
        client_secret = self.spotify_secret_input.text().strip()
        
        if not client_id or not client_secret:
            QMessageBox.warning(self, "Missing Info", "Please enter both Client ID and Secret!")
            return
        
        if self.auth_handler.setup_spotify(client_id, client_secret):
            QMessageBox.information(self, "Success", "Spotify API configured! ✅")
        else:
            QMessageBox.critical(self, "Error", "Failed to configure Spotify API")
    
    def save_twitch_config(self):
        """Save Twitch API configuration"""
        client_id = self.twitch_id_input.text().strip()
        client_secret = self.twitch_secret_input.text().strip()
        
        if not client_id or not client_secret:
            QMessageBox.warning(self, "Missing Info", "Please enter both Client ID and Secret!")
            return
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        success = loop.run_until_complete(self.auth_handler.setup_twitch(client_id, client_secret))
        
        if success:
            QMessageBox.information(self, "Success", "Twitch API configured! ✅")
        else:
            QMessageBox.critical(self, "Error", "Failed to configure Twitch API")
    
    def load_youtube_credentials(self):
        """Load YouTube credentials JSON"""
        file_name, _ = QFileDialog.getOpenFileName(self, "Load YouTube Credentials", "", "JSON Files (*.json)")
        if file_name:
            if self.auth_handler.setup_youtube(file_name):
                QMessageBox.information(self, "Success", "YouTube API configured! ✅")
            else:
                QMessageBox.critical(self, "Error", "Failed to configure YouTube API")
    
    def load_settings(self):
        """Load saved settings"""
        pass
    
    def save_settings(self):
        """Save current settings"""
        pass
    
    def closeEvent(self, a0):
        """Handle application close"""
        self.save_settings()
        a0.accept()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = FeastFlowCheckerPro()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
