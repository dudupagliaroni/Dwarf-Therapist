#!/usr/bin/env python3
"""
Visualizador de Dados Decodificados
Mostra as informações legíveis para humanos do JSON exportado
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any

def print_divider(char="=", length=80):
    """Imprime uma linha divisória"""
    print(char * length)

def print_section(title: str):
    """Imprime um cabeçalho de seção"""
    print(f"\n{'='*80}")
    print(f" {title}")
    print(f"{'='*80}")

def display_dwarf_summary(dwarf: Dict[str, Any]):
    """Exibe um resumo legível de um dwarf"""
    
    print_section(f"🧙 DWARF: {dwarf.get('name', 'Unknown')}")
    
    # Dados básicos
    print(f"\n📋 DADOS BÁSICOS:")
    print(f"   ID: {dwarf.get('id', 'N/A')}")
    print(f"   Idade: {dwarf.get('age', 'N/A')} anos")
    print(f"   Sexo: {dwarf.get('sex', 'N/A')}")
    print(f"   Profissão: {dwarf.get('profession', 'N/A')}")
    
    # Decodificações legíveis
    if '_decoded' in dwarf:
        decoded = dwarf['_decoded']
        
        # Corpo
        if 'body' in decoded:
            body = decoded['body']
            print(f"\n📏 TAMANHO DO CORPO:")
            print(f"   {body.get('display_text', 'N/A')}")
            print(f"   Categoria: {body.get('age_group', 'N/A')}")
        
        # Sangue
        if 'blood' in decoded:
            blood = decoded['blood']
            print(f"\n🩸 NÍVEL DE SANGUE:")
            print(f"   {blood.get('display_text', 'N/A')}")
            if blood.get('critical', False):
                print(f"   ⚠️  ESTADO CRÍTICO!")
        
        # Esquadrão
        if 'squad' in decoded:
            squad = decoded['squad']
            print(f"\n⚔️  INFORMAÇÃO MILITAR:")
            print(f"   {squad.get('display_text', 'N/A')}")
        
        # Histórico
        if 'history' in decoded:
            history = decoded['history']
            print(f"\n🏛️  IMPORTÂNCIA HISTÓRICA:")
            print(f"   {history.get('description', 'N/A')}")
        
        # Pet
        if 'pet' in decoded:
            pet = decoded['pet']
            if pet.get('is_pet', False):
                print(f"\n🐾 INFORMAÇÃO DE PET:")
                print(f"   {pet.get('display_text', 'N/A')}")
        
        # Flags
        if 'flags' in decoded:
            flags = decoded['flags']
            print(f"\n🚩 STATUS FLAGS:")
            print(f"   Unidade Válida: {'✓ Sim' if flags.get('is_valid_unit', False) else '✗ Não'}")
            print(f"   Flags1: {flags.get('flags1_hex', 'N/A')}")
            print(f"   Flags2: {flags.get('flags2_hex', 'N/A')}")
            print(f"   Flags3: {flags.get('flags3_hex', 'N/A')}")
            
            # Problemas de saúde
            health_issues = flags.get('health_issues', [])
            if health_issues:
                print(f"\n   ⚕️  Problemas de Saúde:")
                for issue in health_issues:
                    print(f"      - {issue}")
            
            # Status flags
            status_flags = flags.get('status_flags', [])
            if status_flags:
                print(f"\n   ⚠️  Status Especial:")
                for status in status_flags:
                    print(f"      - {status}")
    
    # Skills
    skills = dwarf.get('skills', [])
    if skills:
        print(f"\n🛠️  HABILIDADES ({len(skills)}):")
        for skill in skills[:5]:  # Mostrar apenas as 5 primeiras
            print(f"   - {skill.get('name', 'Unknown')}: Level {skill.get('level', 0)} (XP: {skill.get('experience', 0)})")
        if len(skills) > 5:
            print(f"   ... e mais {len(skills) - 5} habilidades")
    
    # Equipamentos
    equipment = dwarf.get('equipment', [])
    if equipment:
        print(f"\n🎒 EQUIPAMENTOS ({len(equipment)}):")
        for item in equipment[:5]:  # Mostrar apenas os 5 primeiros
            quality = item.get('quality', -1)
            wear = item.get('wear', -1)
            quality_str = f"Quality: {quality}" if quality != -1 else "Quality: N/A"
            wear_str = f"Wear: {wear}" if wear != -1 else "Wear: N/A"
            print(f"   - Item #{item.get('item_id', 0)}: Type {item.get('item_type', 0)} ({quality_str}, {wear_str})")
        if len(equipment) > 5:
            print(f"   ... e mais {len(equipment) - 5} itens")
    
    # Ferimentos
    wounds = dwarf.get('wounds', [])
    if wounds:
        print(f"\n🩹 FERIMENTOS ({len(wounds)}):")
        for wound in wounds:
            pain = wound.get('pain', -1)
            pain_str = f"Dor: {pain}" if pain != -1 else "Sem dados de dor"
            print(f"   - Parte #{wound.get('body_part', 0)}: Layer {wound.get('layer', 0)}, Bleeding: {wound.get('bleeding', 0)}, {pain_str}")

def main():
    """Função principal"""
    print("=" * 80)
    print(" VISUALIZADOR DE DADOS DECODIFICADOS - DWARF THERAPIST")
    print("=" * 80)
    
    # Encontrar o JSON mais recente
    exports_dir = Path(__file__).parent.parent / "exports"
    
    if not exports_dir.exists():
        print(f"\n❌ ERRO: Diretório exports não encontrado: {exports_dir}")
        return
    
    json_files = sorted(exports_dir.glob("complete_dwarves_data_*.json"), reverse=True)
    
    if not json_files:
        print(f"\n❌ ERRO: Nenhum arquivo JSON encontrado em {exports_dir}")
        return
    
    latest_file = json_files[0]
    print(f"\n📂 Carregando: {latest_file.name}")
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        metadata = data.get('metadata', {})
        dwarves = data.get('dwarves', [])
        
        print(f"\n📊 METADADOS:")
        print(f"   Versão: {metadata.get('version', 'N/A')}")
        print(f"   Decoder: {metadata.get('decoder_version', 'N/A')}")
        print(f"   Total de Dwarves: {metadata.get('dwarf_count', 0)}")
        print(f"   Timestamp: {metadata.get('timestamp', 'N/A')}")
        
        if 'statistics' in metadata:
            stats = metadata['statistics']
            print(f"\n   Estatísticas:")
            print(f"      - Dwarves com skills: {stats.get('dwarves_with_skills', 0)}")
            print(f"      - Dwarves com ferimentos: {stats.get('dwarves_with_wounds', 0)}")
            print(f"      - Dwarves com equipamentos: {stats.get('dwarves_with_equipment', 0)}")
        
        if not dwarves:
            print(f"\n❌ Nenhum dwarf encontrado no arquivo!")
            return
        
        # Mostrar primeiro dwarf completo
        display_dwarf_summary(dwarves[0])
        
        # Opção para ver mais
        print(f"\n" + "=" * 80)
        print(f"Total de {len(dwarves)} dwarves disponíveis no arquivo.")
        print(f"Primeiro dwarf mostrado acima.")
        
        # Estatísticas gerais
        print_section("📈 ESTATÍSTICAS GERAIS")
        
        civilians = sum(1 for d in dwarves if d.get('squad_id', -1) == -1)
        military = len(dwarves) - civilians
        
        print(f"\n⚔️  Distribuição Militar:")
        print(f"   Civis: {civilians} ({100*civilians/len(dwarves):.1f}%)")
        print(f"   Militares: {military} ({100*military/len(dwarves):.1f}%)")
        
        # Contagem de problemas de saúde
        health_issues_count = {}
        for dwarf in dwarves:
            if '_decoded' in dwarf and 'flags' in dwarf['_decoded']:
                for issue in dwarf['_decoded']['flags'].get('health_issues', []):
                    health_issues_count[issue] = health_issues_count.get(issue, 0) + 1
        
        if health_issues_count:
            print(f"\n⚕️  Problemas de Saúde Detectados:")
            for issue, count in sorted(health_issues_count.items(), key=lambda x: x[1], reverse=True):
                print(f"   {issue}: {count} dwarves ({100*count/len(dwarves):.1f}%)")
        
        # Distribuição de tamanho corporal
        body_categories = {}
        for dwarf in dwarves:
            if '_decoded' in dwarf and 'body' in dwarf['_decoded']:
                category = dwarf['_decoded']['body'].get('age_group', 'unknown')
                body_categories[category] = body_categories.get(category, 0) + 1
        
        if body_categories:
            print(f"\n👥 Distribuição por Categoria de Idade:")
            for category, count in sorted(body_categories.items(), key=lambda x: x[1], reverse=True):
                print(f"   {category.capitalize()}: {count} ({100*count/len(dwarves):.1f}%)")
        
        print(f"\n{'='*80}")
        print(f"✅ Análise completa!")
        
    except Exception as e:
        print(f"\n❌ ERRO ao carregar arquivo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
