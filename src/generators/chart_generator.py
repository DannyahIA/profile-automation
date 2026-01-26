"""
Chart Generator

This module generates SVG charts and visualizations for the README.

Why SVG?
- Native GitHub support (renders inline)
- Scalable and crisp on any resolution
- No external dependencies needed
- Lightweight and fast to load
"""

import os
from datetime import datetime, timezone
from typing import Dict, Any, List, Tuple
from pathlib import Path


class ChartGenerator:
    """
    Generates SVG charts and visualizations.
    """
    
    # Color schemes
    COLORS = {
        'primary': '#EB6F92',      # Rose Pine
        'secondary': '#9CCFD8',    # Foam
        'tertiary': '#F6C177',     # Gold
        'success': '#31748F',      # Pine
        'background': '#191724',   # Base
        'surface': '#1F1D2E',      # Surface
        'text': '#E0DEF4',         # Text
        'muted': '#6E6A86',        # Muted
    }
    
    # Tier colors
    TIER_COLORS = {
        'S+': '#FFD700',  # Gold
        'S':  '#C0C0C0',  # Silver
        'A':  '#CD7F32',  # Bronze
        'B':  '#4A90E2',  # Blue
        'C':  '#50C878',  # Emerald
        'D':  '#FFA500',  # Orange
        'F':  '#808080',  # Gray
    }
    
    def __init__(self, metrics: Dict[str, Any], rankings: Dict[str, Any], 
                 output_dir: str = 'assets'):
        """
        Initialize with metrics and output directory.
        
        Args:
            metrics: Processed metrics dictionary
            rankings: Rankings dictionary
            output_dir: Directory to save generated charts
        """
        self.metrics = metrics
        self.rankings = rankings
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_language_chart(self, width: int = 800, height: int = 400) -> str:
        """
        Generate a horizontal bar chart for language distribution.
        
        Why horizontal bars?
        - Better for longer language names
        - Easier to read percentages
        - More compact layout
        
        Returns:
            Path to generated SVG file
        """
        languages = self.metrics.get('top_languages', {})
        if not languages:
            return None
        
        # Calculate percentages
        total = sum(languages.values())
        lang_data = [
            (lang, count, (count / total) * 100)
            for lang, count in list(languages.items())[:8]  # Top 8
        ]
        
        # SVG setup
        bar_height = 35
        bar_spacing = 15
        margin = {'top': 60, 'right': 120, 'bottom': 40, 'left': 200}
        chart_height = len(lang_data) * (bar_height + bar_spacing) + margin['top'] + margin['bottom']
        
        svg = [
            f'<svg width="{width}" height="{chart_height}" xmlns="http://www.w3.org/2000/svg">',
            f'<rect width="{width}" height="{chart_height}" fill="{self.COLORS["background"]}"/>',
            
            # Title
            f'<text x="{width/2}" y="35" font-family="Arial, sans-serif" font-size="24" '
            f'font-weight="bold" fill="{self.COLORS["text"]}" text-anchor="middle">',
            '💻 Language Distribution',
            '</text>',
        ]
        
        # Draw bars
        max_bar_width = width - margin['left'] - margin['right']
        
        for i, (lang, count, percentage) in enumerate(lang_data):
            y = margin['top'] + i * (bar_height + bar_spacing)
            bar_width = (percentage / 100) * max_bar_width
            
            # Color gradient based on position
            color = self._get_gradient_color(i, len(lang_data))
            
            # Language label
            svg.append(
                f'<text x="{margin["left"] - 10}" y="{y + bar_height/2 + 5}" '
                f'font-family="monospace" font-size="14" fill="{self.COLORS["text"]}" '
                f'text-anchor="end">{lang}</text>'
            )
            
            # Bar background
            svg.append(
                f'<rect x="{margin["left"]}" y="{y}" width="{max_bar_width}" '
                f'height="{bar_height}" fill="{self.COLORS["surface"]}" rx="5"/>'
            )
            
            # Animated bar
            svg.append(
                f'<rect x="{margin["left"]}" y="{y}" width="0" height="{bar_height}" '
                f'fill="{color}" rx="5">'
                f'<animate attributeName="width" from="0" to="{bar_width}" '
                f'dur="1s" fill="freeze"/>'
                f'</rect>'
            )
            
            # Percentage text
            svg.append(
                f'<text x="{margin["left"] + bar_width + 10}" y="{y + bar_height/2 + 5}" '
                f'font-family="monospace" font-size="14" font-weight="bold" '
                f'fill="{self.COLORS["text"]}">{percentage:.1f}%</text>'
            )
        
        svg.append('</svg>')
        
        # Save file
        output_path = self.output_dir / 'language_chart.svg'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(svg))
        
        return str(output_path)
    
    def generate_activity_timeline(self, width: int = 800, height: int = 200) -> str:
        """
        Generate an activity timeline showing commit/PR/issue trends.
        
        Why timeline?
        - Shows activity patterns over time
        - Identifies busy periods
        - Visual trend analysis
        
        Returns:
            Path to generated SVG file
        """
        # For now, create a simple streak visualization
        streak = self.metrics.get('activity_streak', {})
        current = streak.get('current', 0)
        longest = streak.get('longest', 0)
        
        svg = [
            f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
            f'<rect width="{width}" height="{height}" fill="{self.COLORS["background"]}"/>',
            
            # Title
            f'<text x="{width/2}" y="35" font-family="Arial, sans-serif" font-size="24" '
            f'font-weight="bold" fill="{self.COLORS["text"]}" text-anchor="middle">',
            '🔥 Contribution Streak',
            '</text>',
            
            # Current streak (left side)
            f'<g transform="translate(150, 100)">',
            f'<circle cx="0" cy="0" r="50" fill="{self.COLORS["primary"]}" opacity="0.2"/>',
            f'<circle cx="0" cy="0" r="45" fill="{self.COLORS["primary"]}"/>',
            f'<text x="0" y="10" font-family="Arial, sans-serif" font-size="36" '
            f'font-weight="bold" fill="white" text-anchor="middle">{current}</text>',
            f'<text x="0" y="60" font-family="Arial, sans-serif" font-size="12" '
            f'fill="{self.COLORS["text"]}" text-anchor="middle">Current Streak</text>',
            f'</g>',
            
            # Longest streak (right side)
            f'<g transform="translate(650, 100)">',
            f'<circle cx="0" cy="0" r="50" fill="{self.COLORS["secondary"]}" opacity="0.2"/>',
            f'<circle cx="0" cy="0" r="45" fill="{self.COLORS["secondary"]}"/>',
            f'<text x="0" y="10" font-family="Arial, sans-serif" font-size="36" '
            f'font-weight="bold" fill="white" text-anchor="middle">{longest}</text>',
            f'<text x="0" y="60" font-family="Arial, sans-serif" font-size="12" '
            f'fill="{self.COLORS["text"]}" text-anchor="middle">Longest Streak</text>',
            f'</g>',
            
            # Connecting line
            f'<line x1="200" y1="100" x2="600" y2="100" '
            f'stroke="{self.COLORS["muted"]}" stroke-width="2" stroke-dasharray="5,5"/>',
            
            '</svg>'
        ]
        
        output_path = self.output_dir / 'activity_timeline.svg'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(svg))
        
        return str(output_path)
    
    def generate_tier_distribution(self, width: int = 600, height: int = 400) -> str:
        """
        Generate a pie chart showing tier distribution of projects.
        
        Why pie chart?
        - Shows proportion of projects in each tier
        - Quick visual understanding
        - Colorful and engaging
        
        Returns:
            Path to generated SVG file
        """
        # Count projects per tier
        tier_counts = {'S+': 0, 'S': 0, 'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        
        for project in self.rankings.get('top_projects', []):
            score = project['score']
            tier = self._calculate_tier(score)
            tier_counts[tier] += 1
        
        # Filter out empty tiers
        tier_data = [(tier, count) for tier, count in tier_counts.items() if count > 0]
        
        if not tier_data:
            return None
        
        total = sum(count for _, count in tier_data)
        
        # SVG setup
        center_x, center_y = width / 2, height / 2
        radius = min(width, height) / 3
        
        svg = [
            f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
            f'<rect width="{width}" height="{height}" fill="{self.COLORS["background"]}"/>',
            
            # Title
            f'<text x="{width/2}" y="30" font-family="Arial, sans-serif" font-size="20" '
            f'font-weight="bold" fill="{self.COLORS["text"]}" text-anchor="middle">',
            '🏆 Project Tier Distribution',
            '</text>',
        ]
        
        # Draw pie slices
        start_angle = -90  # Start at top
        
        for tier, count in tier_data:
            angle = (count / total) * 360
            end_angle = start_angle + angle
            
            # Calculate slice path
            path = self._create_pie_slice(center_x, center_y, radius, start_angle, end_angle)
            color = self.TIER_COLORS[tier]
            
            svg.append(
                f'<path d="{path}" fill="{color}" stroke="{self.COLORS["background"]}" stroke-width="2"/>'
            )
            
            # Add label in the middle of the slice
            mid_angle = start_angle + angle / 2
            label_radius = radius * 0.7
            label_x = center_x + label_radius * self._cos(mid_angle)
            label_y = center_y + label_radius * self._sin(mid_angle)
            
            svg.append(
                f'<text x="{label_x}" y="{label_y}" font-family="monospace" font-size="16" '
                f'font-weight="bold" fill="white" text-anchor="middle">{tier}</text>'
            )
            svg.append(
                f'<text x="{label_x}" y="{label_y + 18}" font-family="monospace" font-size="12" '
                f'fill="white" text-anchor="middle">({count})</text>'
            )
            
            start_angle = end_angle
        
        svg.append('</svg>')
        
        output_path = self.output_dir / 'tier_distribution.svg'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(svg))
        
        return str(output_path)
    
    def generate_stats_card(self, width: int = 500, height: int = 200) -> str:
        """
        Generate a compact stats card with key metrics.
        
        Why stats card?
        - Quick overview at the top of README
        - Professional look
        - Easy to scan
        
        Returns:
            Path to generated SVG file
        """
        svg = [
            f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
            
            # Background with gradient
            '<defs>',
            '<linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">',
            f'<stop offset="0%" style="stop-color:{self.COLORS["primary"]};stop-opacity:0.8" />',
            f'<stop offset="100%" style="stop-color:{self.COLORS["secondary"]};stop-opacity:0.8" />',
            '</linearGradient>',
            '</defs>',
            
            f'<rect width="{width}" height="{height}" fill="url(#grad1)" rx="15"/>',
            
            # Title
            '<text x="250" y="35" font-family="Arial, sans-serif" font-size="20" '
            'font-weight="bold" fill="white" text-anchor="middle">',
            '📊 GitHub Activity Summary',
            '</text>',
            
            # Stats row
            f'<text x="70" y="90" font-family="monospace" font-size="32" '
            f'font-weight="bold" fill="white" text-anchor="middle">',
            f'{self.metrics.get("total_commits", 0)}',
            '</text>',
            f'<text x="70" y="115" font-family="Arial, sans-serif" font-size="12" '
            f'fill="white" text-anchor="middle">Commits</text>',
            
            f'<text x="180" y="90" font-family="monospace" font-size="32" '
            f'font-weight="bold" fill="white" text-anchor="middle">',
            f'{self.metrics.get("total_prs", 0)}',
            '</text>',
            f'<text x="180" y="115" font-family="Arial, sans-serif" font-size="12" '
            f'fill="white" text-anchor="middle">Pull Requests</text>',
            
            f'<text x="320" y="90" font-family="monospace" font-size="32" '
            f'font-weight="bold" fill="white" text-anchor="middle">',
            f'{self.metrics.get("total_issues", 0)}',
            '</text>',
            f'<text x="320" y="115" font-family="Arial, sans-serif" font-size="12" '
            f'fill="white" text-anchor="middle">Issues</text>',
            
            f'<text x="430" y="90" font-family="monospace" font-size="32" '
            f'font-weight="bold" fill="white" text-anchor="middle">',
            f'{self.metrics.get("total_repos", 0)}',
            '</text>',
            f'<text x="430" y="115" font-family="Arial, sans-serif" font-size="12" '
            f'fill="white" text-anchor="middle">Repositories</text>',
            
            # Footer
            f'<text x="250" y="165" font-family="Arial, sans-serif" font-size="10" '
            f'fill="white" text-anchor="middle" opacity="0.7">',
            f'Last 30 days • Updated {datetime.now(timezone.utc).strftime("%B %d, %Y")}',
            '</text>',
            
            '</svg>'
        ]
        
        output_path = self.output_dir / 'stats_card.svg'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(svg))
        
        return str(output_path)
    
    def generate_all_charts(self) -> Dict[str, str]:
        """
        Generate all charts and return their paths.
        
        Returns:
            Dictionary mapping chart names to file paths
        """
        charts = {}
        
        print("🎨 Generating visualizations...")
        
        chart = self.generate_stats_card()
        if chart:
            charts['stats_card'] = chart
            print(f"   ✅ Stats card generated")
        
        chart = self.generate_language_chart()
        if chart:
            charts['language_chart'] = chart
            print(f"   ✅ Language chart generated")
        
        chart = self.generate_activity_timeline()
        if chart:
            charts['activity_timeline'] = chart
            print(f"   ✅ Activity timeline generated")
        
        chart = self.generate_tier_distribution()
        if chart:
            charts['tier_distribution'] = chart
            print(f"   ✅ Tier distribution generated")
        
        return charts
    
    # Helper methods
    
    def _get_gradient_color(self, index: int, total: int) -> str:
        """Get color from gradient based on position."""
        colors = [
            self.COLORS['primary'],
            self.COLORS['secondary'],
            self.COLORS['tertiary'],
            self.COLORS['success'],
        ]
        return colors[index % len(colors)]
    
    def _calculate_tier(self, score: int) -> str:
        """Calculate tier from score."""
        if score >= 100: return 'S+'
        if score >= 50: return 'S'
        if score >= 30: return 'A'
        if score >= 20: return 'B'
        if score >= 10: return 'C'
        if score >= 5: return 'D'
        return 'F'
    
    def _create_pie_slice(self, cx: float, cy: float, r: float, 
                         start_angle: float, end_angle: float) -> str:
        """Create SVG path for pie slice."""
        import math
        
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)
        
        x1 = cx + r * math.cos(start_rad)
        y1 = cy + r * math.sin(start_rad)
        x2 = cx + r * math.cos(end_rad)
        y2 = cy + r * math.sin(end_rad)
        
        large_arc = 1 if end_angle - start_angle > 180 else 0
        
        return f"M {cx} {cy} L {x1} {y1} A {r} {r} 0 {large_arc} 1 {x2} {y2} Z"
    
    def _cos(self, angle: float) -> float:
        """Calculate cosine (angle in degrees)."""
        import math
        return math.cos(math.radians(angle))
    
    def _sin(self, angle: float) -> float:
        """Calculate sine (angle in degrees)."""
        import math
        return math.sin(math.radians(angle))
