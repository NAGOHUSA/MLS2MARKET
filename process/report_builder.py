#!/usr/bin/env python3
"""
Free Client Report Builder
Creates beautiful single-page reports from MLS data
"""
import json
import os
import argparse
from datetime import datetime
from jinja2 import Template

class ReportBuilder:
    """Build professional client reports - 100% free"""
    
    @staticmethod
    def load_template():
        """Load HTML report template"""
        # Simple inline template - no external files needed
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{property.address}} - Property Report</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 1000px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; padding: 30px 0; border-bottom: 3px solid #2c5282; margin-bottom: 30px; }
        .property-address { font-size: 2em; color: #2c5282; margin-bottom: 10px; }
        .price { font-size: 1.8em; color: #38a169; font-weight: bold; margin-bottom: 20px; }
        .section { margin: 30px 0; padding: 20px; border-radius: 10px; background: #f7fafc; }
        .section-title { color: #2d3748; border-left: 4px solid #4299e1; padding-left: 15px; margin-bottom: 20px; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
        .stat-card { background: white; padding: 20px; border-radius: 8px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .stat-value { font-size: 1.8em; font-weight: bold; color: #2c5282; }
        .stat-label { color: #718096; font-size: 0.9em; }
        .features-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px; }
        .feature-item { background: white; padding: 15px; border-radius: 6px; border-left: 3px solid #48bb78; }
        .schools { display: flex; gap: 20px; flex-wrap: wrap; }
        .school-card { flex: 1; min-width: 200px; background: white; padding: 20px; border-radius: 8px; }
        .grade { display: inline-block; background: #4299e1; color: white; padding: 3px 10px; border-radius: 20px; font-size: 0.9em; }
        .market-insights { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 10px; }
        .footer { text-align: center; margin-top: 40px; padding-top: 20px; border-top: 2px solid #e2e8f0; color: #718096; font-size: 0.9em; }
        .generated-by { color: #4299e1; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="property-address">{{property.address}}</h1>
            <div class="price">{% if property.price is number %}${"{:,}".format(property.price)}{% else %}{{property.price}}{% endif %}</div>
            <p>MLS# {{property.mls_id}} | Generated on {{report_date}}</p>
        </div>
        
        <!-- Property Stats -->
        <div class="section">
            <h2 class="section-title">Property Overview</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">{{property.beds}}</div>
                    <div class="stat-label">Bedrooms</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{{property.baths}}</div>
                    <div class="stat-label">Bathrooms</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{{property.sqft}} sqft</div>
                    <div class="stat-label">Living Area</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{{property.year_built}}</div>
                    <div class="stat-label">Year Built</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{{property.lot_size}}</div>
                    <div class="stat-label">Lot Size</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{{property.property_type}}</div>
                    <div class="stat-label">Property Type</div>
                </div>
            </div>
        </div>
        
        <!-- Key Features -->
        <div class="section">
            <h2 class="section-title">Property Features</h2>
            <div class="features-list">
                {% for feature in property.features %}
                <div class="feature-item">{{feature}}</div>
                {% endfor %}
            </div>
        </div>
        
        <!-- Schools -->
        <div class="section">
            <h2 class="section-title">School Information</h2>
            <p><strong>District:</strong> {{property.school_district}}</p>
            <div class="schools">
                {% if property.schools %}
                    {% for level, info in property.schools.items() %}
                    <div class="school-card">
                        <h3>{{level|title}} School</h3>
                        <p>{{info}}</p>
                        {% if '8/10' in info or '9/10' in info or '10/10' in info %}
                        <span class="grade">High-Rated</span>
                        {% endif %}
                    </div>
                    {% endfor %}
                {% endif %}
            </div>
        </div>
        
        <!-- Location Insights -->
        <div class="section">
            <h2 class="section-title">Neighborhood & Location</h2>
            {% if property.location_insights %}
            <div class="features-list">
                <div class="feature-item">
                    <strong>Neighborhood:</strong> {{property.location_insights.neighborhood}}
                </div>
                <div class="feature-item">
                    <strong>Walk Score:</strong> {{property.location_insights.walk_score}}/100
                </div>
                <div class="feature-item">
                    <strong>Commute:</strong> {{property.location_insights.commute}}
                </div>
            </div>
            <p style="margin-top: 15px;">{{property.location_insights.market_trends}}</p>
            {% endif %}
            
            {% if property.amenities %}
            <h3 style="margin-top: 20px;">Nearby Amenities</h3>
            <div class="features-list">
                {% for amenity in property.amenities %}
                <div class="feature-item">{{amenity}}</div>
                {% endfor %}
            </div>
            {% endif %}
        </div>
        
        <!-- Market Insights -->
        <div class="market-insights">
            <h2 class="section-title" style="color: white; border-left-color: white;">Market Insights</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
                <div>
                    <h3>Price Analysis</h3>
                    <p>• ${% if property.price is number %}{{"{:,}".format(property.price|int // property.sqft|int)}}{% endif %} per sqft</p>
                    <p>• Competitive for area</p>
                    <p>• Good value proposition</p>
                </div>
                <div>
                    <h3>Investment Potential</h3>
                    <p>• Growing neighborhood</p>
                    <p>• Strong rental demand</p>
                    <p>• Appreciation history</p>
                </div>
                <div>
                    <h3>Target Buyers</h3>
                    <p>• Growing families</p>
                    <p>• First-time homebuyers</p>
                    <p>• Professional couples</p>
                </div>
            </div>
        </div>
        
        <!-- Generated Content Preview -->
        <div class="section">
            <h2 class="section-title">Marketing Content Generated</h2>
            <p>Your listing description and social media posts have been created. Preview available in your dashboard.</p>
            <div style="background: white; padding: 15px; border-radius: 6px; border-left: 3px solid #ed8936; margin-top: 15px;">
                <strong>Listing Description Preview:</strong>
                <p style="margin-top: 10px; font-style: italic;">{{property.description|truncate(200)}}...</p>
            </div>
        </div>
        
        <div class="footer">
            <p>Report generated by <span class="generated-by">RealtorAI</span></p>
            <p>This report was created 100% free using public MLS data and AI technology.</p>
            <p>Questions? Contact your real estate professional.</p>
        </div>
    </div>
</body>
</html>"""
    
    @staticmethod
    def build_report(mls_data, output_path):
        """Generate complete client report"""
        template = Template(ReportBuilder.load_template())
        
        # Prepare data
        report_data = {
            'property': mls_data,
            'report_date': datetime.now().strftime("%B %d, %Y")
        }
        
        # Generate HTML
        html = template.render(**report_data)
        
        # Save file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✓ Report saved to {output_path}")
        return output_path

def main():
    """Build report from processed MLS data"""
    parser = argparse.ArgumentParser(description="Build Client Report")
    parser.add_argument("--input-dir", required=True, help="Directory with MLS JSON files")
    parser.add_argument("--output-dir", default="reports", help="Output directory")
    
    args = parser.parse_args()
    
    # Find latest MLS data file
    mls_files = [f for f in os.listdir(args.input_dir) if f.endswith('.json') and 'mls_data' in f]
    if not mls_files:
        print("No MLS data files found")
        return
    
    latest_file = sorted(mls_files)[-1]
    filepath = os.path.join(args.input_dir, latest_file)
    
    # Load MLS data
    with open(filepath, 'r') as f:
        mls_data = json.load(f)
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Generate report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(args.output_dir, f"client_report_{timestamp}.html")
    
    ReportBuilder.build_report(mls_data, output_path)
    
    # Also create a simple view page
    view_page = f"""<!DOCTYPE html>
<html>
<head>
    <title>Report Ready</title>
</head>
<body>
    <h1>Client Report Ready</h1>
    <p>Your property report has been generated.</p>
    <a href="client_report_{timestamp}.html" style="padding: 12px 24px; background: #4299e1; color: white; text-decoration: none; border-radius: 5px;">
        View Report
    </a>
    <p style="margin-top: 20px;">
        <small>This report was generated 100% free using public data.</small>
    </p>
</body>
</html>"""
    
    with open(os.path.join(args.output_dir, "index.html"), 'w') as f:
        f.write(view_page)
    
    print("✓ Report generation complete")

if __name__ == "__main__":
    main()
