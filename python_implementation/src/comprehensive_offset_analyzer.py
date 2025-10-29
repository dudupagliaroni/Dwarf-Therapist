#!/usr/bin/env python3
"""
COMPREHENSIVE OFFSET ANALYZER
=============================

Analisa todos os offsets do Dwarf Therapist e explora as possibilidades dentro de cada offset,
incluindo enums, valores possíveis, estruturas relacionadas e exemplos de uso.

Este script gera um relatório ampliado com detalhes completos de cada offset.
"""

import os
import sys
import json
import configparser
import re
from collections import defaultdict
from datetime import datetime

class ComprehensiveOffsetAnalyzer:
    def __init__(self, base_path):
        self.base_path = base_path
        self.memory_layouts_path = os.path.join(base_path, "share", "memory_layouts")
        self.game_data_file = os.path.join(base_path, "resources", "game_data.ini")
        self.src_path = os.path.join(base_path, "src")
        
        # Estruturas de dados
        self.offset_dictionary = defaultdict(lambda: defaultdict(dict))
        self.enums = {}
        self.game_data = {}
        self.code_usage = defaultdict(list)
        self.offset_relationships = defaultdict(list)
        
    def analyze_comprehensive(self):
        """Análise completa de todos os offsets e suas possibilidades"""
        print("🔍 Iniciando análise comprehensiva...")
        
        # 1. Analisa memory layouts básicos
        self.analyze_memory_layouts()
        
        # 2. Analisa game_data.ini para valores possíveis
        self.analyze_game_data()
        
        # 3. Analisa código fonte para enums e constantes
        self.analyze_source_code()
        
        # 4. Analisa relacionamentos entre offsets
        self.analyze_offset_relationships()
        
        print(f"📊 Análise concluída:")
        print(f"   Offsets: {sum(len(section) for section in self.offset_dictionary.values())}")
        print(f"   Enums: {len(self.enums)}")
        print(f"   Seções de game data: {len(self.game_data)}")
    
    def analyze_memory_layouts(self):
        """Analisa os memory layouts básicos"""
        print("📂 Analisando memory layouts...")
        
        for root, dirs, files in os.walk(self.memory_layouts_path):
            for file in files:
                if file.endswith('.ini'):
                    file_path = os.path.join(root, file)
                    self.parse_layout_file(file_path)
    
    def parse_layout_file(self, file_path):
        """Parse de um arquivo de layout específico"""
        try:
            config = configparser.ConfigParser(interpolation=None)
            config.read(file_path, encoding='utf-8')
            
            platform = "unknown"
            if "windows" in file_path:
                platform = "windows"
            elif "linux" in file_path:
                platform = "linux"
            elif "osx" in file_path:
                platform = "osx"
                
            filename = os.path.basename(file_path)
            version = filename.replace('.ini', '')
            
            for section_name in config.sections():
                if section_name in ['info', 'valid_flags_1', 'valid_flags_2', 'valid_flags_3', 'invalid_flags_1', 'invalid_flags_2', 'invalid_flags_3']:
                    continue
                    
                section_items = dict(config.items(section_name))
                
                for key, value in section_items.items():
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
                    
                    if key not in self.offset_dictionary[section_name]:
                        self.offset_dictionary[section_name][key] = {
                            'hex_value': hex_value,
                            'int_value': int_value,
                            'meaning': self.infer_meaning(section_name, key),
                            'platforms': [platform],
                            'versions': [version],
                            'possible_values': [],
                            'related_enums': [],
                            'data_type': self.infer_data_type(section_name, key),
                            'size_bytes': self.infer_size(section_name, key),
                            'examples': [],
                            'relationships': []
                        }
                    else:
                        if platform not in self.offset_dictionary[section_name][key]['platforms']:
                            self.offset_dictionary[section_name][key]['platforms'].append(platform)
                        if version not in self.offset_dictionary[section_name][key]['versions']:
                            self.offset_dictionary[section_name][key]['versions'].append(version)
                            
        except Exception as e:
            print(f"❌ Erro ao analisar {file_path}: {e}")
    
    def analyze_game_data(self):
        """Analisa game_data.ini para valores possíveis"""
        print("🎮 Analisando game_data.ini...")
        
        if not os.path.exists(self.game_data_file):
            return
        
        config = configparser.ConfigParser(interpolation=None)
        config.read(self.game_data_file, encoding='utf-8')
        
        for section_name in config.sections():
            self.game_data[section_name] = dict(config.items(section_name))
            
            # Analisa seções específicas para valores de offsets
            if section_name == 'professions':
                self.analyze_professions(config[section_name])
            elif section_name == 'attributes':
                self.analyze_attributes(config[section_name])
            elif section_name == 'skills':
                self.analyze_skills(config[section_name])
            elif section_name == 'labors':
                self.analyze_labors(config[section_name])
            elif section_name == 'unit_thoughts':
                self.analyze_thoughts(config[section_name])
            elif section_name == 'moods':
                self.analyze_moods(config[section_name])
            elif section_name == 'races':
                self.analyze_races(config[section_name])
    
    def analyze_professions(self, section):
        """Analisa profissões possíveis"""
        professions = {}
        for key, value in section.items():
            if '/' in key:
                parts = key.split('/')
                if len(parts) == 2:
                    prof_id = int(parts[0])
                    field = parts[1]
                    
                    if prof_id not in professions:
                        professions[prof_id] = {}
                    
                    if field == 'name':
                        professions[prof_id]['name'] = value
                    elif field == 'id':
                        professions[prof_id]['game_id'] = int(value)
        
        # Associa com offsets relacionados
        if 'dwarf_offsets' in self.offset_dictionary:
            if 'profession' in self.offset_dictionary['dwarf_offsets']:
                self.offset_dictionary['dwarf_offsets']['profession']['possible_values'] = [
                    f"{prof_id}: {data.get('name', 'Unknown')}" for prof_id, data in professions.items()
                ]
                self.offset_dictionary['dwarf_offsets']['profession']['data_type'] = 'uint32 (profession_id)'
                self.offset_dictionary['dwarf_offsets']['profession']['examples'] = [
                    "0: Miner", "1: Woodworker", "2: Carpenter", "10: Ranger", "22: Gem Cutter"
                ]
    
    def analyze_attributes(self, section):
        """Analisa atributos físicos/mentais"""
        attributes = {}
        for key, value in section.items():
            if '/' in key:
                parts = key.split('/')
                if len(parts) == 2:
                    attr_id = int(parts[0])
                    field = parts[1]
                    
                    if attr_id not in attributes:
                        attributes[attr_id] = {}
                    
                    if field == 'name':
                        attributes[attr_id]['name'] = value
        
        # Associa com offsets de atributos
        if 'dwarf_offsets' in self.offset_dictionary:
            attr_offsets = ['physical_attrs', 'mental_attrs']
            for offset in attr_offsets:
                if offset in self.offset_dictionary['dwarf_offsets']:
                    self.offset_dictionary['dwarf_offsets'][offset]['possible_values'] = [
                        f"{attr_id}: {data.get('name', 'Unknown')}" for attr_id, data in attributes.items()
                    ]
                    self.offset_dictionary['dwarf_offsets'][offset]['data_type'] = 'vector<attribute_struct>'
                    self.offset_dictionary['dwarf_offsets'][offset]['examples'] = [
                        "Strength, Agility, Toughness, Endurance", "Analytical Ability, Focus, Willpower"
                    ]
    
    def analyze_skills(self, section):
        """Analisa habilidades possíveis"""
        skills = {}
        for key, value in section.items():
            if '/' in key:
                parts = key.split('/')
                if len(parts) == 2:
                    skill_id = int(parts[0])
                    field = parts[1]
                    
                    if skill_id not in skills:
                        skills[skill_id] = {}
                    
                    if field == 'name':
                        skills[skill_id]['name'] = value
        
        # Associa com mood_skill
        if 'dwarf_offsets' in self.offset_dictionary:
            if 'mood_skill' in self.offset_dictionary['dwarf_offsets']:
                self.offset_dictionary['dwarf_offsets']['mood_skill']['possible_values'] = [
                    f"{skill_id}: {data.get('name', 'Unknown')}" for skill_id, data in skills.items()
                ]
                self.offset_dictionary['dwarf_offsets']['mood_skill']['data_type'] = 'uint32 (skill_id)'
                self.offset_dictionary['dwarf_offsets']['mood_skill']['examples'] = [
                    "0: Mining", "1: Woodcutting", "38: Weaponsmith", "39: Armorer"
                ]
    
    def analyze_labors(self, section):
        """Analisa trabalhos possíveis"""
        labors = {}
        for key, value in section.items():
            if '/' in key:
                parts = key.split('/')
                if len(parts) == 2:
                    labor_id = int(parts[0])
                    field = parts[1]
                    
                    if labor_id not in labors:
                        labors[labor_id] = {}
                    
                    if field == 'name':
                        labors[labor_id]['name'] = value
        
        # Associa com labors offset
        if 'dwarf_offsets' in self.offset_dictionary:
            if 'labors' in self.offset_dictionary['dwarf_offsets']:
                self.offset_dictionary['dwarf_offsets']['labors']['possible_values'] = [
                    f"Bit {labor_id}: {data.get('name', 'Unknown')}" for labor_id, data in labors.items()
                ]
                self.offset_dictionary['dwarf_offsets']['labors']['data_type'] = 'bitfield (labor flags)'
                self.offset_dictionary['dwarf_offsets']['labors']['examples'] = [
                    "Bit 0: Mining", "Bit 1: Woodcutting", "Bit 2: Carpentry", "Bit 6: Masonry"
                ]
    
    def analyze_thoughts(self, section):
        """Analisa pensamentos possíveis"""
        thoughts = {}
        for key, value in section.items():
            if '/' in key:
                parts = key.split('/')
                if len(parts) == 2:
                    thought_id = int(parts[0])
                    field = parts[1]
                    
                    if thought_id not in thoughts:
                        thoughts[thought_id] = {}
                    
                    if field == 'title':
                        thoughts[thought_id]['title'] = value
        
        # Associa com emotion offsets
        if 'emotion_offsets' in self.offset_dictionary:
            if 'thought_id' in self.offset_dictionary['emotion_offsets']:
                self.offset_dictionary['emotion_offsets']['thought_id']['possible_values'] = [
                    f"{thought_id}: {data.get('title', 'Unknown')}" for thought_id, data in thoughts.items()
                ][:50]  # Limita para os primeiros 50
                self.offset_dictionary['emotion_offsets']['thought_id']['data_type'] = 'uint32 (thought_id)'
                self.offset_dictionary['emotion_offsets']['thought_id']['examples'] = [
                    "1: Conflict", "10: Crafted Masterwork", "32: Death (Pet)", "98: Meal"
                ]
    
    def analyze_moods(self, section):
        """Analisa humores possíveis"""
        moods = {}
        for key, value in section.items():
            if '/' in key:
                parts = key.split('/')
                if len(parts) == 2:
                    mood_id = int(parts[0])
                    field = parts[1]
                    
                    if mood_id not in moods:
                        moods[mood_id] = {}
                    
                    if field == 'name':
                        moods[mood_id]['name'] = value
        
        # Associa com mood offset
        if 'dwarf_offsets' in self.offset_dictionary:
            if 'mood' in self.offset_dictionary['dwarf_offsets']:
                self.offset_dictionary['dwarf_offsets']['mood']['possible_values'] = [
                    f"{mood_id}: {data.get('name', 'Unknown')}" for mood_id, data in moods.items()
                ]
                self.offset_dictionary['dwarf_offsets']['mood']['data_type'] = 'uint32 (mood_id)'
                self.offset_dictionary['dwarf_offsets']['mood']['examples'] = [
                    "-1: No Mood", "0: Fey", "1: Secretive", "2: Possessed", "3: Macabre"
                ]
    
    def analyze_races(self, section):
        """Analisa raças possíveis"""
        races = {}
        for key, value in section.items():
            if '/' in key:
                parts = key.split('/')
                if len(parts) == 2:
                    race_id = int(parts[0])
                    field = parts[1]
                    
                    if race_id not in races:
                        races[race_id] = {}
                    
                    if field == 'name':
                        races[race_id]['name'] = value
        
        # Associa com race offset
        if 'dwarf_offsets' in self.offset_dictionary:
            if 'race' in self.offset_dictionary['dwarf_offsets']:
                self.offset_dictionary['dwarf_offsets']['race']['possible_values'] = [
                    f"{race_id}: {data.get('name', 'Unknown')}" for race_id, data in races.items()
                ]
                self.offset_dictionary['dwarf_offsets']['race']['data_type'] = 'uint32 (race_id)'
                self.offset_dictionary['dwarf_offsets']['race']['examples'] = [
                    "0: Dwarf", "1: Elf", "2: Human", "3: Goblin"
                ]
    
    def analyze_source_code(self):
        """Analisa código fonte para enums e constantes"""
        print("🔧 Analisando código fonte...")
        
        # Procura por arquivos relevantes
        relevant_files = [
            'dwarf.h', 'dwarf.cpp', 'global_enums.h', 'defines.h',
            'memorylayout.h', 'dfinstance.h'
        ]
        
        for filename in relevant_files:
            file_path = os.path.join(self.src_path, filename)
            if os.path.exists(file_path):
                self.analyze_cpp_file(file_path)
    
    def analyze_cpp_file(self, file_path):
        """Analisa um arquivo C++ específico"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Procura por enums
            enum_pattern = r'enum\s+(\w+)?\s*\{([^}]+)\}'
            for match in re.finditer(enum_pattern, content, re.MULTILINE | re.DOTALL):
                enum_name = match.group(1) or "unnamed"
                enum_body = match.group(2)
                
                enum_values = []
                for line in enum_body.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('//') and not line.startswith('/*'):
                        # Remove comentários inline
                        if '//' in line:
                            line = line[:line.index('//')]
                        if '/*' in line:
                            line = line[:line.index('/*')]
                        
                        # Extrai nome do enum
                        if '=' in line:
                            enum_value = line.split('=')[0].strip().rstrip(',')
                        else:
                            enum_value = line.strip().rstrip(',')
                        
                        if enum_value:
                            enum_values.append(enum_value)
                
                if enum_values:
                    self.enums[enum_name] = enum_values
            
            # Procura por constantes relacionadas a offsets
            self.extract_offset_usage(content, os.path.basename(file_path))
            
        except Exception as e:
            print(f"❌ Erro ao analisar {file_path}: {e}")
    
    def extract_offset_usage(self, content, filename):
        """Extrai uso de offsets no código"""
        # Procura por padrões como dwarf_offset("campo")
        offset_pattern = r'(\w+)_offset\("([^"]+)"\)'
        for match in re.finditer(offset_pattern, content):
            section_type = match.group(1)
            offset_name = match.group(2)
            
            section_map = {
                'dwarf': 'dwarf_offsets',
                'squad': 'squad_offsets',
                'emotion': 'emotion_offsets'
            }
            
            section = section_map.get(section_type, f"{section_type}_offsets")
            
            if section in self.offset_dictionary and offset_name in self.offset_dictionary[section]:
                self.code_usage[f"{section}.{offset_name}"].append(filename)
    
    def analyze_offset_relationships(self):
        """Analisa relacionamentos entre offsets"""
        print("🔗 Analisando relacionamentos...")
        
        # Relacionamentos conhecidos
        relationships = {
            'dwarf_offsets.id': ['hist_figure_offsets', 'squad_offsets.members'],
            'dwarf_offsets.race': ['race_offsets'],
            'dwarf_offsets.caste': ['caste_offsets'],
            'dwarf_offsets.squad_id': ['squad_offsets.id'],
            'dwarf_offsets.current_job': ['job_details'],
            'addresses.world_data': ['world_map', 'active_sites_vector'],
            'addresses.creature_vector': ['dwarf_offsets'],
            'addresses.squad_vector': ['squad_offsets']
        }
        
        for offset_key, related in relationships.items():
            if '.' in offset_key:
                section, offset = offset_key.split('.')
                if section in self.offset_dictionary and offset in self.offset_dictionary[section]:
                    self.offset_dictionary[section][offset]['relationships'] = related
    
    def infer_meaning(self, section, key):
        """Infere significado do offset (versão expandida)"""
        # Mapeamento detalhado conhecido
        detailed_meanings = {
            # Dwarf/Unit offsets - dados fundamentais
            'id': 'ID único da unidade (32-bit integer, usado como chave primária)',
            'race': 'ID da raça da criatura (referência para race_offsets)',
            'caste': 'ID da casta/subtipo da raça (referência para caste_offsets)',
            'sex': 'Gênero da criatura (0=fêmea, 1=macho, -1=desconhecido)',
            'birth_year': 'Ano de nascimento no calendário do jogo',
            'birth_time': 'Tick específico no ano de nascimento (granularidade temporal)',
            'name': 'Estrutura complexa contendo primeiro nome, apelido e sobrenome',
            'profession': 'ID da profissão atual (referência para professions em game_data)',
            'custom_profession': 'String customizada para profissão definida pelo jogador',
            
            # Estados e flags
            'mood': 'Estado de humor/temperamento atual (normal, fey, possessed, etc.)',
            'temp_mood': 'Humor temporário sobrepondo o humor base',
            'flags1': 'Flags primárias de estado (ativo, vivo, cidadão, etc.)',
            'flags2': 'Flags secundárias de estado (ferido, inconsciente, etc.)',
            'flags3': 'Flags terciárias de estado (estados especiais adicionais)',
            'states': 'Vetor de estados especiais (migrante, adaptado à caverna, etc.)',
            
            # Trabalho e habilidades
            'current_job': 'Ponteiro para estrutura do trabalho atual sendo executado',
            'labors': 'Bitfield de trabalhos habilitados para esta unidade',
            'mood_skill': 'Habilidade relacionada ao humor atual (para moods especiais)',
            
            # Atributos e corpo
            'physical_attrs': 'Vetor de atributos físicos (força, agilidade, resistência, etc.)',
            'body_size': 'Tamanho físico atual do corpo (afeta capacidade de carga)',
            'size_info': 'Informações detalhadas sobre tamanho e crescimento',
            'size_base': 'Tamanho base natural da criatura',
            'blood': 'Nível atual de sangue no corpo (afeta sobrevivência)',
            
            # Relacionamentos e social
            'civ': 'ID da civilização de origem desta unidade',
            'hist_id': 'ID da figura histórica (para personagens importantes)',
            'specific_refs': 'Vetor de referências específicas a outros objetos',
            'pet_owner_id': 'ID do dono se esta for uma criatura domesticada',
            
            # Militar
            'squad_id': 'ID do esquadrão militar ao qual pertence',
            'squad_position': 'Posição/rank dentro do esquadrão',
            'recheck_equipment': 'Flag para revalidar equipamentos militares',
            
            # Saúde e ferimentos
            'wounds_vector': 'Vetor de ferimentos ativos na criatura',
            'unit_health_info': 'Estrutura com informações detalhadas de saúde',
            'active_syndrome_vector': 'Vetor de síndromes ativas (doenças, maldições)',
            'syn_sick_flag': 'Flag indicando se está doente por síndrome',
            'body_component_info': 'Informações sobre componentes corporais',
            'layer_status_vector': 'Estado das camadas corporais (pele, músculos, etc.)',
            
            # Inventário e posses
            'inventory': 'Vetor de itens carregados pela unidade',
            'used_items_vector': 'Vetor de itens sendo ativamente utilizados',
            'inventory_item_mode': 'Modo de carregamento de item no inventário',
            'inventory_item_bodypart': 'Parte do corpo onde item está equipado',
            
            # Contadores e timing
            'turn_count': 'Contador de turnos de existência da unidade',
            'counters1': 'Grupo 1 de contadores diversos (ações, eventos)',
            'counters2': 'Grupo 2 de contadores diversos',
            'counters3': 'Grupo 3 de contadores diversos',
            'limb_counters': 'Contadores específicos de membros corporais',
            
            # Sobrenatural
            'curse': 'Informações sobre maldições ativas (vampirismo, licantropia)',
            'curse_add_flags1': 'Flags adicionais relacionadas a maldições',
            'souls': 'Vetor de almas (normalmente 1, múltiplas em casos especiais)',
            
            # Relacionamentos específicos
            'artifact_name': 'Nome de artefato associado (se criador ou portador)',
            'meeting': 'Informações sobre reuniões ou encontros agendados',
            'affection_level': 'Nível de afeição em relacionamentos',
            
            # Endereços globais do mundo
            'world_data': 'Ponteiro principal para todos os dados do mundo gerado',
            'current_year': 'Ano atual no calendário interno do jogo',
            'cur_year_tick': 'Tick atual dentro do ano (granularidade temporal)',
            'creature_vector': 'Vetor mestre contendo todas as criaturas existentes',
            'active_creature_vector': 'Subconjunto de criaturas atualmente ativas/carregadas',
            'fortress_entity': 'Ponteiro para a entidade que representa sua fortaleza',
            'dwarf_race_index': 'Índice da raça dos anões na tabela de raças',
            'dwarf_civ_index': 'Índice da civilização dos anões',
            
            # Vetores de objetos
            'squad_vector': 'Vetor de todos os esquadrões militares',
            'artifacts_vector': 'Vetor de todos os artefatos existentes no mundo',
            'activities_vector': 'Vetor de atividades em andamento',
            'historical_entities_vector': 'Vetor de entidades históricas (civilizações)',
            'historical_figures_vector': 'Vetor de figuras históricas importantes',
            'active_sites_vector': 'Vetor de sites ativos no mundo (fortalezas, cidades)',
            
            # Vetores de itens por tipo
            'weapons_vector': 'Vetor de todas as armas existentes',
            'armor_vector': 'Vetor de todas as armaduras existentes',
            'ammo_vector': 'Vetor de munições (flechas, virotes)',
            'shields_vector': 'Vetor de escudos',
            'backpacks_vector': 'Vetor de mochilas e containers',
            'flasks_vector': 'Vetor de frascos e recipientes de líquidos',
            
            # Definições e templates
            'material_templates_vector': 'Templates de materiais (metais, pedras, etc.)',
            'inorganics_vector': 'Materiais inorgânicos (minerais, pedras)',
            'plants_vector': 'Definições de plantas e árvores',
            'races_vector': 'Definições de todas as raças de criaturas',
            'base_materials': 'Materiais base do sistema',
            
            # Sistema de linguagem
            'language_vector': 'Definições de idiomas',
            'translation_vector': 'Tabelas de tradução entre idiomas',
            'colors_vector': 'Definições de cores disponíveis',
            'shapes_vector': 'Definições de formas geométricas',
            
            # Sistema de reações e química
            'reactions_vector': 'Reações químicas e de workshop',
            'all_syndromes_vector': 'Todas as síndromes definidas (doenças, etc.)',
            
            # Interface e visualização
            'gview': 'Visualização gráfica principal do jogo',
            'external_flag': 'Flag para comunicação com ferramentas externas',
            'viewscreen_setupdwarfgame_vtable': 'VTable da tela de setup inicial',
            
            # Sistema militar - esquadrões
            'members': 'Vetor de membros do esquadrão',
            'positions': 'Posições disponíveis no esquadrão',
            'orders': 'Ordens militares ativas',
            'uniform': 'Definição do uniforme padrão',
            'alert': 'Estado de alerta atual do esquadrão',
            
            # Emoções e pensamentos
            'emotion_type': 'Tipo específico da emoção (felicidade, raiva, etc.)',
            'thought_id': 'ID do pensamento específico (referência para unit_thoughts)',
            'strength': 'Intensidade da emoção (escala numérica)',
            'year': 'Ano em que a emoção foi gerada',
            'year_tick': 'Tick específico quando a emoção foi gerada',
            'sub_id': 'ID de subcategoria para emoções complexas',
            'level': 'Nível de intensidade em emoções graduais',
            
            # Ferimentos
            'parts': 'Partes do corpo afetadas pelo ferimento',
            'layer': 'Camada corporal afetada (pele, músculo, osso)',
            'bleeding': 'Estado e intensidade do sangramento',
            'infection': 'Presença e severidade de infecção',
            'pain': 'Nível de dor causado pelo ferimento',
            
            # Necessidades
            'focus': 'Foco ou prioridade da necessidade',
            
            # Materiais
            'material_type': 'Tipo do material (metal, pedra, madeira, etc.)',
            'quality': 'Qualidade do item (obra-prima, superior, etc.)',
            'wear': 'Nível de desgaste ou deterioração',
            'stack_size': 'Quantidade de itens na pilha',
            
            # Saúde detalhada
            'layers_vector': 'Camadas corporais (pele, gordura, músculo, osso)',
            'tissue_flags': 'Flags de estado dos tecidos corporais',
            'body_part_flags': 'Flags de estado das partes corporais',
            'parent_id': 'ID da parte corporal pai (hierarquia)',
            'tissue_name': 'Nome específico do tecido',
            'layer_tissue': 'Tipo de tecido da camada',
            'names_vector': 'Nomes das partes corporais',
            'layer_global_id': 'ID global da camada no sistema',
        }
        
        # Busca significado detalhado conhecido
        if key in detailed_meanings:
            return detailed_meanings[key]
        
        # Fallback para inferência básica
        return self.basic_meaning_inference(key)
    
    def basic_meaning_inference(self, key):
        """Inferência básica de significado"""
        if 'vector' in key:
            return f"Vetor contendo coleção de {key.replace('_vector', '').replace('_', ' ')}"
        elif 'offset' in key:
            return f"Offset para localizar {key.replace('_offset', '').replace('_', ' ')}"
        elif 'addr' in key or 'address' in key:
            return f"Endereço de memória para {key.replace('_addr', '').replace('_address', '').replace('_', ' ')}"
        elif 'count' in key:
            return f"Contador numérico para {key.replace('_count', '').replace('_', ' ')}"
        elif 'size' in key:
            return f"Tamanho em bytes de {key.replace('_size', '').replace('_', ' ')}"
        elif 'flag' in key:
            return f"Flag booleana indicando {key.replace('_flag', '').replace('_', ' ')}"
        elif 'id' in key:
            return f"Identificador único para {key.replace('_id', '').replace('_', ' ')}"
        elif key.endswith('_x') or key.endswith('_y') or key.endswith('_z'):
            return f"Coordenada {key[-1].upper()} em sistema tridimensional"
        else:
            return f"Campo de dados para {key.replace('_', ' ')}"
    
    def infer_data_type(self, section, key):
        """Infere o tipo de dados do offset"""
        type_mapping = {
            # Tipos específicos conhecidos
            'id': 'uint32',
            'race': 'uint32',
            'caste': 'uint32', 
            'sex': 'int16',
            'birth_year': 'uint32',
            'birth_time': 'uint32',
            'mood': 'int32',
            'flags1': 'uint32',
            'flags2': 'uint32', 
            'flags3': 'uint32',
            'squad_id': 'uint32',
            'squad_position': 'uint32',
            'body_size': 'uint32',
            'blood': 'uint32',
            'turn_count': 'uint32',
            'thought_id': 'uint32',
            'emotion_type': 'uint32',
            'strength': 'uint32',
            'year': 'uint32',
            'year_tick': 'uint32',
            'level': 'uint32',
            'layer': 'uint16',
            'pain': 'uint32',
            'bleeding': 'bool',
            'infection': 'bool'
        }
        
        if key in type_mapping:
            return type_mapping[key]
        elif 'vector' in key:
            return 'std::vector<>'
        elif 'addr' in key or 'address' in key or key.endswith('_ptr'):
            return 'void*'
        elif 'flag' in key:
            return 'bool'
        elif 'count' in key or 'size' in key:
            return 'uint32'
        elif key.endswith('_id'):
            return 'uint32'
        else:
            return 'unknown'
    
    def infer_size(self, section, key):
        """Infere o tamanho em bytes do offset"""
        type_sizes = {
            'uint32': 4,
            'int32': 4,
            'uint16': 2,
            'int16': 2,
            'uint8': 1,
            'int8': 1,
            'bool': 1,
            'void*': 8,  # 64-bit pointer
            'std::vector<>': 24  # std::vector overhead
        }
        
        data_type = self.infer_data_type(section, key)
        return type_sizes.get(data_type, 'variable')
    
    def export_comprehensive_analysis(self):
        """Exporta análise comprehensiva"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Gera estatísticas
        stats = self.generate_comprehensive_stats()
        
        export_data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'description': 'Análise comprehensiva de offsets do Dwarf Therapist',
                'version': '2.0 - Expandida com possibilidades de valores'
            },
            'statistics': stats,
            'sections': dict(self.offset_dictionary),
            'enums_found': self.enums,
            'game_data_sections': list(self.game_data.keys()),
            'code_usage': dict(self.code_usage)
        }
        
        # Exporta JSON
        json_file = os.path.join(self.base_path, "python_implementation", "exports", f"comprehensive_offsets_{timestamp}.json")
        os.makedirs(os.path.dirname(json_file), exist_ok=True)
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        # Gera relatório markdown
        md_file = self.generate_comprehensive_markdown(stats, timestamp)
        
        return json_file, md_file
    
    def generate_comprehensive_stats(self):
        """Gera estatísticas comprehensivas"""
        total_offsets = sum(len(section) for section in self.offset_dictionary.values())
        offsets_with_values = sum(
            1 for section in self.offset_dictionary.values()
            for offset in section.values()
            if offset.get('possible_values')
        )
        
        return {
            'total_sections': len(self.offset_dictionary),
            'total_offsets': total_offsets,
            'offsets_with_possible_values': offsets_with_values,
            'enums_found': len(self.enums),
            'game_data_sections': len(self.game_data),
            'coverage_percentage': round((offsets_with_values / total_offsets) * 100, 2) if total_offsets > 0 else 0
        }
    
    def generate_comprehensive_markdown(self, stats, timestamp):
        """Gera relatório markdown comprehensivo"""
        md_file = os.path.join(self.base_path, f"RELATORIO_OFFSETS_COMPLETO_{timestamp}.md")
        
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write("# Relatório Comprehensivo de Offsets - Dwarf Therapist\n\n")
            f.write(f"**Gerado em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## 📊 Estatísticas Expandidas\n\n")
            f.write(f"- **Total de seções:** {stats['total_sections']}\n")
            f.write(f"- **Total de offsets:** {stats['total_offsets']}\n")
            f.write(f"- **Offsets com valores possíveis:** {stats['offsets_with_possible_values']}\n")
            f.write(f"- **Cobertura de análise:** {stats['coverage_percentage']}%\n")
            f.write(f"- **Enums encontrados:** {stats['enums_found']}\n")
            f.write(f"- **Seções de game data:** {stats['game_data_sections']}\n\n")
            
            f.write("## 🎯 Principais Descobertas\n\n")
            f.write("### Offsets com Valores Mapeados\n\n")
            
            mapped_count = 0
            for section_name, section in self.offset_dictionary.items():
                section_mapped = sum(1 for offset in section.values() if offset.get('possible_values'))
                if section_mapped > 0:
                    f.write(f"- **{section_name}:** {section_mapped}/{len(section)} offsets mapeados\n")
                    mapped_count += 1
            
            f.write(f"\n**Total:** {mapped_count} seções com offsets mapeados\n\n")
            
            # Seções detalhadas
            for section_name in sorted(self.offset_dictionary.keys()):
                section = self.offset_dictionary[section_name]
                f.write(f"## 🔧 {section_name}\n\n")
                
                # Descrição da seção
                section_descriptions = {
                    'dwarf_offsets': 'Offsets para dados de unidades/criaturas - anões, animais, invasores, visitantes',
                    'addresses': 'Endereços globais fundamentais - ponteiros para estruturas principais do jogo',
                    'squad_offsets': 'Offsets para esquadrões militares - organização, membros, ordens',
                    'emotion_offsets': 'Offsets para sistema emocional - pensamentos, sentimentos, humores',
                    'item_offsets': 'Offsets para itens genéricos - armas, ferramentas, materiais',
                    'race_offsets': 'Offsets para definições de raças - anões, elfos, humanos, goblins',
                    'health_offsets': 'Offsets para sistema de saúde - ferimentos, doenças, estado físico'
                }
                
                if section_name in section_descriptions:
                    f.write(f"**Descrição:** {section_descriptions[section_name]}\n\n")
                
                f.write(f"**Total de offsets:** {len(section)}\n\n")
                
                # Tabela expandida
                f.write("| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |\n")
                f.write("|--------|-----|-----|------|---------|-------------|-------------------|----------|\n")
                
                for key in sorted(section.keys()):
                    data = section[key]
                    
                    # Trunca valores possíveis se muito longo
                    possible_values = ""
                    if data.get('possible_values'):
                        values_list = data['possible_values'][:3]  # Primeiros 3
                        possible_values = "; ".join(values_list)
                        if len(data['possible_values']) > 3:
                            possible_values += f"; +{len(data['possible_values'])-3} mais"
                    
                    # Trunca exemplos
                    examples = ""
                    if data.get('examples'):
                        examples = "; ".join(data['examples'][:2])
                    
                    # Trunca significado se muito longo
                    meaning = data['meaning']
                    if len(meaning) > 100:
                        meaning = meaning[:97] + "..."
                    
                    f.write(f"| `{key}` | `{data['hex_value']}` | {data['int_value']} | {data['data_type']} | {data['size_bytes']} | {meaning} | {possible_values} | {examples} |\n")
                
                f.write("\n### Detalhes dos Offsets\n\n")
                
                # Detalhes expandidos para offsets importantes
                important_offsets = [k for k, v in section.items() if v.get('possible_values') or v.get('examples')]
                
                for key in important_offsets[:10]:  # Limita a 10 por seção
                    data = section[key]
                    f.write(f"#### `{key}` (Offset {data['hex_value']})\n\n")
                    f.write(f"**Significado:** {data['meaning']}\n\n")
                    f.write(f"**Tipo de dados:** {data['data_type']} ({data['size_bytes']} bytes)\n\n")
                    
                    if data.get('possible_values'):
                        f.write("**Valores possíveis:**\n")
                        for value in data['possible_values'][:20]:  # Primeiros 20
                            f.write(f"- {value}\n")
                        if len(data['possible_values']) > 20:
                            f.write(f"- ... e mais {len(data['possible_values'])-20} valores\n")
                        f.write("\n")
                    
                    if data.get('examples'):
                        f.write("**Exemplos de uso:**\n")
                        for example in data['examples']:
                            f.write(f"- {example}\n")
                        f.write("\n")
                    
                    if data.get('relationships'):
                        f.write("**Relacionamentos:**\n")
                        for rel in data['relationships']:
                            f.write(f"- Relacionado com: {rel}\n")
                        f.write("\n")
                    
                    f.write("---\n\n")
                
                f.write("\n")
            
            # Apêndices
            f.write("## 📚 Apêndices\n\n")
            
            f.write("### A. Enums Encontrados no Código\n\n")
            for enum_name, values in self.enums.items():
                f.write(f"**{enum_name}:**\n")
                for value in values[:10]:  # Primeiros 10
                    f.write(f"- {value}\n")
                if len(values) > 10:
                    f.write(f"- ... e mais {len(values)-10} valores\n")
                f.write("\n")
            
            f.write("### B. Uso no Código Fonte\n\n")
            for offset_key, files in self.code_usage.items():
                f.write(f"**{offset_key}:** usado em {', '.join(files)}\n")
            
            f.write("\n### C. Guia de Tipos de Dados\n\n")
            f.write("| Tipo | Tamanho | Descrição |\n")
            f.write("|------|---------|----------|\n")
            f.write("| `uint32` | 4 bytes | Inteiro sem sinal 32-bit (0 a 4,294,967,295) |\n")
            f.write("| `int32` | 4 bytes | Inteiro com sinal 32-bit (-2,147,483,648 a 2,147,483,647) |\n")
            f.write("| `uint16` | 2 bytes | Inteiro sem sinal 16-bit (0 a 65,535) |\n")
            f.write("| `int16` | 2 bytes | Inteiro com sinal 16-bit (-32,768 a 32,767) |\n")
            f.write("| `bool` | 1 byte | Valor booleano (0=false, 1=true) |\n")
            f.write("| `void*` | 8 bytes | Ponteiro de memória (64-bit) |\n")
            f.write("| `std::vector<>` | 24+ bytes | Container dinâmico C++ |\n")
            f.write("| `bitfield` | variável | Campo de bits para flags múltiplas |\n")
        
        return md_file

def main():
    base_path = r"C:\Users\Eduardo\Documents\projetinhos\Dwarf-Therapist"
    
    print("=" * 70)
    print("COMPREHENSIVE OFFSET ANALYZER")
    print("=" * 70)
    print()
    print("Gerando relatório ampliado com todas as possibilidades de cada offset...")
    print()
    
    analyzer = ComprehensiveOffsetAnalyzer(base_path)
    analyzer.analyze_comprehensive()
    
    json_file, md_file = analyzer.export_comprehensive_analysis()
    
    print()
    print("=" * 70)
    print("ANÁLISE COMPREHENSIVA CONCLUÍDA")
    print("=" * 70)
    print()
    print(f"📊 RESUMO EXPANDIDO:")
    print(f"   Total de offsets: {sum(len(section) for section in analyzer.offset_dictionary.values())}")
    print(f"   Seções analisadas: {len(analyzer.offset_dictionary)}")
    print(f"   Enums extraídos: {len(analyzer.enums)}")
    print(f"   Seções game_data: {len(analyzer.game_data)}")
    print()
    print(f"📁 ARQUIVOS GERADOS:")
    print(f"   JSON: {json_file}")
    print(f"   Markdown: {md_file}")
    print()
    print("🎯 RECURSOS EXPANDIDOS:")
    print("   ✅ Valores possíveis para cada offset")
    print("   ✅ Tipos de dados inferidos")
    print("   ✅ Tamanhos em bytes")
    print("   ✅ Exemplos de uso")
    print("   ✅ Relacionamentos entre offsets")
    print("   ✅ Análise de código fonte")
    print("   ✅ Mapeamento de enums")
    print()

if __name__ == "__main__":
    main()