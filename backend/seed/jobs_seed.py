import uuid
from datetime import datetime, timedelta
from app.models import models


def seed_jobs(roles):
    """Seed jobs data with role requirements - spread across Berlin region"""
    now = datetime.now()
    
    # Berlin and surrounding area coordinates (spread across the region)
    berlin_locations = [
        # Central Berlin
        (13.404954, 52.520008, "Berlin", "Alexanderplatz", "1", "10178"),
        (13.388860, 52.517037, "Berlin", "Friedrichstraße", "85", "10117"),
        (13.377704, 52.516071, "Berlin", "Unter den Linden", "42", "10117"),
        (13.401270, 52.520007, "Berlin", "Karl-Liebknecht-Straße", "8", "10178"),
        
        # East Berlin
        (13.429889, 52.508530, "Berlin", "Warschauer Straße", "33", "10243"),
        (13.453416, 52.514223, "Berlin", "Simon-Dach-Straße", "12", "10245"),
        (13.441854, 52.506317, "Berlin", "Boxhagener Straße", "76", "10245"),
        
        # West Berlin
        (13.331889, 52.503892, "Berlin", "Kurfürstendamm", "155", "10709"),
        (13.291720, 52.504043, "Berlin", "Kantstraße", "89", "10627"),
        (13.325097, 52.508629, "Berlin", "Tauentzienstraße", "9", "10789"),
        
        # North Berlin
        (13.387811, 52.547975, "Berlin", "Brunnenstraße", "145", "10115"),
        (13.401389, 52.544270, "Berlin", "Schönhauser Allee", "88", "10439"),
        (13.412440, 52.538326, "Berlin", "Prenzlauer Allee", "234", "10405"),
        
        # South Berlin
        (13.385983, 52.486197, "Berlin", "Gneisenaustraße", "77", "10961"),
        (13.421197, 52.475063, "Berlin", "Karl-Marx-Straße", "156", "12043"),
        (13.404589, 52.461926, "Berlin", "Sonnenallee", "203", "12059"),
        
        # Potsdam area
        (13.064473, 52.390569, "Potsdam", "Brandenburger Straße", "45", "14467"),
        (13.074410, 52.395715, "Potsdam", "Friedrich-Ebert-Straße", "56", "14469"),
        (13.059984, 52.400902, "Potsdam", "Am Neuen Palais", "10", "14469"),
        (13.065722, 52.398189, "Potsdam", "Hegelallee", "24", "14467"),
        
        # Brandenburg an der Havel area
        (12.546284, 52.412067, "Brandenburg", "Hauptstraße", "12", "14770"),
        (12.551742, 52.408779, "Brandenburg", "Steinstraße", "34", "14776"),
        (12.556821, 52.414122, "Brandenburg", "Große Gartenstraße", "67", "14770"),
        (12.540913, 52.406889, "Brandenburg", "Wilhelmsdorfer Straße", "89", "14776"),
        
        # Outskirts and suburbs
        (13.575825, 52.494167, "Erkner", "Friedrichstraße", "45", "15537"),
        (13.240878, 52.413452, "Teltow", "Potsdamer Straße", "123", "14513"),
        (13.265897, 52.578392, "Falkensee", "Bahnhofstraße", "78", "14612"),
        (13.629389, 52.426517, "Woltersdorf", "Schloßstraße", "34", "15569"),
        (13.155642, 52.392761, "Kleinmachnow", "Karl-Marx-Straße", "56", "14532"),
        (13.478531, 52.565139, "Bernau", "Brauerstraße", "90", "16321"),
        
        # Additional Berlin districts
        (13.281389, 52.461639, "Berlin", "Steglitzer Damm", "145", "12169"),
        (13.283056, 52.436111, "Berlin", "Schloßstraße", "78", "12163"),
        (13.589722, 52.519444, "Berlin", "Allee der Kosmonauten", "234", "12681"),
        (13.343889, 52.527778, "Berlin", "Turmstraße", "56", "10551"),
        (13.432778, 52.461667, "Berlin", "Hermannstraße", "123", "12049"),
        (13.467222, 52.484722, "Berlin", "Landsberger Allee", "187", "10369"),
        
        # More outer ring locations
        (13.197222, 52.520833, "Berlin", "Heerstraße", "234", "14052"),
        (13.282500, 52.568056, "Berlin", "Berliner Straße", "67", "13507"),
        (13.577222, 52.453333, "Schönefeld", "Hans-Grade-Allee", "45", "12529"),
        (13.131111, 52.484167, "Stahnsdorf", "Potsdamer Straße", "89", "14532"),
    ]
    
    job_templates = [
        ("Electrical Panel Upgrade", "Upgrade and modernize electrical distribution panel", [0], [0, 5], 8, 4),
        ("Kitchen Plumbing Installation", "Install new kitchen sink, dishwasher, and water lines", [1], [1, 5], 6, 3),
        ("Office Furniture Assembly", "Assemble and install modular office furniture system", [2, 5], [2, 5], 8, 6),
        ("Apartment Painting", "Interior painting of 3-room apartment", [3, 5], [3, 5], 8, 8),
        ("HVAC System Maintenance", "Annual maintenance and inspection of heating system", [4], [4, 5], 4, 2),
        ("Bathroom Renovation", "Complete bathroom renovation with plumbing and tiling", [1, 2], [1, 2, 5], 16, 8),
        ("Lighting Installation", "Install ceiling lights and wall fixtures throughout office", [0, 5], [0, 5], 6, 4),
        ("Window Frame Repair", "Repair and repaint wooden window frames", [2, 3], [2, 3], 6, 4),
        ("Roof Leak Repair", "Identify and repair roof leak, replace damaged materials", [2, 5], [2, 5], 8, 6),
        ("Commercial Kitchen Setup", "Install commercial kitchen equipment with plumbing and electrical", [0, 1], [0, 1, 5], 12, 8),
    ]
    
    jobs = []
    job_items_list = []
    
    for i in range(40):
        location = berlin_locations[i]
        template_idx = i % len(job_templates)
        template = job_templates[template_idx]
        
        job_name, description, role_indices, item_indices, duration_hours, items_count = template
        
        # Add variation to job names
        job_name = f"{job_name} #{i+1}"
        
        # Calculate start time (spread over next 2 weeks, mostly during business hours)
        days_offset = (i // 3) + 1  # Multiple jobs per day
        hour = 7 + (i % 3) * 3  # Start at 7 AM, 10 AM, or 1 PM
        start_time = now + timedelta(days=days_offset, hours=hour)
        end_time = start_time + timedelta(hours=duration_hours)
        
        job = models.Job(
            job_id=str(uuid.uuid4()),
            job_name=job_name,
            job_description=description,
            longitude=location[0],
            latitude=location[1],
            country="Germany",
            city=location[2],
            street=location[3],
            house_number=location[4],
            postal_code=location[5],
            start_datetime=start_time,
            end_datetime=end_time
        )
        
        # Assign roles
        for role_idx in role_indices:
            job.roles.append(roles[role_idx])
        
        jobs.append(job)
        
        # Store item assignments for later (after job IDs are available)
        job_items_list.append((i, item_indices, items_count))
    
    return jobs, job_items_list


def seed_job_items(jobs, items, job_items_list):
    """Seed job-item associations - requires jobs and items to be flushed first"""
    job_items = []
    
    for job_idx, item_indices, items_count in job_items_list:
        job = jobs[job_idx]
        
        # Track which items have been added to avoid duplicates
        added_items = set()
        
        # Safety equipment is always needed
        safety_item_id = items[5].item_id
        job_items.append(
            models.JobItem(
                job_id=job.job_id,
                item_id=safety_item_id,
                required_quantity=max(1, items_count // 4)
            )
        )
        added_items.add(safety_item_id)
        
        # Add specific items based on role requirements (skip if already added)
        for item_idx in item_indices:
            if item_idx < len(items):
                item_id = items[item_idx].item_id
                if item_id not in added_items:
                    quantity = 1 if item_idx == 5 else (items_count // len(item_indices))
                    job_items.append(
                        models.JobItem(
                            job_id=job.job_id,
                            item_id=item_id,
                            required_quantity=max(1, quantity)
                        )
                    )
                    added_items.add(item_id)
    
    return job_items
