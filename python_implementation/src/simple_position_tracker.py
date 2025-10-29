"""
Simple Position Tracker - Versão simplificada para rastreamento de posições
Monitora mudanças nos offsets de coordenadas conhecidos
"""

import logging
import time
import json
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import ctypes
from ctypes import wintypes
import psutil

# Setup básico de logging
def setup_logging(log_file: str = "simple_position_tracker.log"):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

@dataclass
class PositionReading:
    """Uma leitura de posição de um anão"""
    dwarf_name: str
    dwarf_address: int
    timestamp: float
    coordinates: Dict[str, Tuple[int, int, int]]  # offset -> (x, y, z)

class SimpleMemoryReader:
    """Leitor de memória simplificado"""
    
    def __init__(self):
        self.process_handle = None
        self.kernel32 = ctypes.windll.kernel32
        
    def find_df_process(self) -> Optional[int]:
        """Encontra o processo do Dwarf Fortress"""
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'Dwarf Fortress.exe':
                return proc.info['pid']
        return None
    
    def open_process(self, pid: int) -> bool:
        """Abre o processo para leitura"""
        PROCESS_VM_READ = 0x0010
        self.process_handle = self.kernel32.OpenProcess(PROCESS_VM_READ, False, pid)
        return self.process_handle != 0
    
    def read_memory(self, address: int, size: int) -> bytes:
        """Lê memória do processo"""
        buffer = ctypes.create_string_buffer(size)
        bytes_read = ctypes.c_size_t()
        
        if self.kernel32.ReadProcessMemory(
            self.process_handle, address, buffer, size, ctypes.byref(bytes_read)
        ):
            return buffer.raw[:bytes_read.value]
        return b''
    
    def read_int32(self, address: int) -> int:
        """Lê um inteiro de 32 bits"""
        data = self.read_memory(address, 4)
        if len(data) == 4:
            return int.from_bytes(data, byteorder='little', signed=True)
        return 0
    
    def close(self):
        """Fecha o handle do processo"""
        if self.process_handle:
            self.kernel32.CloseHandle(self.process_handle)

class SimplePositionTracker:
    """Rastreador de posições simplificado"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.memory_reader = SimpleMemoryReader()
        self.base_addresses = []
        
        # Offsets interessantes baseados na análise anterior
        self.coordinate_offsets = [
            0x134,  # (7, 9, -1) - coordenadas consistentes 
            0x140,  # Coordenadas variáveis - posição real provável
            0xb4,   # (1, 26, 0) - coordenadas de referência
            0xc,    # Valores únicos por anão
            0x6c,   # (0, 0, 1) ou (0, 0, 0)
        ]
        
        self.position_history = []
        
    def connect_to_df(self) -> bool:
        """Conecta ao Dwarf Fortress"""
        try:
            pid = self.memory_reader.find_df_process()
            if not pid:
                self.logger.error("Processo do Dwarf Fortress não encontrado")
                return False
                
            if not self.memory_reader.open_process(pid):
                self.logger.error(f"Falha ao abrir processo PID {pid}")
                return False
                
            self.logger.info(f"Conectado ao DF. PID: {pid}")
            
            # Usar endereços conhecidos dos anões baseados na análise anterior
            # Estes são endereços que funcionaram no location_finder
            self.base_addresses = [
                0x267cbae7040,  # sodel
                0x267cbae84b0,  # skzul  
                0x267cbae9920,  # tobul
                0x267cbaead90,  # thele
                0x267cbaec200,  # lime
                0x267cbaed670,  # mifava
                0x267cbaeede0,  # lolama
                0x267cbaeff50,  # adela
                0x267cbaf13c0,  # rayali
                0x267cbaf2830,  # rovod
            ]
            
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao conectar: {e}")
            return False
    
    def read_dwarf_coordinates(self, dwarf_address: int, dwarf_name: str) -> Dict[str, Tuple[int, int, int]]:
        """Lê coordenadas de um anão específico"""
        coordinates = {}
        
        try:
            for offset in self.coordinate_offsets:
                address = dwarf_address + offset
                
                # Lê 3 inteiros consecutivos (x, y, z)
                x = self.memory_reader.read_int32(address)
                y = self.memory_reader.read_int32(address + 4)
                z = self.memory_reader.read_int32(address + 8)
                
                # Filtros para coordenadas válidas do DF
                if self._is_valid_coordinate(x, y, z):
                    coordinates[f"0x{offset:x}"] = (x, y, z)
                    self.logger.debug(f"{dwarf_name} offset 0x{offset:x}: ({x}, {y}, {z})")
                    
        except Exception as e:
            self.logger.warning(f"Erro ao ler coordenadas de {dwarf_name}: {e}")
            
        return coordinates
    
    def _is_valid_coordinate(self, x: int, y: int, z: int) -> bool:
        """Verifica se coordenadas são válidas"""
        return (0 <= x <= 600 and 
                0 <= y <= 600 and 
                -200 <= z <= 200)
    
    def take_snapshot(self) -> List[PositionReading]:
        """Captura um snapshot das posições"""
        readings = []
        timestamp = time.time()
        
        dwarf_names = ["sodel", "skzul", "tobul", "thele", "lime", 
                      "mifava", "lolama", "adela", "rayali", "rovod"]
        
        for i, address in enumerate(self.base_addresses):
            if i >= len(dwarf_names):
                break
                
            dwarf_name = dwarf_names[i]
            coordinates = self.read_dwarf_coordinates(address, dwarf_name)
            
            if coordinates:
                reading = PositionReading(
                    dwarf_name=dwarf_name,
                    dwarf_address=address,
                    timestamp=timestamp,
                    coordinates=coordinates
                )
                readings.append(reading)
                
        self.position_history.append(readings)
        self.logger.info(f"Snapshot capturado: {len(readings)} anões")
        return readings
    
    def detect_changes(self) -> List[Dict]:
        """Detecta mudanças de posição entre snapshots"""
        changes = []
        
        if len(self.position_history) < 2:
            return changes
            
        current = self.position_history[-1]
        previous = self.position_history[-2]
        
        # Cria dicionários para lookup rápido
        current_dict = {r.dwarf_name: r for r in current}
        previous_dict = {r.dwarf_name: r for r in previous}
        
        for dwarf_name in current_dict:
            if dwarf_name not in previous_dict:
                continue
                
            curr_reading = current_dict[dwarf_name]
            prev_reading = previous_dict[dwarf_name]
            
            # Verifica cada offset para mudanças
            for offset in set(curr_reading.coordinates.keys()) | set(prev_reading.coordinates.keys()):
                curr_coords = curr_reading.coordinates.get(offset)
                prev_coords = prev_reading.coordinates.get(offset)
                
                if curr_coords != prev_coords and curr_coords and prev_coords:
                    change = {
                        "dwarf_name": dwarf_name,
                        "offset": offset,
                        "old_coordinates": prev_coords,
                        "new_coordinates": curr_coords,
                        "timestamp": curr_reading.timestamp,
                        "distance": self._calculate_distance(prev_coords, curr_coords)
                    }
                    changes.append(change)
                    
                    self.logger.info(f"MUDANÇA DETECTADA: {dwarf_name} {offset}: {prev_coords} -> {curr_coords}")
                    
        return changes
    
    def _calculate_distance(self, coord1: Tuple[int, int, int], coord2: Tuple[int, int, int]) -> float:
        """Calcula distância entre duas coordenadas"""
        dx = coord2[0] - coord1[0]
        dy = coord2[1] - coord1[1]
        dz = coord2[2] - coord1[2]
        return (dx*dx + dy*dy + dz*dz) ** 0.5
    
    def monitor_positions(self, duration_seconds: int = 30, interval_seconds: int = 3):
        """Monitora posições por um período"""
        self.logger.info(f"Iniciando monitoramento por {duration_seconds}s (intervalo: {interval_seconds}s)")
        
        start_time = time.time()
        snapshot_count = 0
        all_changes = []
        
        while time.time() - start_time < duration_seconds:
            snapshot_count += 1
            self.logger.info(f"Snapshot {snapshot_count}")
            
            # Captura snapshot
            readings = self.take_snapshot()
            
            # Detecta mudanças se não é o primeiro
            if snapshot_count > 1:
                changes = self.detect_changes()
                all_changes.extend(changes)
                
            # Aguarda próximo intervalo
            time.sleep(interval_seconds)
            
        self.logger.info(f"Monitoramento concluído. {snapshot_count} snapshots, {len(all_changes)} mudanças")
        
        # Análise dos resultados
        analysis = self.analyze_changes(all_changes)
        return analysis
    
    def analyze_changes(self, changes: List[Dict]) -> Dict:
        """Analisa as mudanças detectadas"""
        analysis = {
            "total_changes": len(changes),
            "changes_by_offset": {},
            "changes_by_dwarf": {},
            "movement_patterns": {},
            "recommendations": []
        }
        
        # Conta mudanças por offset
        for change in changes:
            offset = change["offset"]
            dwarf = change["dwarf_name"]
            
            if offset not in analysis["changes_by_offset"]:
                analysis["changes_by_offset"][offset] = 0
            analysis["changes_by_offset"][offset] += 1
            
            if dwarf not in analysis["changes_by_dwarf"]:
                analysis["changes_by_dwarf"][dwarf] = 0
            analysis["changes_by_dwarf"][dwarf] += 1
            
        # Identifica offset mais ativo
        if analysis["changes_by_offset"]:
            most_active_offset = max(analysis["changes_by_offset"].items(), key=lambda x: x[1])
            analysis["most_active_offset"] = most_active_offset[0]
            analysis["most_active_changes"] = most_active_offset[1]
            
            # Recomendações
            if most_active_offset[1] >= 3:
                analysis["recommendations"].append(
                    f"Offset {most_active_offset[0]} é o melhor candidato para posição real "
                    f"({most_active_offset[1]} mudanças detectadas)"
                )
            else:
                analysis["recommendations"].append(
                    "Poucas mudanças detectadas. Mova mais anões para melhor análise."
                )
        else:
            analysis["recommendations"].append(
                "Nenhuma mudança detectada. Certifique-se de mover anões durante o monitoramento."
            )
            
        return analysis
    
    def export_results(self, analysis: Dict, changes: List[Dict]) -> str:
        """Exporta resultados"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        exports_dir = Path(__file__).parent.parent / "exports"
        exports_dir.mkdir(exist_ok=True)
        
        filename = f"simple_position_tracking_{timestamp}.json"
        filepath = exports_dir / filename
        
        export_data = {
            "analysis_type": "simple_position_tracking",
            "description": "Rastreamento simplificado de mudanças de posição",
            "analysis": analysis,
            "detected_changes": changes,
            "coordinate_offsets_tested": [f"0x{offset:x}" for offset in self.coordinate_offsets],
            "timestamp": timestamp
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
            
        self.logger.info(f"Resultados exportados para: {filepath}")
        return str(filepath)
    
    def disconnect(self):
        """Desconecta do processo"""
        self.memory_reader.close()

def main():
    """Função principal"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    print("=== SIMPLE POSITION TRACKER ===")
    print()
    print("Rastreador simplificado de mudanças de posição dos anões")
    print()
    print("INSTRUÇÕES:")
    print("1. Deixe o Dwarf Fortress aberto")
    print("2. Durante o monitoramento, MOVA ALGUNS ANÕES NO JOGO")
    print("3. O script detectará mudanças nos offsets de coordenadas")
    print()
    
    tracker = SimplePositionTracker()
    
    # Conecta ao DF
    if not tracker.connect_to_df():
        print("❌ Erro: Não foi possível conectar ao Dwarf Fortress")
        return
        
    print("✅ Conectado ao Dwarf Fortress")
    print()
    
    # Configuração do monitoramento
    try:
        duration = int(input("Duração do monitoramento em segundos (padrão: 30): ") or "30")
        interval = int(input("Intervalo entre snapshots em segundos (padrão: 3): ") or "3")
    except ValueError:
        duration = 30
        interval = 3
        
    print(f"\n🔍 Iniciando monitoramento por {duration} segundos...")
    print("💡 MOVA ALGUNS ANÕES NO JOGO AGORA!")
    print()
    
    try:
        # Monitora e coleta mudanças
        all_changes = []
        start_time = time.time()
        snapshot_count = 0
        
        while time.time() - start_time < duration:
            snapshot_count += 1
            print(f"📸 Snapshot {snapshot_count}")
            
            readings = tracker.take_snapshot()
            
            if snapshot_count > 1:
                changes = tracker.detect_changes()
                all_changes.extend(changes)
                
                if changes:
                    print(f"   🎯 {len(changes)} mudanças detectadas!")
                    for change in changes:
                        print(f"      {change['dwarf_name']} {change['offset']}: "
                              f"{change['old_coordinates']} -> {change['new_coordinates']}")
                else:
                    print("   ⭕ Nenhuma mudança detectada")
                    
            time.sleep(interval)
            
        # Análise final
        analysis = tracker.analyze_changes(all_changes)
        filepath = tracker.export_results(analysis, all_changes)
        
        print("\n" + "="*60)
        print("ANÁLISE CONCLUÍDA")
        print("="*60)
        
        print(f"\n📊 RESULTADOS:")
        print(f"   Total de mudanças: {analysis['total_changes']}")
        if analysis.get('most_active_offset'):
            print(f"   Offset mais ativo: {analysis['most_active_offset']} ({analysis['most_active_changes']} mudanças)")
        
        print(f"\n💡 RECOMENDAÇÕES:")
        for rec in analysis['recommendations']:
            print(f"   • {rec}")
            
        print(f"\n📁 ARQUIVO: {filepath}")
        
    except KeyboardInterrupt:
        print("\n🛑 Monitoramento interrompido pelo usuário")
    finally:
        tracker.disconnect()

if __name__ == "__main__":
    main()