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
    
    def generate_daily_comparison_chart(self) -> str:
        """
        Generate a daily comparison chart showing today vs previous days.
        
        Shows:
        - Commits comparison (today vs avg)
        - Bar chart with last 7 days
        - Percentage change indicators
        """
        daily_stats = self.metrics.get('daily_stats', {})
        commits_per_day = daily_stats.get('commits_per_day', [])
        
        if not commits_per_day:
            return None
        
        # Get today's data and calculate averages
        today_data = commits_per_day[-1] if commits_per_day else {'date': 'Today', 'count': 0}
        avg_commits = daily_stats.get('average_commits', 0)
        
        # Calculate percentage change
        if avg_commits > 0:
            change_pct = ((today_data['count'] - avg_commits) / avg_commits) * 100
        else:
            change_pct = 100 if today_data['count'] > 0 else 0
        
        # Get last 7 days for bar chart
        last_7_days = commits_per_day[-7:] if len(commits_per_day) >= 7 else commits_per_day
        max_commits = max([d['count'] for d in last_7_days]) if last_7_days else 1
        
        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="320" '
            f'viewBox="0 0 800 320">',
            
            # Background
            f'<rect width="800" height="320" fill="{self.COLORS["background"]}" rx="10"/>',
            
            # Title
            f'<text x="400" y="30" font-family="Arial, sans-serif" font-size="18" '
            f'font-weight="bold" fill="white" text-anchor="middle">',
            '📊 Daily Activity Comparison',
            '</text>',
            
            # Today's stats box
            f'<rect x="50" y="50" width="200" height="100" fill="{self.COLORS["surface"]}" '
            f'rx="8" stroke="{self.COLORS["primary"]}" stroke-width="2"/>',
            
            f'<text x="150" y="75" font-family="Arial, sans-serif" font-size="14" '
            f'fill="{self.COLORS["muted"]}" text-anchor="middle">Today</text>',
            
            f'<text x="150" y="110" font-family="Arial, sans-serif" font-size="32" '
            f'font-weight="bold" fill="white" text-anchor="middle">{today_data["count"]}</text>',
            
            f'<text x="150" y="135" font-family="Arial, sans-serif" font-size="12" '
            f'fill="{self.COLORS["muted"]}" text-anchor="middle">commits</text>',
            
            # Average stats box
            f'<rect x="280" y="50" width="200" height="100" fill="{self.COLORS["surface"]}" rx="8"/>',
            
            f'<text x="380" y="75" font-family="Arial, sans-serif" font-size="14" '
            f'fill="{self.COLORS["muted"]}" text-anchor="middle">Average</text>',
            
            f'<text x="380" y="110" font-family="Arial, sans-serif" font-size="32" '
            f'font-weight="bold" fill="{self.COLORS["secondary"]}" text-anchor="middle">{avg_commits:.1f}</text>',
            
            f'<text x="380" y="135" font-family="Arial, sans-serif" font-size="12" '
            f'fill="{self.COLORS["muted"]}" text-anchor="middle">commits/day</text>',
            
            # Change indicator
            f'<rect x="510" y="50" width="240" height="100" fill="{self.COLORS["surface"]}" rx="8"/>',
        ]
        
        # Change arrow and percentage
        arrow = '↑' if change_pct >= 0 else '↓'
        change_color = self.COLORS['success'] if change_pct >= 0 else self.COLORS['primary']
        
        svg.extend([
            f'<text x="630" y="75" font-family="Arial, sans-serif" font-size="14" '
            f'fill="{self.COLORS["muted"]}" text-anchor="middle">Change</text>',
            
            f'<text x="630" y="110" font-family="Arial, sans-serif" font-size="32" '
            f'font-weight="bold" fill="{change_color}" text-anchor="middle">{arrow} {abs(change_pct):.0f}%</text>',
            
            f'<text x="630" y="135" font-family="Arial, sans-serif" font-size="12" '
            f'fill="{self.COLORS["muted"]}" text-anchor="middle">vs average</text>',
        ])
        
        # Bar chart for last 7 days
        svg.append(f'<text x="400" y="185" font-family="Arial, sans-serif" font-size="14" '
                   f'font-weight="bold" fill="white" text-anchor="middle">Last 7 Days</text>')
        
        bar_width = 80
        bar_spacing = 100
        bar_height_max = 90
        start_x = 60
        
        for i, day in enumerate(last_7_days):
            x = start_x + (i * bar_spacing)
            bar_height = (day['count'] / max_commits * bar_height_max) if max_commits > 0 else 0
            y = 280 - bar_height
            
            # Bar
            is_today = (i == len(last_7_days) - 1)
            bar_color = self.COLORS['primary'] if is_today else self.COLORS['secondary']
            
            svg.extend([
                f'<rect x="{x}" y="{y}" width="{bar_width}" height="{bar_height}" '
                f'fill="{bar_color}" rx="4" opacity="0.8">',
                f'<animate attributeName="height" from="0" to="{bar_height}" dur="0.5s" fill="freeze"/>',
                f'<animate attributeName="y" from="280" to="{y}" dur="0.5s" fill="freeze"/>',
                '</rect>',
                
                # Count on top
                f'<text x="{x + bar_width/2}" y="{y - 5}" font-family="Arial, sans-serif" '
                f'font-size="12" font-weight="bold" fill="white" text-anchor="middle">{day["count"]}</text>',
                
                # Date label
                f'<text x="{x + bar_width/2}" y="300" font-family="Arial, sans-serif" '
                f'font-size="10" fill="{self.COLORS["muted"]}" text-anchor="middle">{day["date"][-5:]}</text>',
            ])
        
        svg.append('</svg>')
        
        output_path = self.output_dir / 'daily_comparison.svg'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(svg))
        
        return str(output_path)
    
    def generate_language_pie_chart(self) -> str:
        """
        Generate a pie chart showing language distribution.
        """
        top_languages = self.metrics.get('top_languages', {})
        
        if not top_languages:
            return None
        
        # Sort and get top 5
        sorted_langs = sorted(top_languages.items(), key=lambda x: x[1], reverse=True)[:5]
        total = sum([count for _, count in sorted_langs])
        
        if total == 0:
            return None
        
        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" '
            f'viewBox="0 0 400 400">',
            
            # Background
            f'<rect width="400" height="400" fill="{self.COLORS["background"]}" rx="10"/>',
            
            # Title
            f'<text x="200" y="30" font-family="Arial, sans-serif" font-size="16" '
            f'font-weight="bold" fill="white" text-anchor="middle">',
            '🥧 Language Distribution',
            '</text>',
        ]
        
        # Draw pie chart
        cx, cy, r = 200, 220, 80
        start_angle = 0
        
        colors = [
            self.COLORS['primary'],
            self.COLORS['secondary'],
            self.COLORS['tertiary'],
            self.COLORS['success'],
            self.COLORS['muted'],
        ]
        
        for i, (lang, count) in enumerate(sorted_langs):
            percentage = (count / total) * 100
            angle = (count / total) * 360
            
            # Create pie slice
            path = self._create_pie_slice(cx, cy, r, start_angle, start_angle + angle)
            color = colors[i % len(colors)]
            
            svg.extend([
                f'<path d="{path}" fill="{color}" opacity="0.9" stroke="{self.COLORS["background"]}" stroke-width="2">',
                f'<animate attributeName="opacity" values="0;0.9" dur="0.5s" fill="freeze"/>',
                '</path>',
            ])
            
            # Add legend
            legend_y = 60 + (i * 25)
            svg.extend([
                f'<rect x="20" y="{legend_y}" width="15" height="15" fill="{color}" rx="2"/>',
                f'<text x="40" y="{legend_y + 12}" font-family="Arial, sans-serif" font-size="12" fill="white">',
                f'{lang}: {count} repos ({percentage:.1f}%)',
                '</text>',
            ])
            
            start_angle += angle
        
        svg.append('</svg>')
        
        output_path = self.output_dir / 'language_pie.svg'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(svg))
        
        return str(output_path)
    
    def generate_weekly_trend_chart(self) -> str:
        """
        Generate a line chart showing weekly trends (PRs and issues).
        """
        weekly_stats = self.metrics.get('weekly_stats', {})
        prs_per_week = weekly_stats.get('prs_per_week', [])
        issues_per_week = weekly_stats.get('issues_closed_per_week', [])
        
        if not prs_per_week and not issues_per_week:
            return None
        
        # Get last 8 weeks
        all_weeks = {}
        for pr in prs_per_week[-8:]:
            all_weeks[pr['week']] = {'prs': pr['count'], 'issues': 0}
        for issue in issues_per_week[-8:]:
            if issue['week'] in all_weeks:
                all_weeks[issue['week']]['issues'] = issue['count']
            else:
                all_weeks[issue['week']] = {'prs': 0, 'issues': issue['count']}
        
        weeks = sorted(all_weeks.keys())
        if not weeks:
            return None
        
        max_value = max([max(all_weeks[w]['prs'], all_weeks[w]['issues']) for w in weeks]) or 1
        
        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="700" height="300" '
            f'viewBox="0 0 700 300">',
            
            # Background
            f'<rect width="700" height="300" fill="{self.COLORS["background"]}" rx="10"/>',
            
            # Title
            f'<text x="350" y="30" font-family="Arial, sans-serif" font-size="16" '
            f'font-weight="bold" fill="white" text-anchor="middle">',
            '📈 Weekly Trends',
            '</text>',
            
            # Legend
            f'<circle cx="480" cy="22" r="5" fill="{self.COLORS["primary"]}"/>',
            f'<text x="490" y="27" font-family="Arial, sans-serif" font-size="12" fill="white">Pull Requests</text>',
            
            f'<circle cx="580" cy="22" r="5" fill="{self.COLORS["secondary"]}"/>',
            f'<text x="590" y="27" font-family="Arial, sans-serif" font-size="12" fill="white">Issues</text>',
        ]
        
        # Draw grid lines
        for i in range(5):
            y = 60 + (i * 45)
            svg.append(f'<line x1="60" y1="{y}" x2="640" y2="{y}" stroke="{self.COLORS["surface"]}" stroke-width="1"/>')
        
        # Calculate points for lines
        chart_width = 580
        chart_height = 180
        point_spacing = chart_width / (len(weeks) - 1) if len(weeks) > 1 else chart_width
        
        pr_points = []
        issue_points = []
        
        for i, week in enumerate(weeks):
            x = 60 + (i * point_spacing)
            pr_y = 240 - (all_weeks[week]['prs'] / max_value * chart_height)
            issue_y = 240 - (all_weeks[week]['issues'] / max_value * chart_height)
            
            pr_points.append(f"{x},{pr_y}")
            issue_points.append(f"{x},{issue_y}")
            
            # Week label
            svg.append(f'<text x="{x}" y="265" font-family="Arial, sans-serif" font-size="10" '
                      f'fill="{self.COLORS["muted"]}" text-anchor="middle">{week[-2:]}</text>')
        
        # Draw PR line
        if len(pr_points) > 1:
            svg.extend([
                f'<polyline points="{" ".join(pr_points)}" fill="none" '
                f'stroke="{self.COLORS["primary"]}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">',
                f'<animate attributeName="stroke-dasharray" from="0,1000" to="1000,0" dur="1s" fill="freeze"/>',
                '</polyline>',
            ])
            
            # Draw points
            for point in pr_points:
                x, y = point.split(',')
                svg.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{self.COLORS["primary"]}"/>')
        
        # Draw issues line
        if len(issue_points) > 1:
            svg.extend([
                f'<polyline points="{" ".join(issue_points)}" fill="none" '
                f'stroke="{self.COLORS["secondary"]}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">',
                f'<animate attributeName="stroke-dasharray" from="0,1000" to="1000,0" dur="1s" fill="freeze"/>',
                '</polyline>',
            ])
            
            # Draw points
            for point in issue_points:
                x, y = point.split(',')
                svg.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{self.COLORS["secondary"]}"/>')
        
        svg.append('</svg>')
        
        output_path = self.output_dir / 'weekly_trend.svg'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(svg))
        
        return str(output_path)
    
    def generate_streak_progress_chart(self) -> str:
        """
        Generate a visual chart showing activity streak progress.
        """
        streak = self.metrics.get('activity_streak', {})
        current = streak.get('current', 0)
        longest = streak.get('longest', 0)
        
        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" '
            f'viewBox="0 0 600 200">',
            
            # Background
            f'<rect width="600" height="200" fill="{self.COLORS["background"]}" rx="10"/>',
            
            # Title
            f'<text x="300" y="30" font-family="Arial, sans-serif" font-size="16" '
            f'font-weight="bold" fill="white" text-anchor="middle">',
            '🔥 Activity Streak',
            '</text>',
        ]
        
        # Current streak bar
        current_width = min((current / max(longest, 1)) * 450, 450)
        svg.extend([
            f'<text x="50" y="75" font-family="Arial, sans-serif" font-size="14" fill="{self.COLORS["muted"]}">',
            'Current:',
            '</text>',
            
            f'<rect x="120" y="60" width="450" height="30" fill="{self.COLORS["surface"]}" rx="15"/>',
            
            f'<rect x="120" y="60" width="{current_width}" height="30" fill="{self.COLORS["primary"]}" rx="15">',
            f'<animate attributeName="width" from="0" to="{current_width}" dur="1s" fill="freeze"/>',
            '</rect>',
            
            f'<text x="545" y="80" font-family="Arial, sans-serif" font-size="14" '
            f'font-weight="bold" fill="white" text-anchor="end">{current} days</text>',
        ])
        
        # Longest streak bar
        svg.extend([
            f'<text x="50" y="135" font-family="Arial, sans-serif" font-size="14" fill="{self.COLORS["muted"]}">',
            'Record:',
            '</text>',
            
            f'<rect x="120" y="120" width="450" height="30" fill="{self.COLORS["surface"]}" rx="15"/>',
            
            f'<rect x="120" y="120" width="450" height="30" fill="{self.COLORS["secondary"]}" rx="15">',
            f'<animate attributeName="width" from="0" to="450" dur="1s" fill="freeze"/>',
            '</rect>',
            
            f'<text x="545" y="140" font-family="Arial, sans-serif" font-size="14" '
            f'font-weight="bold" fill="white" text-anchor="end">{longest} days</text>',
        ])
        
        # Progress percentage
        progress = (current / max(longest, 1)) * 100 if longest > 0 else 100
        svg.append(f'<text x="300" y="180" font-family="Arial, sans-serif" font-size="12" '
                  f'fill="{self.COLORS["muted"]}" text-anchor="middle">{progress:.0f}% of record</text>')
        
        svg.append('</svg>')
        
        output_path = self.output_dir / 'streak_progress.svg'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(svg))
        
        return str(output_path)
    
    def generate_tier_evolution_chart(self) -> str:
        """
        Generate a chart showing tier distribution evolution.
        Shows how many projects are in each tier.
        """
        projects = self.rankings.get('by_activity', [])
        
        if not projects:
            return None
        
        # Count projects per tier
        tier_counts = {}
        for proj in projects:
            tier = self._calculate_tier(proj['score'])
            tier_counts[tier] = tier_counts.get(tier, 0) + 1
        
        # Sort by tier order
        tier_order = ['S+', 'S', 'A', 'B', 'C', 'D', 'F']
        sorted_tiers = [(t, tier_counts.get(t, 0)) for t in tier_order if tier_counts.get(t, 0) > 0]
        
        if not sorted_tiers:
            return None
        
        total_projects = len(projects)
        max_count = max([count for _, count in sorted_tiers])
        
        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="700" height="350" '
            f'viewBox="0 0 700 350">',
            
            # Background
            f'<rect width="700" height="350" fill="{self.COLORS["background"]}" rx="10"/>',
            
            # Title
            f'<text x="350" y="30" font-family="Arial, sans-serif" font-size="16" '
            f'font-weight="bold" fill="white" text-anchor="middle">',
            '🎯 Project Tier Distribution',
            '</text>',
            
            f'<text x="350" y="50" font-family="Arial, sans-serif" font-size="12" '
            f'fill="{self.COLORS["muted"]}" text-anchor="middle">',
            f'Total: {total_projects} projects',
            '</text>',
        ]
        
        # Draw bars
        bar_width = 70
        bar_spacing = 95
        bar_height_max = 200
        start_x = 50
        
        for i, (tier, count) in enumerate(sorted_tiers):
            x = start_x + (i * bar_spacing)
            bar_height = (count / max_count * bar_height_max) if max_count > 0 else 0
            y = 280 - bar_height
            
            percentage = (count / total_projects) * 100
            tier_color = self.TIER_COLORS.get(tier, self.COLORS['muted'])
            
            svg.extend([
                # Bar
                f'<rect x="{x}" y="{y}" width="{bar_width}" height="{bar_height}" '
                f'fill="{tier_color}" rx="6" opacity="0.9">',
                f'<animate attributeName="height" from="0" to="{bar_height}" dur="0.8s" fill="freeze"/>',
                f'<animate attributeName="y" from="280" to="{y}" dur="0.8s" fill="freeze"/>',
                '</rect>',
                
                # Count on top
                f'<text x="{x + bar_width/2}" y="{y - 10}" font-family="Arial, sans-serif" '
                f'font-size="16" font-weight="bold" fill="white" text-anchor="middle">{count}</text>',
                
                # Percentage
                f'<text x="{x + bar_width/2}" y="{y - 25}" font-family="Arial, sans-serif" '
                f'font-size="11" fill="{self.COLORS["muted"]}" text-anchor="middle">{percentage:.0f}%</text>',
                
                # Tier badge
                f'<rect x="{x + 5}" y="290" width="{bar_width - 10}" height="35" '
                f'fill="{tier_color}" rx="6"/>',
                f'<text x="{x + bar_width/2}" y="313" font-family="Arial, sans-serif" '
                f'font-size="18" font-weight="bold" fill="white" text-anchor="middle">{tier}</text>',
            ])
        
        svg.append('</svg>')
        
        output_path = self.output_dir / 'tier_evolution.svg'
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
        
        chart = self.generate_tier_ranking_chart()
        if chart:
            charts['tier_ranking'] = chart
            print(f"   ✅ Tier ranking generated")
        
        chart = self.generate_repo_grid(limit=12)
        if chart:
            charts['repo_grid'] = chart
            print(f"   ✅ Repository grid generated")
        
        chart = self.generate_daily_comparison_chart()
        if chart:
            charts['daily_comparison'] = chart
            print(f"   ✅ Daily comparison generated")
        
        chart = self.generate_language_pie_chart()
        if chart:
            charts['language_pie'] = chart
            print(f"   ✅ Language pie chart generated")
        
        chart = self.generate_weekly_trend_chart()
        if chart:
            charts['weekly_trend'] = chart
            print(f"   ✅ Weekly trend generated")
        
        chart = self.generate_streak_progress_chart()
        if chart:
            charts['streak_progress'] = chart
            print(f"   ✅ Streak progress generated")
        
        chart = self.generate_tier_evolution_chart()
        if chart:
            charts['tier_evolution'] = chart
            print(f"   ✅ Tier evolution generated")
        
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
    
    def _truncate_text(self, text: str, max_length: int) -> str:
        """Truncate text with ellipsis if too long."""
        if not text:
            return ""
        return text[:max_length] + "..." if len(text) > max_length else text
    
    def _escape_xml(self, text: str) -> str:
        """Escape special XML characters."""
        if not text:
            return ""
        return (text.replace('&', '&amp;')
                    .replace('<', '&lt;')
                    .replace('>', '&gt;')
                    .replace('"', '&quot;')
                    .replace("'", '&apos;'))
    
    def generate_repo_grid(self, limit: int = 12) -> str:
        """
        Generate a grid of repository cards (3 columns).
        
        Why grid layout?
        - Professional, portfolio-like appearance
        - Easy to scan visually
        - Makes good use of horizontal space
        - Each card is clickable
        
        Args:
            limit: Maximum number of repos to display
            
        Returns:
            Path to generated SVG file
        """
        top_projects = self.rankings.get('top_projects', [])[:limit]
        
        if not top_projects:
            return None
        
        # Grid configuration
        cols = 3
        card_width = 260
        card_height = 140
        gap = 15
        margin = 20
        
        rows = (len(top_projects) + cols - 1) // cols
        
        width = cols * card_width + (cols - 1) * gap + 2 * margin
        height = rows * card_height + (rows - 1) * gap + 2 * margin + 60  # +60 for title
        
        svg = [
            f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
            f'<rect width="{width}" height="{height}" fill="{self.COLORS["background"]}"/>',
            
            # Title
            f'<text x="{width/2}" y="40" font-family="Arial, sans-serif" font-size="24" '
            f'font-weight="bold" fill="{self.COLORS["text"]}" text-anchor="middle">',
            '🏆 Top Repositories',
            '</text>',
        ]
        
        # Generate cards
        for i, project in enumerate(top_projects):
            row = i // cols
            col = i % cols
            
            x = margin + col * (card_width + gap)
            y = 70 + row * (card_height + gap)  # 70 offset for title
            
            # Calculate tier
            tier = self._calculate_tier(project['score'])
            tier_color = self.TIER_COLORS[tier]
            
            # Prepare data
            name = self._truncate_text(project['name'], 25)
            lang = project['language'] or 'N/A'
            stars = project['stars']
            score = project['score']
            url = project.get('html_url', '#')
            private = project['private']
            
            # Card with link
            svg.append(f'<a href="{self._escape_xml(url)}" target="_blank">')
            
            # Card background
            svg.append(
                f'<rect x="{x}" y="{y}" width="{card_width}" height="{card_height}" '
                f'fill="{self.COLORS["surface"]}" rx="10" '
                f'stroke="{tier_color}" stroke-width="2">'
                f'<animate attributeName="opacity" values="0.8;1;0.8" dur="3s" repeatCount="indefinite"/>'
                f'</rect>'
            )
            
            # Tier badge (top-left)
            svg.append(
                f'<rect x="{x + 10}" y="{y + 10}" width="40" height="24" '
                f'fill="{tier_color}" rx="5"/>'
            )
            svg.append(
                f'<text x="{x + 30}" y="{y + 26}" font-family="monospace" font-size="14" '
                f'font-weight="bold" fill="white" text-anchor="middle">{tier}</text>'
            )
            
            # Private/Public icon (top-right)
            icon = "🔒" if private else "📂"
            svg.append(
                f'<text x="{x + card_width - 25}" y="{y + 28}" font-size="20">{icon}</text>'
            )
            
            # Repository name
            svg.append(
                f'<text x="{x + card_width/2}" y="{y + 55}" font-family="Arial, sans-serif" '
                f'font-size="16" font-weight="bold" fill="{self.COLORS["text"]}" '
                f'text-anchor="middle">{self._escape_xml(name)}</text>'
            )
            
            # Language
            svg.append(
                f'<text x="{x + card_width/2}" y="{y + 78}" font-family="monospace" '
                f'font-size="12" fill="{self.COLORS["muted"]}" text-anchor="middle">{lang}</text>'
            )
            
            # Stats row
            stats_y = y + 105
            
            # Score
            svg.append(
                f'<text x="{x + 35}" y="{stats_y}" font-family="monospace" font-size="13" '
                f'fill="{self.COLORS["primary"]}" font-weight="bold">⚡ {score}</text>'
            )
            
            # Stars (if any)
            if stars > 0:
                svg.append(
                    f'<text x="{x + card_width - 60}" y="{stats_y}" font-family="monospace" '
                    f'font-size="13" fill="{self.COLORS["tertiary"]}" font-weight="bold">⭐ {stars}</text>'
                )
            
            # Hover effect (make it obvious it's clickable)
            svg.append(
                f'<rect x="{x}" y="{y}" width="{card_width}" height="{card_height}" '
                f'fill="white" opacity="0" rx="10">'
                f'<set attributeName="opacity" to="0.1" begin="mouseover" end="mouseout"/>'
                f'</rect>'
            )
            
            svg.append('</a>')
        
        svg.append('</svg>')
        
        # Save file
        output_path = self.output_dir / 'repo_grid.svg'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(svg))
        
        return str(output_path)
    
    def generate_tier_ranking_chart(self) -> str:
        """
        Generate a horizontal tier ranking chart.
        
        Why horizontal?
        - Better use of screen width
        - Shows tier progression clearly
        - Clean, modern look
        
        Returns:
            Path to generated SVG file
        """
        top_projects = self.rankings.get('top_projects', [])[:20]
        
        if not top_projects:
            return None
        
        # Group by tier
        tier_groups = {'S+': [], 'S': [], 'A': [], 'B': [], 'C': [], 'D': [], 'F': []}
        
        for project in top_projects:
            tier = self._calculate_tier(project['score'])
            tier_groups[tier].append(project)
        
        # Filter non-empty tiers
        active_tiers = {k: v for k, v in tier_groups.items() if v}
        
        if not active_tiers:
            return None
        
        width = 800
        tier_height = 60
        header_height = 80
        height = header_height + len(active_tiers) * tier_height + 40
        
        svg = [
            f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
            f'<rect width="{width}" height="{height}" fill="{self.COLORS["background"]}"/>',
            
            # Title
            f'<text x="{width/2}" y="40" font-family="Arial, sans-serif" font-size="26" '
            f'font-weight="bold" fill="{self.COLORS["text"]}" text-anchor="middle">',
            '🎖️ Project Tier Rankings',
            '</text>',
            f'<text x="{width/2}" y="65" font-family="Arial, sans-serif" font-size="13" '
            f'fill="{self.COLORS["muted"]}" text-anchor="middle">',
            'Ranked by activity score (commits + PRs + issues)',
            '</text>',
        ]
        
        y_offset = header_height
        
        for tier, projects in active_tiers.items():
            tier_color = self.TIER_COLORS[tier]
            count = len(projects)
            
            # Tier row background
            svg.append(
                f'<rect x="20" y="{y_offset}" width="{width - 40}" height="{tier_height - 10}" '
                f'fill="{self.COLORS["surface"]}" rx="8"/>'
            )
            
            # Tier badge
            svg.append(
                f'<rect x="35" y="{y_offset + 10}" width="60" height="35" '
                f'fill="{tier_color}" rx="6"/>'
            )
            svg.append(
                f'<text x="65" y="{y_offset + 35}" font-family="monospace" font-size="20" '
                f'font-weight="bold" fill="white" text-anchor="middle">{tier}</text>'
            )
            
            # Project count
            svg.append(
                f'<text x="120" y="{y_offset + 35}" font-family="Arial, sans-serif" '
                f'font-size="16" fill="{self.COLORS["text"]}" font-weight="bold">'
                f'{count} project{"s" if count > 1 else ""}</text>'
            )
            
            # Top projects in this tier (show names)
            x_start = 280
            for i, proj in enumerate(projects[:4]):  # Max 4 names
                proj_name = self._truncate_text(proj['name'], 15)
                x_pos = x_start + i * 130
                
                if x_pos + 120 > width - 40:
                    break
                
                svg.append(
                    f'<text x="{x_pos}" y="{y_offset + 35}" font-family="monospace" '
                    f'font-size="12" fill="{self.COLORS["muted"]}">'
                    f'{"🔒" if proj["private"] else "📂"} {self._escape_xml(proj_name)}</text>'
                )
            
            if count > 4:
                svg.append(
                    f'<text x="{width - 80}" y="{y_offset + 35}" font-family="monospace" '
                    f'font-size="12" fill="{self.COLORS["muted"]}" font-style="italic">+{count - 4} more</text>'
                )
            
            y_offset += tier_height
        
        svg.append('</svg>')
        
        # Save file
        output_path = self.output_dir / 'tier_ranking.svg'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(svg))
        
        return str(output_path)
