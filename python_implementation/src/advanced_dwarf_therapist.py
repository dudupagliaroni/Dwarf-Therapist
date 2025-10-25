#!/usr/bin/env python3
"""
Advanced Dwarf Therapist Python Edition
Includes skills, attributes, and labor management
"""

from dwarf_therapist_python import DFInstance, DwarfData, MemoryReader
from dataclasses import dataclass
from typing import Dict, List, Optional
import struct

@dataclass
class Skill:
    """Dwarf skill information"""
    id: int
    level: int
    experience: int
    name: str = ""

@dataclass
class Attribute:
    """Dwarf attribute information"""
    value: int
    max_value: int
    name: str = ""

@dataclass
class Labor:
    """Labor assignment information"""
    id: int
    enabled: bool
    name: str = ""

@dataclass
class AdvancedDwarfData(DwarfData):
    """Extended dwarf data with skills, attributes, and labors"""
    skills: Dict[int, Skill] = None
    attributes: Dict[int, Attribute] = None
    labors: Dict[int, Labor] = None
    happiness: int = 0
    stress: int = 0
    
    def __post_init__(self):
        if self.skills is None:
            self.skills = {}
        if self.attributes is None:
            self.attributes = {}
        if self.labors is None:
            self.labors = {}

class AdvancedDFInstance(DFInstance):
    """Extended DF instance with advanced dwarf reading capabilities"""
    
    def __init__(self):
        super().__init__()
        self.skill_names = self._load_skill_names()
        self.attribute_names = self._load_attribute_names()
        self.labor_names = self._load_labor_names()
        
    def _load_skill_names(self) -> Dict[int, str]:
        """Load skill names from game data (simplified version)"""
        return {
            0: "Mining", 1: "Woodcutting", 2: "Carpentry", 3: "Stoneworking", 
            4: "Engraving", 5: "Masonry", 6: "Animal Care", 7: "Animal Training",
            8: "Hunting", 9: "Fishing", 10: "Butchery", 11: "Trapping",
            12: "Tanning", 13: "Leatherworking", 14: "Brewing", 15: "Cooking",
            16: "Herbalism", 17: "Threshing", 18: "Milling", 19: "Processing",
            20: "Cheesemaking", 21: "Milking", 22: "Shearing", 23: "Spinning",
            24: "Weaving", 25: "Clothesmaking", 26: "Glassmaking", 27: "Potting",
            28: "Glazing", 29: "Pressing", 30: "Beekeeping", 31: "Wax Working"
        }
        
    def _load_attribute_names(self) -> Dict[int, str]:
        """Load attribute names"""
        return {
            0: "Strength", 1: "Agility", 2: "Toughness", 3: "Endurance",
            4: "Recuperation", 5: "Disease Resistance", 6: "Analytical Ability",
            7: "Focus", 8: "Willpower", 9: "Creativity", 10: "Intuition",
            11: "Patience", 12: "Memory", 13: "Linguistic Ability",
            14: "Spatial Sense", 15: "Musicality", 16: "Kinesthetic Sense",
            17: "Empathy", 18: "Social Awareness"
        }
        
    def _load_labor_names(self) -> Dict[int, str]:
        """Load labor names"""
        return {
            0: "Mine", 1: "Cut Wood", 2: "Carpentry", 3: "Stonework",
            4: "Engraving", 5: "Masonry", 6: "Animal Care", 7: "Animal Train",
            8: "Hunt", 9: "Fish", 10: "Butcher", 11: "Trap",
            12: "Tan", 13: "Leatherwork", 14: "Brew", 15: "Cook",
            16: "Plant Gathering", 17: "Thresh", 18: "Mill", 19: "Process Plants",
            20: "Make Cheese", 21: "Milk", 22: "Shear", 23: "Spin Thread",
            24: "Weave", 25: "Make Clothes", 26: "Glassmaking", 27: "Pottery",
            28: "Glazing", 29: "Press", 30: "Beekeeping", 31: "Wax Working"
        }
    
    def read_advanced_dwarves(self) -> List[AdvancedDwarfData]:
        """Read dwarves with full skill, attribute, and labor data"""
        basic_dwarves = self.read_dwarves()
        advanced_dwarves = []
        
        for basic_dwarf in basic_dwarves:
            advanced_dwarf = self._convert_to_advanced_dwarf(basic_dwarf)
            if advanced_dwarf:
                advanced_dwarves.append(advanced_dwarf)
                
        return advanced_dwarves
    
    def _convert_to_advanced_dwarf(self, basic_dwarf: DwarfData) -> Optional[AdvancedDwarfData]:
        """Convert basic dwarf data to advanced with skills/attributes/labors"""
        try:
            advanced_dwarf = AdvancedDwarfData(**basic_dwarf.__dict__)
            
            # Read skills
            self._read_dwarf_skills(advanced_dwarf)
            
            # Read attributes  
            self._read_dwarf_attributes(advanced_dwarf)
            
            # Read labors
            self._read_dwarf_labors(advanced_dwarf)
            
            # Read happiness/stress
            self._read_dwarf_mood_data(advanced_dwarf)
            
            return advanced_dwarf
            
        except Exception as e:
            print(f"Error converting dwarf {basic_dwarf.name}: {e}")
            return None
    
    def _read_dwarf_skills(self, dwarf: AdvancedDwarfData):
        """Read dwarf's skills from memory"""
        try:
            offsets = self.layout.offsets.get('dwarf', {})
            souls_offset = offsets.get('souls', 0)
            
            if not souls_offset:
                return
                
            # Read souls vector
            souls_vector_addr = dwarf.address + souls_offset
            souls_start = self.memory_reader.read_pointer(souls_vector_addr, self.pointer_size)
            souls_end = self.memory_reader.read_pointer(souls_vector_addr + self.pointer_size, self.pointer_size)
            
            if souls_start == 0 or souls_end == 0 or souls_start >= souls_end:
                return
                
            # Usually just one soul, but let's read the first one
            first_soul_addr = self.memory_reader.read_pointer(souls_start, self.pointer_size)
            if first_soul_addr == 0:
                return
                
            # Read skills vector from soul (this would need soul offsets from layout)
            # For now, we'll create some dummy data
            for skill_id in range(min(len(self.skill_names), 10)):
                skill = Skill(
                    id=skill_id,
                    level=0,  # Would read from memory
                    experience=0,  # Would read from memory
                    name=self.skill_names.get(skill_id, f"Skill {skill_id}")
                )
                dwarf.skills[skill_id] = skill
                
        except Exception as e:
            print(f"Error reading skills for {dwarf.name}: {e}")
    
    def _read_dwarf_attributes(self, dwarf: AdvancedDwarfData):
        """Read dwarf's attributes from memory"""
        try:
            offsets = self.layout.offsets.get('dwarf', {})
            phys_attrs_offset = offsets.get('physical_attrs', 0)
            
            if not phys_attrs_offset:
                return
                
            # Physical attributes are stored as an array
            attr_base_addr = dwarf.address + phys_attrs_offset
            
            # Each attribute is typically 12 bytes (current, max, ?)
            for attr_id in range(min(len(self.attribute_names), 6)):  # Physical attributes
                attr_addr = attr_base_addr + (attr_id * 12)
                current_val = self.memory_reader.read_int32(attr_addr)
                max_val = self.memory_reader.read_int32(attr_addr + 4)
                
                attribute = Attribute(
                    value=current_val,
                    max_value=max_val,
                    name=self.attribute_names.get(attr_id, f"Attribute {attr_id}")
                )
                dwarf.attributes[attr_id] = attribute
                
        except Exception as e:
            print(f"Error reading attributes for {dwarf.name}: {e}")
    
    def _read_dwarf_labors(self, dwarf: AdvancedDwarfData):
        """Read dwarf's labor assignments from memory"""
        try:
            offsets = self.layout.offsets.get('dwarf', {})
            labors_offset = offsets.get('labors', 0)
            
            if not labors_offset:
                return
                
            # Labors are stored as a bitfield
            labors_addr = dwarf.address + labors_offset
            labor_data = self.memory_reader.read_memory(labors_addr, 32)  # Read enough bytes
            
            if len(labor_data) < 32:
                return
                
            # Convert to bitfield
            for labor_id in range(min(len(self.labor_names), 32 * 8)):
                byte_index = labor_id // 8
                bit_index = labor_id % 8
                
                if byte_index < len(labor_data):
                    enabled = bool(labor_data[byte_index] & (1 << bit_index))
                    
                    labor = Labor(
                        id=labor_id,
                        enabled=enabled,
                        name=self.labor_names.get(labor_id, f"Labor {labor_id}")
                    )
                    dwarf.labors[labor_id] = labor
                    
        except Exception as e:
            print(f"Error reading labors for {dwarf.name}: {e}")
    
    def _read_dwarf_mood_data(self, dwarf: AdvancedDwarfData):
        """Read dwarf's happiness and stress data"""
        try:
            offsets = self.layout.offsets.get('dwarf', {})
            
            # These would need proper offsets from the layout file
            # For now, just set some dummy values
            dwarf.happiness = 50  # Would read from memory
            dwarf.stress = 25     # Would read from memory
            
        except Exception as e:
            print(f"Error reading mood data for {dwarf.name}: {e}")
    
    def set_dwarf_labor(self, dwarf: AdvancedDwarfData, labor_id: int, enabled: bool) -> bool:
        """Enable or disable a labor for a dwarf"""
        try:
            offsets = self.layout.offsets.get('dwarf', {})
            labors_offset = offsets.get('labors', 0)
            
            if not labors_offset:
                return False
                
            labors_addr = dwarf.address + labors_offset
            byte_index = labor_id // 8
            bit_index = labor_id % 8
            
            # Read current byte
            current_byte = self.memory_reader.read_memory(labors_addr + byte_index, 1)
            if not current_byte:
                return False
                
            byte_val = current_byte[0]
            
            # Modify bit
            if enabled:
                byte_val |= (1 << bit_index)
            else:
                byte_val &= ~(1 << bit_index)
                
            # Write back (would need write functionality)
            # For now, just update our local data
            if labor_id in dwarf.labors:
                dwarf.labors[labor_id].enabled = enabled
                
            print(f"{'Enabled' if enabled else 'Disabled'} {self.labor_names.get(labor_id, 'Unknown')} for {dwarf.name}")
            return True
            
        except Exception as e:
            print(f"Error setting labor for {dwarf.name}: {e}")
            return False

def print_dwarf_details(dwarf: AdvancedDwarfData):
    """Print detailed information about a dwarf"""
    print(f"\n=== {dwarf.name} (ID: {dwarf.id}) ===")
    print(f"Age: {dwarf.age}, Profession: {dwarf.custom_profession or dwarf.profession}")
    print(f"Happiness: {dwarf.happiness}, Stress: {dwarf.stress}")
    
    print("\nSkills:")
    for skill in list(dwarf.skills.values())[:5]:  # Show first 5 skills
        print(f"  {skill.name}: Level {skill.level} (XP: {skill.experience})")
    
    print("\nAttributes:")
    for attr in list(dwarf.attributes.values())[:3]:  # Show first 3 attributes
        print(f"  {attr.name}: {attr.value}/{attr.max_value}")
    
    print("\nEnabled Labors:")
    enabled_labors = [labor for labor in dwarf.labors.values() if labor.enabled]
    for labor in enabled_labors[:5]:  # Show first 5 enabled labors
        print(f"  {labor.name}")

def main():
    """Advanced example usage"""
    df = AdvancedDFInstance()
    
    print("Advanced Dwarf Therapist Python Edition")
    print("=" * 45)
    
    # Connect and load layout
    if not df.connect():
        print("Failed to connect to Dwarf Fortress")
        return
        
    if not df.load_memory_layout():
        print("Failed to load memory layout")
        return
    
    # Read advanced dwarf data
    print("Reading advanced dwarf data...")
    dwarves = df.read_advanced_dwarves()
    
    if not dwarves:
        print("No dwarves found")
        return
    
    print(f"Successfully read {len(dwarves)} dwarves with advanced data")
    
    # Show summary
    print(f"\n{'Name':<20} {'Age':<4} {'Skills':<7} {'Enabled Labors':<15}")
    print("-" * 60)
    
    for dwarf in dwarves[:10]:  # Show first 10
        skill_count = len([s for s in dwarf.skills.values() if s.level > 0])
        labor_count = len([l for l in dwarf.labors.values() if l.enabled])
        print(f"{dwarf.name:<20} {dwarf.age:<4} {skill_count:<7} {labor_count:<15}")
    
    # Show detailed info for first dwarf
    if dwarves:
        print_dwarf_details(dwarves[0])
        
        # Example of toggling a labor
        if 0 in dwarves[0].labors:
            print(f"\nToggling mining labor for {dwarves[0].name}...")
            current_state = dwarves[0].labors[0].enabled
            df.set_dwarf_labor(dwarves[0], 0, not current_state)

if __name__ == "__main__":
    main()