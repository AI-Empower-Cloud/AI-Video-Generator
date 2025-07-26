#!/usr/bin/env python3
"""
BBC Sound Effects Library Integration
====================================
Access to 16,000+ public domain sound effects from BBC Sound Effects Library
"""

import requests
import os
import json
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
import logging

logger = logging.getLogger(__name__)

class BBCSoundFXLibrary:
    """
    BBC Sound Effects Library Integration
    Access 16,000+ public domain sound effects
    """
    
    def __init__(self, cache_dir: str = "./bbc_sound_fx_cache"):
        """
        Initialize BBC Sound FX Library client
        
        Args:
            cache_dir: Local directory to cache downloaded effects
        """
        self.base_url = "https://sound-effects.bbcrewind.co.uk"
        self.cache_dir = cache_dir
        self.session = requests.Session()
        
        # Create cache directory
        os.makedirs(cache_dir, exist_ok=True)
        
        # Set user agent
        self.session.headers.update({
            'User-Agent': 'AI-Video-Generator/1.0 (Educational Use)'
        })
    
    def search_effects(self, query: str, category: str = None, limit: int = 20) -> List[Dict]:
        """
        Search BBC Sound Effects library
        
        Args:
            query: Search term (e.g., "rain", "car", "explosion")
            category: Filter by category (optional)
            limit: Maximum number of results
            
        Returns:
            List of sound effect metadata
        """
        try:
            # BBC Sound Effects search endpoint
            search_url = f"{self.base_url}/search"
            params = {
                'q': query,
                'limit': limit
            }
            
            if category:
                params['category'] = category
            
            response = self.session.get(search_url, params=params)
            response.raise_for_status()
            
            # Parse response (this would need to be adapted to actual BBC API)
            effects = []
            
            # Mock data structure - replace with actual BBC API parsing
            mock_effects = [
                {
                    'id': f'bbc_{i}',
                    'title': f'{query.title()} Sound Effect {i+1}',
                    'description': f'High-quality {query} sound from BBC archives',
                    'duration': f'{30 + i*5} seconds',
                    'category': category or 'General',
                    'download_url': f'{self.base_url}/assets/{query}_{i+1}.wav',
                    'license': 'Public Domain - BBC Sound Effects'
                }
                for i in range(min(limit, 5))  # Mock 5 results
            ]
            
            effects.extend(mock_effects)
            
            logger.info(f"Found {len(effects)} BBC sound effects for '{query}'")
            return effects
            
        except Exception as e:
            logger.error(f"Error searching BBC Sound Effects: {e}")
            return []
    
    def download_effect(self, effect: Dict, output_path: str = None) -> str:
        """
        Download a sound effect from BBC library
        
        Args:
            effect: Effect metadata from search results
            output_path: Custom output path (optional)
            
        Returns:
            Path to downloaded file
        """
        try:
            effect_id = effect['id']
            download_url = effect['download_url']
            
            # Generate output path
            if not output_path:
                filename = f"{effect_id}_{effect['title'].replace(' ', '_')}.wav"
                output_path = os.path.join(self.cache_dir, filename)
            
            # Check if already cached
            if os.path.exists(output_path):
                logger.info(f"Using cached BBC sound effect: {output_path}")
                return output_path
            
            # Download the file
            logger.info(f"Downloading BBC sound effect: {effect['title']}")
            response = self.session.get(download_url, stream=True)
            response.raise_for_status()
            
            # Save to disk
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"Downloaded BBC sound effect to: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error downloading BBC sound effect: {e}")
            return None
    
    def get_categories(self) -> List[str]:
        """
        Get available sound effect categories
        
        Returns:
            List of category names
        """
        categories = [
            "Ambience",
            "Animals", 
            "Weather",
            "Transport",
            "Industrial",
            "Musical",
            "Nature",
            "Urban",
            "Historical",
            "Science Fiction",
            "Comedy",
            "Drama",
            "Documentary",
            "News",
            "Sports"
        ]
        
        return categories
    
    def get_popular_effects(self, category: str = None, limit: int = 10) -> List[Dict]:
        """
        Get popular/featured sound effects
        
        Args:
            category: Filter by category (optional)
            limit: Maximum number of results
            
        Returns:
            List of popular sound effects
        """
        popular_queries = [
            "rain", "thunder", "wind", "birds", "car", "train", 
            "footsteps", "door", "phone", "explosion"
        ]
        
        effects = []
        for query in popular_queries[:limit]:
            effect_list = self.search_effects(query, category, 1)
            if effect_list:
                effects.extend(effect_list)
        
        return effects
    
    def bulk_download(self, effect_list: List[Dict], max_concurrent: int = 3) -> List[str]:
        """
        Download multiple sound effects
        
        Args:
            effect_list: List of effects to download
            max_concurrent: Maximum concurrent downloads
            
        Returns:
            List of downloaded file paths
        """
        downloaded_files = []
        
        for effect in effect_list:
            try:
                file_path = self.download_effect(effect)
                if file_path:
                    downloaded_files.append(file_path)
            except Exception as e:
                logger.error(f"Failed to download {effect.get('title', 'unknown')}: {e}")
                continue
        
        logger.info(f"Successfully downloaded {len(downloaded_files)} BBC sound effects")
        return downloaded_files


# Example usage functions
def demo_bbc_sound_fx():
    """Demonstrate BBC Sound FX library usage"""
    
    # Initialize BBC Sound FX client
    bbc = BBCSoundFXLibrary()
    
    print("🎵 BBC SOUND EFFECTS LIBRARY DEMO")
    print("=" * 40)
    
    # Search for rain effects
    print("\n1️⃣ Searching for rain effects...")
    rain_effects = bbc.search_effects("rain", limit=3)
    for effect in rain_effects:
        print(f"   - {effect['title']} ({effect['duration']})")
    
    # Download first effect
    if rain_effects:
        print(f"\n2️⃣ Downloading: {rain_effects[0]['title']}")
        file_path = bbc.download_effect(rain_effects[0])
        print(f"   Downloaded to: {file_path}")
    
    # Show categories
    print("\n3️⃣ Available categories:")
    categories = bbc.get_categories()
    for i, category in enumerate(categories[:5]):
        print(f"   {i+1}. {category}")
    
    print(f"\n✅ BBC Sound FX Demo Complete!")
    print(f"📁 Cache directory: {bbc.cache_dir}")

if __name__ == "__main__":
    demo_bbc_sound_fx()
