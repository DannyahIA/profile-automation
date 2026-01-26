"""
README Generator - LinkedIn Style

This module generates an elegant, minimal README for GitHub profiles.
Focuses on visual SVGs and clean presentation.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List, Tuple
import re


class ReadmeGenerator:
    """
    Generates elegant, LinkedIn-style README sections.
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
        Generate DASHBOARD-STYLE metrics section with SVG charts arranged in grid layout.
        
        Design Philosophy:
        - Remove ALL text lists
        - Pure visual dashboard using HTML tables for layout
        - Everything clickable and interactive
        - LinkedIn-style professional appearance
        
        Layout Structure:
        Row 1: Stats Card (Full width)
        Row 2: Tier Ranking (Left) | Language Chart (Right)
        Row 3: Recent Activity Timeline (Left) | Achievements Grid (Right)
        Row 4: Repo Grid (Full width)
        
        Returns:
            Markdown/HTML formatted dashboard string
        """
        content = """
<!-- DASHBOARD: Visual Analytics -->
<div align="center">

## 📊 GitHub Analytics Dashboard

<!-- Row 1: Full-width Stats Card -->
![Stats Card](./assets/stats_card.svg)

<br>

<!-- Row 2: Two-column layout - Tier Ranking + Languages -->
<table>
<tr>
<td width="50%" valign="top">

### 🏆 Project Tiers

![Tier Ranking](./assets/tier_ranking.svg)

</td>
<td width="50%" valign="top">

### 💻 Language Stack

![Language Chart](./assets/language_chart.svg)

</td>
</tr>
</table>

<br>

<!-- Row 3: Two-column layout - Recent Activity + Achievements -->
<table>
<tr>
<td width="50%" valign="top">

### 🚀 Latest Activity

![Recent Activity](./assets/recent_activity.svg)

</td>
<td width="50%" valign="top">

### 🎮 Achievements

![Achievements](./assets/achievements.svg)

</td>
</tr>
</table>

<br>

<!-- Row 4: Full-width Repository Grid -->
### 🗂️ Featured Repositories

![Repository Grid](./assets/repo_grid.svg)

</div>

"""
        return content

</div>

<div align="center">

![Tier Ranking](./assets/tier_ranking.svg)

</div>

<div align="center">

![Repository Grid](./assets/repo_grid.svg)

</div>

<details>
<summary><b>View Detailed Stats</b></summary>

<br>

<div align="center">

![Activity Timeline](./assets/activity_timeline.svg)

</div>

<table align="center">
<tr>
<td align="center" width="50%">

**This Month**

📝 `{monthly.get('commits_this_month', 0)}` commits  
🔀 `{monthly.get('prs_this_month', 0)}` pull requests  
✅ `{monthly.get('issues_this_month', 0)}` issues  

</td>
<td align="center" width="50%">

**Contribution Streak**

🔥 `{streak.get('current', 0)}` days current  
🏆 `{streak.get('longest', 0)}` days record  

</td>
</tr>
</table>

</details>

<details>
<summary><b>📊 Comparative Analytics</b></summary>

<br>

<div align="center">

### Daily Performance

![Daily Comparison](./assets/daily_comparison.svg)

### Trends & Patterns

![Weekly Trend](./assets/weekly_trend.svg)

### Language Breakdown

<table>
<tr>
<td align="center">

![Language Pie](./assets/language_pie.svg)

</td>
<td align="center">

![Streak Progress](./assets/streak_progress.svg)

</td>
</tr>
</table>

### Project Distribution

![Tier Evolution](./assets/tier_evolution.svg)

</div>

</details>

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

<br>

### 📉 Trends & Patterns

![Weekly Trend](./assets/weekly_trend.svg)

<br>

### 🎯 Distribution Analysis

<table>
<tr>
<td align="center" width="50%">

![Language Pie](./assets/language_pie.svg)

</td>
<td align="center" width="50%">

![Streak Progress](./assets/streak_progress.svg)

</td>
</tr>
</table>

<br>

### 🏅 Project Tier Evolution

![Tier Evolution](./assets/tier_evolution.svg)

</div>

</details>

"""
        return content
        
        # Group by tier
        tier_groups = {'S+': [], 'S': [], 'Other': []}
        
        for project in top_projects:
            tier, emoji, color = self._get_tier(project['score'])
            project_data = {**project, 'tier': tier, 'emoji': emoji}
            
            if tier == 'S+':
                tier_groups['S+'].append(project_data)
            elif tier == 'S':
                tier_groups['S'].append(project_data)
            else:
                tier_groups['Other'].append(project_data)
        
        # Show S+ projects (if any) - these are the real stars
        if tier_groups['S+']:
            content += "<div align=\"center\">\n\n"
            content += "### 👑 Elite Projects (100+ activity)\n\n"
            content += "</div>\n\n"
            
            for proj in tier_groups['S+']:
                icon = "🔒" if proj['private'] else "📂"
                lang = proj['language'] or 'Various'
                content += f"<div align=\"center\">\n\n"
                content += f"{icon} **[{proj['name']}]({proj.get('html_url', '#')})** • {lang} • "
                content += f"⚡ {proj['score']} points"
                if proj['stars'] > 0:
                    content += f" • ⭐ {proj['stars']}"
                content += "\n\n</div>\n\n"
            content += "\n"
        
        # All other projects in collapsed details
        other_projects = tier_groups['S'] + tier_groups['Other']
        if other_projects:
            content += "<details>\n"
            content += "<summary><b>� View All Projects</b></summary>\n\n"
            content += "<br>\n\n"
            
            for proj in other_projects:
                icon = "🔒" if proj['private'] else "📂"
                lang = proj['language'] or 'Various'
                tier = proj['tier']
                content += f"- {icon} **[{proj['name']}]({proj.get('html_url', '#')})** • {tier} • {lang} • ⚡ {proj['score']}\n"
            
            content += "\n</details>\n\n"
        
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
