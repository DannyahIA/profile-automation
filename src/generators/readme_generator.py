"""
README Generator - Dashboard Style

This module generates an elegant, visual dashboard README for GitHub profiles.
Focuses on interactive SVG charts with minimal text.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List, Tuple
import re


class ReadmeGenerator:
    """
    Generates interactive, dashboard-style README sections.
    """
    
    # Tier system configuration
    TIERS = {
        'S+': {'min': 100, 'emoji': '👑', 'color': '#FFD700'},
        'S':  {'min': 50,  'emoji': '🏆', 'color': '#C0C0C0'},
        'A':  {'min': 30,  'emoji': '🥇', 'color': '#CD7F32'},
        'B':  {'min': 20,  'emoji': '🥈', 'color': '#4A90E2'},
        'C':  {'min': 10,  'emoji': '🥉', 'color': '#50C878'},
        'D':  {'min': 5,   'emoji': '📊', 'color': '#FFA500'},
        'F':  {'min': 0,   'emoji': '📉', 'color': '#808080'}
    }
    
    def __init__(self, metrics: Dict[str, Any], rankings: Dict[str, Any]):
        """
        Initialize with processed metrics and rankings.
        
        Args:
            metrics: Dictionary with aggregated metrics
            rankings: Dictionary with project rankings
        """
        self.metrics = metrics
        self.rankings = rankings
    
    def _get_tier(self, score: int) -> Tuple[str, str, str]:
        """Calculate tier based on activity score."""
        for tier, config in self.TIERS.items():
            if score >= config['min']:
                return tier, config['emoji'], config['color']
        return 'F', '📉', '#808080'
    
    def _format_number(self, num: int) -> str:
        """Format large numbers with K/M suffixes."""
        if num >= 1_000_000:
            return f"{num/1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num/1_000:.1f}K"
        return str(num)
    
    def generate_metrics_section(self) -> str:
        """
        Generate DASHBOARD-STYLE metrics section with SVG charts in clean vertical layout.
        
        Design Philosophy:
        - Remove ALL text lists and tables
        - Pure visual dashboard with simple vertical flow
        - Everything clickable and interactive
        - LinkedIn-style professional appearance
        
        Layout Structure:
        - Stats Card (Full width)
        - Project Tiers
        - Language Stack
        - Latest Activity
        - Achievements
        - Featured Repositories
        
        Returns:
            Markdown/HTML formatted dashboard string
        """
        content = """
<!-- DASHBOARD: Visual Analytics -->
<div align="center">

## 📊 GitHub Analytics Dashboard

![Stats Card](./assets/stats_card.svg)

### 🏆 Project Tiers

![Tier Ranking](./assets/tier_ranking.svg)

### 💻 Language Stack

![Language Chart](./assets/language_chart.svg)

### 🚀 Latest Activity

![Recent Activity](./assets/recent_activity.svg)

### 🎮 Achievements

![Achievements](./assets/achievements.svg)

### 🗂️ Featured Repositories

![Repository Grid](./assets/repo_grid.svg)

</div>
"""
        return content
    
    def generate_rankings_section(self) -> str:
        """
        Generate OPTIONAL collapsible section for advanced analytics.
        Most users will just see the main dashboard.
        This section is for deep-dive analysis enthusiasts.
        
        Why collapsible?
        - Keeps main page clean and visual
        - Advanced metrics available on demand
        - Demonstrates data processing capabilities
        
        Returns:
            Markdown formatted string
        """
        content = """
<details>
<summary><b>📈 Advanced Analytics (Click to expand)</b></summary>

<br>

<div align="center">

### 📊 Comparative Performance

![Daily Comparison](./assets/daily_comparison.svg)

### 📉 Trends & Patterns

![Weekly Trend](./assets/weekly_trend.svg)

### 🎯 Distribution Analysis

![Language Pie](./assets/language_pie.svg)

![Streak Progress](./assets/streak_progress.svg)

### 🏅 Project Tier Evolution

![Tier Evolution](./assets/tier_evolution.svg)

</div>

</details>
"""
        return content
    
    def generate_recent_activity_section(self) -> str:
        """
        DEPRECATED: Recent activity now handled by generate_recent_activity_svg() in chart_generator.
        This method returns empty string as activity is shown visually in the main dashboard.
        
        Returns:
            Empty string (visual SVG replaces text lists)
        """
        return ""
    
    def update_readme(self, readme_path: str) -> bool:
        """
        Update README.md with automated sections.
        
        Why HTML markers?
        - Invisible in rendered output
        - Clearly mark automated sections
        - Allow manual editing outside markers
        
        Args:
            readme_path: Path to README.md file
            
        Returns:
            True if successful
        """
        try:
            # Read current README
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Generate new sections
            metrics_section = self.generate_metrics_section()
            rankings_section = self.generate_rankings_section()
            recent_section = self.generate_recent_activity_section()
            
            # Update metrics section
            content = self._replace_section(
                content,
                'METRICS_START',
                'METRICS_END',
                metrics_section
            )
            
            # Update rankings section (includes recent activity)
            content = self._replace_section(
                content,
                'RANKINGS_START',
                'RANKINGS_END',
                rankings_section + recent_section
            )
            
            # Update timestamp
            now = datetime.now(timezone.utc).strftime('%B %d, %Y')
            content = re.sub(
                r'\*Last updated:.*?\*',
                f'*Last updated: {now}*',
                content
            )
            
            # Save updated README
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
            
        except Exception as e:
            print(f"Error updating README: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _replace_section(self, content: str, start_marker: str, 
                        end_marker: str, new_content: str) -> str:
        """
        Replace content between HTML comment markers.
        
        Args:
            content: Full README content
            start_marker: Start marker name
            end_marker: End marker name
            new_content: New content to insert
            
        Returns:
            Updated content
        """
        pattern = f'<!-- {start_marker} -->.*?<!-- {end_marker} -->'
        replacement = f'<!-- {start_marker} -->\n{new_content}\n<!-- {end_marker} -->'
        
        # re.DOTALL makes . match newlines
        return re.sub(pattern, replacement, content, flags=re.DOTALL)
