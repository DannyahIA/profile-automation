"""
GitHub Data Collector

Este módulo coleta dados da API do GitHub.
Por quê separar em um módulo?
- Facilita testar isoladamente
- Pode ser reutilizado por diferentes jobs
- Centraliza a lógica de acesso à API
"""

from github import Github
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any
import os


class GitHubCollector:
    """
    Coleta dados do GitHub usando a biblioteca PyGithub.
    
    Por quê usar PyGithub?
    - Abstrai a complexidade da API REST do GitHub
    - Gerencia autenticação e rate limits automaticamente
    - Tem suporte a repos privados quando autenticado
    """
    
    def __init__(self, token: str):
        """
        Inicializa o coletor com um token de acesso.
        
        Args:
            token: GitHub Personal Access Token
                   Por quê precisa de token?
                   - Acesso a repos privados
                   - Rate limit maior (5000 req/hora vs 60/hora)
        """
        self.github = Github(token)
        self.user = self.github.get_user()
    
    def collect_all_repos(self) -> List[Dict[str, Any]]:
        """
        Coleta informações de TODOS os repositórios (públicos + privados).
        
        Returns:
            Lista de dicionários com dados dos repos
            
        Por quê retornar dict e não objetos?
        - Dicts são serializáveis para JSON
        - Facilita salvar e manipular depois
        """
        repos_data = []
        
        # affiliation='owner' pega repos que você é dono
        # Por quê? Porque você quer dados dos seus projetos, não de forks/contribuições
        for repo in self.user.get_repos(affiliation='owner'):
            repos_data.append({
                'name': repo.name,
                'full_name': repo.full_name,
                'private': repo.private,
                'language': repo.language,
                'stars': repo.stargazers_count,
                'forks': repo.forks_count,
                'created_at': repo.created_at.isoformat(),
                'updated_at': repo.updated_at.isoformat(),
                'pushed_at': repo.pushed_at.isoformat() if repo.pushed_at else None,
                'size': repo.size,
                'open_issues': repo.open_issues_count,
                'description': repo.description
            })
        
        return repos_data
    
    def collect_commits(self, since: datetime = None, until: datetime = None) -> List[Dict[str, Any]]:
        """
        Coleta commits de todos os repos em um período.
        
        Args:
            since: Data inicial (padrão: 30 dias atrás)
            until: Data final (padrão: agora)
            
        Returns:
            Lista de commits com metadados
            
        Por quê filtrar por data?
        - Evita processar dados antigos desnecessariamente
        - Otimiza o rate limit da API
        """
        if since is None:
            since = datetime.now(timezone.utc) - timedelta(days=30)
        elif since.tzinfo is None:
            # Adiciona timezone se não tiver
            since = since.replace(tzinfo=timezone.utc)
            
        if until is None:
            until = datetime.now(timezone.utc)
        elif until.tzinfo is None:
            # Adiciona timezone se não tiver
            until = until.replace(tzinfo=timezone.utc)
        
        commits_data = []
        
        for repo in self.user.get_repos(affiliation='owner'):
            try:
                # Pega commits do autor autenticado neste repo
                commits = repo.get_commits(author=self.user, since=since, until=until)
                
                for commit in commits:
                    commits_data.append({
                        'repo': repo.name,
                        'sha': commit.sha,
                        'message': commit.commit.message,
                        'date': commit.commit.author.date.isoformat(),
                        'additions': commit.stats.additions if commit.stats else 0,
                        'deletions': commit.stats.deletions if commit.stats else 0,
                        'total_changes': commit.stats.total if commit.stats else 0
                    })
            except Exception as e:
                # Por quê capturar exceções?
                # - Repos vazios podem dar erro
                # - Não queremos que um erro pare toda a coleta
                print(f"Erro ao coletar commits de {repo.name}: {e}")
                continue
        
        return commits_data
    
    def collect_pull_requests(self, since: datetime = None) -> List[Dict[str, Any]]:
        """
        Coleta Pull Requests criados ou atualizados recentemente.
        
        Por quê coletar PRs?
        - Indicam trabalho colaborativo
        - Mostram revisão de código
        - Importantes para métricas de produtividade
        """
        if since is None:
            since = datetime.now(timezone.utc) - timedelta(days=30)
        elif since.tzinfo is None:
            # Adiciona timezone se não tiver
            since = since.replace(tzinfo=timezone.utc)
        
        prs_data = []
        
        for repo in self.user.get_repos(affiliation='owner'):
            try:
                # state='all' pega abertos E fechados
                prs = repo.get_pulls(state='all', sort='updated', direction='desc')
                
                for pr in prs:
                    # Filtra apenas PRs relevantes para o período
                    if pr.updated_at < since:
                        break
                    
                    prs_data.append({
                        'repo': repo.name,
                        'number': pr.number,
                        'title': pr.title,
                        'state': pr.state,
                        'created_at': pr.created_at.isoformat(),
                        'updated_at': pr.updated_at.isoformat(),
                        'merged_at': pr.merged_at.isoformat() if pr.merged_at else None,
                        'closed_at': pr.closed_at.isoformat() if pr.closed_at else None,
                        'user': pr.user.login,
                        'additions': pr.additions,
                        'deletions': pr.deletions,
                        'changed_files': pr.changed_files,
                        'comments': pr.comments
                    })
            except Exception as e:
                print(f"Erro ao coletar PRs de {repo.name}: {e}")
                continue
        
        return prs_data
    
    def collect_issues(self, since: datetime = None) -> List[Dict[str, Any]]:
        """
        Coleta Issues (problemas/tarefas) dos repositórios.
        
        Por quê issues são importantes?
        - Mostram gestão de tarefas
        - Indicam problemas resolvidos
        - Revelam manutenção ativa do projeto
        """
        if since is None:
            since = datetime.now(timezone.utc) - timedelta(days=30)
        elif since.tzinfo is None:
            # Adiciona timezone se não tiver
            since = since.replace(tzinfo=timezone.utc)
        
        issues_data = []
        
        for repo in self.user.get_repos(affiliation='owner'):
            try:
                issues = repo.get_issues(state='all', since=since)
                
                for issue in issues:
                    # Pull requests também aparecem como issues, vamos filtrar
                    if issue.pull_request is not None:
                        continue
                    
                    issues_data.append({
                        'repo': repo.name,
                        'number': issue.number,
                        'title': issue.title,
                        'state': issue.state,
                        'created_at': issue.created_at.isoformat(),
                        'updated_at': issue.updated_at.isoformat(),
                        'closed_at': issue.closed_at.isoformat() if issue.closed_at else None,
                        'comments': issue.comments,
                        'labels': [label.name for label in issue.labels]
                    })
            except Exception as e:
                print(f"Erro ao coletar issues de {repo.name}: {e}")
                continue
        
        return issues_data
    
    def get_rate_limit_info(self) -> Dict[str, Any]:
        """
        Verifica o rate limit da API.
        
        Por quê isso é importante?
        - GitHub limita número de requisições
        - Evita erros por excesso de chamadas
        - Ajuda a planejar quando rodar os jobs
        """
        try:
            rate_limit = self.github.get_rate_limit()
            # Tenta acessar via atributo
            if hasattr(rate_limit, 'core'):
                return {
                    'core': {
                        'remaining': rate_limit.core.remaining,
                        'limit': rate_limit.core.limit,
                        'reset': rate_limit.core.reset.isoformat()
                    }
                }
            # Fallback: acessa via propriedade rate
            elif hasattr(rate_limit, 'rate'):
                return {
                    'core': {
                        'remaining': rate_limit.rate.remaining,
                        'limit': rate_limit.rate.limit,
                        'reset': rate_limit.rate.reset.isoformat() if rate_limit.rate.reset else 'N/A'
                    }
                }
            else:
                # Fallback simples
                return {
                    'core': {
                        'remaining': 'N/A',
                        'limit': 'N/A',
                        'reset': 'N/A'
                    }
                }
        except Exception as e:
            print(f"⚠️  Não foi possível verificar rate limit: {e}")
            return {
                'core': {
                    'remaining': 'N/A',
                    'limit': 'N/A',
                    'reset': 'N/A'
                }
            }
