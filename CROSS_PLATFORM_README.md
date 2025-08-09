# Wi-Fi Security Assessment Tool - Cross-Platform Edition

This enhanced version of the Wi-Fi Security Assessment Tool supports both desktop (Windows, macOS, Linux) and mobile platforms (Android, iOS).

## Features

### Desktop Version (PyQt5)
- Advanced network scanning with detailed security analysis
- Real-time monitoring of Wi-Fi networks
- Password strength analysis and cracking simulation
- Interactive data visualizations and reports
- Comprehensive security recommendations

### Mobile Version (Kivy)
- Simplified interface optimized for touch screens
- Core network scanning functionality
- Basic password analysis
- Security tips and recommendations
- Compatible with Android and iOS

## Architecture

The application uses a modular architecture with shared core functionality:

```
├── main.py                  # Desktop application entry point
├── mobile_app.py            # Mobile application entry point
├── modules/
│   ├── core/                # Shared core functionality
│   │   ├── wifi_scanner.py  # Platform-independent Wi-Fi scanning
│   │   ├── password_analyzer.py  # Password analysis logic
│   │   └── security_analyzer.py  # Security analysis logic
│   ├── ui/                  # Desktop UI components
│   │   ├── dashboard.py
│   │   ├── network_scanner.py
│   │   ├── password_analyzer.py
│   │   └── ...
```

## Installation

### Desktop Version

1. Install Python 3.7+ and pip
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python main.py
   ```

### Mobile Version

#### Android
1. Install Kivy and Python-for-Android
2. Build the APK:
   ```
   buildozer android debug
   ```
3. Install on your Android device

#### iOS
1. Install Kivy and Kivy-iOS
2. Build the iOS app:
   ```
   toolchain build kivy
   toolchain create wifi_security_tool
   ```
3. Deploy to your iOS device through Xcode

## Usage

### Desktop Version
1. Launch the application using `python main.py`
2. Navigate through the tabs to access different features
3. Use the Network Scanner to analyze nearby Wi-Fi networks
4. Use the Password Analyzer to test password strength
5. Generate reports and security recommendations

### Mobile Version
1. Launch the application on your mobile device
2. Tap on the Network Scanner tab to scan for networks
3. Tap on a network to view detailed security information
4. Use the Password Analyzer to test password strength
5. View security tips and recommendations

## Security Considerations

- This tool is for educational and security assessment purposes only
- Only scan networks you own or have explicit permission to test
- Follow responsible disclosure practices if vulnerabilities are found
- Some features may require root/jailbreak on mobile devices

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- PyQt5 for desktop UI
- Kivy for mobile UI
- pywifi for Wi-Fi scanning
- zxcvbn for password strength analysis
