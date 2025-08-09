#!/usr/bin/env python3
"""
Wi-Fi Security Assessment Tool - Main Application
Educational purposes only - Use responsibly
"""

import sys
import os
import json
import logging
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QMessageBox,
                             QMenuBar, QMenu, QAction, QDialog, QVBoxLayout,
                             QLabel, QComboBox, QPushButton, QCheckBox, QStatusBar)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSettings, QSize

# Import modules
from modules.ui.dashboard import DashboardWidget
from modules.ui.network_scanner import NetworkScannerWidget
from modules.ui.handshake_capture import HandshakeCaptureWidget
from modules.ui.password_analyzer import PasswordAnalyzerWidget
from modules.ui.education_hub import EducationHubWidget
from modules.ui.reports import ReportsWidget
from modules.ui.monitoring_dashboard import MonitoringDashboard

# Set up logging
log_dir = os.path.join(os.path.expanduser("~"), ".wifi_security_tool", "logs")
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, "app.log"),
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("wifi_security_tool")

# Application version
APP_VERSION = "1.1.0"

class SettingsDialog(QDialog):
    """Settings dialog for the application"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.settings = QSettings("WiFiSecurityTool", "Settings")
        self.init_ui()
        
    def init_ui(self):
        """Initialize the settings dialog UI"""
        self.setWindowTitle("Settings")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        # Theme selection
        theme_label = QLabel("Application Theme:")
        theme_label.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(theme_label)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "Blue", "Professional"])
        current_theme = self.settings.value("theme", "Light")
        self.theme_combo.setCurrentText(current_theme)
        layout.addWidget(self.theme_combo)
        
        # Auto-save settings
        self.autosave_check = QCheckBox("Auto-save scan results")
        self.autosave_check.setChecked(self.settings.value("autosave", True, type=bool))
        layout.addWidget(self.autosave_check)
        
        # Show advanced options
        self.advanced_check = QCheckBox("Show advanced options")
        self.advanced_check.setChecked(self.settings.value("show_advanced", False, type=bool))
        layout.addWidget(self.advanced_check)
        
        # Verbose logging
        self.verbose_check = QCheckBox("Enable verbose logging")
        self.verbose_check.setChecked(self.settings.value("verbose_logging", False, type=bool))
        layout.addWidget(self.verbose_check)
        
        # Save button
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)
        
        self.setLayout(layout)
    
    def save_settings(self):
        """Save settings and apply them"""
        self.settings.setValue("theme", self.theme_combo.currentText())
        self.settings.setValue("autosave", self.autosave_check.isChecked())
        self.settings.setValue("show_advanced", self.advanced_check.isChecked())
        self.settings.setValue("verbose_logging", self.verbose_check.isChecked())
        
        # Apply theme immediately
        if self.parent:
            self.parent.apply_theme(self.theme_combo.currentText())
        
        # Update logging level if needed
        if self.verbose_check.isChecked():
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)
        
        self.accept()

class AboutDialog(QDialog):
    """About dialog for the application"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the about dialog UI"""
        self.setWindowTitle("About Wi-Fi Security Assessment Tool")
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("Wi-Fi Security Assessment Tool")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Version
        version_label = QLabel(f"Version {APP_VERSION}")
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)
        
        # Description
        desc_label = QLabel(
            "<p>A comprehensive educational tool for Wi-Fi security assessment and learning.</p>"
            "<p>This application is designed for educational purposes to help users understand "
            "Wi-Fi security concepts, vulnerabilities, and best practices.</p>"
        )
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc_label)
        
        # Disclaimer
        disclaimer_label = QLabel(
            "<p><b>DISCLAIMER:</b> This tool is for EDUCATIONAL PURPOSES ONLY. "
            "Only use on networks you own or have explicit permission to test. "
            "Unauthorized network scanning may violate local, state, and federal laws.</p>"
        )
        disclaimer_label.setWordWrap(True)
        disclaimer_label.setStyleSheet("color: red;")
        layout.addWidget(disclaimer_label)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.settings = QSettings("WiFiSecurityTool", "Settings")
        self.setWindowTitle("Wi-Fi Security Assessment Tool")
        self.setMinimumSize(1000, 700)
        
        # Create application directories
        self.create_app_directories()
        
        # Show disclaimer on first run
        if self.settings.value("first_run", True, type=bool):
            self.show_disclaimer()
            self.settings.setValue("first_run", False)
        
        # Initialize UI
        self.init_ui()
        
        # Apply saved theme
        theme = self.settings.value("theme", "Light")
        self.apply_theme(theme)
        
        # Log application start
        logger.info(f"Application started - Version {APP_VERSION}")
    
    def create_app_directories(self):
        """Create necessary application directories"""
        base_dir = os.path.join(os.path.expanduser("~"), ".wifi_security_tool")
        dirs = ["data", "logs", "reports", "captures", "configs"]
        
        for directory in dirs:
            os.makedirs(os.path.join(base_dir, directory), exist_ok=True)
    
    def init_ui(self):
        """Initialize the user interface"""
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(f"Wi-Fi Security Assessment Tool v{APP_VERSION} - Ready")
        
        # Create tab widget
        self.tabs = QTabWidget()
        
        # Create tabs
        self.dashboard_tab = DashboardWidget()
        self.scanner_tab = NetworkScannerWidget()
        self.handshake_tab = HandshakeCaptureWidget()
        self.password_tab = PasswordAnalyzerWidget()
        self.education_tab = EducationHubWidget()
        self.reports_tab = ReportsWidget()
        self.monitoring_tab = MonitoringDashboard(self)
        
        # Add tabs
        self.tabs.addTab(self.dashboard_tab, "Dashboard")
        self.tabs.addTab(self.scanner_tab, "Network Scanner")
        self.tabs.addTab(self.handshake_tab, "Handshake Capture")
        self.tabs.addTab(self.password_tab, "Password Analyzer")
        self.tabs.addTab(self.monitoring_tab, "Continuous Monitoring")
        self.tabs.addTab(self.education_tab, "Education Hub")
        self.tabs.addTab(self.reports_tab, "Reports")
        
        # Connect tab change signal
        self.tabs.currentChanged.connect(self.tab_changed)
        
        # Set central widget
        self.setCentralWidget(self.tabs)
    
    def create_menu_bar(self):
        """Create the application menu bar"""
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("File")
        
        # Settings action
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.show_settings)
        file_menu.addAction(settings_action)
        
        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Tools menu
        tools_menu = menu_bar.addMenu("Tools")
        
        # Network scan action
        scan_action = QAction("Network Scan", self)
        scan_action.triggered.connect(lambda: self.tabs.setCurrentIndex(1))
        tools_menu.addAction(scan_action)
        
        # Handshake capture action
        handshake_action = QAction("Handshake Capture", self)
        handshake_action.triggered.connect(lambda: self.tabs.setCurrentIndex(2))
        tools_menu.addAction(handshake_action)
        
        # Password analysis action
        password_action = QAction("Password Analysis", self)
        password_action.triggered.connect(lambda: self.tabs.setCurrentIndex(3))
        tools_menu.addAction(password_action)
        
        # Reports action
        reports_action = QAction("Generate Report", self)
        reports_action.triggered.connect(lambda: self.tabs.setCurrentIndex(5))
        tools_menu.addAction(reports_action)
        
        # Help menu
        help_menu = menu_bar.addMenu("Help")
        
        # Education hub action
        education_action = QAction("Education Hub", self)
        education_action.triggered.connect(lambda: self.tabs.setCurrentIndex(4))
        help_menu.addAction(education_action)
        
        # About action
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        # Disclaimer action
        disclaimer_action = QAction("Show Disclaimer", self)
        disclaimer_action.triggered.connect(lambda: self.show_disclaimer(force=True))
        help_menu.addAction(disclaimer_action)
    
    def tab_changed(self, index):
        """Handle tab change event"""
        tab_names = ["Dashboard", "Network Scanner", "Handshake Capture", 
                    "Password Analyzer", "Education Hub", "Reports"]
        
        if 0 <= index < len(tab_names):
            self.status_bar.showMessage(f"Current module: {tab_names[index]}")
            logger.info(f"Switched to {tab_names[index]} tab")
    
    def show_settings(self):
        """Show settings dialog"""
        dialog = SettingsDialog(self)
        dialog.exec_()
    
    def show_about(self):
        """Show about dialog"""
        dialog = AboutDialog(self)
        dialog.exec_()
    
    def apply_theme(self, theme_name):
        """Apply the selected theme to the application"""
        if theme_name == "Dark":
            self.set_dark_theme()
        elif theme_name == "Blue":
            self.set_blue_theme()
        elif theme_name == "Professional":
            self.set_professional_theme()
        else:  # Default to Light theme
            self.set_light_theme()
        
        logger.info(f"Applied {theme_name} theme")
    
    def set_light_theme(self):
        """Set light theme stylesheet"""
        self.setStyleSheet("""
            QMainWindow, QDialog {
                background-color: #f0f0f0;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background-color: #ffffff;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                border-bottom: 2px solid #3498db;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLabel {
                color: #333333;
            }
            QMenuBar {
                background-color: #f8f8f8;
                border-bottom: 1px solid #dddddd;
            }
            QMenuBar::item {
                padding: 4px 10px;
                background-color: transparent;
            }
            QMenuBar::item:selected {
                background-color: #e0e0e0;
            }
            QStatusBar {
                background-color: #f8f8f8;
                color: #555555;
            }
        """)
    
    def set_dark_theme(self):
        """Set dark theme stylesheet"""
        self.setStyleSheet("""
            QMainWindow, QDialog {
                background-color: #2c3e50;
            }
            QTabWidget::pane {
                border: 1px solid #34495e;
                background-color: #34495e;
            }
            QTabBar::tab {
                background-color: #2c3e50;
                color: #ecf0f1;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #34495e;
                border-bottom: 2px solid #3498db;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLabel {
                color: #ecf0f1;
            }
            QTextEdit, QLineEdit, QComboBox, QSpinBox {
                background-color: #34495e;
                color: #ecf0f1;
                border: 1px solid #7f8c8d;
            }
            QMenuBar {
                background-color: #2c3e50;
                color: #ecf0f1;
            }
            QMenuBar::item {
                padding: 4px 10px;
                background-color: transparent;
                color: #ecf0f1;
            }
            QMenuBar::item:selected {
                background-color: #34495e;
            }
            QMenu {
                background-color: #34495e;
                color: #ecf0f1;
            }
            QMenu::item:selected {
                background-color: #3498db;
            }
            QStatusBar {
                background-color: #2c3e50;
                color: #ecf0f1;
            }
            QCheckBox {
                color: #ecf0f1;
            }
        """)
    
    def set_blue_theme(self):
        """Set blue theme stylesheet"""
        self.setStyleSheet("""
            QMainWindow, QDialog {
                background-color: #e8f4fc;
            }
            QTabWidget::pane {
                border: 1px solid #bde0fe;
                background-color: #ffffff;
            }
            QTabBar::tab {
                background-color: #bde0fe;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                border-bottom: 2px solid #1e88e5;
            }
            QPushButton {
                background-color: #1e88e5;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QLabel {
                color: #0d47a1;
            }
            QMenuBar {
                background-color: #bbdefb;
                border-bottom: 1px solid #90caf9;
            }
            QMenuBar::item {
                padding: 4px 10px;
                background-color: transparent;
            }
            QMenuBar::item:selected {
                background-color: #90caf9;
            }
            QStatusBar {
                background-color: #bbdefb;
                color: #0d47a1;
            }
        """)
    
    def set_professional_theme(self):
        """Set professional theme stylesheet"""
        self.setStyleSheet("""
            QMainWindow, QDialog {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #d1d1d1;
                background-color: #ffffff;
            }
            QTabBar::tab {
                background-color: #e6e6e6;
                color: #555555;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                color: #000000;
                border-bottom: 2px solid #4caf50;
            }
            QPushButton {
                background-color: #4caf50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 2px;
            }
            QPushButton:hover {
                background-color: #388e3c;
            }
            QLabel {
                color: #333333;
            }
            QMenuBar {
                background-color: #f5f5f5;
                border-bottom: 1px solid #d1d1d1;
            }
            QMenuBar::item {
                padding: 4px 10px;
                background-color: transparent;
            }
            QMenuBar::item:selected {
                background-color: #e0e0e0;
            }
            QStatusBar {
                background-color: #f5f5f5;
                color: #555555;
                border-top: 1px solid #d1d1d1;
            }
        """)
    
    def show_disclaimer(self, force=False):
        """Show legal disclaimer on startup or when requested"""
        disclaimer_text = (
            "IMPORTANT DISCLAIMER\n\n"
            "This tool is for EDUCATIONAL PURPOSES ONLY.\n\n"
            "By using this software, you agree to:\n"
            "1. Only scan networks you own or have explicit permission to test\n"
            "2. Use this tool responsibly and ethically\n"
            "3. Accept full responsibility for your actions\n\n"
            "Unauthorized network scanning may violate local, state, and federal laws."
        )
        
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Legal Disclaimer")
        msg_box.setText(disclaimer_text)
        msg_box.setIcon(QMessageBox.Warning)
        
        if force:
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
        else:
            msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            result = msg_box.exec_()
            if result == QMessageBox.Cancel:
                logger.info("User declined disclaimer - exiting application")
                sys.exit(0)

def main():
    """Application entry point"""
    try:
        # Start application
        app = QApplication(sys.argv)
        app.setApplicationName("Wi-Fi Security Assessment Tool")
        app.setApplicationVersion(APP_VERSION)
        
        # Set application icon (if available)
        # app.setWindowIcon(QIcon("path/to/icon.png"))
        
        window = MainWindow()
        window.show()
        
        sys.exit(app.exec_())
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
        QMessageBox.critical(None, "Error", f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
