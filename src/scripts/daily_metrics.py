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
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Adiciona o diretório src ao path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from collectors.github_collector import GitHubCollector
from processors.metrics_processor import MetricsProcessor
from processors.rankings_processor import RankingsProcessor
from generators.readme_generator import ReadmeGenerator
from generators.chart_generator import ChartGenerator


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
    Main function that executes the daily pipeline.
    
    PIPELINE:
    1. Setup and validation
    2. Data collection
    3. Processing
    4. Output generation
    5. File updates
    """
    print("🚀 Starting daily metrics collection...")
    print(f"⏰ Timestamp: {datetime.now(timezone.utc).isoformat()}")
    
    # 1. SETUP
    # Get token from environment (configured in GitHub Actions)
    token = os.environ.get('GH_TOKEN')
    if not token:
        print("❌ ERROR: GH_TOKEN not found in environment variables")
        print("💡 Tip: Configure the token in repository secrets")
        sys.exit(1)
    
    # Get README path (profile repo or local)
    readme_path_env = os.environ.get('PROFILE_README_PATH')
    
    # Define file paths
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / 'data'
    
    if readme_path_env:
        readme_path = Path(readme_path_env)
        print(f"📄 Using profile README: {readme_path}")
    else:
        readme_path = project_root / 'README.md'
        print(f"📄 Using local README: {readme_path}")
    
    # 2. DATA COLLECTION
    print("\n📡 Collecting data from GitHub...")
    
    try:
        collector = GitHubCollector(token)
        
        # Check rate limit before starting (optional, doesn't fail on error)
        try:
            rate_limit = collector.get_rate_limit_info()
            remaining = rate_limit['core']['remaining']
            limit = rate_limit['core']['limit']
            print(f"   Rate limit: {remaining}/{limit}")
        except Exception as e:
            print(f"   ⚠️  Rate limit info unavailable: {e}")
            print(f"   ➡️  Continuing collection anyway...")
        
        # Collect data from last 30 days
        since = datetime.now(timezone.utc) - timedelta(days=30)
        
        print("   - Collecting repositories...")
        repos = collector.collect_all_repos()
        print(f"   ✅ {len(repos)} repositories found")
        
        print("   - Collecting commits...")
        commits = collector.collect_commits(since=since)
        print(f"   ✅ {len(commits)} commits collected")
        
        print("   - Collecting pull requests...")
        prs = collector.collect_pull_requests(since=since)
        print(f"   ✅ {len(prs)} PRs collected")
        
        print("   - Collecting issues...")
        issues = collector.collect_issues(since=since)
        print(f"   ✅ {len(issues)} issues collected")
        
    except Exception as e:
        print(f"❌ Error collecting data: {e}")
        sys.exit(1)
    
    # 3. PROCESSING
    print("\n⚙️  Processing metrics...")
    
    try:
        # Process metrics
        metrics_processor = MetricsProcessor(repos, commits, prs, issues)
        metrics = metrics_processor.generate_metrics()
        print("   ✅ Metrics calculated")
        
        # Process rankings
        rankings_processor = RankingsProcessor(repos, commits, prs, issues)
        rankings = rankings_processor.generate_rankings()
        print("   ✅ Rankings generated")
        
    except Exception as e:
        print(f"❌ Error processing data: {e}")
        sys.exit(1)
    
    # 4. DATA SAVING
    print("\n💾 Saving data...")
    
    try:
        save_json(str(data_dir / 'metrics.json'), metrics)
        print("   ✅ metrics.json saved")
        
        save_json(str(data_dir / 'rankings.json'), rankings)
        print("   ✅ rankings.json saved")
        
    except Exception as e:
        print(f"❌ Error saving data: {e}")
        sys.exit(1)
    
    # 4.5 GENERATE CHARTS
    print("\n🎨 Generating visualizations...")
    
    try:
        # Create assets directory for charts
        assets_dir = readme_path.parent / 'assets' if readme_path_env else project_root / 'assets'
        chart_generator = ChartGenerator(metrics, rankings, str(assets_dir))
        charts = chart_generator.generate_all_charts()
        print(f"   ✅ Generated {len(charts)} visualizations")
        
    except Exception as e:
        print(f"⚠️  Warning: Could not generate charts: {e}")
        charts = {}
    
    # 5. README UPDATE
    print("\n📝 Updating README...")
    
    try:
        generator = ReadmeGenerator(metrics, rankings)
        success = generator.update_readme(str(readme_path))
        
        if success:
            print(f"   ✅ README updated successfully: {readme_path}")
        else:
            print(f"   ⚠️  README was not updated")
            
    except Exception as e:
        print(f"❌ Error updating README: {e}")
        sys.exit(1)
    
    # 6. FINAL SUMMARY
    print("\n" + "="*50)
    print("✨ Execution completed successfully!")
    print("="*50)
    print(f"\n📊 Summary:")
    print(f"   - {len(repos)} repositories")
    print(f"   - {len(commits)} commits")
    print(f"   - {len(prs)} PRs")
    print(f"   - {len(issues)} issues")
    print(f"   - Streak: {metrics['activity_streak']['current']} days")
    print(f"\n💾 Data saved in: {data_dir}")
    print(f"📝 README updated: {readme_path}")
    print("\n🎉 All done!")


if __name__ == '__main__':
    main()
