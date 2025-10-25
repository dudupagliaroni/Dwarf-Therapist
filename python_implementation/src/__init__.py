"""
Dwarf Therapist Python Implementation

Este pacote contém uma implementação completa em Python para leitura 
direta da memória do Dwarf Fortress, fornecendo acesso aos dados dos 
anões sem modificar o jogo.

Módulos principais:
- complete_dwarf_reader: Implementação completa e otimizada
- dwarf_therapist_verbose: Versão com logging detalhado  
- dwarf_therapist_python: Versão inicial básica

Classes principais:
- CompleteDwarfData: Estrutura de dados completa para anões
- MemoryReader: Leitor de memória do processo DF
- CompleteDFInstance: Interface principal com Dwarf Fortress
"""

__version__ = "1.0.0"
__author__ = "AI Assistant"
__description__ = "Python implementation of Dwarf Therapist memory reading"

# Importações principais
try:
    from .complete_dwarf_reader import CompleteDwarfData, MemoryReader, CompleteDFInstance
except ImportError:
    # Para execução direta dos scripts
    pass