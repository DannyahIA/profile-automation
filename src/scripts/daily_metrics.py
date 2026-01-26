#!/usr/bin/env python3
"""
Daily Metrics Script

Este script roda DIARIAMENTE e:
1. Coleta dados do GitHub
2. Processa métricas
3. Gera rankings
4. Atualiza README

Por quê rodar diariamente?
- Mantém dados atualizados
- Não sobrecarrega a API (rate limit)
- Permite tracking diário de progresso
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

# Adiciona o diretório src ao path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from collectors.github_collector import GitHubCollector
from processors.metrics_processor import MetricsProcessor
from processors.rankings_processor import RankingsProcessor
from generators.readme_generator import ReadmeGenerator


def load_json(filepath: str, default=None):
    """
    Carrega arquivo JSON ou retorna default se não existir.
    
    Por quê função auxiliar?
    - Evita repetir try/except em vários lugares
    - Centraliza tratamento de erros
    - Facilita testes
    """
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return default if default is not None else {}


def save_json(filepath: str, data: dict):
    """
    Salva dados em arquivo JSON.
    
    Por quê indent=2?
    - JSON fica legível por humanos
    - Facilita debug e versionamento
    - Ocupa pouco espaço extra
    """
    # Garante que o diretório existe
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    """
    Função principal que executa o pipeline diário.
    
    PIPELINE:
    1. Setup e validação
    2. Coleta de dados
    3. Processamento
    4. Geração de outputs
    5. Atualização de arquivos
    """
    print("🚀 Iniciando coleta diária de métricas...")
    print(f"⏰ Timestamp: {datetime.now().isoformat()}")
    
    # 1. SETUP
    # Pega token do ambiente (configurado no GitHub Actions)
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print("❌ ERRO: GITHUB_TOKEN não encontrado nas variáveis de ambiente")
        print("💡 Dica: Configure o token nas secrets do repositório")
        sys.exit(1)
    
    # Define caminhos dos arquivos
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / 'data'
    readme_path = project_root / 'README.md'
    
    # 2. COLETA DE DADOS
    print("\n📡 Coletando dados do GitHub...")
    
    try:
        collector = GitHubCollector(token)
        
        # Verifica rate limit antes de começar (opcional, não falha se der erro)
        try:
            rate_limit = collector.get_rate_limit_info()
            remaining = rate_limit['core']['remaining']
            limit = rate_limit['core']['limit']
            print(f"   Rate limit: {remaining}/{limit}")
        except Exception as e:
            print(f"   ⚠️  Rate limit info indisponível: {e}")
            print(f"   ➡️  Continuando coleta mesmo assim...")
        
        # Coleta dados dos últimos 30 dias
        since = datetime.now() - timedelta(days=30)
        
        print("   - Coletando repositórios...")
        repos = collector.collect_all_repos()
        print(f"   ✅ {len(repos)} repositórios encontrados")
        
        print("   - Coletando commits...")
        commits = collector.collect_commits(since=since)
        print(f"   ✅ {len(commits)} commits coletados")
        
        print("   - Coletando pull requests...")
        prs = collector.collect_pull_requests(since=since)
        print(f"   ✅ {len(prs)} PRs coletados")
        
        print("   - Coletando issues...")
        issues = collector.collect_issues(since=since)
        print(f"   ✅ {len(issues)} issues coletadas")
        
    except Exception as e:
        print(f"❌ Erro na coleta de dados: {e}")
        sys.exit(1)
    
    # 3. PROCESSAMENTO
    print("\n⚙️  Processando métricas...")
    
    try:
        # Processa métricas
        metrics_processor = MetricsProcessor(repos, commits, prs, issues)
        metrics = metrics_processor.generate_metrics()
        print("   ✅ Métricas calculadas")
        
        # Processa rankings
        rankings_processor = RankingsProcessor(repos, commits, prs, issues)
        rankings = rankings_processor.generate_rankings()
        print("   ✅ Rankings gerados")
        
    except Exception as e:
        print(f"❌ Erro no processamento: {e}")
        sys.exit(1)
    
    # 4. SALVAMENTO DE DADOS
    print("\n💾 Salvando dados...")
    
    try:
        save_json(str(data_dir / 'metrics.json'), metrics)
        print("   ✅ metrics.json salvo")
        
        save_json(str(data_dir / 'rankings.json'), rankings)
        print("   ✅ rankings.json salvo")
        
    except Exception as e:
        print(f"❌ Erro ao salvar dados: {e}")
        sys.exit(1)
    
    # 5. ATUALIZAÇÃO DO README
    print("\n📝 Atualizando README...")
    
    try:
        generator = ReadmeGenerator(metrics, rankings)
        success = generator.update_readme(str(readme_path))
        
        if success:
            print("   ✅ README atualizado com sucesso!")
        else:
            print("   ⚠️  README não foi atualizado")
            
    except Exception as e:
        print(f"❌ Erro ao atualizar README: {e}")
        sys.exit(1)
    
    # 6. RESUMO FINAL
    print("\n" + "="*50)
    print("✨ Execução concluída com sucesso!")
    print("="*50)
    print(f"\n📊 Resumo:")
    print(f"   - {len(repos)} repositórios")
    print(f"   - {len(commits)} commits")
    print(f"   - {len(prs)} PRs")
    print(f"   - {len(issues)} issues")
    print(f"   - Streak: {metrics['activity_streak']['current']} dias")
    print(f"\n💾 Dados salvos em: {data_dir}")
    print(f"📝 README atualizado: {readme_path}")
    print("\n🎉 Tudo pronto!")


if __name__ == '__main__':
    main()
