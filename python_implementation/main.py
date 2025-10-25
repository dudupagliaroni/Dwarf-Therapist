#!/usr/bin/env python3
"""
Script principal para executar apenas o complete_dwarf_reader.py

Este script executa diretamente o leitor completo de dados do Dwarf Fortress.
"""

import sys
import os
from pathlib import Path

def main():
    """Executa apenas o complete_dwarf_reader.py"""
    print("=" * 60)
    print("DWARF THERAPIST - PYTHON IMPLEMENTATION")
    print("=" * 60)
    print("Executando leitura completa da memória do Dwarf Fortress")
    print()
    
    # Definir caminho para o complete_dwarf_reader.py
    base_dir = Path(__file__).parent
    script_path = base_dir / "src" / "complete_dwarf_reader.py"
    
    # Verificar se o arquivo existe
    if not script_path.exists():
        print(f"ERRO: Script não encontrado: {script_path}")
        sys.exit(1)
    
    # Executar o script diretamente
    try:
        # Importar e executar
        sys.path.insert(0, str(script_path.parent))
        import complete_dwarf_reader
        complete_dwarf_reader.main()
        
    except Exception as e:
        print(f"ERRO ao executar complete_dwarf_reader.py: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExecução interrompida pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\nERRO inesperado: {e}")
        sys.exit(1)