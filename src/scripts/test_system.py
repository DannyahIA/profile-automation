#!/usr/bin/env python3
"""
Test Script - Para testar componentes individuais

Por quê ter um script de teste?
- Valida instalação
- Debug rápido
- Aprende como usar cada módulo
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Setup do path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_connection():
    """Testa conexão com GitHub API"""
    print("\n" + "="*50)
    print("🧪 Teste 1: Conexão com GitHub API")
    print("="*50)
    
    try:
        from collectors.github_collector import GitHubCollector
        
        token = os.getenv('GITHUB_TOKEN')
        if not token:
            print("❌ GITHUB_TOKEN não encontrado")
            print("💡 Execute: export GITHUB_TOKEN='seu_token'")
            return False
        
        collector = GitHubCollector(token)
        user = collector.user
        
        print(f"✅ Conectado como: {user.login}")
        print(f"📧 Email: {user.email or 'N/A'}")
        print(f"📍 Localização: {user.location or 'N/A'}")
        print(f"📦 Repos públicos: {user.public_repos}")
        
        rate = collector.get_rate_limit_info()
        print(f"⏱️  Rate limit: {rate['core']['remaining']}/{rate['core']['limit']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def test_data_collection():
    """Testa coleta de dados"""
    print("\n" + "="*50)
    print("🧪 Teste 2: Coleta de Dados")
    print("="*50)
    
    try:
        from collectors.github_collector import GitHubCollector
        
        token = os.getenv('GITHUB_TOKEN')
        collector = GitHubCollector(token)
        
        # Coleta últimos 7 dias (mais rápido para teste)
        since = datetime.now() - timedelta(days=7)
        
        print("📦 Coletando repositórios...")
        repos = collector.collect_all_repos()
        print(f"   ✅ {len(repos)} repos encontrados")
        if repos:
            print(f"   Exemplo: {repos[0]['name']} ({repos[0]['language']})")
        
        print("💻 Coletando commits...")
        commits = collector.collect_commits(since=since)
        print(f"   ✅ {len(commits)} commits (últimos 7 dias)")
        if commits:
            print(f"   Último: {commits[0]['message'][:50]}...")
        
        print("🔀 Coletando PRs...")
        prs = collector.collect_pull_requests(since=since)
        print(f"   ✅ {len(prs)} PRs")
        
        print("🐛 Coletando issues...")
        issues = collector.collect_issues(since=since)
        print(f"   ✅ {len(issues)} issues")
        
        return True, (repos, commits, prs, issues)
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def test_processing(data):
    """Testa processamento de métricas"""
    print("\n" + "="*50)
    print("🧪 Teste 3: Processamento de Métricas")
    print("="*50)
    
    if not data:
        print("⚠️  Sem dados para processar")
        return False
    
    try:
        from processors.metrics_processor import MetricsProcessor
        from processors.rankings_processor import RankingsProcessor
        
        repos, commits, prs, issues = data
        
        print("📊 Processando métricas...")
        processor = MetricsProcessor(repos, commits, prs, issues)
        metrics = processor.generate_metrics()
        
        print(f"   ✅ Total commits: {metrics['total_commits']}")
        print(f"   ✅ Total PRs: {metrics['total_prs']}")
        print(f"   ✅ Total issues: {metrics['total_issues']}")
        print(f"   ✅ Streak atual: {metrics['activity_streak']['current']} dias")
        print(f"   ✅ Top linguagem: {list(metrics['top_languages'].keys())[0] if metrics['top_languages'] else 'N/A'}")
        
        print("🏆 Processando rankings...")
        ranker = RankingsProcessor(repos, commits, prs, issues)
        rankings = ranker.generate_rankings()
        
        if rankings['top_projects']:
            top = rankings['top_projects'][0]
            print(f"   ✅ Top projeto: {top['name']} (score: {top['score']})")
        else:
            print("   ⚠️  Nenhum projeto com atividade")
        
        return True, (metrics, rankings)
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def test_readme_generation(processed_data):
    """Testa geração de README"""
    print("\n" + "="*50)
    print("🧪 Teste 4: Geração de README")
    print("="*50)
    
    if not processed_data:
        print("⚠️  Sem dados processados")
        return False
    
    try:
        from generators.readme_generator import ReadmeGenerator
        
        metrics, rankings = processed_data
        
        generator = ReadmeGenerator(metrics, rankings)
        
        print("📝 Gerando seção de métricas...")
        metrics_section = generator.generate_metrics_section()
        print("   ✅ Gerado! Prévia:")
        print("   " + "\n   ".join(metrics_section.split('\n')[:10]))
        
        print("\n🏆 Gerando seção de rankings...")
        rankings_section = generator.generate_rankings_section()
        print("   ✅ Gerado! Prévia:")
        print("   " + "\n   ".join(rankings_section.split('\n')[:8]))
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Executa todos os testes"""
    print("\n" + "🚀"*25)
    print("SUITE DE TESTES - Profile Automation")
    print("🚀"*25)
    
    results = []
    
    # Teste 1: Conexão
    result = test_connection()
    results.append(("Conexão API", result))
    
    if not result:
        print("\n⚠️  Pare aqui! Configure o GITHUB_TOKEN primeiro.")
        sys.exit(1)
    
    # Teste 2: Coleta
    result, data = test_data_collection()
    results.append(("Coleta de Dados", result))
    
    # Teste 3: Processamento
    if result and data:
        result, processed = test_processing(data)
        results.append(("Processamento", result))
    else:
        processed = None
    
    # Teste 4: Geração
    if processed:
        result = test_readme_generation(processed)
        results.append(("Geração README", result))
    
    # Resumo
    print("\n" + "="*50)
    print("📊 RESUMO DOS TESTES")
    print("="*50)
    
    for name, success in results:
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"{status} - {name}")
    
    all_passed = all(r[1] for r in results)
    
    if all_passed:
        print("\n🎉 Todos os testes passaram!")
        print("✅ Sistema pronto para uso!")
        print("\n💡 Próximos passos:")
        print("   1. Execute: python src/scripts/daily_metrics.py")
        print("   2. Configure no GitHub Actions")
        print("   3. Veja o SETUP.md para mais detalhes")
    else:
        print("\n⚠️  Alguns testes falharam")
        print("💡 Revise os erros acima e tente novamente")
    
    print("\n" + "="*50)


if __name__ == '__main__':
    main()
