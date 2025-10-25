#!/usr/bin/env python3
"""
Leitor de Dados Existentes - Dwarf Therapist Python
Mostra os dados já extraídos quando DF não está rodando
"""

import json
from pathlib import Path

def show_existing_data():
    """Mostra dados já extraídos anteriormente"""
    
    data_file = Path("data/complete_dwarves_data.json")
    
    if not data_file.exists():
        print("AVISO: Nenhum dado encontrado.")
        print("Execute o script com Dwarf Fortress rodando para extrair dados.")
        return False
    
    print("DWARF THERAPIST PYTHON - DADOS EXISTENTES")
    print("=" * 60)
    print("Carregando dados previamente extraídos...")
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Informações do arquivo
        metadata = data.get('metadata', {})
        dwarves = data.get('dwarves', [])
        
        print("SUCESSO: Dados carregados!")
        print(f"Arquivo: {data_file.name} ({data_file.stat().st_size:,} bytes)")
        
        # Metadata
        print(f"\nMETADATA:")
        print(f"   Versão: {metadata.get('version', 'N/A')}")
        print(f"   Data extração: {metadata.get('timestamp', 'N/A')}")
        print(f"   Versão DF: {metadata.get('layout_info', {}).get('version_name', 'N/A')}")
        print(f"   Endereço base: {metadata.get('base_address', 'N/A')}")
        
        # Estatísticas
        stats = metadata.get('statistics', {})
        print(f"\nESTATÍSTICAS:")
        print(f"   Total anões: {len(dwarves)}")
        print(f"   Habilidades: {stats.get('total_skills_read', 0)}")
        print(f"   Equipamentos: {stats.get('total_equipment_read', 0)}")
        print(f"   Ferimentos: {stats.get('total_wounds_read', 0)}")
        print(f"   Anões c/ skills: {stats.get('dwarves_with_skills', 0)}")
        print(f"   Anões c/ equipamentos: {stats.get('dwarves_with_equipment', 0)}")
        print(f"   Anões feridos: {stats.get('dwarves_with_wounds', 0)}")
        
        # Exemplo de anão
        if dwarves:
            first = dwarves[0]
            print(f"\nEXEMPLO - Anão: {first.get('name', 'N/A')}")
            print(f"   ID: {first.get('id', 'N/A')}")
            print(f"   Idade: {first.get('age', 'N/A')}")
            print(f"   Profissão: {first.get('profession', 'N/A')}")
            print(f"   Skills: {len(first.get('skills', []))}")
            print(f"   Equipamentos: {len(first.get('equipment', []))}")
            print(f"   Ferimentos: {len(first.get('wounds', []))}")
        
        # Resumo final
        total_data_points = (
            len(dwarves) + 
            stats.get('total_skills_read', 0) + 
            stats.get('total_equipment_read', 0) + 
            stats.get('total_wounds_read', 0)
        )
        
        print(f"\nRESUMO FINAL:")
        print(f"   TOTAL DE PONTOS DE DADOS: {total_data_points:,}")
        print(f"   STATUS: Dados completos disponíveis!")
        print(f"   ARQUIVO JSON: {data_file}")
        
        return True
        
    except Exception as e:
        print(f"ERRO ao carregar dados: {e}")
        return False

def main():
    """Função principal"""
    if not show_existing_data():
        print("\nPARA EXTRAIR NOVOS DADOS:")
        print("1. Inicie o Dwarf Fortress")
        print("2. Carregue uma fortaleza")
        print("3. Execute: python main.py read")
        print("4. Aguarde a extração completa")

if __name__ == "__main__":
    main()