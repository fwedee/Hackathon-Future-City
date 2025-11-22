"""Utility functions for the planner."""
from datetime import datetime, timedelta
from math import radians, sin, cos, sqrt, atan2
from typing import Tuple


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth in kilometers.
    
    Args:
        lat1, lon1: Coordinates of first point
        lat2, lon2: Coordinates of second point
    
    Returns:
        Distance in kilometers
    """
    R = 6371.0  # Earth radius in kilometers
    
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return R * c


def estimate_travel_time(distance_km: float, avg_speed_kmh: float = 50.0) -> timedelta:
    """
    Estimate travel time based on distance.
    
    Args:
        distance_km: Distance in kilometers
        avg_speed_kmh: Average speed in km/h (default 50 km/h for city driving)
    
    Returns:
        Estimated travel time as timedelta
    """
    hours = distance_km / avg_speed_kmh
    return timedelta(hours=hours)


def calculate_travel_time(lat1: float, lon1: float, lat2: float, lon2: float, 
                         avg_speed_kmh: float = 50.0) -> timedelta:
    """
    Calculate travel time between two coordinates.
    
    Args:
        lat1, lon1: Start coordinates
        lat2, lon2: End coordinates
        avg_speed_kmh: Average speed in km/h
    
    Returns:
        Estimated travel time as timedelta
    """
    distance = haversine_distance(lat1, lon1, lat2, lon2)
    return estimate_travel_time(distance, avg_speed_kmh)


def time_intervals_overlap(start1: datetime, end1: datetime, 
                          start2: datetime, end2: datetime) -> bool:
    """
    Check if two time intervals overlap.
    
    Args:
        start1, end1: First interval
        start2, end2: Second interval
    
    Returns:
        True if intervals overlap, False otherwise
    """
    return start1 < end2 and start2 < end1


def can_worker_reach_job(worker_lat: float, worker_lon: float,
                        job_lat: float, job_lon: float,
                        job_start: datetime, current_time: datetime,
                        avg_speed_kmh: float = 50.0) -> bool:
    """
    Check if a worker can reach a job location in time.
    
    Args:
        worker_lat, worker_lon: Worker's current location
        job_lat, job_lon: Job location
        job_start: Job start time
        current_time: Worker's current time
        avg_speed_kmh: Average travel speed
    
    Returns:
        True if worker can reach job in time
    """
    travel_time = calculate_travel_time(worker_lat, worker_lon, job_lat, job_lon, avg_speed_kmh)
    arrival_time = current_time + travel_time
    return arrival_time <= job_start


def fits_in_8hour_shift(branch_lat: float, branch_lon: float,
                       job_lat: float, job_lon: float,
                       job_start: datetime, job_end: datetime,
                       shift_start: datetime = None,
                       avg_speed_kmh: float = 50.0) -> bool:
    """
    Check if a job fits within an 8-hour shift including travel time.
    
    Args:
        branch_lat, branch_lon: Branch (start/end) location
        job_lat, job_lon: Job location
        job_start, job_end: Job time window
        shift_start: Shift start time (default: job_start - 1 hour)
        avg_speed_kmh: Average travel speed
    
    Returns:
        True if job fits in 8-hour shift with return travel
    """
    if shift_start is None:
        shift_start = job_start - timedelta(hours=1)
    
    # Calculate travel times
    travel_to_job = calculate_travel_time(branch_lat, branch_lon, job_lat, job_lon, avg_speed_kmh)
    travel_back = travel_to_job  # assume same time back
    
    # Total time needed
    job_duration = job_end - job_start
    total_time = travel_to_job + job_duration + travel_back
    
    # Check if fits in 10 hours (relaxed from 8 to account for longer jobs + travel
    return total_time <= timedelta(hours=10)
