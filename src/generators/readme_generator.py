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
        Generate elegant, minimal metrics section with SVG charts.
        
        Why minimal design?
        - Professional LinkedIn-style appearance
        - Focus on visual elements (SVGs)
        - Clean, scannable layout
        
        Returns:
            Markdown formatted string
        """
        monthly = self.metrics.get('monthly_stats', {})
        streak = self.metrics.get('activity_streak', {})
        
        content = f"""
<div align="center">

## 📊 GitHub Activity

![Stats](./assets/stats_card.svg)

</div>

<div align="center">

![Languages](./assets/language_chart.svg)

</div>

<details>
<summary><b>📈 View Detailed Stats</b></summary>

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

"""
        return content
    
    def generate_rankings_section(self) -> str:
        """
        Generate clean project rankings section.
        
        Why minimal rankings?
        - Focus on top projects only
        - Use collapsible sections for details
        - Visual tier indicators
        
        Returns:
            Markdown formatted string
        """
        content = "\n## 🏆 Featured Projects\n\n"
        
        top_projects = self.rankings.get('top_projects', [])[:10]  # Top 10 only
        
        if not top_projects:
            content += "_No recent project activity._\n\n"
            return content
        
        # Group by tier
        tier_groups = {'S+': [], 'S': [], 'A': [], 'Other': []}
        
        for project in top_projects:
            tier, emoji, color = self._get_tier(project['score'])
            project_data = {**project, 'tier': tier, 'emoji': emoji}
            
            if tier in ['S+', 'S', 'A']:
                tier_groups[tier].append(project_data)
            else:
                tier_groups['Other'].append(project_data)
        
        # Show S+ projects (if any)
        if tier_groups['S+']:
            content += "<div align=\"center\">\n\n"
            content += "### 👑 Elite Projects (100+ activity)\n\n"
            content += "</div>\n\n"
            
            for proj in tier_groups['S+']:
                icon = "🔒" if proj['private'] else "📂"
                lang = proj['language'] or 'Various'
                content += f"- {icon} **[{proj['name']}]({proj.get('html_url', '#')})** • {lang} • "
                content += f"⚡ {proj['score']} points"
                if proj['stars'] > 0:
                    content += f" • ⭐ {proj['stars']}"
                content += "\n"
            content += "\n"
        
        # Show S projects (if any)
        if tier_groups['S']:
            content += "<div align=\"center\">\n\n"
            content += "### 🏆 Top Projects (50+ activity)\n\n"
            content += "</div>\n\n"
            
            for proj in tier_groups['S']:
                icon = "🔒" if proj['private'] else "📂"
                lang = proj['language'] or 'Various'
                content += f"- {icon} **[{proj['name']}]({proj.get('html_url', '#')})** • {lang} • "
                content += f"⚡ {proj['score']} points"
                if proj['stars'] > 0:
                    content += f" • ⭐ {proj['stars']}"
                content += "\n"
            content += "\n"
        
        # Show A projects (if any)
        if tier_groups['A']:
            content += "<details>\n"
            content += "<summary><b>🥇 Active Projects (30+ activity)</b></summary>\n\n"
            content += "<br>\n\n"
            
            for proj in tier_groups['A']:
                icon = "🔒" if proj['private'] else "📂"
                lang = proj['language'] or 'Various'
                content += f"- {icon} **{proj['name']}** • {lang} • ⚡ {proj['score']} points\n"
            
            content += "\n</details>\n\n"
        
        # Show other projects in collapsed section
        if tier_groups['Other']:
            content += "<details>\n"
            content += "<summary><b>📦 Other Projects</b></summary>\n\n"
            content += "<br>\n\n"
            
            for proj in tier_groups['Other'][:5]:  # Limit to 5
                icon = "🔒" if proj['private'] else "📂"
                lang = proj['language'] or 'Various'
                content += f"- {icon} **{proj['name']}** • {lang}\n"
            
            content += "\n</details>\n\n"
        
        return content
    
    def generate_recent_activity_section(self) -> str:
        """
        Generate minimal recent activity section.
        
        Why minimal?
        - Quick glance at current work
        - Collapsed by default
        - Focus on most recent only
        
        Returns:
            Markdown formatted string
        """
        recent = self.rankings.get('most_recent', [])[:5]  # Top 5
        
        if not recent:
            return ""
        
        content = "<details>\n"
        content += "<summary><b>🚀 Recent Work</b></summary>\n\n"
        content += "<br>\n\n"
        
        for project in recent:
            icon = "🔒" if project['private'] else "📂"
            lang = project['language'] or 'Various'
            days = project['days_ago']
            
            # Format time
            if days == 0:
                time_str = "today"
            elif days == 1:
                time_str = "yesterday"
            elif days < 7:
                time_str = f"{days}d ago"
            elif days < 30:
                time_str = f"{days//7}w ago"
            else:
                time_str = f"{days//30}mo ago"
            
            content += f"- {icon} **{project['name']}** • {lang} • _{time_str}_\n"
        
        content += "\n</details>\n\n"
        return content
    
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
