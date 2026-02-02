"""
Free MLS Content Generator
Creates marketing content from MLS data
"""
import random
from datetime import datetime

class ContentGenerator:
    """Generate real estate marketing content - 100% free"""
    
    @staticmethod
    def generate_listing_content(mls_data):
        """Create professional listing description"""
        address = mls_data.get('address', 'Beautiful Home')
        price = mls_data.get('price', 0)
        beds = mls_data.get('beds', 3)
        baths = mls_data.get('baths', 2)
        sqft = mls_data.get('sqft', 2000)
        
        # Format price
        price_str = f"${price:,}" if isinstance(price, (int, float)) else price
        
        # Select templates based on property type
        property_type = mls_data.get('property_type', '').lower()
        
        templates = {
            'family': [
                f"""Welcome to your dream home at {address}! This stunning {beds} bedroom, {baths} bath residence offers {sqft} sqft of beautifully appointed living space.

🏡 HOME HIGHLIGHTS:
• Spacious open-concept floor plan perfect for entertaining
• Gourmet kitchen with stainless appliances and granite counters
• Luxurious master suite with walk-in closet
• Professionally landscaped backyard oasis
• Hardwood floors throughout main living areas
• Energy-efficient upgrades including new HVAC (2020)

🎓 EXCELLENT SCHOOLS:
Located in the highly-rated {mls_data.get('school_district', 'local')} school district, with {mls_data.get('schools', {}).get('elementary', 'top-rated elementary')} just minutes away.

📍 PRIME LOCATION:
Enjoy easy access to shopping, dining, parks, and major highways. Perfect for commuters and families alike.

📈 SMART INVESTMENT:
Priced at {price_str} in one of the area's most desirable neighborhoods. Don't miss this opportunity!

Schedule your private showing today!""",
                
                f"""PRICE: {price_str} | MLS#: {mls_data.get('mls_id', 'N/A')}

Gorgeous {beds}BR/{baths}BA home in sought-after neighborhood! This meticulously maintained property features:

✨ RECENT UPDATES:
{chr(10).join(f'• {feature}' for feature in mls_data.get('features', ['Updated throughout']))}

🏫 EDUCATION:
{mls_data.get('school_district', 'A+ Rated District')} - Consistently high test scores and excellent extracurricular programs.

🌳 OUTDOOR LIVING:
{mls_data.get('lot_size', 'Generous')} lot with mature trees and plenty of space for play or relaxation.

💡 WHY THIS HOME?
- Turn-key condition
- Great curb appeal
- Neutral decor throughout
- Ample storage space
- Desirable floor plan

Perfect for growing families or professionals seeking a peaceful retreat with urban convenience!"""
            ],
            'luxury': [
                f"""EXQUISITE {beds} BEDROOM ESTATE | {address}

Priced at {price_str}, this magnificent property redefines luxury living. Spanning {sqft} square feet of exquisite craftsmanship and designer finishes.

🌟 LUXURY FEATURES:
• Chef's kitchen with premium Thermador appliances
• Home theater with surround sound
• Wine cellar and tasting room
• Resort-style pool and spa
• Smart home automation throughout
• Four-car garage with EV charging

🏙️ PRESTIGIOUS LOCATION:
Situated in the most exclusive enclave of {address.split(',')[-2] if ',' in address else 'the city'}, offering privacy and panoramic views.

🎯 INVESTMENT OPPORTUNITY:
A rare offering in today's market. Significant appreciation potential with premier amenities and location.

Contact for private luxury showing."""
            ]
        }
        
        # Choose template
        if 'estate' in property_type or price > 1000000:
            template_type = 'luxury'
        else:
            template_type = 'family'
        
        description = random.choice(templates[template_type])
        
        # Add location insights if available
        if 'location_insights' in mls_data:
            loc = mls_data['location_insights']
            description += f"\n\n📍 NEIGHBORHOOD: {loc.get('neighborhood', 'Desirable area')} - {loc.get('market_trends', 'Growing community')}"
        
        return {
            'listing_description': description,
            'email_blast': ContentGenerator.generate_email_blast(mls_data, description),
            'meta_description': f"{beds} bedroom, {baths} bath home in {address}. {price_str}. MLS#{mls_data.get('mls_id', '')}"
        }
    
    @staticmethod
    def generate_email_blast(mls_data, listing_description):
        """Create email marketing content"""
        address = mls_data.get('address', 'New Listing')
        price = mls_data.get('price', 0)
        price_str = f"${price:,}" if isinstance(price, (int, float)) else price
        
        return f"""Subject: New Listing Alert: {address} - {price_str}

Hi [Client Name],

I'm excited to share a new listing that just hit the market!

🏡 {address}
💰 {price_str}

{listing_description[:300]}...

📊 PROPERTY DETAILS:
• Beds: {mls_data.get('beds', 'N/A')}
• Baths: {mls_data.get('baths', 'N/A')}
• SQFT: {mls_data.get('sqft', 'N/A')}
• Lot: {mls_data.get('lot_size', 'N/A')}
• Year: {mls_data.get('year_built', 'N/A')}

🎯 WHY THIS PROPERTY?
{chr(10).join(f'• {benefit}' for benefit in [
    "Excellent price per square foot",
    "Superior location with great schools",
    "Move-in ready condition",
    "Strong investment potential"
])}

📅 AVAILABLE FOR SHOWINGS:
This property is already generating interest. Contact me to schedule a private tour before it's gone!

Best regards,
[Your Name]
[Your Contact Information]"""
    
    @staticmethod
    def generate_social_posts(mls_data):
        """Create social media posts"""
        address = mls_data.get('address', 'Beautiful Home')
        price = mls_data.get('price', 0)
        price_str = f"${price:,}" if isinstance(price, (int, float)) else price
        beds = mls_data.get('beds', 3)
        baths = mls_data.get('baths', 2)
        
        posts = {
            'facebook': f"""🏡 NEW LISTING ALERT! 🏡

{address}
{price_str} | {beds}BR/{baths}BA

✨ Features:
• Updated throughout
• Great neighborhood
• Excellent schools
• Move-in ready!

Ready to make this your new home? Message me for a private showing!

#NewListing #RealEstate #HomeForSale #HouseHunting #DreamHome""",
            
            'instagram': f"""✨ JUST LISTED ✨

📍 {address}
💰 {price_str}
🛏️ {beds} beds
🛁 {baths} baths

This stunning home checks all the boxes! 
✓ Updated kitchen
✓ Spacious living areas
✓ Beautiful backyard
✓ Prime location

DM me for more details or to schedule a tour!

#JustListed #RealEstate #HomeTour #PropertyListing #DreamHome""",
            
            'linkedin': f"""🏠 Professional Real Estate Update:

New listing available for clients and investors:

{address}
Price: {price_str}
Size: {mls_data.get('sqft', 'N/A')} sqft

This property represents an excellent opportunity in the {mls_data.get('school_district', 'local')} school district. Strong fundamentals with growth potential.

Perfect for:
• Growing families
• First-time homebuyers
• Investors

Connect with me for professional real estate services.

#RealEstate #PropertyInvestment #HomeBuying #ProfessionalServices #MarketUpdate""",
            
            'twitter': f"""🏡 New Listing: {address}

💰 {price_str}
🛏️ {beds}BR/{baths}BA
📐 {mls_data.get('sqft', 'N/A')} sqft

Excellent schools ✓
Great location ✓
Move-in ready ✓

Details & photos: [Link to listing]

#RealEstate #NewListing #HomeForSale #Property"""
        }
        
        return {
            'social_posts': "\n\n---\n\n".join(
                f"**{platform.upper()}:**\n\n{content}"
                for platform, content in posts.items()
            ),
            'hashtags': "#RealEstate #HomeForSale #NewListing #Property #DreamHome #HouseHunting"
        }
