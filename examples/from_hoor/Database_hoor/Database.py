

import os
import random
from datetime import datetime, timedelta
from typing import List, Tuple, Optional
import logging
from dataclasses import dataclass

# Database and ORM imports
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool

# Scheduler import
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('travel_time.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Step 1: Database Setup
# Create database model using SQLAlchemy ORM

Base = declarative_base()

class TravelTimeRecord(Base):
    """Database model for storing travel time estimates"""
    __tablename__ = 'travel_times'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    source = Column(String(100), nullable=False)
    destination = Column(String(100), nullable=False)
    travel_time_minutes = Column(Float, nullable=False)
    
    def __repr__(self):
        return f"<TravelTime(source='{self.source}', dest='{self.destination}', time={self.travel_time_minutes})>"

# Step 2: Database Connection Manager
class DatabaseManager:
    """Manages database connections with connection pooling"""
    
    def __init__(self, database_url: str = None):
        if database_url is None:
            # Default to SQLite for demo (replace with MySQL URL in production)
            database_url = "sqlite:///travel_times.db"
            # For MySQL: "mysql+pymysql://user:password@localhost/travel_times"
        
        # Create engine with connection pooling
        self.engine = create_engine(
            database_url,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            pool_recycle=3600,  # Recycle connections after 1 hour
            echo=False  # Set to True for SQL debugging
        )
        
        # Create session factory
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        # Create tables if they don't exist
        self.create_tables()
        logger.info("[INFO] Connected to database")
    
    def create_tables(self):
        """Create database tables"""
        Base.metadata.create_all(bind=self.engine)
        logger.info("[INFO] Database tables created/verified")
    
    def get_session(self) -> Session:
        """Get database session with automatic cleanup"""
        return self.SessionLocal()
    
    def close(self):
        """Close database engine"""
        self.engine.dispose()
        logger.info("[INFO] Database connection closed")

# Step 3: Travel Time Service
class TravelTimeService:
    """Service for recording and retrieving travel time data"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def get_travel_time_estimate(self, source: str, destination: str) -> float:
        """
        Simulate getting travel time estimate from external API
        In production, this would call Google Maps API, Waze API, etc.
        """
        # Simulate realistic travel times with some randomness
        base_times = {
            ("home", "work"): 25,
            ("work", "home"): 27,
            ("home", "store"): 15,
            ("store", "home"): 16,
        }
        
        route = (source.lower(), destination.lower())
        base_time = base_times.get(route, 20)  # Default 20 minutes
        
        # Add random variation (±5 minutes)
        variation = random.uniform(-5, 5)
        return max(5, base_time + variation)  # Minimum 5 minutes
    
    def record_travel_time(self, source: str, destination: str) -> bool:
        """
        Record current travel time estimate to database
        Returns True if successful, False otherwise
        """
        try:
            # Get travel time estimate
            travel_time = self.get_travel_time_estimate(source, destination)
            
            # Record to database
            with self.db_manager.get_session() as session:
                record = TravelTimeRecord(
                    source=source,
                    destination=destination,
                    travel_time_minutes=round(travel_time, 1),
                    timestamp=datetime.now()
                )
                session.add(record)
                session.commit()
                
                logger.info(f"[INFO] Recorded travel time: {travel_time:.0f} minutes ({source} -> {destination}) at {record.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                return True
                
        except Exception as e:
            logger.error(f"[ERROR] Failed to record travel time: {e}")
            return False
    
    def get_historical_data(self, source: str, destination: str, date: str) -> List[Tuple[datetime, float]]:
        """
        Retrieve historical travel time data for a specific route and date
        
        Args:
            source: Starting location
            destination: Ending location  
            date: Date string in format 'YYYY-MM-DD'
        
        Returns:
            List of (timestamp, travel_time) tuples
        """
        try:
            # Parse date
            target_date = datetime.strptime(date, '%Y-%m-%d').date()
            
            with self.db_manager.get_session() as session:
                records = session.query(TravelTimeRecord).filter(
                    TravelTimeRecord.source == source,
                    TravelTimeRecord.destination == destination,
                    TravelTimeRecord.timestamp >= target_date,
                    TravelTimeRecord.timestamp < target_date + timedelta(days=1)
                ).order_by(TravelTimeRecord.timestamp).all()
                
                return [(record.timestamp, record.travel_time_minutes) for record in records]
                
        except Exception as e:
            logger.error(f"[ERROR] Failed to retrieve historical data: {e}")
            return []

# Step 4: Scheduler for Automated Data Collection
class TravelTimeScheduler:
    """Scheduler for automatically recording travel time data"""
    
    def __init__(self, travel_service: TravelTimeService):
        self.travel_service = travel_service
        self.scheduler = BlockingScheduler()
        self.routes = [
            ("home", "work"),
            ("work", "home"),
            ("home", "store"),
            ("store", "home")
        ]
    
    def record_all_routes(self):
        """Record travel times for all configured routes"""
        logger.info("[INFO] Starting scheduled travel time recording...")
        
        for source, destination in self.routes:
            self.travel_service.record_travel_time(source, destination)
    
    def start_scheduler(self):
        """Start the scheduler to record data every 15 minutes"""
        logger.info("[INFO] Starting travel time scheduler (every 15 minutes)...")
        
        # Schedule job to run every 15 minutes
        self.scheduler.add_job(
            func=self.record_all_routes,
            trigger=IntervalTrigger(minutes=15),
            id='travel_time_recording',
            name='Record travel times',
            replace_existing=True
        )
        
        # Run once immediately
        self.record_all_routes()
        
        try:
            self.scheduler.start()
        except KeyboardInterrupt:
            logger.info("[INFO] Scheduler stopped by user")
            self.scheduler.shutdown()

# Step 5: Main Application Class
class TravelTimeApp:
    """Main application orchestrating all components"""
    
    def __init__(self):
        # Initialize database manager
        self.db_manager = DatabaseManager()
        
        # Initialize travel time service
        self.travel_service = TravelTimeService(self.db_manager)
        
        # Initialize scheduler
        self.scheduler = TravelTimeScheduler(self.travel_service)
    
    def demonstrate_functionality(self):
        """Demonstrate the system functionality with sample data"""
        logger.info("=== Travel Time Tracking System Demo ===")
        
        # Step 1: Record some sample data
        logger.info("\n--- Recording Sample Travel Times ---")
        routes = [("home", "work"), ("work", "home"), ("home", "store")]
        
        for source, dest in routes:
            self.travel_service.record_travel_time(source, dest)
        
        # Step 2: Retrieve and display historical data
        logger.info("\n--- Retrieving Historical Data ---")
        today = datetime.now().strftime('%Y-%m-%d')
        
        historical_data = self.travel_service.get_historical_data("home", "work", today)
        
        if historical_data:
            print(f"\nDate: {today}")
            for timestamp, travel_time in historical_data:
                print(f"{timestamp.strftime('%H:%M:%S')} - {travel_time:.0f} minutes")
        else:
            print("No historical data found for today")
    
    def start_continuous_monitoring(self):
        """Start continuous monitoring (runs indefinitely)"""
        logger.info("Starting continuous travel time monitoring...")
        logger.info("Press Ctrl+C to stop")
        
        try:
            self.scheduler.start_scheduler()
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        logger.info("Cleaning up resources...")
        self.db_manager.close()

# Step 6: Usage Examples and Entry Point
def main():
    """Main entry point demonstrating different usage patterns"""
    
    # Create application instance
    app = TravelTimeApp()
    
    try:
        # Option 1: Run demonstration
        print("Choose an option:")
        print("1. Run demonstration (record sample data and show results)")
        print("2. Start continuous monitoring (every 15 minutes)")
        
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == "1":
            app.demonstrate_functionality()
        elif choice == "2":
            app.start_continuous_monitoring()
        else:
            print("Invalid choice. Running demonstration...")
            app.demonstrate_functionality()
            
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
    finally:
        app.cleanup()

# Step 7: Advanced Features (Optional)
class TravelTimeAnalyzer:
    """Advanced analytics for travel time data"""
    
    def __init__(self, travel_service: TravelTimeService):
        self.travel_service = travel_service
    
    def get_average_travel_time(self, source: str, destination: str, days_back: int = 7) -> Optional[float]:
        """Calculate average travel time for a route over specified days"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        with self.travel_service.db_manager.get_session() as session:
            records = session.query(TravelTimeRecord).filter(
                TravelTimeRecord.source == source,
                TravelTimeRecord.destination == destination,
                TravelTimeRecord.timestamp >= start_date,
                TravelTimeRecord.timestamp <= end_date
            ).all()
            
            if records:
                total_time = sum(record.travel_time_minutes for record in records)
                return total_time / len(records)
            return None
    
    def get_peak_hours(self, source: str, destination: str) -> List[Tuple[int, float]]:
        """Identify peak traffic hours for a route"""
        with self.travel_service.db_manager.get_session() as session:
            records = session.query(TravelTimeRecord).filter(
                TravelTimeRecord.source == source,
                TravelTimeRecord.destination == destination
            ).all()
            
            # Group by hour and calculate average
            hourly_data = {}
            for record in records:
                hour = record.timestamp.hour
                if hour not in hourly_data:
                    hourly_data[hour] = []
                hourly_data[hour].append(record.travel_time_minutes)
            
            # Calculate averages and sort by travel time (descending)
            peak_hours = []
            for hour, times in hourly_data.items():
                avg_time = sum(times) / len(times)
                peak_hours.append((hour, avg_time))
            
            return sorted(peak_hours, key=lambda x: x[1], reverse=True)

if __name__ == "__main__":
    main()
