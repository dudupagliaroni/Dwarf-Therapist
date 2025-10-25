#!/usr/bin/env python3
"""
Script principal para executar a implementação Python do Dwarf Therapist

Este script fornece uma interface simples para executar as diferentes
funcionalidades da implementação Python.

Uso:
    python main.py [comando] [opções]

Comandos disponíveis:
    read       - Lê dados do Dwarf Fortress e exporta para JSON
    analyze    - Analisa dados existentes e gera relatórios
    decode     - Decodifica habilidades e profissões
    all        - Executa leitura, análise e decodificação
    help       - Mostra esta ajuda

Exemplos:
    python main.py read
    python main.py analyze  
    python main.py decode
    python main.py all
"""

import sys
import os
import subprocess
from pathlib import Path

def print_header():
    """Imprime cabeçalho do programa"""
    print("=" * 60)
    print("🏔️  DWARF THERAPIST - PYTHON IMPLEMENTATION")
    print("=" * 60)
    print("Leitura direta da memória do Dwarf Fortress")
    print()

def run_script(script_path, description):
    """Executa um script Python e trata erros"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, check=True)
        print(f"✅ {description} concluído com sucesso!")
        if result.stdout:
            print("Saída:")
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro em {description}:")
        print(f"Código de saída: {e.returncode}")
        if e.stderr:
            print("Erro:")
            print(e.stderr)
        return False
    except FileNotFoundError:
        print(f"❌ Script não encontrado: {script_path}")
        return False

def main():
    """Função principal"""
    print_header()
    
    # Definir caminhos
    base_dir = Path(__file__).parent
    src_dir = base_dir / "src"
    analysis_dir = base_dir / "analysis"
    tools_dir = base_dir / "tools"
    
    # Scripts disponíveis
    scripts = {
        "read": (src_dir / "complete_dwarf_reader.py", "Lendo dados do Dwarf Fortress"),
        "analyze": (analysis_dir / "analyze_json_simple.py", "Analisando dados extraídos"),
        "decode_skills": (tools_dir / "decode_skills.py", "Decodificando habilidades"),
        "decode_professions": (tools_dir / "decode_professions.py", "Decodificando profissões"),
    }
    
    # Verificar argumentos
    if len(sys.argv) < 2:
        command = "help"
    else:
        command = sys.argv[1].lower()
    
    # Executar comando
    if command == "read":
        run_script(scripts["read"][0], scripts["read"][1])
        
    elif command == "analyze":
        if not (base_dir / "data" / "complete_dwarves_data.json").exists():
            print("⚠️  Dados não encontrados. Executando leitura primeiro...")
            if run_script(scripts["read"][0], scripts["read"][1]):
                run_script(scripts["analyze"][0], scripts["analyze"][1])
        else:
            run_script(scripts["analyze"][0], scripts["analyze"][1])
            
    elif command == "decode":
        # Executar ambos os decodificadores
        run_script(scripts["decode_skills"][0], scripts["decode_skills"][1])
        run_script(scripts["decode_professions"][0], scripts["decode_professions"][1])
        
    elif command == "all":
        print("🚀 Executando pipeline completo...\n")
        
        # 1. Leitura
        if run_script(scripts["read"][0], scripts["read"][1]):
            print()
            
            # 2. Análise
            if run_script(scripts["analyze"][0], scripts["analyze"][1]):
                print()
                
                # 3. Decodificação
                run_script(scripts["decode_skills"][0], scripts["decode_skills"][1])
                run_script(scripts["decode_professions"][0], scripts["decode_professions"][1])
                
                print("\n🎉 Pipeline completo executado com sucesso!")
            
    elif command == "help" or command == "--help" or command == "-h":
        print(__doc__)
        
    else:
        print(f"❌ Comando desconhecido: {command}")
        print("Use 'python main.py help' para ver comandos disponíveis")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Execução interrompida pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)