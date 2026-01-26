"""
README Generator

Este módulo atualiza o README.md automaticamente.

Por quê usar marcadores especiais?
- Permite editar outras partes do README manualmente
- Atualiza apenas seções específicas
- Mantém formatação customizada
"""

from datetime import datetime, timezone
from typing import Dict, Any
import re


class ReadmeGenerator:
    """
    Gera e atualiza seções do README.md automaticamente.
    """
    
    def __init__(self, metrics: Dict[str, Any], rankings: Dict[str, Any]):
        """
        Inicializa com métricas e rankings processados.
        
        Args:
            metrics: Dicionário com métricas agregadas
            rankings: Dicionário com rankings de projetos
        """
        self.metrics = metrics
        self.rankings = rankings
    
    def generate_metrics_section(self) -> str:
        """
        Gera a seção de métricas em tempo real.
        
        Por quê badges/emojis?
        - Visual atrativo
        - Informação rápida
        - Padrão em READMEs de perfil
        
        Returns:
            String formatada em Markdown
        """
        streak = self.metrics['activity_streak']
        monthly = self.metrics['monthly_stats']
        
        content = f"""### 📊 Estatísticas Gerais

- 📝 **{self.metrics['total_commits']}** commits nos últimos 30 dias
- 🔀 **{self.metrics['total_prs']}** pull requests
- 🐛 **{self.metrics['total_issues']}** issues trabalhadas
- 📦 **{self.metrics['total_repos']}** repositórios ativos

### 🔥 Streak Atual

- 🎯 Sequência atual: **{streak['current']}** dias
- 🏆 Maior sequência: **{streak['longest']}** dias

### 📅 Mês Atual ({monthly.get('month', 'N/A')})

- ✨ {monthly['commits_this_month']} commits
- 🔀 {monthly['prs_this_month']} pull requests
- ✅ {monthly['issues_this_month']} issues

### 💻 Linguagens Mais Usadas

"""
        
        # Adiciona linguagens com barra de progresso visual
        languages = self.metrics['top_languages']
        if languages:
            total = sum(languages.values())
            for lang, count in list(languages.items())[:5]:  # Top 5
                percentage = (count / total) * 100
                bar_length = int(percentage / 5)  # Cada # = 5%
                bar = '█' * bar_length
                content += f"- **{lang}**: {bar} {percentage:.1f}%\n"
        else:
            content += "*Nenhuma linguagem detectada ainda.*\n"
        
        return content
    
    def generate_rankings_section(self) -> str:
        """
        Gera a seção de top projetos.
        
        Por quê mostrar rankings?
        - Destaca trabalho mais relevante
        - Facilita navegação no perfil
        - Mostra diversidade de projetos
        """
        content = "### 🏆 Top Projetos (por atividade)\n\n"
        
        top_projects = self.rankings['top_projects'][:5]  # Top 5
        
        if not top_projects:
            return content + "*Nenhum projeto com atividade recente.*\n"
        
        for i, project in enumerate(top_projects, 1):
            icon = "🔒" if project['private'] else "📂"
            lang = project['language'] or 'N/A'
            stars = f"⭐ {project['stars']}" if project['stars'] > 0 else ""
            
            content += f"{i}. {icon} **{project['name']}** "
            content += f"({lang}) - Score: {project['score']} {stars}\n"
            content += f"   - 💻 {project['breakdown']['commits']} commits "
            content += f"| 🔀 {project['breakdown']['prs']} PRs "
            content += f"| 🐛 {project['breakdown']['issues']} issues\n\n"
        
        # Adiciona seção de projetos mais estrelas (se houver)
        starred = self.rankings['most_stars'][:3]
        if starred and any(p['stars'] > 0 for p in starred):
            content += "\n### ⭐ Projetos com Mais Estrelas\n\n"
            for project in starred:
                if project['stars'] > 0:
                    content += f"- **{project['name']}**: ⭐ {project['stars']} "
                    content += f"| 🍴 {project['forks']} forks"
                    if project['description']:
                        content += f"\n  *{project['description']}*"
                    content += "\n"
        
        return content
    
    def generate_recent_activity_section(self) -> str:
        """
        Gera seção com atividade recente.
        
        Por quê mostrar atividade recente?
        - Indica em que você está trabalhando agora
        - Mantém perfil atualizado
        - Mostra engajamento contínuo
        """
        content = "### 🚀 Trabalhando Recentemente Em\n\n"
        
        recent = self.rankings['most_recent'][:5]
        
        if not recent:
            return content + "*Nenhuma atividade recente.*\n"
        
        for project in recent:
            icon = "🔒" if project['private'] else "📂"
            lang = project['language'] or 'N/A'
            days = project['days_ago']
            
            # Formata tempo de forma amigável
            if days == 0:
                time_str = "hoje"
            elif days == 1:
                time_str = "ontem"
            elif days < 7:
                time_str = f"{days} dias atrás"
            elif days < 30:
                weeks = days // 7
                time_str = f"{weeks} semana{'s' if weeks > 1 else ''} atrás"
            else:
                months = days // 30
                time_str = f"{months} mês{'es' if months > 1 else ''} atrás"
            
            content += f"- {icon} **{project['name']}** ({lang}) - {time_str}\n"
        
        return content
    
    def update_readme(self, readme_path: str) -> bool:
        """
        Atualiza o arquivo README.md.
        
        Por quê usar marcadores <!-- -->?
        - São comentários HTML invisíveis no GitHub
        - Delimitam seções automatizadas
        - Permitem edição manual de outras partes
        
        Args:
            readme_path: Caminho para o README.md
            
        Returns:
            True se atualizou com sucesso
        """
        try:
            # Lê README atual
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Gera novas seções
            metrics_section = self.generate_metrics_section()
            rankings_section = self.generate_rankings_section()
            recent_section = self.generate_recent_activity_section()
            
            # Atualiza seção de métricas
            content = self._replace_section(
                content,
                'METRICS_START',
                'METRICS_END',
                metrics_section
            )
            
            # Atualiza seção de rankings
            content = self._replace_section(
                content,
                'RANKINGS_START',
                'RANKINGS_END',
                rankings_section + "\n" + recent_section
            )
            
            # Adiciona timestamp de última atualização
            now = datetime.now(timezone.utc).strftime('%d/%m/%Y às %H:%M')
            content = re.sub(
                r'\*Última atualização:.*?\*',
                f'*Última atualização: {now} UTC*',
                content
            )
            
            # Salva README atualizado
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
            
        except Exception as e:
            print(f"Erro ao atualizar README: {e}")
            return False
    
    def _replace_section(self, content: str, start_marker: str, 
                        end_marker: str, new_content: str) -> str:
        """
        Substitui conteúdo entre marcadores.
        
        Por quê método auxiliar?
        - Reutilizável para várias seções
        - Centraliza lógica de regex
        - Facilita manutenção
        
        Args:
            content: Conteúdo completo do README
            start_marker: Marcador inicial (ex: METRICS_START)
            end_marker: Marcador final (ex: METRICS_END)
            new_content: Novo conteúdo para inserir
            
        Returns:
            Conteúdo atualizado
        """
        pattern = f'<!-- {start_marker} -->.*?<!-- {end_marker} -->'
        replacement = f'<!-- {start_marker} -->\n{new_content}\n<!-- {end_marker} -->'
        
        # re.DOTALL faz o . incluir quebras de linha
        return re.sub(pattern, replacement, content, flags=re.DOTALL)
