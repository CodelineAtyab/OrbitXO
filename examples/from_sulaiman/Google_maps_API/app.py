"""
Web interface for Google Maps Route Tracking System
This Flask application provides a web frontend to the route tracking system.
"""
from flask import Flask, render_template, request, jsonify
import sys
import os
import logging
from datetime import datetime

# Add the current directory to the path to import main.py modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import functions from main.py
from main import run_complete_system, setup_environment

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/web_app.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("web_app")

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/track_route', methods=['POST'])
def track_route():
    """API endpoint to track a route between two locations"""
    try:
        # Get form data
        origin = request.form.get('origin', '')
        destination = request.form.get('destination', '')
        
        if not origin or not destination:
            return jsonify({
                'success': False,
                'message': 'Both origin and destination are required'
            })
        
        logger.info(f"Web request to track route from {origin} to {destination}")
        
        # Call the main system
        result = run_complete_system(
            origin=origin,
            destination=destination,
            continuous=False,
            interval=300,
            slack_notify=True
        )
        
        if result:
            # Get route data from the tracker
            from route_tracker import RouteTracker
            tracker = RouteTracker(origin=origin, destination=destination)
            route_data = tracker.check_route()
            
            if route_data:
                return jsonify({
                    'success': True,
                    'message': 'Route tracked successfully',
                    'data': {
                        'origin': route_data['origin'],
                        'destination': route_data['destination'],
                        'distance': route_data['distance_text'],
                        'distance_meters': route_data['distance_meters'],
                        'duration': route_data['duration_text'],
                        'duration_seconds': route_data['duration_seconds'],
                        'is_min_distance': route_data['is_min_distance'],
                        'is_min_duration': route_data['is_min_duration'],
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Route tracking completed but no data was returned'
                })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to track route. Check logs for details.'
            })
    
    except Exception as e:
        logger.error(f"Error processing route tracking request: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/api_status')
def api_status():
    """Check if the Google Maps API key is configured"""
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    return jsonify({
        'api_configured': bool(api_key)
    })

if __name__ == '__main__':
    # Setup environment before starting
    setup_environment()
    
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
        logger.info("Created templates directory")
    
    # Create static directory if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')
        logger.info("Created static directory")
    
    # Start the Flask app
    logger.info("Starting web application")
    app.run(debug=True, host='0.0.0.0', port=5000)
