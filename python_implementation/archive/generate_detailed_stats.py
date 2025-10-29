#!/usr/bin/env python3
"""
Gerador de Estatísticas Detalhadas do Mapeamento de Memória
Complemento ao relatório final em Markdown
"""

import json
import os
from pathlib import Path

def main():
    print("🔍 GERANDO ESTATÍSTICAS DETALHADAS DO MAPEAMENTO...")
    
    # Carregar dados dos arquivos de análise
    exports_dir = Path("exports")
    
    stats = {
        "arquivos_analisados": [],
        "total_offsets": 0,
        "secoes_mapeadas": [],
        "tipos_dados": {},
        "plataformas": set(),
        "versoes_df": set(),
        "dados_geograficos": {},
        "dados_dwarfs": {},
        "capacidades_demonstradas": []
    }
    
    # Analisar comprehensive offsets
    try:
        comp_file = "exports/comprehensive_offsets_20251029_001658.json"
        if os.path.exists(comp_file):
            with open(comp_file, 'r', encoding='utf-8') as f:
                comp_data = json.load(f)
            
            stats["total_offsets"] = comp_data['statistics']['total_offsets']
            stats["secoes_mapeadas"] = list(comp_data['sections'].keys())
            
            # Contar tipos de dados por seção
            for secao, dados in comp_data['sections'].items():
                if isinstance(dados, dict):
                    stats["tipos_dados"][secao] = len(dados)
            
            print(f"✅ Comprehensive offsets: {stats['total_offsets']} offsets em {len(stats['secoes_mapeadas'])} seções")
    except Exception as e:
        print(f"⚠️ Erro ao carregar comprehensive offsets: {e}")
    
    # Analisar world data
    try:
        world_files = list(Path("exports").glob("world_data_analysis_*.json"))
        if world_files:
            latest_world = max(world_files, key=os.path.getmtime)
            with open(latest_world, 'r', encoding='utf-8') as f:
                world_data = json.load(f)
            
            if 'world_map' in world_data and 'regions' in world_data['world_map']:
                regions = world_data['world_map']['regions']
                for key, value in regions.items():
                    if isinstance(value, dict) and 'count' in value:
                        stats["dados_geograficos"][key] = value['count']
            
            if 'active_sites' in world_data:
                stats["dados_geograficos"]["sites_ativos"] = world_data['active_sites'].get('site_count', 0)
            
            print(f"✅ World data: {sum(stats['dados_geograficos'].values())} elementos geográficos")
    except Exception as e:
        print(f"⚠️ Erro ao carregar world data: {e}")
    
    # Analisar thoughts
    try:
        thoughts_files = list(Path("exports").glob("thoughts_analysis_*.json"))
        if thoughts_files:
            latest_thoughts = max(thoughts_files, key=os.path.getmtime)
            with open(latest_thoughts, 'r', encoding='utf-8') as f:
                thoughts_data = json.load(f)
            
            if 'thought_types' in thoughts_data:
                stats["dados_dwarfs"]["tipos_pensamentos"] = len(thoughts_data['thought_types'])
            
            print(f"✅ Thoughts: {stats['dados_dwarfs'].get('tipos_pensamentos', 0)} tipos de pensamentos")
    except Exception as e:
        print(f"⚠️ Erro ao carregar thoughts: {e}")
    
    # Contar memory layouts
    layouts_dir = Path("../share/memory_layouts")
    if layouts_dir.exists():
        total_layouts = 0
        for platform_dir in layouts_dir.iterdir():
            if platform_dir.is_dir():
                stats["plataformas"].add(platform_dir.name)
                layouts = list(platform_dir.glob("*.ini"))
                total_layouts += len(layouts)
                
                # Extrair versões
                for layout in layouts:
                    version = layout.stem
                    stats["versoes_df"].add(version)
        
        print(f"✅ Memory layouts: {total_layouts} arquivos em {len(stats['plataformas'])} plataformas")
    
    # Gerar relatório de estatísticas
    stats_report = f"""
# Estatísticas Detalhadas do Mapeamento

## 📊 Resumo Numérico
- **Total de Offsets Mapeados:** {stats['total_offsets']}
- **Seções de Dados:** {len(stats['secoes_mapeadas'])}
- **Plataformas Suportadas:** {len(stats['plataformas'])}
- **Versões DF Suportadas:** {len(stats['versoes_df'])}

## 🗺️ Dados Geográficos Extraídos
"""
    
    for key, value in stats['dados_geograficos'].items():
        stats_report += f"- **{key}:** {value}\n"
    
    stats_report += f"""
## 👥 Dados de Dwarfs Mapeados
- **Tipos de Pensamentos:** {stats['dados_dwarfs'].get('tipos_pensamentos', 'N/A')}

## 📂 Seções Mapeadas
"""
    
    for i, secao in enumerate(stats['secoes_mapeadas'], 1):
        count = stats['tipos_dados'].get(secao, 0)
        stats_report += f"{i}. **{secao}** ({count} offsets)\n"
    
    stats_report += f"""
## 🔧 Plataformas e Versões
### Plataformas:
"""
    for plat in sorted(stats['plataformas']):
        stats_report += f"- {plat}\n"
    
    stats_report += f"""
### Versões do Dwarf Fortress (primeiras 10):
"""
    for version in sorted(list(stats['versoes_df']))[:10]:
        stats_report += f"- {version}\n"
    
    if len(stats['versoes_df']) > 10:
        stats_report += f"- ... e mais {len(stats['versoes_df']) - 10} versões\n"
    
    # Salvar estatísticas
    with open('ESTATISTICAS_DETALHADAS.md', 'w', encoding='utf-8') as f:
        f.write(stats_report)
    
    # Salvar dados JSON para processamento
    with open('estatisticas_mapeamento.json', 'w', encoding='utf-8') as f:
        # Converter sets para listas para JSON
        stats_json = stats.copy()
        stats_json['plataformas'] = list(stats['plataformas'])
        stats_json['versoes_df'] = list(stats['versoes_df'])
        json.dump(stats_json, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Relatórios gerados:")
    print(f"📄 RELATORIO_FINAL_MAPEAMENTO_MEMORIA_DF.md")
    print(f"📊 ESTATISTICAS_DETALHADAS.md")
    print(f"🔢 estatisticas_mapeamento.json")
    print(f"\n🎉 MAPEAMENTO COMPLETO DOCUMENTADO!")

if __name__ == "__main__":
    main()