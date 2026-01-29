"""
Career Timeline Generator - Timeline profissional elegante

Cria uma timeline horizontal de 1200px com:
- Experiências profissionais
- Educação
- Certificações
- Controle de privacidade (ocultar datas, duração, etc)
- Visual moderno com animações
"""

import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
from dateutil.relativedelta import relativedelta


class CareerTimelineGenerator:
    """Gerador de timeline de carreira."""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.theme = self._load_theme()
        self.career_data = self._load_career_data()
        self.output_dir = self.base_path / "assets"
        self.output_dir.mkdir(exist_ok=True)
        
    def _load_theme(self, theme_name: str = "dark") -> Dict[str, Any]:
        theme_path = self.base_path / "themes" / f"{theme_name}.json"
        with open(theme_path, 'r') as f:
            return json.load(f)
    
    def _load_career_data(self) -> Dict[str, Any]:
        """Carrega dados de carreira."""
        career_path = self.base_path / "data" / "career.json"
        if career_path.exists():
            with open(career_path, 'r') as f:
                return json.load(f)
        return {"professional_timeline": [], "certifications": []}
    
    def _parse_date(self, date_str: str) -> datetime:
        """Parse date string."""
        if date_str.lower() == "present":
            return datetime.now()
        return datetime.strptime(date_str, "%Y-%m")
    
    def _format_date(self, date_str: str, mode: str = "month_year") -> str:
        """Formata data baseado no modo de privacidade."""
        if date_str.lower() == "present":
            return "Present"
        
        date = self._parse_date(date_str)
        
        if mode == "year_only":
            return date.strftime("%Y")
        elif mode == "month_year":
            return date.strftime("%b %Y")
        elif mode == "hidden":
            return "•••"
        
        return date.strftime("%b %Y")
    
    def _calculate_duration(self, start: str, end: str) -> str:
        """Calcula duração entre datas."""
        start_date = self._parse_date(start)
        end_date = self._parse_date(end)
        
        delta = relativedelta(end_date, start_date)
        
        years = delta.years
        months = delta.months
        
        parts = []
        if years > 0:
            parts.append(f"{years}y")
        if months > 0:
            parts.append(f"{months}m")
        
        return " ".join(parts) if parts else "< 1m"
    
    def _create_styles(self) -> str:
        """Estilos CSS para timeline."""
        return f"""
        * {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica', 'Arial', sans-serif;
        }}
        text {{ fill: {self.theme['colors']['text']}; }}
        .title {{ 
            font-size: 24px; 
            font-weight: 700; 
            fill: {self.theme['colors']['accent']}; 
        }}
        .subtitle {{ 
            font-size: 14px; 
            fill: {self.theme['colors']['textSecondary']}; 
        }}
        .entry-title {{
            font-size: 15px;
            font-weight: 600;
            fill: {self.theme['colors']['text']};
        }}
        .entry-company {{
            font-size: 13px;
            font-weight: 500;
        }}
        .entry-date {{
            font-size: 11px;
            fill: {self.theme['colors']['textSecondary']};
        }}
        .entry-desc {{
            font-size: 11px;
            fill: {self.theme['colors']['textMuted']};
        }}
        .label-small {{
            font-size: 9px;
            fill: {self.theme['colors']['textSecondary']};
        }}
        .tech-badge {{
            font-size: 9px;
            font-weight: 600;
            fill: {self.theme['colors']['accent']};
        }}
        .timeline-line {{
            stroke: {self.theme['colors']['border']};
            stroke-width: 3;
        }}
        .timeline-dot {{
            fill: {self.theme['colors']['accent']};
        }}
        .timeline-dot-work {{
            fill: {self.theme['colors']['success']};
        }}
        .timeline-dot-education {{
            fill: {self.theme['colors']['purple']};
        }}
        .timeline-dot-current {{
            fill: {self.theme['colors']['warning']};
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        @keyframes slideIn {{
            from {{ transform: translateX(-20px); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}
        .animated {{ animation: fadeIn 0.6s ease-out; }}
        .slide-in {{ animation: slideIn 0.5s ease-out; }}
        .pulse {{ animation: pulse 2s ease-in-out infinite; }}
        .cert-badge {{
            font-size: 11px;
            font-weight: 600;
        }}
        """
    
    def generate_timeline(self, output_name: str = "career_timeline.svg") -> str:
        """Gera timeline profissional completa."""
        width, height = 1200, 650  # Aumentado para acomodar cards
        
        timeline_entries = self.career_data.get('professional_timeline', [])
        certifications = self.career_data.get('certifications', [])
        meta = self.career_data.get('meta', {})
        
        # Configurações de privacidade
        date_mode = meta.get('show_dates', 'year_only')
        show_duration = meta.get('show_duration', False)
        
        svg_parts = [f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
    <style>{self._create_styles()}</style>
    <rect width="{width}" height="{height}" fill="{self.theme['colors']['card']}" rx="12"/>
    
    <!-- Header -->
    <text class="title animated" x="40" y="45">💼 Professional Journey</text>
    <text class="subtitle animated" x="40" y="70">Career milestones and achievements</text>
''']
        
        # Timeline horizontal
        timeline_y = 280  # Centralizado verticalmente
        timeline_start_x = 80
        timeline_end_x = width - 80
        
        # Linha da timeline
        svg_parts.append(f'''
    <line class="timeline-line animated" x1="{timeline_start_x}" y1="{timeline_y}" 
          x2="{timeline_end_x}" y2="{timeline_y}" stroke-linecap="round"/>
''')
        
        # Calcular durações e posições proporcionais
        if not timeline_entries:
            svg_parts.append('</svg>')
            output_path = self.output_dir / output_name
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(svg_parts))
            return str(output_path)
        
        # Calcular duração total e individual de cada entry
        entry_durations = []
        total_months = 0
        
        for entry in timeline_entries:
            start = self._parse_date(entry.get('date_start', ''))
            end = self._parse_date(entry.get('date_end', 'present'))
            delta = relativedelta(end, start)
            months = delta.years * 12 + delta.months
            entry_durations.append({
                'entry': entry,
                'months': months,
                'start_date': start
            })
            total_months += months
        
        # Ordenar por data de início (mais antigo primeiro)
        entry_durations.sort(key=lambda x: x['start_date'])
        
        # Calcular posições X baseadas em proporção temporal
        available_width = timeline_end_x - timeline_start_x
        cumulative_months = 0
        
        for i, entry_data in enumerate(entry_durations):
            entry = entry_data['entry']
            months = entry_data['months']
            
            # Posição X proporcional ao tempo acumulado
            # Colocamos o ponto no meio do período
            x_pos = timeline_start_x + (cumulative_months + months / 2) / total_months * available_width
            cumulative_months += months
            
            # Alternar posição (em cima/embaixo da linha)
            is_top = i % 2 == 0
            y_offset = -20 if is_top else 20
            content_y = timeline_y + y_offset + (-180 if is_top else 60)  # Ajustado para mais espaço
            
            # Determinar cor do dot
            entry_type = entry.get('type', 'work')
            is_current = entry.get('date_end', '').lower() == 'present'
            
            if is_current:
                dot_class = 'timeline-dot-current pulse'
                dot_radius = 8
            elif entry_type == 'work':
                dot_class = 'timeline-dot-work'
                dot_radius = 6
            else:
                dot_class = 'timeline-dot-education'
                dot_radius = 6
            
            # Linha conectora
            connector_end_y = content_y + 140 if is_top else content_y - 10  # Ajustado
            svg_parts.append(f'''
    <line class="slide-in" x1="{x_pos}" y1="{timeline_y}" x2="{x_pos}" y2="{connector_end_y}" 
          stroke="{self.theme['colors']['border']}" stroke-width="2" stroke-dasharray="4,4" 
          opacity="0.5" style="animation-delay: {i * 0.15}s"/>
''')
            
            # Dot na timeline
            svg_parts.append(f'''
    <circle class="{dot_class}" cx="{x_pos}" cy="{timeline_y}" r="{dot_radius}" 
            style="animation-delay: {i * 0.15}s"/>
''')
            
            # Card do entry
            card_width = 260  # Aumentado
            card_height = 140  # Aumentado
            card_x = x_pos - card_width / 2
            card_y = content_y
            
            # Cor do card baseada no tipo
            if entry_type == 'work':
                border_color = self.theme['colors']['success']
                type_icon = "💼"
            else:
                border_color = self.theme['colors']['purple']
                type_icon = "🎓"
            
            svg_parts.append(f'''
    <g class="slide-in" style="animation-delay: {i * 0.15}s">
        <rect x="{card_x}" y="{card_y}" width="{card_width}" height="{card_height}" 
              rx="8" fill="{self.theme['colors']['background']}" 
              stroke="{border_color}" stroke-width="2" opacity="0.95"/>
''')
            
            # Conteúdo do card
            text_x = card_x + 12
            text_y = card_y + 22
            
            # Título
            title = entry.get('title', 'Position')
            if len(title) > 28:
                title = title[:25] + "..."
            svg_parts.append(f'''
        <text class="entry-title" x="{text_x}" y="{text_y}">{type_icon} {title}</text>
''')
            
            # Empresa
            company = entry.get('company', 'Company')
            if len(company) > 30:
                company = company[:27] + "..."
            svg_parts.append(f'''
        <text class="entry-company" x="{text_x}" y="{text_y + 18}" fill="{border_color}">{company}</text>
''')
            
            # Datas
            start_date = self._format_date(entry.get('date_start', ''), date_mode)
            end_date = self._format_date(entry.get('date_end', 'present'), date_mode)
            date_text = f"{start_date} - {end_date}"
            
            if show_duration or entry.get('show_duration', False):
                duration = self._calculate_duration(entry.get('date_start', ''), entry.get('date_end', 'present'))
                date_text += f" ({duration})"
            
            svg_parts.append(f'''
        <text class="entry-date" x="{text_x}" y="{text_y + 36}">{date_text}</text>
''')
            
            # Descrição (truncada)
            desc = entry.get('description', '')
            if len(desc) > 38:
                desc = desc[:35] + "..."
            svg_parts.append(f'''
        <text class="entry-desc" x="{text_x}" y="{text_y + 52}">{desc}</text>
''')
            
            # Tecnologias (badges)
            techs = entry.get('technologies', [])[:3]  # Máximo 3
            badge_y = text_y + 70
            badge_x = text_x
            
            for tech in techs:
                tech_width = len(tech) * 6 + 12
                svg_parts.append(f'''
        <rect x="{badge_x}" y="{badge_y}" width="{tech_width}" height="16" 
              rx="8" fill="{border_color}" opacity="0.15"/>
        <text class="tech-badge" x="{badge_x + 6}" y="{badge_y + 11}" fill="{border_color}">{tech}</text>
''')
                badge_x += tech_width + 6
            
            # Indicador de duração (barra proporcional)
            duration_bar_y = text_y + 95
            duration_bar_width = (months / total_months) * (card_width - 24)
            svg_parts.append(f'''
        <rect x="{text_x}" y="{duration_bar_y}" width="{card_width - 24}" height="4" 
              rx="2" fill="{self.theme['colors']['border']}" opacity="0.2"/>
        <rect x="{text_x}" y="{duration_bar_y}" width="{duration_bar_width}" height="4" 
              rx="2" fill="{border_color}" opacity="0.6"/>
        <text class="label-small" x="{text_x}" y="{duration_bar_y + 16}" fill="{border_color}">
            {months} months • {(months/total_months*100):.1f}% of career
        </text>
''')
            
            svg_parts.append('    </g>')
        
        # Certificações (footer)
        if certifications:
            cert_y = height - 100  # Ajustado para nova altura
            svg_parts.append(f'''
    <line x1="80" y1="{cert_y - 10}" x2="{width - 80}" y2="{cert_y - 10}" 
          stroke="{self.theme['colors']['border']}" stroke-width="1" opacity="0.3"/>
    <text class="subtitle animated" x="80" y="{cert_y + 10}">🏆 Certifications</text>
''')
            
            cert_x = 80
            cert_item_y = cert_y + 35
            
            for cert in certifications[:5]:  # Máximo 5 certificações
                if not cert.get('show', True):
                    continue
                
                cert_name = cert.get('name', 'Certification')
                cert_date = self._format_date(cert.get('date', ''), 'year_only')
                
                svg_parts.append(f'''
    <g class="animated">
        <circle cx="{cert_x}" cy="{cert_item_y}" r="4" fill="{self.theme['colors']['warning']}"/>
        <text class="cert-badge" x="{cert_x + 12}" y="{cert_item_y + 4}">{cert_name}</text>
        <text class="entry-date" x="{cert_x + 12}" y="{cert_item_y + 17}">({cert_date})</text>
    </g>
''')
                cert_x += 230  # Reduzido para caber 5
        
        # Adicionar legenda de tempo total no canto
        total_years = total_months / 12
        svg_parts.append(f'''
    <g class="animated">
        <rect x="{width - 220}" y="95" width="180" height="50" rx="8" 
              fill="{self.theme['colors']['background']}" opacity="0.8"/>
        <text class="subtitle" x="{width - 210}" y="115">Total Experience</text>
        <text style="font-size: 20px; font-weight: 700" x="{width - 210}" y="138" 
              fill="{self.theme['colors']['success']}">{total_years:.1f} years</text>
    </g>
''')
        
        svg_parts.append('</svg>')
        
        output_path = self.output_dir / output_name
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(svg_parts))
        
        return str(output_path)
    
    def generate_compact_experience(self, output_name: str = "experience_compact.svg") -> str:
        """Gera versão compacta de experiência (para usar com outros cards)."""
        width, height = 450, 240
        
        timeline_entries = self.career_data.get('professional_timeline', [])
        work_entries = [e for e in timeline_entries if e.get('type') == 'work']
        
        # Calcular total de experiência
        total_months = 0
        for entry in work_entries:
            start = self._parse_date(entry.get('date_start', ''))
            end = self._parse_date(entry.get('date_end', 'present'))
            delta = relativedelta(end, start)
            total_months += delta.years * 12 + delta.months
        
        years = total_months // 12
        months = total_months % 12
        
        svg_content = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
    <style>{self._create_styles()}</style>
    <rect width="{width}" height="{height}" fill="{self.theme['colors']['card']}" rx="12"/>
    
    <text class="title animated" x="24" y="35" style="font-size: 20px">💼 Experience</text>
    <text class="subtitle animated" x="24" y="60">Professional background</text>
    
    <!-- Total Experience -->
    <g class="animated" style="animation-delay: 0.2s">
        <circle cx="80" cy="130" r="50" fill="{self.theme['colors']['success']}" opacity="0.15"/>
        <text style="font-size: 32px; font-weight: 700" x="80" y="135" text-anchor="middle" 
              fill="{self.theme['colors']['success']}">{years}</text>
        <text class="entry-date" x="80" y="155" text-anchor="middle">years</text>
    </g>
    
    <!-- Recent Positions -->
    <g class="slide-in" style="animation-delay: 0.3s">
        <text class="subtitle" x="160" y="100">Current Position</text>
        <text class="entry-title" x="160" y="125" style="font-size: 13px">{work_entries[0].get('title', 'N/A') if work_entries else 'N/A'}</text>
        <text class="entry-company" x="160" y="145" fill="{self.theme['colors']['success']}">{work_entries[0].get('company', 'N/A') if work_entries else 'N/A'}</text>
    </g>
    
    <g class="slide-in" style="animation-delay: 0.4s">
        <text class="subtitle" x="160" y="170">Total Positions</text>
        <text style="font-size: 24px; font-weight: 700" x="160" y="200" fill="{self.theme['colors']['accent']}">{len(work_entries)}</text>
    </g>
</svg>'''
        
        output_path = self.output_dir / output_name
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        return str(output_path)
