#!/usr/bin/env python3
"""
OFFSET DICTIONARY ANALYZER
===========================

Analisa todos os memory layouts do Dwarf Therapist para criar um dicionário 
completo dos offsets e seus significados baseado nos nomes das chaves.

Este script gera uma documentação completa de todos os offsets disponíveis
organizados por categoria (dwarf, squad, item, etc.).
"""

import os
import sys
import json
import configparser
from collections import defaultdict
from datetime import datetime

class OffsetDictionaryAnalyzer:
    def __init__(self, base_path):
        self.base_path = base_path
        self.memory_layouts_path = os.path.join(base_path, "share", "memory_layouts")
        self.offset_dictionary = defaultdict(lambda: defaultdict(dict))
        self.offset_meanings = {}
        
    def analyze_all_layouts(self):
        """Analisa todos os arquivos de memory layout"""
        print("🔍 Analisando memory layouts...")
        
        layouts_found = 0
        for root, dirs, files in os.walk(self.memory_layouts_path):
            for file in files:
                if file.endswith('.ini'):
                    layouts_found += 1
                    file_path = os.path.join(root, file)
                    self.analyze_layout_file(file_path)
        
        print(f"📊 {layouts_found} arquivos de layout analisados")
        
    def analyze_layout_file(self, file_path):
        """Analisa um arquivo de memory layout específico"""
        try:
            config = configparser.ConfigParser()
            config.read(file_path, encoding='utf-8')
            
            # Extrai informações do arquivo
            platform = "unknown"
            version = "unknown"
            
            if "windows" in file_path:
                platform = "windows"
            elif "linux" in file_path:
                platform = "linux"
            elif "osx" in file_path:
                platform = "osx"
                
            filename = os.path.basename(file_path)
            version = filename.replace('.ini', '')
            
            # Analisa cada seção de offsets
            for section_name in config.sections():
                if section_name in ['info', 'valid_flags_1', 'valid_flags_2', 'valid_flags_3', 'invalid_flags_1', 'invalid_flags_2', 'invalid_flags_3']:
                    continue
                    
                section_items = dict(config.items(section_name))
                
                for key, value in section_items.items():
                    # Converte valor hexadecimal se possível
                    try:
                        if value.startswith('0x'):
                            hex_value = value
                            int_value = int(value, 16)
                        else:
                            int_value = int(value)
                            hex_value = f"0x{int_value:04x}"
                    except ValueError:
                        hex_value = value
                        int_value = value
                    
                    # Armazena no dicionário
                    if key not in self.offset_dictionary[section_name]:
                        self.offset_dictionary[section_name][key] = {
                            'hex_value': hex_value,
                            'int_value': int_value,
                            'meaning': self.infer_meaning(section_name, key),
                            'platforms': [platform],
                            'versions': [version]
                        }
                    else:
                        # Adiciona plataforma e versão se não existir
                        if platform not in self.offset_dictionary[section_name][key]['platforms']:
                            self.offset_dictionary[section_name][key]['platforms'].append(platform)
                        if version not in self.offset_dictionary[section_name][key]['versions']:
                            self.offset_dictionary[section_name][key]['versions'].append(version)
                            
        except Exception as e:
            print(f"❌ Erro ao analisar {file_path}: {e}")
    
    def infer_meaning(self, section, key):
        """Infere o significado do offset baseado no nome da chave"""
        
        # Mapeamento conhecido de offsets com significados
        known_meanings = {
            # Dwarf/Unit offsets
            'id': 'ID único da unidade',
            'race': 'ID da raça da criatura',
            'caste': 'ID da casta (sub-raça)',
            'sex': 'Gênero (0=fêmea, 1=macho)',
            'birth_year': 'Ano de nascimento',
            'birth_time': 'Tick de nascimento no ano',
            'name': 'Estrutura do nome da criatura',
            'first_name': 'Primeiro nome',
            'nickname': 'Apelido',
            'last_name': 'Sobrenome',
            'profession_id': 'ID da profissão',
            'current_job': 'Ponteiro para o trabalho atual',
            'mood': 'Estado de humor atual',
            'happiness': 'Nível de felicidade',
            'stress': 'Nível de stress',
            'thoughts': 'Vetor de pensamentos',
            'labors': 'Array de trabalhos habilitados',
            'skills': 'Vetor de habilidades',
            'attributes': 'Vetor de atributos físicos/mentais',
            'physical_attrs': 'Atributos físicos (força, agilidade, etc.)',
            'mental_attrs': 'Atributos mentais (inteligência, foco, etc.)',
            'body_size': 'Tamanho do corpo',
            'size_info': 'Informações de tamanho',
            'curse': 'Informações sobre maldições',
            'squad_id': 'ID do esquadrão militar',
            'squad_position': 'Posição no esquadrão',
            'inventory': 'Vetor de itens no inventário',
            'wounds': 'Vetor de ferimentos',
            'health': 'Informações de saúde',
            'souls': 'Vetor de almas',
            'states': 'Estados especiais (migrante, adaptado caverna)',
            'flags1': 'Flags de estado primárias',
            'flags2': 'Flags de estado secundárias',
            'flags3': 'Flags de estado terciárias',
            'civ': 'ID da civilização',
            'hist_id': 'ID da figura histórica',
            'animal_type': 'Tipo de animal (se for animal)',
            'pet_owner_id': 'ID do dono (se for pet)',
            'meeting': 'Informações de reunião/encontro',
            'counters1': 'Contadores diversos grupo 1',
            'counters2': 'Contadores diversos grupo 2',
            'counters3': 'Contadores diversos grupo 3',
            'turn_count': 'Contador de turnos',
            'blood': 'Nível de sangue',
            'temp_mood': 'Humor temporário',
            
            # World/Global offsets
            'world_data': 'Ponteiro para dados do mundo',
            'current_year': 'Ano atual do jogo',
            'cur_year_tick': 'Tick atual no ano',
            'creature_vector': 'Vetor de todas as criaturas',
            'active_creature_vector': 'Vetor de criaturas ativas',
            'dwarf_race_index': 'Índice da raça dos anões',
            'fortress_entity': 'Entidade da fortaleza',
            'squad_vector': 'Vetor de esquadrões',
            'artifacts_vector': 'Vetor de artefatos',
            'activities_vector': 'Vetor de atividades',
            'historical_entities_vector': 'Vetor de entidades históricas',
            'historical_figures_vector': 'Vetor de figuras históricas',
            'world_site_type': 'Tipo de site mundial',
            'active_sites_vector': 'Vetor de sites ativos',
            
            # Item offsets
            'item_type': 'Tipo do item',
            'item_subtype': 'Subtipo do item',
            'material': 'Material do item',
            'quality': 'Qualidade do item',
            'wear': 'Nível de desgaste',
            'stack_size': 'Tamanho da pilha',
            
            # Squad offsets
            'id': 'ID do esquadrão',
            'name': 'Nome do esquadrão',
            'members': 'Vetor de membros',
            'positions': 'Posições no esquadrão',
            'orders': 'Ordens atuais',
            'uniform': 'Uniforme do esquadrão',
            'alert': 'Estado de alerta',
            
            # Syndrome offsets
            'cie_effects': 'Efeitos da síndrome',
            'cie_end': 'Fim da síndrome',
            'syn_classes': 'Classes da síndrome',
            
            # Emotion offsets
            'type': 'Tipo da emoção',
            'strength': 'Intensidade da emoção',
            'year': 'Ano da emoção',
            'target': 'Alvo da emoção',
            
            # Activity offsets
            'type': 'Tipo da atividade',
            'participants': 'Participantes da atividade',
            
            # Wound offsets
            'parts': 'Partes do corpo afetadas',
            'layer': 'Camada afetada',
            'bleeding': 'Estado de sangramento',
            'infection': 'Estado de infecção',
            'pain': 'Nível de dor',
            
            # Need offsets
            'id': 'ID da necessidade',
            'level': 'Nível da necessidade',
            'focus': 'Foco da necessidade',
        }
        
        # Busca significado conhecido
        if key in known_meanings:
            return known_meanings[key]
        
        # Inferência baseada em padrões
        if 'vector' in key:
            return f"Vetor de {key.replace('_vector', '').replace('_', ' ')}"
        elif 'offset' in key:
            return f"Offset para {key.replace('_offset', '').replace('_', ' ')}"
        elif 'addr' in key or 'address' in key:
            return f"Endereço de {key.replace('_addr', '').replace('_address', '').replace('_', ' ')}"
        elif 'count' in key:
            return f"Contador de {key.replace('_count', '').replace('_', ' ')}"
        elif 'size' in key:
            return f"Tamanho de {key.replace('_size', '').replace('_', ' ')}"
        elif 'flag' in key:
            return f"Flag de {key.replace('_flag', '').replace('_', ' ')}"
        elif 'id' in key:
            return f"ID de {key.replace('_id', '').replace('_', ' ')}"
        elif 'year' in key:
            return f"Ano de {key.replace('_year', '').replace('_', ' ')}"
        elif 'time' in key:
            return f"Tempo de {key.replace('_time', '').replace('_', ' ')}"
        elif key.endswith('_x') or key.endswith('_y') or key.endswith('_z'):
            return f"Coordenada {key[-1].upper()} de {key[:-2].replace('_', ' ')}"
        else:
            return f"Campo {key.replace('_', ' ')}"
    
    def generate_category_descriptions(self):
        """Gera descrições das categorias de offset"""
        return {
            'addresses': 'Endereços globais do jogo (ponteiros para estruturas principais)',
            'dwarf_offsets': 'Offsets para dados de unidades/criaturas (anões, animais, invasores)',
            'squad_offsets': 'Offsets para dados de esquadrões militares',
            'word_offsets': 'Offsets para estruturas de palavras e linguagem',
            'race_offsets': 'Offsets para dados de raças (anão, elfo, humano, etc.)',
            'caste_offsets': 'Offsets para dados de castas (subtipos de raça)',
            'hist_figure_offsets': 'Offsets para figuras históricas',
            'hist_event_offsets': 'Offsets para eventos históricos',
            'hist_entity_offsets': 'Offsets para entidades históricas (civilizações)',
            'item_offsets': 'Offsets para itens genéricos',
            'weapon_subtype_offsets': 'Offsets para subtipos de armas',
            'armor_subtype_offsets': 'Offsets para subtipos de armaduras',
            'material_offsets': 'Offsets para dados de materiais',
            'plant_offsets': 'Offsets para dados de plantas',
            'syndrome_offsets': 'Offsets para síndromes (doenças, maldições)',
            'emotion_offsets': 'Offsets para estados emocionais',
            'activity_offsets': 'Offsets para atividades das unidades',
            'health_offsets': 'Offsets para informações de saúde',
            'unit_wound_offsets': 'Offsets para ferimentos de unidades',
            'general_ref_offsets': 'Offsets para referências gerais',
            'art_offsets': 'Offsets para objetos de arte',
            'job_details': 'Offsets para trabalhos/tarefas',
            'soul_details': 'Offsets para dados da alma',
            'need_offsets': 'Offsets para necessidades das unidades',
            'viewscreen_offsets': 'Offsets para telas do jogo',
            'offsets': 'Offsets diversos de linguagem'
        }
    
    def export_dictionary(self):
        """Exporta o dicionário completo para JSON"""
        export_data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'description': 'Dicionário completo de offsets do Dwarf Therapist',
                'total_sections': len(self.offset_dictionary),
                'total_offsets': sum(len(section) for section in self.offset_dictionary.values())
            },
            'category_descriptions': self.generate_category_descriptions(),
            'sections': dict(self.offset_dictionary)
        }
        
        # Calcula estatísticas por seção
        section_stats = {}
        for section_name, offsets in self.offset_dictionary.items():
            section_stats[section_name] = {
                'total_offsets': len(offsets),
                'platforms': set(),
                'versions': set()
            }
            
            for offset_data in offsets.values():
                section_stats[section_name]['platforms'].update(offset_data['platforms'])
                section_stats[section_name]['versions'].update(offset_data['versions'])
            
            # Converte sets para listas para JSON
            section_stats[section_name]['platforms'] = list(section_stats[section_name]['platforms'])
            section_stats[section_name]['versions'] = list(section_stats[section_name]['versions'])
        
        export_data['section_statistics'] = section_stats
        
        # Exporta para arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_file = os.path.join(self.base_path, "python_implementation", "exports", f"offset_dictionary_{timestamp}.json")
        
        os.makedirs(os.path.dirname(export_file), exist_ok=True)
        
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"📁 Dicionário exportado para: {export_file}")
        return export_file
    
    def generate_markdown_report(self, json_file):
        """Gera relatório em markdown"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        md_file = os.path.join(self.base_path, f"DICIONARIO_OFFSETS_{timestamp}.md")
        
        category_descriptions = self.generate_category_descriptions()
        
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write("# Dicionário de Offsets - Dwarf Therapist\n\n")
            f.write(f"**Gerado em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Total de seções:** {len(self.offset_dictionary)}\n")
            f.write(f"**Total de offsets:** {sum(len(section) for section in self.offset_dictionary.values())}\n\n")
            
            f.write("## 📋 Índice\n\n")
            for section_name in sorted(self.offset_dictionary.keys()):
                count = len(self.offset_dictionary[section_name])
                f.write(f"- [{section_name}](#{section_name.replace('_', '-')}) ({count} offsets)\n")
            f.write("\n")
            
            f.write("## 📖 Descrição das Categorias\n\n")
            for section_name, description in category_descriptions.items():
                if section_name in self.offset_dictionary:
                    f.write(f"**{section_name}:** {description}\n\n")
            
            f.write("## 🔧 Seções de Offsets\n\n")
            
            for section_name in sorted(self.offset_dictionary.keys()):
                section = self.offset_dictionary[section_name]
                f.write(f"### {section_name}\n\n")
                
                if section_name in category_descriptions:
                    f.write(f"**Descrição:** {category_descriptions[section_name]}\n\n")
                
                f.write(f"**Total de offsets:** {len(section)}\n\n")
                
                f.write("| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |\n")
                f.write("|--------|-------------|-------------|-------------|-------------|---------|\n")
                
                for key in sorted(section.keys()):
                    data = section[key]
                    platforms = ", ".join(data['platforms'][:3])  # Limita para 3 plataformas
                    if len(data['platforms']) > 3:
                        platforms += "..."
                    
                    versions = ", ".join(data['versions'][:2])  # Limita para 2 versões
                    if len(data['versions']) > 2:
                        versions += "..."
                    
                    f.write(f"| `{key}` | `{data['hex_value']}` | {data['int_value']} | {data['meaning']} | {platforms} | {versions} |\n")
                
                f.write("\n---\n\n")
        
        print(f"📄 Relatório markdown gerado: {md_file}")
        return md_file

def main():
    # Configuração
    base_path = r"C:\Users\Eduardo\Documents\projetinhos\Dwarf-Therapist"
    
    print("=" * 60)
    print("OFFSET DICTIONARY ANALYZER")
    print("=" * 60)
    print()
    print("Criando dicionário completo de offsets do Dwarf Therapist...")
    print()
    
    # Inicializa analisador
    analyzer = OffsetDictionaryAnalyzer(base_path)
    
    # Analisa todos os layouts
    analyzer.analyze_all_layouts()
    
    # Exporta dicionário
    json_file = analyzer.export_dictionary()
    
    # Gera relatório markdown
    md_file = analyzer.generate_markdown_report(json_file)
    
    print()
    print("=" * 60)
    print("ANÁLISE CONCLUÍDA")
    print("=" * 60)
    print()
    print(f"📊 RESUMO:")
    print(f"   Total de seções: {len(analyzer.offset_dictionary)}")
    print(f"   Total de offsets: {sum(len(section) for section in analyzer.offset_dictionary.values())}")
    print()
    print(f"📁 ARQUIVOS GERADOS:")
    print(f"   JSON: {json_file}")
    print(f"   Markdown: {md_file}")
    print()

if __name__ == "__main__":
    main()