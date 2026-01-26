"""
README Generator

This module automatically updates the README.md file.

Why use special markers?
- Allows manual editing of other README parts
- Updates only specific sections
- Maintains custom formatting
"""

from datetime import datetime, timezone
from typing import Dict, Any, List, Tuple
import re


class ReadmeGenerator:
    """
    Generates and updates README.md sections automatically.
    """
    
    # Tier system configuration
    TIERS = {
        'S+': {'min': 100, 'emoji': '👑', 'color': '#FFD700'},
        'S':  {'min': 80,  'emoji': '🏆', 'color': '#C0C0C0'},
        'S-': {'min': 70,  'emoji': '🎖️', 'color': '#DAA520'},
        'A+': {'min': 60,  'emoji': '🥇', 'color': '#CD7F32'},
        'A':  {'min': 50,  'emoji': '🏅', 'color': '#E6A23C'},
        'A-': {'min': 40,  'emoji': '🎯', 'color': '#F0AD4E'},
        'B+': {'min': 35,  'emoji': '🥈', 'color': '#4A90E2'},
        'B':  {'min': 30,  'emoji': '📘', 'color': '#5DADE2'},
        'B-': {'min': 25,  'emoji': '📗', 'color': '#85C1E9'},
        'C+': {'min': 20,  'emoji': '🥉', 'color': '#50C878'},
        'C':  {'min': 15,  'emoji': '📙', 'color': '#52BE80'},
        'C-': {'min': 12,  'emoji': '📕', 'color': '#82E0AA'},
        'D+': {'min': 10,  'emoji': '📊', 'color': '#FFA500'},
        'D':  {'min': 7,   'emoji': '📈', 'color': '#FFB74D'},
        'D-': {'min': 5,   'emoji': '📉', 'color': '#FFCC80'},
        'F+': {'min': 3,   'emoji': '🔰', 'color': '#95A5A6'},
        'F':  {'min': 0,   'emoji': '💤', 'color': '#808080'}
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
        """
        Calculate tier based on activity score.
        
        Why tier system?
        - Visual hierarchy for projects
        - Easy to identify most important repositories
        - Gamification element that's intuitive
        
        Args:
            score: Activity score (commits + PRs + issues)
            
        Returns:
            Tuple of (tier_name, emoji, color)
        """
        for tier, config in self.TIERS.items():
            if score >= config['min']:
                return tier, config['emoji'], config['color']
        return 'F', '📉', '#808080'
    
    def _create_progress_bar(self, percentage: float, length: int = 25) -> str:
        """
        Create a visual progress bar.
        
        Why ASCII bars?
        - Works in any Markdown viewer
        - No external dependencies
        - Clear visual representation
        
        Args:
            percentage: Value from 0 to 100
            length: Total bar length in characters
            
        Returns:
            Formatted progress bar string
        """
        filled = int((percentage / 100) * length)
        bar = '█' * filled + '░' * (length - filled)
        return f"{bar} {percentage:.1f}%"
    
    def _format_number(self, num: int) -> str:
        """
        Format large numbers with K/M suffixes.
        
        Args:
            num: Number to format
            
        Returns:
            Formatted string (e.g., "1.2K", "3.5M")
        """
        if num >= 1_000_000:
            return f"{num/1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num/1_000:.1f}K"
        return str(num)
    
    def generate_metrics_section(self) -> str:
        """
        Generate real-time metrics section with visual enhancements.
        
        Why badges and emojis?
        - Attractive visual presentation
        - Quick information scanning
        - Standard in GitHub profile READMEs
        
        Returns:
            Markdown formatted string
        """
        streak = self.metrics['activity_streak']
        monthly = self.metrics['monthly_stats']
        
        # Header with stats cards
        content = f"""## 📊 GitHub Statistics

<div align="center">

| 📝 Commits | 🔀 Pull Requests | 🐛 Issues | 📦 Repositories |
|:----------:|:----------------:|:---------:|:---------------:|
| **{self._format_number(self.metrics['total_commits'])}** | **{self._format_number(self.metrics['total_prs'])}** | **{self._format_number(self.metrics['total_issues'])}** | **{self.metrics['total_repos']}** |

</div>

### 🔥 Contribution Streak

```
Current Streak: {streak['current']} days �
Longest Streak: {streak['longest']} days 🏆
```

### 📅 This Month ({monthly.get('month', 'N/A')})

<table>
<tr>
<td>

**Activity Overview**
- ✨ `{monthly['commits_this_month']}` commits
- 🔀 `{monthly['prs_this_month']}` pull requests  
- ✅ `{monthly['issues_this_month']}` issues

</td>
<td>

**Daily Average**
- 📊 `{monthly['commits_this_month'] / 30:.1f}` commits/day
- 🎯 `{(monthly['commits_this_month'] + monthly['prs_this_month'] + monthly['issues_this_month']) / 30:.1f}` actions/day

</td>
</tr>
</table>

### 💻 Language Distribution

"""
        
        # Add languages with visual progress bars
        languages = self.metrics['top_languages']
        if languages:
            total = sum(languages.values())
            content += "<div align=\"center\">\n\n"
            content += "| Language | Usage |\n"
            content += "|:---------|:------|\n"
            
            for lang, count in list(languages.items())[:8]:  # Top 8
                percentage = (count / total) * 100
                bar = self._create_progress_bar(percentage, 20)
                content += f"| **{lang}** | `{bar}` |\n"
            
            content += "\n</div>\n"
        else:
            content += "*No languages detected yet.*\n"
        
        return content
    
    def generate_rankings_section(self) -> str:
        """
        Generate project rankings with tier system (F to S+).
        
        Why show rankings?
        - Highlights most relevant work
        - Easy profile navigation
        - Shows project diversity
        
        Why tier system?
        - Intuitive visual hierarchy
        - Common in gaming/achievement systems
        - Makes it easy to spot top projects
        """
        content = "## 🏆 Project Rankings\n\n"
        content += "*Projects ranked by activity (commits + PRs + issues)*\n\n"
        
        top_projects = self.rankings['top_projects'][:15]  # Top 15
        
        if not top_projects:
            return content + "*No projects with recent activity.*\n"
        
        # Group projects by tier
        tier_groups = {tier: [] for tier in self.TIERS.keys()}
        
        for project in top_projects:
            tier, emoji, color = self._get_tier(project['score'])
            tier_groups[tier].append({**project, 'tier': tier, 'emoji': emoji, 'color': color})
        
        # Display each tier
        for tier_name in self.TIERS.keys():
            projects = tier_groups[tier_name]
            if not projects:
                continue
            
            tier_config = self.TIERS[tier_name]
            content += f"\n### {tier_config['emoji']} Tier {tier_name}\n"
            content += f"*Score Range: {tier_config['min']}+ points*\n\n"
            
            # Table header
            content += "| Project | Language | Score | Breakdown | Stars |\n"
            content += "|:--------|:---------|------:|:----------|------:|\n"
            
            for project in projects:
                icon = "🔒" if project['private'] else "📂"
                lang = project['language'] or 'N/A'
                stars = f"⭐ {project['stars']}" if project['stars'] > 0 else "-"
                
                breakdown = f"`💻 {project['breakdown']['commits']}` " \
                           f"`� {project['breakdown']['prs']}` " \
                           f"`� {project['breakdown']['issues']}`"
                
                content += f"| {icon} **{project['name']}** | {lang} | **{project['score']}** | {breakdown} | {stars} |\n"
        
        # Add most starred projects section
        starred = self.rankings['most_stars'][:5]
        if starred and any(p['stars'] > 0 for p in starred):
            content += "\n---\n\n"
            content += "## ⭐ Most Starred Projects\n\n"
            
            for i, project in enumerate(starred, 1):
                if project['stars'] > 0:
                    content += f"### {i}. {project['name']}\n"
                    content += f"**⭐ {self._format_number(project['stars'])} stars** "
                    content += f"| 🍴 {self._format_number(project['forks'])} forks"
                    
                    if project['language']:
                        content += f" | 💻 {project['language']}"
                    
                    content += "\n\n"
                    
                    if project['description']:
                        content += f"> {project['description']}\n\n"
        
        return content
    
    def generate_recent_activity_section(self) -> str:
        """
        Generate recent activity section.
        
        Why show recent activity?
        - Indicates what you're currently working on
        - Keeps profile up-to-date
        - Shows continuous engagement
        """
        content = "\n## 🚀 Recent Activity\n\n"
        content += "*Projects I'm currently working on*\n\n"
        
        recent = self.rankings['most_recent'][:8]
        
        if not recent:
            return content + "*No recent activity.*\n"
        
        content += "| Project | Language | Last Active |\n"
        content += "|:--------|:---------|:-----------:|\n"
        
        for project in recent:
            icon = "🔒" if project['private'] else "📂"
            lang = project['language'] or 'N/A'
            days = project['days_ago']
            
            # Format time in user-friendly way
            if days == 0:
                time_str = "🟢 Today"
            elif days == 1:
                time_str = "🟢 Yesterday"
            elif days < 7:
                time_str = f"🟡 {days} days ago"
            elif days < 30:
                weeks = days // 7
                time_str = f"🟡 {weeks} week{'s' if weeks > 1 else ''} ago"
            else:
                months = days // 30
                time_str = f"🔴 {months} month{'s' if months > 1 else ''} ago"
            
            content += f"| {icon} **{project['name']}** | {lang} | {time_str} |\n"
        
        return content
    
    def update_readme(self, readme_path: str) -> bool:
        """
        Update the README.md file.
        
        Why use <!-- --> markers?
        - They are invisible HTML comments on GitHub
        - Delimit automated sections
        - Allow manual editing of other parts
        
        Args:
            readme_path: Path to README.md
            
        Returns:
            True if updated successfully
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
            
            # Update rankings section
            content = self._replace_section(
                content,
                'RANKINGS_START',
                'RANKINGS_END',
                rankings_section + "\n" + recent_section
            )
            
            # Add last update timestamp
            now = datetime.now(timezone.utc).strftime('%B %d, %Y at %H:%M')
            content = re.sub(
                r'\*Last updated:.*?\*',
                f'*Last updated: {now} UTC*',
                content
            )
            
            # Save updated README
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
            
        except Exception as e:
            print(f"Error updating README: {e}")
            return False
    
    def _replace_section(self, content: str, start_marker: str, 
                        end_marker: str, new_content: str) -> str:
        """
        Replace content between markers.
        
        Why helper method?
        - Reusable for multiple sections
        - Centralizes regex logic
        - Easier maintenance
        
        Args:
            content: Full README content
            start_marker: Start marker (e.g., METRICS_START)
            end_marker: End marker (e.g., METRICS_END)
            new_content: New content to insert
            
        Returns:
            Updated content
        """
        pattern = f'<!-- {start_marker} -->.*?<!-- {end_marker} -->'
        replacement = f'<!-- {start_marker} -->\n{new_content}\n<!-- {end_marker} -->'
        
        # re.DOTALL makes . include line breaks
        return re.sub(pattern, replacement, content, flags=re.DOTALL)
