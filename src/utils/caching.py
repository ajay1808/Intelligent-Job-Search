import os
import json
from datetime import datetime, timedelta

CACHE_DIR = "cache"
CACHE_FILE = os.path.join(CACHE_DIR, "job_cache.json")
CACHE_DURATION_DAYS = 7

def load_cache():
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=4)

def add_to_cache(job_postings):
    cache = load_cache()
    cache["last_updated"] = datetime.now().isoformat()
    if "jobs" not in cache:
        cache["jobs"] = []
    
    # Create a set of existing URLs for faster lookup
    existing_urls = {job['url'] for job in cache['jobs']}
    
    for job in job_postings:
        if job.get("url") and job["url"] not in existing_urls:
            cache["jobs"].append(job)
            existing_urls.add(job["url"])
    
    save_cache(cache)

def is_cache_valid():
    cache = load_cache()
    if "last_updated" in cache:
        last_updated = datetime.fromisoformat(cache["last_updated"])
        if datetime.now() - last_updated < timedelta(days=CACHE_DURATION_DAYS):
            return True
    return False

def get_cached_jobs():
    cache = load_cache()
    return cache.get("jobs", [])

def clear_cache():
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
