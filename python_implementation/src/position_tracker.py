"""
Position Tracker - Rastreamento de posições específicas dos anões no DF
Detecta mudanças de posição e identifica os offsets corretos de coordenadas
"""

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Set
from complete_dwarf_reader import CompleteDFInstance

def setup_logging(log_file: str = "position_tracker.log"):
    """Configura o sistema de logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

@dataclass
class PositionSnapshot:
    """Snapshot da posição de um anão em um momento específico"""
    dwarf_id: int
    dwarf_name: str
    timestamp: float
    coordinates: Dict[str, Tuple[int, int, int]]  # offset -> (x, y, z)
    
@dataclass 
class PositionChange:
    """Mudança detectada na posição de um anão"""
    dwarf_id: int
    dwarf_name: str
    offset: str
    old_coords: Tuple[int, int, int]
    new_coords: Tuple[int, int, int]
    timestamp: float

class PositionTracker:
    """Rastrea as posições dos anões para identificar coordenadas verdadeiras"""
    
    def __init__(self):
        self.df_instance = None
        self.logger = logging.getLogger(__name__)
        
        # Offsets interessantes baseados na análise anterior
        self.candidate_offsets = [
            0x134,  # Coordenadas (7, 9, -1) - consistente em muitos anões
            0x140,  # Coordenadas variáveis entre anões
            0xb4,   # Coordenadas (1, 26, 0) - consistente
            0xc,    # Valores únicos por anão (97, 100, 101, 108)
            0x10,   # Sempre (0, 0, 5) ou (0, 0, 6)
            0x14,   # Sempre (0, 5, 0) ou (0, 6, 0)
            0x18,   # Sempre (5, 0, 15) ou (6, 0, 15)
            0x6c,   # (0, 0, 1) ou (0, 0, 0)
        ]
        
        self.position_history: Dict[int, List[PositionSnapshot]] = {}
        self.detected_changes: List[PositionChange] = []
        
    def connect_to_df(self) -> bool:
        """Conecta à instância do DF"""
        try:
            self.df_instance = CompleteDFInstance()
            if not self.df_instance.connect():
                self.logger.error("Falha ao conectar com DF")
                return False
            
            self.logger.info(f"Conectado ao DF. PID: {self.df_instance.pid}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao conectar com DF: {e}")
            return False
    
    def read_dwarf_position_candidates(self, dwarf_id: int, dwarf_name: str, 
                                     base_address: int) -> Dict[str, Tuple[int, int, int]]:
        """Lê as coordenadas candidatas para um anão específico"""
        coordinates = {}
        
        try:
            for offset in self.candidate_offsets:
                address = base_address + offset
                
                # Lê 3 inteiros consecutivos (x, y, z)
                x = self.df_instance.memory_reader.read_int32(address)
                y = self.df_instance.memory_reader.read_int32(address + 4)
                z = self.df_instance.memory_reader.read_int32(address + 8)
                
                # Filtra valores razoáveis para coordenadas do DF
                if self._is_valid_coordinate_set(x, y, z):
                    coordinates[f"0x{offset:x}"] = (x, y, z)
                    
        except Exception as e:
            self.logger.warning(f"Erro ao ler coordenadas do anão {dwarf_name}: {e}")
            
        return coordinates
    
    def _is_valid_coordinate_set(self, x: int, y: int, z: int) -> bool:
        """Verifica se um conjunto de coordenadas é válido para o DF"""
        # Coordenadas do DF geralmente estão em ranges específicos
        # X e Y: 0-200 (tamanho típico do mundo)
        # Z: -50 a 150 (underground a surface)
        return (0 <= x <= 500 and 
                0 <= y <= 500 and 
                -100 <= z <= 200)
    
    def take_position_snapshot(self) -> List[PositionSnapshot]:
        """Captura um snapshot das posições atuais de todos os anões"""
        snapshots = []
        timestamp = time.time()
        
        try:
            # Lê diretamente do vetor de criaturas
            creature_vector_addr = self.df_instance.layout.get_address('creature_vector')
            if not creature_vector_addr:
                self.logger.error("creature_vector não encontrado no layout")
                return snapshots
                
            creature_vector_addr += self.df_instance.base_addr
            creature_pointers = self.df_instance.memory_reader.read_vector(creature_vector_addr, self.df_instance.pointer_size)
            
            self.logger.info(f"Encontradas {len(creature_pointers)} criaturas no vetor")
            
            # Processa apenas os primeiros 10 anões para rapidez
            processed = 0
            for i, creature_addr in enumerate(creature_pointers[:50]):
                if processed >= 10:  # Limita a 10 anões por snapshot
                    break
                    
                try:
                    # Lê o ID da criatura
                    dwarf_id = self.df_instance.memory_reader.read_int32(creature_addr + 0x130)
                    
                    # Lê o nome (simplificado)
                    name_addr = creature_addr + 0x14  # Offset típico do nome
                    dwarf_name = f"dwarf_{dwarf_id}"  # Nome simples por enquanto
                    
                    # Só processa se for um ID válido de anão
                    if 900 <= dwarf_id <= 1000:  # Range típico dos IDs dos anões
                        coordinates = self.read_dwarf_position_candidates(
                            dwarf_id, dwarf_name, creature_addr
                        )
                        
                        if coordinates:
                            snapshot = PositionSnapshot(
                                dwarf_id=dwarf_id,
                                dwarf_name=dwarf_name,
                                timestamp=timestamp,
                                coordinates=coordinates
                            )
                            snapshots.append(snapshot)
                            
                            # Armazena no histórico
                            if dwarf_id not in self.position_history:
                                self.position_history[dwarf_id] = []
                            self.position_history[dwarf_id].append(snapshot)
                            
                            processed += 1
                            
                except Exception as e:
                    self.logger.debug(f"Erro ao processar criatura {i}: {e}")
                    continue
                        
        except Exception as e:
            self.logger.error(f"Erro ao capturar snapshot: {e}")
            
        self.logger.info(f"Capturado snapshot com {len(snapshots)} anões")
        return snapshots
    
    def detect_position_changes(self, max_history: int = 2) -> List[PositionChange]:
        """Detecta mudanças de posição comparando snapshots"""
        changes = []
        
        for dwarf_id, history in self.position_history.items():
            if len(history) < 2:
                continue
                
            # Compara os dois últimos snapshots
            current = history[-1]
            previous = history[-2]
            
            # Verifica cada offset para mudanças
            for offset in set(current.coordinates.keys()) | set(previous.coordinates.keys()):
                curr_coords = current.coordinates.get(offset)
                prev_coords = previous.coordinates.get(offset)
                
                # Se as coordenadas mudaram
                if curr_coords != prev_coords and curr_coords and prev_coords:
                    change = PositionChange(
                        dwarf_id=dwarf_id,
                        dwarf_name=current.dwarf_name,
                        offset=offset,
                        old_coords=prev_coords,
                        new_coords=curr_coords,
                        timestamp=current.timestamp
                    )
                    changes.append(change)
                    self.detected_changes.append(change)
                    
        if changes:
            self.logger.info(f"Detectadas {len(changes)} mudanças de posição")
            
        return changes
    
    def analyze_position_patterns(self) -> Dict:
        """Analisa padrões nas mudanças de posição para identificar offsets verdadeiros"""
        analysis = {
            "change_frequency_by_offset": {},
            "coordinate_ranges_by_offset": {},
            "most_active_offsets": [],
            "position_correlations": {},
            "summary": {}
        }
        
        # Conta frequência de mudanças por offset
        offset_changes = {}
        offset_ranges = {}
        
        for change in self.detected_changes:
            offset = change.offset
            
            if offset not in offset_changes:
                offset_changes[offset] = 0
                offset_ranges[offset] = {
                    'x': [float('inf'), float('-inf')],
                    'y': [float('inf'), float('-inf')], 
                    'z': [float('inf'), float('-inf')]
                }
                
            offset_changes[offset] += 1
            
            # Atualiza ranges de coordenadas
            for i, coord in enumerate(['x', 'y', 'z']):
                old_val = change.old_coords[i]
                new_val = change.new_coords[i]
                
                offset_ranges[offset][coord][0] = min(offset_ranges[offset][coord][0], old_val, new_val)
                offset_ranges[offset][coord][1] = max(offset_ranges[offset][coord][1], old_val, new_val)
        
        analysis["change_frequency_by_offset"] = offset_changes
        analysis["coordinate_ranges_by_offset"] = offset_ranges
        
        # Identifica offsets mais ativos (mais prováveis de serem posição real)
        sorted_offsets = sorted(offset_changes.items(), key=lambda x: x[1], reverse=True)
        analysis["most_active_offsets"] = sorted_offsets[:5]
        
        # Analisa correlações - offsets que mudam juntos
        correlations = {}
        for change1 in self.detected_changes:
            for change2 in self.detected_changes:
                if (change1.dwarf_id == change2.dwarf_id and 
                    change1.offset != change2.offset and
                    abs(change1.timestamp - change2.timestamp) < 1.0):  # Mudanças simultâneas
                    
                    key = f"{change1.offset}+{change2.offset}"
                    if key not in correlations:
                        correlations[key] = 0
                    correlations[key] += 1
                    
        analysis["position_correlations"] = correlations
        
        # Resumo da análise
        analysis["summary"] = {
            "total_changes_detected": len(self.detected_changes),
            "unique_offsets_changed": len(offset_changes),
            "most_likely_position_offset": sorted_offsets[0][0] if sorted_offsets else None,
            "recommendation": self._generate_recommendation(sorted_offsets, offset_ranges)
        }
        
        return analysis
    
    def _generate_recommendation(self, sorted_offsets: List, offset_ranges: Dict) -> str:
        """Gera recomendação baseada na análise"""
        if not sorted_offsets:
            return "Nenhuma mudança detectada. Mova alguns anões no jogo e tente novamente."
            
        most_active = sorted_offsets[0]
        offset, changes = most_active
        
        if changes >= 3:
            range_info = offset_ranges.get(offset, {})
            return f"Offset {offset} é o candidato mais provável para posição (mudou {changes} vezes). " \
                   f"Ranges: X({range_info.get('x', [0,0])}), Y({range_info.get('y', [0,0])}), Z({range_info.get('z', [0,0])})"
        else:
            return "Poucas mudanças detectadas. Recomenda-se mais observação."
    
    def monitor_positions(self, duration_seconds: int = 60, interval_seconds: int = 5):
        """Monitora posições por um período específico"""
        self.logger.info(f"Iniciando monitoramento por {duration_seconds}s (intervalo: {interval_seconds}s)")
        
        start_time = time.time()
        snapshot_count = 0
        
        while time.time() - start_time < duration_seconds:
            snapshot_count += 1
            self.logger.info(f"Snapshot {snapshot_count}")
            
            # Captura snapshot atual
            snapshots = self.take_position_snapshot()
            
            # Detecta mudanças se não é o primeiro snapshot
            if snapshot_count > 1:
                changes = self.detect_position_changes()
                if changes:
                    for change in changes:
                        self.logger.info(f"MUDANÇA: {change.dwarf_name} offset {change.offset}: "
                                       f"{change.old_coords} -> {change.new_coords}")
                        
            # Aguarda próximo intervalo
            time.sleep(interval_seconds)
            
        self.logger.info(f"Monitoramento concluído. {snapshot_count} snapshots capturados.")
        
        # Realiza análise final
        analysis = self.analyze_position_patterns()
        return analysis
    
    def export_results(self, analysis: Dict) -> str:
        """Exporta os resultados da análise"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        exports_dir = Path(__file__).parent.parent / "exports"
        exports_dir.mkdir(exist_ok=True)
        
        filename = f"position_tracking_{timestamp}.json"
        filepath = exports_dir / filename
        
        export_data = {
            "analysis_type": "position_tracking",
            "description": "Rastreamento de mudanças de posição dos anões",
            "tracking_results": analysis,
            "position_history": {
                dwarf_id: [
                    {
                        "timestamp": snap.timestamp,
                        "dwarf_name": snap.dwarf_name,
                        "coordinates": snap.coordinates
                    }
                    for snap in history
                ]
                for dwarf_id, history in self.position_history.items()
            },
            "detected_changes": [
                {
                    "dwarf_id": change.dwarf_id,
                    "dwarf_name": change.dwarf_name,
                    "offset": change.offset,
                    "old_coords": change.old_coords,
                    "new_coords": change.new_coords,
                    "timestamp": change.timestamp
                }
                for change in self.detected_changes
            ]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
            
        self.logger.info(f"Resultados exportados para: {filepath}")
        return str(filepath)

def main():
    """Função principal"""
    setup_logging("position_tracker.log")
    logger = logging.getLogger(__name__)
    
    print("=== POSITION TRACKER - Rastreador de Posições ===")
    print()
    print("Este script monitora mudanças de posição dos anões para identificar")
    print("os offsets corretos de coordenadas na memória do DF.")
    print()
    print("INSTRUÇÕES:")
    print("1. Deixe o Dwarf Fortress aberto")
    print("2. Durante o monitoramento, mova alguns anões no jogo")  
    print("3. Aguarde o script detectar as mudanças de posição")
    print()
    
    tracker = PositionTracker()
    
    # Conecta ao DF
    if not tracker.connect_to_df():
        print("❌ Erro: Não foi possível conectar ao Dwarf Fortress")
        print("Certifique-se de que o jogo está rodando e tente novamente.")
        return
        
    print("✅ Conectado ao Dwarf Fortress")
    print()
    
    # Pergunta duração do monitoramento
    try:
        duration = int(input("Digite a duração do monitoramento em segundos (padrão: 60): ") or "60")
        interval = int(input("Digite o intervalo entre snapshots em segundos (padrão: 5): ") or "5")
    except ValueError:
        duration = 60
        interval = 5
        
    print(f"\n🔍 Iniciando monitoramento por {duration} segundos...")
    print("💡 MOVA ALGUNS ANÕES NO JOGO para detectar mudanças de posição!")
    print()
    
    # Monitora posições
    analysis = tracker.monitor_positions(duration, interval)
    
    # Exporta resultados
    filepath = tracker.export_results(analysis)
    
    print("\n" + "="*60)
    print("ANÁLISE DE RASTREAMENTO DE POSIÇÕES CONCLUÍDA")
    print("="*60)
    
    print(f"\n📊 RESUMO:")
    summary = analysis.get("summary", {})
    print(f"   Mudanças detectadas: {summary.get('total_changes_detected', 0)}")
    print(f"   Offsets únicos: {summary.get('unique_offsets_changed', 0)}")
    print(f"   Offset mais provável: {summary.get('most_likely_position_offset', 'N/A')}")
    print(f"\n💡 RECOMENDAÇÃO:")
    print(f"   {summary.get('recommendation', 'N/A')}")
    
    print(f"\n📁 RESULTADOS:")
    print(f"   Arquivo: {filepath}")
    print(f"   Log: position_tracker.log")
    
    if analysis.get("most_active_offsets"):
        print(f"\n🎯 OFFSETS MAIS ATIVOS:")
        for offset, changes in analysis["most_active_offsets"]:
            print(f"   {offset}: {changes} mudanças")

if __name__ == "__main__":
    main()