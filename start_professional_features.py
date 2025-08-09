#!/usr/bin/env python3
"""
Wi-Fi Security Assessment Tool - Professional Features Launcher
This script starts the main application with all professional features enabled
"""

import os
import sys
import logging
from PyQt5.QtWidgets import QApplication, QMessageBox

# Set up logging
log_dir = os.path.join(os.path.expanduser("~"), ".wifi_security_tool", "logs")
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, "pro_features.log"),
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("wifi_security_tool.pro_launcher")

def main():
    """Application entry point with professional features"""
    try:
        # Import the main application
        from main import MainWindow, APP_VERSION
        
        # Import professional features
        from modules.core.professional_features import get_professional_features, integrate_with_main_app
        
        # Start application
        app = QApplication(sys.argv)
        app.setApplicationName("Wi-Fi Security Assessment Tool - Professional Edition")
        app.setApplicationVersion(f"{APP_VERSION} Pro")
        
        # Create main window
        window = MainWindow()
        
        # Integrate professional features
        logger.info("Integrating professional features...")
        success = integrate_with_main_app(window)
        
        if success:
            logger.info("Professional features integrated successfully")
            # Show a welcome message
            QMessageBox.information(
                window,
                "Professional Features Activated",
                "The following professional features have been activated:\n\n"
                "• AI-based Password Analysis\n"
                "• Network Topology Visualization\n"
                "• Threat Intelligence Feed\n"
                "• Continuous Vulnerability Scanning\n"
                "• Advanced Reporting\n"
                "• Enterprise Features\n"
                "• Automated Remediation\n\n"
                "These features are now available in the application."
            )
        else:
            logger.warning("Some professional features could not be integrated")
            QMessageBox.warning(
                window,
                "Partial Feature Activation",
                "Some professional features could not be activated. "
                "Please check the log file for more information."
            )
        
        # Show the window
        window.show()
        
        # Run the application
        sys.exit(app.exec_())
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
        QMessageBox.critical(None, "Error", f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
