#!/usr/bin/env python3
"""
Web version of the Wi-Fi Security Assessment Tool
Allows access from multiple devices simultaneously
"""

from flask import Flask, jsonify, request, render_template, send_from_directory
import os
import json
import datetime
import logging

# Import core functionality
from modules.core.password_analyzer import PasswordAnalyzer
from modules.core.security_analyzer import SecurityAnalyzer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("wifi_security_tool.web")

# Initialize Flask app
app = Flask(__name__, 
            static_folder='web/static',
            template_folder='web/templates')

# Initialize analyzers
password_analyzer = PasswordAnalyzer()
security_analyzer = SecurityAnalyzer()

# Store scan results (in a real app, this would be a database)
scan_results = {}

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/password/analyze', methods=['POST'])
def analyze_password():
    """Analyze password strength"""
    data = request.get_json()
    password = data.get('password', '')
    
    if not password:
        return jsonify({'error': 'No password provided'}), 400
    
    result = password_analyzer.analyze_password(password)
    return jsonify(result)

@app.route('/api/password/generate', methods=['GET'])
def generate_password():
    """Generate a strong password"""
    length = request.args.get('length', 16, type=int)
    include_upper = request.args.get('upper', 'true').lower() == 'true'
    include_lower = request.args.get('lower', 'true').lower() == 'true'
    include_digits = request.args.get('digits', 'true').lower() == 'true'
    include_special = request.args.get('special', 'true').lower() == 'true'
    
    password = password_analyzer.generate_password(
        length, include_upper, include_lower, include_digits, include_special
    )
    
    return jsonify({'password': password})

@app.route('/api/security/tips', methods=['GET'])
def get_security_tips():
    """Get Wi-Fi security tips"""
    category = request.args.get('category')
    tips = security_analyzer.get_security_tips(category)
    return jsonify(tips)

@app.route('/api/scan/submit', methods=['POST'])
def submit_scan():
    """Submit scan results from a device"""
    data = request.get_json()
    networks = data.get('networks', [])
    device_id = data.get('device_id', 'unknown')
    
    if not networks:
        return jsonify({'error': 'No networks provided'}), 400
    
    # Store scan results with timestamp
    scan_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    scan_results[scan_id] = {
        'timestamp': datetime.datetime.now().isoformat(),
        'device_id': device_id,
        'networks': networks
    }
    
    # Generate security report
    report = security_analyzer.generate_security_report(networks)
    
    return jsonify({
        'scan_id': scan_id,
        'report': report
    })

@app.route('/api/scan/results', methods=['GET'])
def get_scan_results():
    """Get all scan results"""
    return jsonify(scan_results)

@app.route('/api/scan/<scan_id>', methods=['GET'])
def get_scan_by_id(scan_id):
    """Get specific scan results by ID"""
    if scan_id not in scan_results:
        return jsonify({'error': 'Scan ID not found'}), 404
    
    return jsonify(scan_results[scan_id])

if __name__ == '__main__':
    # Create directories if they don't exist
    os.makedirs('web/templates', exist_ok=True)
    os.makedirs('web/static', exist_ok=True)
    
    # Get port from environment variable (for Heroku compatibility)
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    app.run(host='0.0.0.0', port=port)
