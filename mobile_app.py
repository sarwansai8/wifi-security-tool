#!/usr/bin/env python3
"""
Mobile version of the Wi-Fi Security Assessment Tool
Compatible with Android and iOS through Kivy
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.utils import platform
from kivy.core.clipboard import Clipboard
import matplotlib.pyplot as plt
import numpy as np
import threading
import time
import os
import json
import datetime
import socket
import requests
import threading

# Import shared core functionality
from modules.core.wifi_scanner import WiFiScanner
from modules.core.password_analyzer import PasswordAnalyzer
from modules.core.security_analyzer import SecurityAnalyzer

# For QR code scanning
try:
    from kivy.uix.camera import Camera
    CAMERA_AVAILABLE = True
except ImportError:
    CAMERA_AVAILABLE = False

try:
    from pyzbar.pyzbar import decode
    from PIL import Image
    QRCODE_SCAN_AVAILABLE = True
except ImportError:
    QRCODE_SCAN_AVAILABLE = False

class NetworkScannerTab(TabbedPanelItem):
    """Network Scanner tab for mobile interface"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Network Scanner'
        self.networks = []
        self.scanner = WiFiScanner()
        
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Scan controls
        controls = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        self.scan_button = Button(text='Start Scan')
        self.scan_button.bind(on_press=self.toggle_scan)
        controls.add_widget(self.scan_button)
        
        # Progress indicator
        self.progress = ProgressBar(max=100, value=0)
        
        # Network list
        self.network_grid = GridLayout(cols=1, spacing=2, size_hint_y=None)
        self.network_grid.bind(minimum_height=self.network_grid.setter('height'))
        
        scroll = ScrollView()
        scroll.add_widget(self.network_grid)
        
        # Add all elements to layout
        layout.add_widget(controls)
        layout.add_widget(self.progress)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
        
    def toggle_scan(self, instance):
        """Start or stop network scanning"""
        if self.scan_button.text == 'Start Scan':
            self.scan_button.text = 'Stop Scan'
            self.start_scan()
        else:
            self.scan_button.text = 'Start Scan'
            self.stop_scan()
    
    def start_scan(self):
        """Start network scanning"""
        self.networks = []
        self.network_grid.clear_widgets()
        self.progress.value = 0
        
        # Start scan in background thread
        self.scan_thread = threading.Thread(target=self.scan_networks)
        self.scan_thread.daemon = True
        self.scan_thread.start()
        
        # Update UI periodically
        Clock.schedule_interval(self.update_ui, 1)
    
    def stop_scan(self):
        """Stop network scanning"""
        if hasattr(self, 'scan_thread') and self.scan_thread.is_alive():
            self.scanner.stop()
            Clock.unschedule(self.update_ui)
    
    def scan_networks(self):
        """Scan for networks in background thread"""
        try:
            self.networks = self.scanner.scan()
        except Exception as e:
            print(f"Error scanning: {e}")
    
    def update_ui(self, dt):
        """Update UI with scan results"""
        if hasattr(self, 'scan_thread') and not self.scan_thread.is_alive():
            # Scan complete
            self.progress.value = 100
            self.scan_button.text = 'Start Scan'
            Clock.unschedule(self.update_ui)
            
            # Display networks
            self.display_networks()
            return
        
        # Update progress
        self.progress.value += 5
        if self.progress.value > 95:
            self.progress.value = 95
    
    def display_networks(self):
        """Display scanned networks in the UI"""
        self.network_grid.clear_widgets()
        
        for network in self.networks:
            # Create network item
            item = BoxLayout(orientation='vertical', size_hint_y=None, height=100, padding=5)
            item.bind(on_touch_down=lambda x, y, n=network: self.show_network_details(n))
            
            # Add border and background based on security
            if network['encryption'] == 'Open':
                item.background_color = (1, 0.5, 0.5, 1)  # Red
            elif 'WPA2' in network['encryption'] or 'WPA3' in network['encryption']:
                item.background_color = (0.5, 1, 0.5, 1)  # Green
            else:
                item.background_color = (1, 1, 0.5, 1)  # Yellow
            
            # Network info
            ssid = Label(text=f"SSID: {network['ssid']}", halign='left', size_hint_y=None, height=25)
            ssid.bind(size=ssid.setter('text_size'))
            
            encryption = Label(text=f"Security: {network['encryption']}", halign='left', size_hint_y=None, height=25)
            encryption.bind(size=encryption.setter('text_size'))
            
            signal = Label(text=f"Signal: {network['signal']} dBm", halign='left', size_hint_y=None, height=25)
            signal.bind(size=signal.setter('text_size'))
            
            item.add_widget(ssid)
            item.add_widget(encryption)
            item.add_widget(signal)
            
            self.network_grid.add_widget(item)
    
    def show_network_details(self, network):
        """Show detailed information about a network"""
        # This would open a popup with network details
        print(f"Selected network: {network['ssid']}")

class PasswordAnalyzerTab(TabbedPanelItem):
    """Password Analyzer tab for mobile interface"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Password Analyzer'
        self.analyzer = PasswordAnalyzer()
        
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Add basic password analysis UI here
        # ...
        
        self.add_widget(layout)

class SecurityEducationTab(TabbedPanelItem):
    """Security Education tab for mobile interface"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Security Tips'
        
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Add security education content here
        # ...
        
        self.add_widget(layout)


class MonitoringTab(TabbedPanelItem):
    """Continuous Monitoring tab for mobile interface"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Monitoring'
        self.connection_info = None
        self.connected = False
        self.events = []
        self.update_timer = None
        
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Connection section
        connection_box = BoxLayout(orientation='vertical', size_hint_y=None, height=200, padding=5)
        connection_box.add_widget(Label(text='Connect to Monitoring Server', size_hint_y=None, height=30, font_size=18))
        
        # Connection methods
        methods_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        
        # QR Code scanning button
        self.scan_button = Button(text='Scan QR Code')
        self.scan_button.bind(on_press=self.scan_qr_code)
        methods_box.add_widget(self.scan_button)
        
        # Manual entry button
        self.manual_button = Button(text='Manual Entry')
        self.manual_button.bind(on_press=self.show_manual_entry)
        methods_box.add_widget(self.manual_button)
        
        connection_box.add_widget(methods_box)
        
        # Connection status
        self.status_label = Label(text='Not connected', size_hint_y=None, height=30)
        connection_box.add_widget(self.status_label)
        
        # Connect/Disconnect button
        self.connect_button = Button(text='Connect', size_hint_y=None, height=50)
        self.connect_button.bind(on_press=self.toggle_connection)
        self.connect_button.disabled = True
        connection_box.add_widget(self.connect_button)
        
        layout.add_widget(connection_box)
        
        # Events section
        events_label = Label(text='Security Events', size_hint_y=None, height=30, font_size=18)
        layout.add_widget(events_label)
        
        # Events list
        self.events_grid = GridLayout(cols=1, spacing=2, size_hint_y=None)
        self.events_grid.bind(minimum_height=self.events_grid.setter('height'))
        
        scroll = ScrollView()
        scroll.add_widget(self.events_grid)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def scan_qr_code(self, instance):
        """Scan QR code to get connection information"""
        if not CAMERA_AVAILABLE or not QRCODE_SCAN_AVAILABLE:
            popup = Popup(title='QR Scanning Not Available',
                        content=Label(text='QR code scanning requires camera and pyzbar library.\n'
                                    'Please use manual entry instead.'),
                        size_hint=(0.8, 0.4))
            popup.open()
            return
        
        # This would normally use the camera to scan a QR code
        # For simplicity, we'll just show a popup asking for manual entry
        self.show_manual_entry(instance)
    
    def show_manual_entry(self, instance):
        """Show manual entry dialog for connection information"""
        content = BoxLayout(orientation='vertical', padding=10)
        
        # Instructions
        content.add_widget(Label(text='Enter connection details from desktop app:', size_hint_y=None, height=30))
        
        # Text input for JSON
        self.connection_input = TextInput(multiline=True, height=150)
        content.add_widget(self.connection_input)
        
        # Buttons
        buttons = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        
        cancel_btn = Button(text='Cancel')
        connect_btn = Button(text='Connect')
        
        buttons.add_widget(cancel_btn)
        buttons.add_widget(connect_btn)
        content.add_widget(buttons)
        
        # Create popup
        popup = Popup(title='Manual Connection', content=content, size_hint=(0.9, 0.6))
        
        # Bind buttons
        cancel_btn.bind(on_press=popup.dismiss)
        connect_btn.bind(on_press=lambda x: self.process_connection_info(popup))
        
        popup.open()
    
    def process_connection_info(self, popup):
        """Process the entered connection information"""
        try:
            # Parse JSON
            connection_text = self.connection_input.text.strip()
            self.connection_info = json.loads(connection_text)
            
            # Validate required fields
            if not all(k in self.connection_info for k in ['ip', 'port', 'api_key']):
                raise ValueError("Missing required connection information")
            
            # Update UI
            self.status_label.text = f"Ready to connect to {self.connection_info['ip']}:{self.connection_info['port']}"  
            self.connect_button.disabled = False
            
            # Close popup
            popup.dismiss()
            
        except Exception as e:
            # Show error
            error_popup = Popup(title='Connection Error',
                            content=Label(text=f'Error processing connection info: {str(e)}'),
                            size_hint=(0.8, 0.4))
            error_popup.open()
    
    def toggle_connection(self, instance):
        """Connect to or disconnect from the monitoring server"""
        if not self.connected:
            self.connect_to_server()
        else:
            self.disconnect_from_server()
    
    def connect_to_server(self):
        """Connect to the monitoring server"""
        if not self.connection_info:
            return
        
        try:
            # Update UI
            self.status_label.text = "Connecting..."
            
            # Test connection
            url = f"http://{self.connection_info['ip']}:{self.connection_info['port']}/api/status"
            headers = {"Authorization": f"Bearer {self.connection_info['api_key']}"}
            
            # Start in a thread to avoid blocking UI
            threading.Thread(target=self._connect_thread, args=(url, headers)).start()
            
        except Exception as e:
            self.status_label.text = f"Connection error: {str(e)}"
    
    def _connect_thread(self, url, headers):
        """Connection thread to avoid blocking UI"""
        try:
            # This would normally make an actual API request
            # For demo purposes, we'll simulate a successful connection
            # response = requests.get(url, headers=headers, timeout=5)
            # if response.status_code == 200:
            
            # Simulate network delay
            time.sleep(2)
            
            # Update UI on success (must be done in main thread)
            Clock.schedule_once(lambda dt: self._connection_success(), 0)
            
        except Exception as e:
            # Update UI on failure (must be done in main thread)
            Clock.schedule_once(lambda dt: self._connection_failure(str(e)), 0)
    
    def _connection_success(self):
        """Handle successful connection"""
        self.connected = True
        self.status_label.text = "Connected to monitoring server"
        self.connect_button.text = "Disconnect"
        
        # Start periodic updates
        self.update_timer = Clock.schedule_interval(self.update_events, 5)
        
        # Simulate initial events
        self.simulate_events()
    
    def _connection_failure(self, error):
        """Handle connection failure"""
        self.status_label.text = f"Connection failed: {error}"
    
    def disconnect_from_server(self):
        """Disconnect from the monitoring server"""
        if self.update_timer:
            Clock.unschedule(self.update_timer)
        
        self.connected = False
        self.status_label.text = "Disconnected"
        self.connect_button.text = "Connect"
        self.events = []
        self.events_grid.clear_widgets()
    
    def update_events(self, dt):
        """Update security events from server"""
        if not self.connected:
            return
        
        # This would normally fetch events from the server
        # For demo purposes, we'll occasionally add a new event
        if random.random() < 0.3:  # 30% chance of new event
            self.simulate_events(1)
    
    def simulate_events(self, count=3):
        """Simulate security events for demonstration"""
        event_types = [
            "Open Network Detected",
            "Weak Encryption",
            "New Device Connected",
            "Suspicious Activity",
            "Signal Strength Low"
        ]
        
        severities = ["INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"]
        
        for _ in range(count):
            event_type = random.choice(event_types)
            severity = random.choice(severities)
            
            event = {
                "id": len(self.events) + 1,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "type": event_type,
                "severity": severity,
                "description": f"{event_type} on your network"
            }
            
            self.events.append(event)
        
        # Update UI
        self.display_events()
        
        # Show notification for high severity events
        for event in self.events[-count:]:
            if event["severity"] in ["HIGH", "CRITICAL"]:
                self.show_notification(event)
    
    def display_events(self):
        """Display security events in the UI"""
        self.events_grid.clear_widgets()
        
        # Sort events by timestamp (newest first)
        sorted_events = sorted(self.events, key=lambda e: e["timestamp"], reverse=True)
        
        for event in sorted_events:
            # Create event item
            item = BoxLayout(orientation='vertical', size_hint_y=None, height=100, padding=5)
            
            # Set background based on severity
            if event["severity"] == "CRITICAL":
                color = "#ffcccc"  # Light red
            elif event["severity"] == "HIGH":
                color = "#ffe0cc"  # Light orange
            elif event["severity"] == "MEDIUM":
                color = "#ffffcc"  # Light yellow
            elif event["severity"] == "LOW":
                color = "#e6f2ff"  # Light blue
            else:  # INFO
                color = "#e6ffe6"  # Light green
            
            # Event info
            header = BoxLayout(orientation='horizontal', size_hint_y=None, height=25)
            time_label = Label(text=event["timestamp"], size_hint_x=0.6, halign='left')
            severity_label = Label(text=event["severity"], size_hint_x=0.4, halign='right')
            header.add_widget(time_label)
            header.add_widget(severity_label)
            
            type_label = Label(text=event["type"], halign='left', size_hint_y=None, height=25, bold=True)
            desc_label = Label(text=event["description"], halign='left', size_hint_y=None, height=50)
            
            item.add_widget(header)
            item.add_widget(type_label)
            item.add_widget(desc_label)
            
            self.events_grid.add_widget(item)
    
    def show_notification(self, event):
        """Show a notification for a security event"""
        popup = Popup(title=f'Security Alert: {event["severity"]}',
                    content=Label(text=event["description"]),
                    size_hint=(0.8, 0.4))
        popup.open()

class WifiSecurityMobileApp(App):
    """Mobile version of the Wi-Fi Security Assessment Tool"""
    
    def build(self):
        """Build the mobile UI"""
        # Create main tabbed interface
        tabs = TabbedPanel(do_default_tab=False)
        
        # Add tabs
        tabs.add_widget(NetworkScannerTab())
        tabs.add_widget(PasswordAnalyzerTab())
        tabs.add_widget(SecurityEducationTab())
        tabs.add_widget(MonitoringTab())
        
        return tabs

if __name__ == '__main__':
    WifiSecurityMobileApp().run()
