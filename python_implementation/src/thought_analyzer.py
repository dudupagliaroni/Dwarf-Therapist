#!/usr/bin/env python3
"""
THOUGHT ANALYZER - Analisador de Tipos de Pensamentos
=====================================================

Analisa o arquivo game_data.ini para extrair e catalogar todos os tipos de thoughts
(pensamentos) disponíveis no Dwarf Therapist/Dwarf Fortress.

Thought_id no offset 0x000c corresponde aos IDs dos pensamentos catalogados aqui.
"""

import os
import sys
import json
import configparser
from datetime import datetime

class ThoughtAnalyzer:
    def __init__(self, base_path):
        self.base_path = base_path
        self.game_data_file = os.path.join(base_path, "resources", "game_data.ini")
        self.thoughts = {}
        self.subthoughts = {}
        
    def analyze_thoughts(self):
        """Analisa todos os thoughts no game_data.ini"""
        print("🧠 Analisando types de thoughts...")
        
        if not os.path.exists(self.game_data_file):
            print(f"❌ Arquivo não encontrado: {self.game_data_file}")
            return
        
        config = configparser.ConfigParser()
        config.read(self.game_data_file, encoding='utf-8')
        
        # Analisa thoughts principais
        if 'unit_thoughts' in config.sections():
            self.parse_unit_thoughts(config['unit_thoughts'])
        
        # Analisa subthoughts
        if 'unit_subthoughts' in config.sections():
            self.parse_unit_subthoughts(config['unit_subthoughts'])
            
        print(f"📊 {len(self.thoughts)} thoughts principais encontrados")
        print(f"📊 {len(self.subthoughts)} grupos de subthoughts encontrados")
    
    def parse_unit_thoughts(self, section):
        """Parse da seção unit_thoughts"""
        size = int(section.get('size', 0))
        print(f"📏 Size oficial dos thoughts: {size}")
        
        for key, value in section.items():
            if '/' in key:
                parts = key.split('/')
                if len(parts) == 2:
                    thought_id = int(parts[0])
                    field = parts[1]
                    
                    if thought_id not in self.thoughts:
                        self.thoughts[thought_id] = {
                            'id': thought_id,
                            'title': '',
                            'thought': '',
                            'subthoughts_type': None
                        }
                    
                    if field == 'title':
                        self.thoughts[thought_id]['title'] = value
                    elif field == 'thought':
                        self.thoughts[thought_id]['thought'] = value
                    elif field == 'subthoughts_type':
                        self.thoughts[thought_id]['subthoughts_type'] = int(value)
    
    def parse_unit_subthoughts(self, section):
        """Parse da seção unit_subthoughts"""
        size = int(section.get('size', 0))
        print(f"📏 Size oficial dos subthoughts: {size}")
        
        # Estrutura mais complexa para subthoughts
        current_group = None
        
        for key, value in section.items():
            if '/' in key:
                parts = key.split('/')
                if len(parts) >= 2:
                    group_id = int(parts[0])
                    
                    if group_id not in self.subthoughts:
                        self.subthoughts[group_id] = {
                            'id': group_id,
                            'subthoughts': {}
                        }
                    
                    if parts[1] == 'id':
                        self.subthoughts[group_id]['group_id'] = int(value)
                    elif len(parts) >= 4 and parts[1] == 'subthoughts':
                        sub_id = int(parts[2])
                        field = parts[3]
                        
                        if sub_id not in self.subthoughts[group_id]['subthoughts']:
                            self.subthoughts[group_id]['subthoughts'][sub_id] = {}
                        
                        if field == 'id':
                            self.subthoughts[group_id]['subthoughts'][sub_id]['id'] = int(value)
                        elif field == 'thought':
                            self.subthoughts[group_id]['subthoughts'][sub_id]['thought'] = value
    
    def generate_statistics(self):
        """Gera estatísticas dos thoughts"""
        stats = {
            'total_thoughts': len(self.thoughts),
            'total_subthought_groups': len(self.subthoughts),
            'thoughts_with_subthoughts': 0,
            'thoughts_by_category': {},
            'max_thought_id': 0,
            'min_thought_id': float('inf')
        }
        
        # Calcula estatísticas
        for thought_id, thought in self.thoughts.items():
            if thought['subthoughts_type'] is not None:
                stats['thoughts_with_subthoughts'] += 1
            
            stats['max_thought_id'] = max(stats['max_thought_id'], thought_id)
            stats['min_thought_id'] = min(stats['min_thought_id'], thought_id)
            
            # Categoriza por palavras-chave no título
            title = thought['title'].lower()
            if 'death' in title or 'killed' in title or 'murder' in title:
                category = 'Death/Violence'
            elif 'clothing' in title or 'clothes' in title:
                category = 'Clothing'
            elif 'meal' in title or 'drink' in title or 'food' in title or 'hunger' in title or 'thirst' in title:
                category = 'Food/Drink'
            elif 'sleep' in title or 'bedroom' in title or 'drowsy' in title:
                category = 'Sleep/Rest'
            elif 'social' in title or 'friend' in title or 'romance' in title or 'love' in title or 'talk' in title:
                category = 'Social'
            elif 'military' in title or 'squad' in title or 'spar' in title or 'patrol' in title:
                category = 'Military'
            elif 'nobility' in title or 'leader' in title or 'mandate' in title or 'tax' in title:
                category = 'Nobility/Politics'
            elif 'craft' in title or 'masterwork' in title or 'artifact' in title or 'skill' in title:
                category = 'Work/Skills'
            elif 'weather' in title or 'rain' in title or 'snow' in title or 'sun' in title:
                category = 'Weather/Environment'
            elif 'injur' in title or 'wound' in title or 'pain' in title or 'health' in title:
                category = 'Health/Injuries'
            elif 'ghost' in title or 'vampire' in title or 'curse' in title or 'syndrome' in title:
                category = 'Supernatural'
            elif 'learning' in title or 'teaching' in title or 'read' in title or 'research' in title:
                category = 'Learning/Knowledge'
            elif 'performance' in title or 'music' in title or 'dance' in title or 'art' in title:
                category = 'Arts/Performance'
            else:
                category = 'Other'
            
            if category not in stats['thoughts_by_category']:
                stats['thoughts_by_category'][category] = 0
            stats['thoughts_by_category'][category] += 1
        
        return stats
    
    def export_analysis(self):
        """Exporta análise completa"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Gera estatísticas
        stats = self.generate_statistics()
        
        # Dados para exportação
        export_data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'description': 'Análise completa de tipos de thoughts do Dwarf Therapist',
                'source_file': self.game_data_file
            },
            'statistics': stats,
            'thoughts': self.thoughts,
            'subthoughts': self.subthoughts
        }
        
        # Exporta JSON
        json_file = os.path.join(self.base_path, "python_implementation", "exports", f"thoughts_analysis_{timestamp}.json")
        os.makedirs(os.path.dirname(json_file), exist_ok=True)
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        # Gera relatório markdown
        md_file = self.generate_markdown_report(stats, timestamp)
        
        return json_file, md_file
    
    def generate_markdown_report(self, stats, timestamp):
        """Gera relatório em markdown"""
        md_file = os.path.join(self.base_path, f"ANALISE_THOUGHTS_{timestamp}.md")
        
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write("# Análise de Types de Thoughts - Dwarf Therapist\n\n")
            f.write(f"**Gerado em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## 📊 Estatísticas Gerais\n\n")
            f.write(f"- **Total de thoughts:** {stats['total_thoughts']}\n")
            f.write(f"- **Thoughts com subthoughts:** {stats['thoughts_with_subthoughts']}\n")
            f.write(f"- **Grupos de subthoughts:** {stats['total_subthought_groups']}\n")
            f.write(f"- **ID mínimo:** {stats['min_thought_id']}\n")
            f.write(f"- **ID máximo:** {stats['max_thought_id']}\n\n")
            
            f.write("## 📋 Thoughts por Categoria\n\n")
            for category, count in sorted(stats['thoughts_by_category'].items(), key=lambda x: x[1], reverse=True):
                f.write(f"- **{category}:** {count} thoughts\n")
            f.write("\n")
            
            f.write("## 🧠 Lista Completa de Thoughts\n\n")
            f.write("| ID | Título | Descrição | Subthoughts |\n")
            f.write("|----|--------|-----------|-------------|\n")
            
            for thought_id in sorted(self.thoughts.keys()):
                thought = self.thoughts[thought_id]
                subthoughts = "Sim" if thought['subthoughts_type'] is not None else "Não"
                title = thought['title'].replace('|', '\\|')
                description = thought['thought'].replace('|', '\\|')
                f.write(f"| {thought_id} | {title} | {description} | {subthoughts} |\n")
            
            f.write("\n## 🔧 Offset thought_id (0x000c)\n\n")
            f.write("O offset `thought_id` em `0x000c` nas emoções corresponde aos IDs listados acima.\n")
            f.write("Este campo é um inteiro de 4 bytes que identifica o tipo específico de pensamento.\n\n")
            f.write("**Exemplos de uso:**\n")
            f.write("- ID 1: Conflict (conflito)\n")
            f.write("- ID 10: Crafted Masterwork (criou obra-prima)\n")
            f.write("- ID 32: Death (Pet) (morte de animal de estimação)\n")
            f.write("- ID 98: Meal (refeição de qualidade)\n")
            f.write("- ID 280: Commune Dedicated Temple (comunhão em templo dedicado)\n\n")
            
            if self.subthoughts:
                f.write("## 🔍 Subthoughts\n\n")
                f.write("Alguns thoughts possuem subthoughts que fornecem detalhes adicionais:\n\n")
                
                for group_id in sorted(self.subthoughts.keys()):
                    group = self.subthoughts[group_id]
                    f.write(f"### Grupo {group_id}\n\n")
                    if 'subthoughts' in group:
                        for sub_id in sorted(group['subthoughts'].keys()):
                            sub = group['subthoughts'][sub_id]
                            f.write(f"- **ID {sub.get('id', 'N/A')}:** {sub.get('thought', 'N/A')}\n")
                        f.write("\n")
        
        return md_file

def main():
    # Configuração
    base_path = r"C:\Users\Eduardo\Documents\projetinhos\Dwarf-Therapist"
    
    print("=" * 60)
    print("THOUGHT ANALYZER")
    print("=" * 60)
    print()
    print("Analisando todos os tipos de thoughts disponíveis...")
    print()
    
    # Inicializa analisador
    analyzer = ThoughtAnalyzer(base_path)
    
    # Analisa thoughts
    analyzer.analyze_thoughts()
    
    # Exporta análise
    json_file, md_file = analyzer.export_analysis()
    
    print()
    print("=" * 60)
    print("ANÁLISE CONCLUÍDA")
    print("=" * 60)
    print()
    print(f"📊 RESUMO:")
    print(f"   Total de thoughts: {len(analyzer.thoughts)}")
    print(f"   Grupos de subthoughts: {len(analyzer.subthoughts)}")
    print(f"   Range de IDs: {min(analyzer.thoughts.keys())} - {max(analyzer.thoughts.keys())}")
    print()
    print(f"📁 ARQUIVOS GERADOS:")
    print(f"   JSON: {json_file}")
    print(f"   Markdown: {md_file}")
    print()
    print("🔧 OFFSET RELEVANTE:")
    print("   thought_id = 0x000c (4 bytes)")
    print("   Tipo: int32")
    print("   Significado: ID do tipo de pensamento (1-280)")
    print()

if __name__ == "__main__":
    main()