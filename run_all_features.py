#!/usr/bin/env python3
"""
Run All Professional Features
Launches the Wi-Fi Security Assessment Tool with all professional features enabled
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
logger = logging.getLogger("wifi_security_tool.all_features")

def main():
    """Application entry point with all professional features enabled"""
    try:
        # Import the main application
        from main import MainWindow, APP_VERSION
        
        # Import professional features
        from modules.core.professional_features import run_all_features
        
        # Start application
        app = QApplication(sys.argv)
        app.setApplicationName("Wi-Fi Security Assessment Tool - All Features Edition")
        app.setApplicationVersion(f"{APP_VERSION} Pro+")
        
        # Create main window
        window = MainWindow()
        
        # Run all professional features
        logger.info("Activating all professional features...")
        success = run_all_features(window)
        
        if success:
            logger.info("All professional features activated successfully")
        else:
            logger.warning("Some features could not be activated")
        
        # Show the window
        window.show()
        
        # Run the application
        return app.exec_()
    
    except Exception as e:
        logger.error(f"Error starting application: {str(e)}")
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
