#!/usr/bin/env python3
"""
Generate visual charts and graphics for property ratings
Uses free chart generation methods
"""
import json
import math
from datetime import datetime
import base64
from io import BytesIO

class AnalyticsGenerator:
    """Generate visual analytics for property data"""
    
    def generate_all_charts(self, property_data):
        """Generate all visual charts for the property"""
        charts = {}
        
        # 1. Ratings radar chart
        charts['ratings_radar'] = self.generate_radar_chart(
            property_data.get('ratings', {})
        )
        
        # 2. Valuation comparison chart
        charts['valuation_chart'] = self.generate_valuation_chart(
            property_data.get('valuation', {})
        )
        
        # 3. Price per sqft comparison
        charts['price_comparison'] = self.generate_price_comparison(
            property_data.get('valuation', {}).get('comparable_sales', []),
            property_data.get('price', 0),
            property_data.get('sqft', 0)
        )
        
        # 4. Market trend indicator
        charts['market_trend'] = self.generate_market_trend(
            property_data.get('valuation', {}).get('price_trend', 'Stable')
        )
        
        # 5. Investment potential gauge
        charts['investment_gauge'] = self.generate_investment_gauge(
            property_data.get('ratings', {}).get('investment_potential', {}).get('score', 75)
        )
        
        return charts
    
    def generate_radar_chart(self, ratings):
        """Generate radar chart SVG for ratings"""
        if not ratings:
            return self.default_radar_chart()
        
        categories = ['Schools', 'Safety', 'Transport', 'Amenities', 'Investment', 'Environment']
        scores = []
        
        # Map ratings to categories
        rating_map = {
            'school_quality': 0,
            'safety': 1,
            'transportation': 2,
            'amenities': 3,
            'investment_potential': 4,
            'environment': 5
        }
        
        for key, idx in rating_map.items():
            if key in ratings:
                scores.append(ratings[key].get('score', 75))
            else:
                scores.append(75)
        
        # Generate SVG radar chart
        svg_width = 400
        svg_height = 300
        center_x = svg_width // 2
        center_y = svg_height // 2
        radius = min(center_x, center_y) - 40
        
        # Create SVG
        svg = f'''<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">
            <style>
                .grid-line {{ stroke: #e2e8f0; stroke-width: 1; fill: none; }}
                .axis-line {{ stroke: #cbd5e0; stroke-width: 1; }}
                .data-line {{ stroke: #4299e1; stroke-width: 2; fill: rgba(66, 153, 225, 0.2); }}
                .data-point {{ fill: #4299e1; }}
                .category-label {{ font-size: 12px; fill: #4a5568; font-family: sans-serif; }}
                .score-label {{ font-size: 10px; fill: #718096; font-family: sans-serif; }}
            </style>
            
            <!-- Background circles -->
            <circle cx="{center_x}" cy="{center_y}" r="{radius}" fill="none" stroke="#f7fafc" stroke-width="2"/>
            <circle cx="{center_x}" cy="{center_y}" r="{radius*0.75}" fill="none" stroke="#f7fafc" stroke-width="1"/>
            <circle cx="{center_x}" cy="{center_y}" r="{radius*0.5}" fill="none" stroke="#f7fafc" stroke-width="1"/>
            <circle cx="{center_x}" cy="{center_y}" r="{radius*0.25}" fill="none" stroke="#f7fafc" stroke-width="1"/>
            
            <!-- Axes -->
            <line x1="{center_x}" y1="{center_y - radius}" x2="{center_x}" y2="{center_y + radius}" class="axis-line"/>
            <line x1="{center_x - radius}" y1="{center_y}" x2="{center_x + radius}" y2="{center_y}" class="axis-line"/>
        '''
        
        # Add category axes and labels
        for i, category in enumerate(categories):
            angle = (2 * math.pi * i / len(categories)) - math.pi / 2
            end_x = center_x + radius * math.cos(angle)
            end_y = center_y + radius * math.sin(angle)
            
            # Axis line
            svg += f'<line x1="{center_x}" y1="{center_y}" x2="{end_x}" y2="{end_y}" class="axis-line"/>'
            
            # Category label (outside the chart)
            label_x = center_x + (radius + 20) * math.cos(angle)
            label_y = center_y + (radius + 20) * math.sin(angle)
            text_anchor = "middle"
            if abs(math.cos(angle)) > 0.7:
                if math.cos(angle) > 0:
                    text_anchor = "start"
                else:
                    text_anchor = "end"
            
            svg += f'<text x="{label_x}" y="{label_y}" text-anchor="{text_anchor}" class="category-label">{category}</text>'
        
        # Add data polygon
        points = []
        for i, score in enumerate(scores):
            angle = (2 * math.pi * i / len(scores)) - math.pi / 2
            score_radius = radius * (score / 100)
            point_x = center_x + score_radius * math.cos(angle)
            point_y = center_y + score_radius * math.sin(angle)
            points.append(f"{point_x},{point_y}")
            
            # Data point
            svg += f'<circle cx="{point_x}" cy="{point_y}" r="4" class="data-point"/>'
            
            # Score label
            label_x = center_x + (score_radius + 15) * math.cos(angle)
            label_y = center_y + (score_radius + 15) * math.sin(angle)
            svg += f'<text x="{label_x}" y="{label_y}" text-anchor="middle" class="score-label">{score}</text>'
        
        # Connect points
        svg += f'<polygon points="{" ".join(points)}" class="data-line"/>'
        
        svg += '</svg>'
        return svg
    
    def generate_valuation_chart(self, valuation_data):
        """Generate bar chart for valuation comparison"""
        comparable_sales = valuation_data.get('comparable_sales', [])
        
        if not comparable_sales:
            return self.default_bar_chart()
        
        svg_width = 500
        svg_height = 300
        bar_width = 40
        padding = 60
        max_price = max([sale['price'] for sale in comparable_sales] + [valuation_data.get('listing_price', 0)])
        
        svg = f'''<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">
            <style>
                .bar {{ fill: #4299e1; }}
                .current-bar {{ fill: #48bb78; }}
                .axis {{ stroke: #cbd5e0; stroke-width: 1; }}
                .label {{ font-size: 12px; fill: #4a5568; font-family: sans-serif; }}
                .price-label {{ font-size: 10px; fill: #718096; font-family: sans-serif; }}
                .grid-line {{ stroke: #e2e8f0; stroke-width: 0.5; stroke-dasharray: 2,2; }}
            </style>
            
            <!-- Grid lines -->
            <line x1="{padding}" y1="50" x2="{svg_width - padding}" y2="50" class="grid-line"/>
            <line x1="{padding}" y1="100" x2="{svg_width - padding}" y2="100" class="grid-line"/>
            <line x1="{padding}" y1="150" x2="{svg_width - padding}" y2="150" class="grid-line"/>
            <line x1="{padding}" y1="200" x2="{svg_width - padding}" y2="200" class="grid-line"/>
            
            <!-- Axis -->
            <line x1="{padding}" y1="50" x2="{padding}" y2="{svg_height - 50}" class="axis"/>
            <line x1="{padding}" y1="{svg_height - 50}" x2="{svg_width - padding}" y2="{svg_height - 50}" class="axis"/>
        '''
        
        # Y-axis labels
        for i, value in enumerate([0.25, 0.5, 0.75, 1.0]):
            y = svg_height - 50 - 150 * value
            price = f"${int(max_price * value):,}"
            svg += f'<text x="{padding - 10}" y="{y + 3}" text-anchor="end" class="price-label">{price}</text>'
        
        chart_width = svg_width - 2 * padding
        available_width = chart_width - (len(comparable_sales) + 1) * bar_width
        spacing = available_width / (len(comparable_sales) + 2)
        
        # Current listing bar
        current_price = valuation_data.get('listing_price', 0)
        current_height = (current_price / max_price) * 150
        x = padding + spacing
        y = svg_height - 50 - current_height
        
        svg += f'''
            <rect x="{x}" y="{y}" width="{bar_width}" height="{current_height}" class="current-bar"/>
            <text x="{x + bar_width/2}" y="{y - 5}" text-anchor="middle" class="price-label">Current (${current_price:,})</text>
            <text x="{x + bar_width/2}" y="{svg_height - 35}" text-anchor="middle" class="label">Listing</text>
        '''
        
        # Comparable sales bars
        for i, sale in enumerate(comparable_sales):
            x = padding + (i + 2) * spacing + (i + 1) * bar_width
            height = (sale['price'] / max_price) * 150
            y = svg_height - 50 - height
            
            svg += f'''
                <rect x="{x}" y="{y}" width="{bar_width}" height="{height}" class="bar"/>
                <text x="{x + bar_width/2}" y="{y - 5}" text-anchor="middle" class="price-label">${sale["price"]:,}</text>
                <text x="{x + bar_width/2}" y="{svg_height - 35}" text-anchor="middle" class="label">Comp {i+1}</text>
            '''
        
        svg += '</svg>'
        return svg
    
    def generate_price_comparison(self, comparables, current_price, current_sqft):
        """Generate price per sqft comparison chart"""
        if not comparables or current_sqft == 0:
            return self.default_comparison_chart()
        
        # Calculate price per sqft
        current_pps = current_price / current_sqft
        comp_pps = [c['price_per_sqft'] for c in comparables]
        avg_pps = sum(comp_pps) / len(comp_pps)
        
        svg = f'''<svg width="400" height="200" xmlns="http://www.w3.org/2000/svg">
            <style>
                .bar {{ fill: #4299e1; }}
                .current-bar {{ fill: #48bb78; }}
                .avg-line {{ stroke: #ed8936; stroke-width: 2; stroke-dasharray: 5,5; }}
                .label {{ font-size: 12px; fill: #4a5568; font-family: sans-serif; }}
                .value {{ font-size: 11px; fill: #718096; font-family: sans-serif; }}
            </style>
            
            <text x="10" y="20" class="label">Price per Sq Ft Comparison</text>
            
            <!-- Current property -->
            <rect x="50" y="40" width="60" height="30" class="current-bar"/>
            <text x="80" y="30" text-anchor="middle" class="value">${current_pps:.0f}</text>
            <text x="80" y="85" text-anchor="middle" class="label">Current</text>
            
            <!-- Average line -->
            <line x1="0" y1="{100 - avg_pps/2}" x2="400" y2="{100 - avg_pps/2}" class="avg-line"/>
            <text x="380" y="{95 - avg_pps/2}" text-anchor="end" class="value">Avg: ${avg_pps:.0f}</text>
        '''
        
        # Comparable bars
        for i, pps in enumerate(comp_pps):
            x = 150 + i * 70
            height = pps / 2
            y = 100 - height
            
            svg += f'''
                <rect x="{x}" y="{y}" width="40" height="{height}" class="bar"/>
                <text x="{x + 20}" y="{y - 5}" text-anchor="middle" class="value">${pps:.0f}</text>
                <text x="{x + 20}" y="85" text-anchor="middle" class="label">Comp {i+1}</text>
            '''
        
        svg += '</svg>'
        return svg
    
    def generate_market_trend(self, trend):
        """Generate market trend indicator"""
        trend_colors = {
            'Rising': '#48bb78',
            'Stable': '#fbbf24', 
            'Declining': '#f56565',
            'Volatile': '#9f7aea'
        }
        
        color = trend_colors.get(trend, '#a0aec0')
        
        return f'''<svg width="150" height="80" xmlns="http://www.w3.org/2000/svg">
            <style>
                .trend-icon {{ fill: {color}; }}
                .trend-text {{ font-size: 14px; fill: #4a5568; font-family: sans-serif; font-weight: bold; }}
                .trend-label {{ font-size: 11px; fill: #718096; font-family: sans-serif; }}
            </style>
            
            <rect x="10" y="30" width="130" height="40" rx="8" fill="#f7fafc" stroke="#e2e8f0" stroke-width="1"/>
            
            <text x="75" y="25" text-anchor="middle" class="trend-label">Market Trend</text>
            <text x="75" y="55" text-anchor="middle" class="trend-text">{trend}</text>
            
            <!-- Trend icon -->
            <path class="trend-icon" d="{
                'M60,65 L75,50 L90,65' if trend == 'Rising' else
                'M60,60 L75,60 L90,60' if trend == 'Stable' else
                'M60,50 L75,65 L90,50' if trend == 'Declining' else
                'M60,55 L68,65 L75,45 L82,65 L90,55'
            }" stroke="{color}" stroke-width="3" fill="none"/>
        </svg>'''
    
    def generate_investment_gauge(self, score):
        """Generate investment potential gauge"""
        color = self.score_to_color(score)
        label = self.score_to_label(score)
        
        # Draw gauge
        svg = f'''<svg width="200" height="120" xmlns="http://www.w3.org/2000/svg">
            <style>
                .gauge-back {{ fill: #e2e8f0; }}
                .gauge-fill {{ fill: {color}; }}
                .gauge-text {{ font-size: 24px; fill: #2d3748; font-family: sans-serif; font-weight: bold; }}
                .gauge-label {{ font-size: 12px; fill: #718096; font-family: sans-serif; }}
            </style>
            
            <!-- Gauge background -->
            <path d="M20,100 A80,80 0 0,1 180,100" fill="none" stroke="#e2e8f0" stroke-width="20"/>
            
            <!-- Gauge fill based on score -->
            <path d="M20,100 A80,80 0 0,1 180,100" fill="none" stroke="{color}" stroke-width="20" 
                  stroke-dasharray="{score * 2.51}, 251" stroke-linecap="round"/>
            
            <!-- Score text -->
            <text x="100" y="85" text-anchor="middle" class="gauge-text">{score}</text>
            <text x="100" y="105" text-anchor="middle" class="gauge-label">{label}</text>
            
            <!-- Labels -->
            <text x="30" y="115" text-anchor="middle" class="gauge-label" font-size="10">0</text>
            <text x="170" y="115" text-anchor="middle" class="gauge-label" font-size="10">100</text>
        </svg>'''
        
        return svg
    
    def score_to_color(self, score):
        """Convert score to color (same as scraper)"""
        if score >= 90: return '#10B981'
        elif score >= 80: return '#34D399'
        elif score >= 70: return '#FBBF24'
        elif score >= 60: return '#F59E0B'
        else: return '#EF4444'
    
    def score_to_label(self, score):
        """Convert score to label"""
        if score >= 90: return 'Excellent'
        elif score >= 80: return 'Very Good'
        elif score >= 70: return 'Good'
        elif score >= 60: return 'Fair'
        else: return 'Needs Attention'
    
    def default_radar_chart(self):
        """Default radar chart when no data"""
        return '''<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="300" fill="#f7fafc" rx="8"/>
            <text x="200" y="150" text-anchor="middle" fill="#a0aec0" font-family="sans-serif">
                Rating data not available
            </text>
        </svg>'''
    
    def default_bar_chart(self):
        """Default bar chart"""
        return '''<svg width="500" height="300" xmlns="http://www.w3.org/2000/svg">
            <rect width="500" height="300" fill="#f7fafc" rx="8"/>
            <text x="250" y="150" text-anchor="middle" fill="#a0aec0" font-family="sans-serif">
                Comparable sales data not available
            </text>
        </svg>'''
    
    def default_comparison_chart(self):
        """Default comparison chart"""
        return '''<svg width="400" height="200" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="200" fill="#f7fafc" rx="8"/>
            <text x="200" y="100" text-anchor="middle" fill="#a0aec0" font-family="sans-serif">
                Price comparison data not available
            </text>
        </svg>'''

def main():
    """Test chart generation"""
    generator = AnalyticsGenerator()
    
    # Test data
    test_data = {
        'ratings': {
            'school_quality': {'score': 85},
            'safety': {'score': 92},
            'transportation': {'score': 78},
            'amenities': {'score': 88},
            'investment_potential': {'score': 82},
            'environment': {'score': 90}
        },
        'valuation': {
            'listing_price': 450000,
            'comparable_sales': [
                {'price': 425000, 'price_per_sqft': 225},
                {'price': 460000, 'price_per_sqft': 240},
                {'price': 440000, 'price_per_sqft': 230}
            ],
            'price_trend': 'Rising'
        }
    }
    
    charts = generator.generate_all_charts(test_data)
    
    # Save charts to files
    for name, chart in charts.items():
        with open(f'{name}.svg', 'w') as f:
            f.write(chart)
        print(f"✓ Generated {name}.svg")
    
    print("\nAll charts generated successfully!")

if __name__ == "__main__":
    main()
