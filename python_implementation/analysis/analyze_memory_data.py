#!/usr/bin/env python3
"""
Análise Completa dos Dados da Memória do Dwarf Fortress
Mostra todos os dados que podem ser extraídos da memória
"""

import json
from pathlib import Path
import configparser

def analisar_layout_memoria():
    """Analisa o layout de memória para mostrar todos os dados disponíveis"""
    
    print("🧠 ANÁLISE COMPLETA DOS DADOS DA MEMÓRIA DO DWARF FORTRESS")
    print("=" * 70)
    
    # Carregar layout de memória
    layout_file = Path("share/memory_layouts/windows/v0.52.05-steam_win64.ini")
    if not layout_file.exists():
        print("❌ Arquivo de layout não encontrado")
        return
    
    config = configparser.ConfigParser()
    config.read(layout_file)
    
    # 1. ENDEREÇOS GLOBAIS
    print("\n🌍 ENDEREÇOS GLOBAIS - Dados do Mundo/Fortress:")
    print("-" * 50)
    
    global_addresses = {
        'current_year': 'Ano atual do jogo',
        'dwarf_civ_index': 'ID da civilização dos dwarves',
        'dwarf_race_index': 'ID da raça dwarf',
        'fortress_entity': 'Entidade da fortaleza',
        'creature_vector': 'Lista de todas as criaturas',
        'active_creature_vector': 'Lista de criaturas ativas',
        'squad_vector': 'Esquadrões militares',
        'historical_figures_vector': 'Figuras históricas',
        'world_data': 'Dados do mundo',
        'artifacts_vector': 'Artefatos',
        'reactions_vector': 'Reações de crafting',
        'materials_vector': 'Materiais disponíveis',
        'plants_vector': 'Plantas do mundo',
        'races_vector': 'Todas as raças',
        'colors_vector': 'Cores disponíveis',
        'language_vector': 'Dados de linguagem'
    }
    
    if 'addresses' in config:
        addresses = dict(config['addresses'])
        for key, desc in global_addresses.items():
            if key in addresses:
                print(f"  ✅ {key:<25} → {desc}")
            else:
                print(f"  ❌ {key:<25} → {desc} (não disponível)")
    
    # 2. DADOS DOS DWARVES/UNIDADES
    print("\n👤 DADOS DOS DWARVES - Informações individuais:")
    print("-" * 50)
    
    dwarf_data = {
        'name': 'Nome do dwarf',
        'custom_profession': 'Profissão customizada',
        'profession': 'Profissão padrão/ID',
        'race': 'ID da raça',
        'caste': 'Casta (sexo/tipo)',
        'sex': 'Sexo (masculino/feminino)',
        'id': 'ID único do dwarf',
        'civ': 'ID da civilização',
        'birth_year': 'Ano de nascimento',
        'birth_time': 'Tempo específico de nascimento',
        'age': 'Idade (calculada)',
        'mood': 'Humor/mood atual',
        'physical_attrs': 'Atributos físicos (força, agilidade, etc.)',
        'souls': 'Dados da "alma" (skills, personalidade)',
        'labors': 'Trabalhos habilitados/desabilitados',
        'squad_id': 'ID do esquadrão militar',
        'squad_position': 'Posição no esquadrão',
        'current_job': 'Trabalho atual sendo executado',
        'hist_id': 'ID como figura histórica',
        'curse': 'Maldições/efeitos mágicos',
        'active_syndrome_vector': 'Síndromes ativas (doenças, etc.)',
        'unit_health_info': 'Informações de saúde',
        'wounds_vector': 'Ferimentos atuais',
        'inventory': 'Itens carregados/equipados',
        'body_size': 'Tamanho do corpo',
        'blood': 'Nível de sangue',
        'temp_mood': 'Humor temporário',
        'counters1/2/3': 'Contadores diversos',
        'artifact_name': 'Nome se for um artefato',
        'pet_owner_id': 'ID do dono se for pet'
    }
    
    if 'dwarf_offsets' in config:
        dwarf_offsets = dict(config['dwarf_offsets'])
        for key, desc in dwarf_data.items():
            base_key = key.split('/')[0]  # Para casos como counters1/2/3
            if base_key in dwarf_offsets:
                offset = dwarf_offsets[base_key]
                print(f"  ✅ {key:<25} → {desc} (offset: {offset})")
            else:
                print(f"  ❌ {key:<25} → {desc} (não disponível)")
    
    # 3. DADOS DA ALMA (SOUL)
    print("\n🧠 DADOS DA ALMA - Skills e personalidade:")
    print("-" * 50)
    
    soul_data = {
        'name': 'Nome da alma',
        'orientation': 'Orientação sexual/romântica',
        'mental_attrs': 'Atributos mentais (inteligência, foco, etc.)',
        'skills': 'Habilidades e níveis',
        'personality': 'Traços de personalidade',
        'beliefs': 'Crenças religiosas/filosóficas',
        'emotions': 'Estado emocional',
        'memories': 'Memórias importantes',
        'relationships': 'Relacionamentos com outros'
    }
    
    if 'soul_details' in config:
        soul_offsets = dict(config['soul_details'])
        for key, desc in soul_data.items():
            if key in soul_offsets:
                offset = soul_offsets[key]
                print(f"  ✅ {key:<25} → {desc} (offset: {offset})")
            else:
                print(f"  ❌ {key:<25} → {desc} (não disponível)")
    
    # 4. DADOS DE SAÚDE
    print("\n🏥 DADOS DE SAÚDE - Ferimentos e status físico:")
    print("-" * 50)
    
    if 'unit_wound_offsets' in config:
        wound_offsets = dict(config['unit_wound_offsets'])
        health_data = {
            'parts': 'Partes do corpo afetadas',
            'layer': 'Camada do ferimento (pele, músculo, etc.)',
            'bleeding': 'Nível de sangramento',
            'pain': 'Nível de dor',
            'effects_vector': 'Efeitos do ferimento',
            'flags1/flags2': 'Status diversos do ferimento'
        }
        
        for key, desc in health_data.items():
            base_key = key.split('/')[0]
            if base_key in wound_offsets:
                offset = wound_offsets[base_key]
                print(f"  ✅ {key:<25} → {desc} (offset: {offset})")
    
    # 5. DADOS DE EQUIPAMENTOS
    print("\n⚔️  DADOS DE EQUIPAMENTOS - Itens e armas:")
    print("-" * 50)
    
    equipment_vectors = [
        'weapons_vector', 'shields_vector', 'armor_vector', 
        'helms_vector', 'gloves_vector', 'shoes_vector',
        'pants_vector', 'backpacks_vector', 'ammo_vector'
    ]
    
    if 'addresses' in config:
        addresses = dict(config['addresses'])
        for vec in equipment_vectors:
            if vec in addresses:
                print(f"  ✅ {vec:<25} → Lista de {vec.replace('_vector', '').replace('_', ' ')}")
    
    # 6. DADOS ATUALMENTE IMPLEMENTADOS
    print("\n📊 DADOS ATUALMENTE LIDOS PELA NOSSA IMPLEMENTAÇÃO:")
    print("-" * 50)
    
    implemented_data = [
        'name', 'custom_profession', 'profession', 'race', 'caste', 
        'sex', 'id', 'age', 'mood', 'address'
    ]
    
    for data in implemented_data:
        print(f"  ✅ {data}")
    
    # 7. POTENCIAL DE EXPANSÃO
    print("\n🚀 DADOS QUE PODEM SER ADICIONADOS:")
    print("-" * 50)
    
    potential_data = [
        '• Skills e níveis de habilidade',
        '• Atributos físicos e mentais',
        '• Status de saúde e ferimentos',
        '• Equipamentos e inventário',
        '• Relacionamentos sociais',
        '• Histórico de trabalhos',
        '• Preferências e personalidade',
        '• Status militar e esquadrão',
        '• Humor e necessidades',
        '• Maldições e síndromes',
        '• Memórias e experiências'
    ]
    
    for item in potential_data:
        print(f"  {item}")

def analisar_dados_exportados():
    """Analisa os dados que foram efetivamente exportados"""
    
    print("\n\n📋 ANÁLISE DOS DADOS EXPORTADOS:")
    print("=" * 50)
    
    try:
        with open('dwarves_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 Metadados:")
        metadata = data['metadata']
        for key, value in metadata.items():
            if key == 'layout_info':
                print(f"  • {key}: {value}")
            else:
                print(f"  • {key}: {value}")
        
        print(f"\n👥 Dwarves analisados: {len(data['dwarves'])}")
        
        if data['dwarves']:
            # Analisar primeiro dwarf como exemplo
            first_dwarf = data['dwarves'][0]
            print(f"\n🔍 Exemplo - Primeiro dwarf:")
            for key, value in first_dwarf.items():
                print(f"  • {key}: {value}")
            
            # Estatísticas
            print(f"\n📈 Estatísticas:")
            
            ages = [d['age'] for d in data['dwarves'] if d['age'] > 0]
            if ages:
                print(f"  • Idades: {min(ages)} - {max(ages)} anos (média: {sum(ages)/len(ages):.1f})")
            
            named_dwarves = [d for d in data['dwarves'] if d['name']]
            print(f"  • Dwarves com nome: {len(named_dwarves)}")
            
            custom_prof = [d for d in data['dwarves'] if d['custom_profession']]
            print(f"  • Profissões customizadas: {len(custom_prof)}")
            
            unique_races = set(d['race'] for d in data['dwarves'])
            print(f"  • Raças diferentes: {len(unique_races)}")
            
    except FileNotFoundError:
        print("❌ Arquivo dwarves_data.json não encontrado")
    except Exception as e:
        print(f"❌ Erro ao analisar dados: {e}")

if __name__ == "__main__":
    analisar_layout_memoria()
    analisar_dados_exportados()