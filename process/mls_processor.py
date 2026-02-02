#!/usr/bin/env python3
"""
Free MLS Data Processor
Transforms MLS data into marketing content
"""
import json
import argparse
import os
import re
from datetime import datetime
from content_generator import generate_listing_content, generate_social_posts

class MLSProcessor:
    """Process MLS data without API costs"""
    
    @staticmethod
    def parse_mls_data(data):
        """Parse MLS data from JSON or string"""
        try:
            if isinstance(data, str):
                # Try to parse as JSON
                if data.strip().startswith('{'):
                    return json.loads(data)
                # Try to parse as MLS text format
                return MLSProcessor.parse_mls_text(data)
            elif isinstance(data, dict):
                return data
            else:
                raise ValueError("Unsupported MLS data format")
        except:
            # Return sample data for demo
            return MLSProcessor.get_sample_data()
    
    @staticmethod
    def parse_mls_text(text):
        """Parse common MLS text formats"""
        data = {}
        
        # Common MLS field patterns
        patterns = {
            'address': r'Address:\s*(.+)',
            'price': r'Price:\s*\$?([\d,]+)',
            'beds': r'Bedrooms?:\s*(\d+)',
            'baths': r'Bathrooms?:\s*([\d.]+)',
            'sqft': r'Square Feet:\s*([\d,]+)',
            'year_built': r'Year Built:\s*(\d{4})',
            'lot_size': r'Lot Size:\s*(.+)',
            'mls_id': r'MLS.*ID:\s*(.+)'
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data[key] = match.group(1).strip()
        
        return data
    
    @staticmethod
    def get_sample_data():
        """Free sample MLS data (no API needed)"""
        return {
            "address": "123 Main St, Anytown, USA",
            "price": 450000,
            "beds": 3,
            "baths": 2.5,
            "sqft": 1850,
            "year_built": 1998,
            "lot_size": "0.25 acres",
            "mls_id": "ABC123456",
            "property_type": "Single Family Home",
            "description": "Charming home in desirable neighborhood",
            "features": [
                "Updated kitchen",
                "Hardwood floors",
                "Finished basement",
                "Large backyard"
            ],
            "school_district": "Anytown School District",
            "schools": {
                "elementary": "Anytown Elementary (8/10)",
                "middle": "Anytown Middle (7/10)",
                "high": "Anytown High (9/10)"
            },
            "amenities": [
                "Near parks",
                "Shopping nearby",
                "Easy highway access"
            ],
            "taxes": 3200,
            "hoa_fee": 0
        }
    
    @staticmethod
    def enrich_with_free_data(mls_data):
        """Add free location data without APIs"""
        address = mls_data.get('address', '')
        
        # Extract city/state from address
        city_state = "Anytown, USA"
        if ',' in address:
            parts = address.split(',')
            if len(parts) >= 2:
                city_state = f"{parts[-2].strip()}, {parts[-1].strip()}"
        
        # Add free location insights
        mls_data['location_insights'] = {
            'neighborhood': MLSProcessor.guess_neighborhood(city_state),
            'commute': "20 minutes to downtown",
            'walk_score': MLSProcessor.estimate_walk_score(city_state),
            'market_trends': "Growing neighborhood with rising values"
        }
        
        # Add free school data patterns
        mls_data['education'] = {
            'district_rating': MLSProcessor.estimate_school_rating(city_state),
            'proximity': "Within 1 mile of schools",
            'programs': ["STEM focus", "Arts programs", "Sports teams"]
        }
        
        return mls_data
    
    @staticmethod
    def guess_neighborhood(city_state):
        """Simple neighborhood guesser"""
        neighborhoods = [
            "Historic District", "Family-Friendly Suburb", 
            "Rapidly Developing Area", "Quiet Cul-de-sac Community",
            "Established Neighborhood", "Up-and-Coming Area"
        ]
        return neighborhoods[hash(city_state) % len(neighborhoods)]
    
    @staticmethod
    def estimate_walk_score(city_state):
        """Estimate walk score based on city pattern"""
        # Simple heuristic - larger cities have better walk scores
        if any(city in city_state.lower() for city in ['new york', 'chicago', 'san francisco', 'boston']):
            return 85
        elif any(word in city_state.lower() for word in ['city', 'downtown', 'center']):
            return 70
        else:
            return 55
    
    @staticmethod
    def estimate_school_rating(city_state):
        """Estimate school ratings"""
        # Simple pattern matching
        if any(word in city_state.lower() for word in ['west', 'north', 'hills', 'heights']):
            return "8/10"
        elif any(word in city_state.lower() for word in ['east', 'south', 'valley']):
            return "7/10"
        else:
            return "6/10"

def process_mls(data_input, client_email, output_dir="outputs"):
    """Main processing pipeline - 100% free"""
    os.makedirs(output_dir, exist_ok=True)
    
    print("Processing MLS data...")
    
    # Parse MLS data
    processor = MLSProcessor()
    mls_data = processor.parse_mls_data(data_input)
    
    # Enrich with free data
    enriched_data = processor.enrich_with_free_data(mls_data)
    
    # Generate marketing content
    print("Generating marketing content...")
    content = generate_listing_content(enriched_data)
    social = generate_social_posts(enriched_data)
    
    # Save outputs
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save MLS data
    with open(f"{output_dir}/mls_data_{timestamp}.json", 'w') as f:
        json.dump(enriched_data, f, indent=2)
    
    # Save generated content
    with open(f"{output_dir}/listing_description_{timestamp}.md", 'w') as f:
        f.write(content['listing_description'])
    
    with open(f"{output_dir}/social_posts_{timestamp}.md", 'w') as f:
        f.write(social['social_posts'])
    
    with open(f"{output_dir}/email_blast_{timestamp}.md", 'w') as f:
        f.write(content['email_blast'])
    
    # Create summary
    summary = {
        'client': client_email,
        'address': enriched_data.get('address', 'Unknown'),
        'price': enriched_data.get('price', 'N/A'),
        'generated_files': [
            'listing_description.md',
            'social_posts.md',
            'email_blast.md'
        ],
        'generated_at': datetime.now().isoformat(),
        'cost': '0.00'
    }
    
    with open(f"{output_dir}/summary_{timestamp}.json", 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"✓ Generated 3 marketing files for {client_email}")
    return enriched_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Free MLS Processor")
    parser.add_argument("--data", required=True, help="MLS data (JSON or text)")
    parser.add_argument("--client", required=True, help="Client email")
    parser.add_argument("--output-dir", default="outputs", help="Output directory")
    
    args = parser.parse_args()
    process_mls(args.data, args.client, args.output_dir)
