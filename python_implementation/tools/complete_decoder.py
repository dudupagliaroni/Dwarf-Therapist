#!/usr/bin/env python3
"""
Sistema Completo de Decodificação para Dwarf Therapist
Interpreta e traduz todos os dados brutos para formato legível
"""

import json
from typing import Dict, List, Any, Optional
from pathlib import Path
import sys

# Adicionar o diretório tools ao path
sys.path.append(str(Path(__file__).parent))

from decode_professions import get_profession_names
from decode_skills import get_skill_names

class DwarfDataDecoder:
    """Decodificador central para todos os dados do Dwarf Fortress"""
    
    def __init__(self):
        self.professions = get_profession_names()
        self.skills = get_skill_names()
        self.attributes = self._load_attribute_names()
        self.labors = self._load_labor_names()
        self.races = self._load_race_names()
        self.castes = self._load_caste_names()
        self.moods = self._load_mood_names()
        self.body_parts = self._load_body_parts()
        self.materials = self._load_materials()
        self.item_types = self._load_item_types()
        
    def _load_attribute_names(self) -> Dict[int, str]:
        """Nomes dos atributos físicos e mentais"""
        return {
            # Atributos Físicos
            0: "Strength",
            1: "Agility", 
            2: "Toughness",
            3: "Endurance",
            4: "Recuperation",
            5: "Disease Resistance",
            
            # Atributos Mentais
            6: "Analytical Ability",
            7: "Focus",
            8: "Willpower", 
            9: "Creativity",
            10: "Intuition",
            11: "Patience",
            12: "Memory",
            13: "Linguistic Ability",
            14: "Spatial Sense",
            15: "Musicality",
            16: "Kinesthetic Sense",
            17: "Empathy",
            18: "Social Awareness"
        }
        
    def _load_labor_names(self) -> Dict[int, str]:
        """Nomes dos trabalhos/labors"""
        return {
            0: "Mine",
            1: "Cut Wood", 
            2: "Carpentry",
            3: "Stonework",
            4: "Engraving",
            5: "Masonry",
            6: "Animal Care",
            7: "Animal Training",
            8: "Hunt",
            9: "Fish",
            10: "Butcher",
            11: "Trap",
            12: "Tan",
            13: "Leatherwork",
            14: "Brew",
            15: "Cook",
            16: "Gather Plants",
            17: "Thresh",
            18: "Mill",
            19: "Process Plants",
            20: "Make Cheese",
            21: "Milk",
            22: "Shear",
            23: "Spin Thread",
            24: "Weave",
            25: "Make Clothes",
            26: "Make Glass",
            27: "Make Pottery"
        }
        
    def _load_race_names(self) -> Dict[int, str]:
        """Nomes das raças"""
        return {
            0: "Dwarf",
            1: "Human", 
            2: "Elf",
            3: "Goblin",
            4: "Kobold",
            5: "Animal",
            # Adicionar mais conforme necessário
        }
        
    def _load_caste_names(self) -> Dict[int, str]:
        """Nomes das castas (gênero/tipo)"""
        return {
            0: "Male",
            1: "Female",
            2: "Neuter"
        }
        
    def _load_mood_names(self) -> Dict[int, str]:
        """Nomes dos estados de humor/mood"""
        return {
            -1: "No Mood",
            0: "Normal",
            1: "Fell Mood",
            2: "Macabre Mood", 
            3: "Fey Mood",
            4: "Secretive Mood",
            5: "Possessed Mood",
            6: "Berserk",
            7: "Melancholy",
            8: "Stark Raving Mad",
            9: "Enraged",
            10: "Depressed"
        }
        
    def _load_body_parts(self) -> Dict[int, str]:
        """Nomes das partes do corpo"""
        return {
            0: "Head",
            1: "Neck", 
            2: "Upper Body",
            3: "Lower Body",
            4: "Left Arm",
            5: "Right Arm",
            6: "Left Leg",
            7: "Right Leg",
            8: "Left Hand",
            9: "Right Hand",
            10: "Left Foot",
            11: "Right Foot"
        }
        
    def _load_materials(self) -> Dict[int, str]:
        """Tipos de materiais"""
        return {
            0: "No Material",
            1: "Stone",
            2: "Metal",
            3: "Wood",
            4: "Leather",
            5: "Cloth",
            6: "Bone",
            7: "Shell",
            8: "Glass",
            9: "Ceramic"
        }
        
    def _load_item_types(self) -> Dict[int, str]:
        """Tipos de itens"""
        return {
            0: "None",
            1: "Weapon",
            2: "Armor",
            3: "Tool",
            4: "Clothing",
            5: "Food",
            6: "Container",
            7: "Furniture"
        }
        
    def decode_dwarf(self, dwarf_data: Dict[str, Any]) -> Dict[str, Any]:
        """Decodifica todos os dados de um dwarf"""
        decoded = dwarf_data.copy()
        
        # Dados básicos decodificados
        decoded['decoded_info'] = {
            'profession_name': self.professions.get(dwarf_data['profession'], f"Unknown Profession ({dwarf_data['profession']})"),
            'race_name': self.races.get(dwarf_data['race'], f"Unknown Race ({dwarf_data['race']})"),
            'caste_name': self.castes.get(dwarf_data['caste'], f"Unknown Caste ({dwarf_data['caste']})"),
            'gender': "Male" if dwarf_data['sex'] == 0 else "Female" if dwarf_data['sex'] == 1 else "Unknown",
            'mood_name': self.moods.get(dwarf_data['mood'], f"Unknown Mood ({dwarf_data['mood']})"),
            'happiness_level': self._decode_happiness(dwarf_data.get('happiness', 0)),
            'stress_level': self._decode_stress(dwarf_data.get('personality', {}).get('stress_level', 0))
        }
        
        # Decodificar skills
        if 'skills' in dwarf_data:
            decoded['skills_decoded'] = [self._decode_skill(skill) for skill in dwarf_data['skills']]
            
        # Decodificar atributos físicos
        if 'physical_attributes' in dwarf_data:
            decoded['physical_attributes_decoded'] = [self._decode_attribute(attr) for attr in dwarf_data['physical_attributes']]
            
        # Decodificar atributos mentais
        if 'mental_attributes' in dwarf_data:
            decoded['mental_attributes_decoded'] = [self._decode_attribute(attr) for attr in dwarf_data['mental_attributes']]
            
        # Decodificar labors
        if 'labors' in dwarf_data:
            decoded['labors_decoded'] = [self._decode_labor(labor) for labor in dwarf_data['labors']]
            
        # Decodificar ferimentos
        if 'wounds' in dwarf_data:
            decoded['wounds_decoded'] = [self._decode_wound(wound) for wound in dwarf_data['wounds']]
            
        # Decodificar equipamentos
        if 'equipment' in dwarf_data:
            decoded['equipment_decoded'] = [self._decode_equipment(item) for item in dwarf_data['equipment']]
            
        # Decodificar personalidade
        if 'personality' in dwarf_data and dwarf_data['personality']:
            decoded['personality_decoded'] = self._decode_personality(dwarf_data['personality'])
            
        return decoded
        
    def _decode_skill(self, skill: Dict[str, Any]) -> Dict[str, Any]:
        """Decodifica um skill individual"""
        decoded = skill.copy()
        skill_id = skill['id']
        
        decoded['skill_name'] = self.skills.get(skill_id, f"Unknown Skill ({skill_id})")
        decoded['level_name'] = self._get_skill_level_name(skill['level'])
        decoded['experience_percentage'] = self._calculate_exp_percentage(skill['level'], skill['experience'])
        
        return decoded
        
    def _decode_attribute(self, attr: Dict[str, Any]) -> Dict[str, Any]:
        """Decodifica um atributo"""
        decoded = attr.copy()
        attr_id = attr['id']
        
        decoded['attribute_name'] = self.attributes.get(attr_id, f"Unknown Attribute ({attr_id})")
        decoded['percentage'] = (attr['value'] / max(attr['max_value'], 1)) * 100 if attr['max_value'] > 0 else 0
        decoded['description'] = self._get_attribute_description(attr['value'])
        
        return decoded
        
    def _decode_labor(self, labor: Dict[str, Any]) -> Dict[str, Any]:
        """Decodifica um labor"""
        decoded = labor.copy()
        labor_id = labor['id']
        
        decoded['labor_name'] = self.labors.get(labor_id, f"Unknown Labor ({labor_id})")
        decoded['status'] = "Enabled" if labor['enabled'] else "Disabled"
        
        return decoded
        
    def _decode_wound(self, wound: Dict[str, Any]) -> Dict[str, Any]:
        """Decodifica um ferimento"""
        decoded = wound.copy()
        
        decoded['body_part_name'] = self.body_parts.get(wound['body_part'], f"Unknown Body Part ({wound['body_part']})")
        decoded['severity'] = self._get_wound_severity(wound['pain'], wound['bleeding'])
        
        return decoded
        
    def _decode_equipment(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Decodifica um equipamento"""
        decoded = item.copy()
        
        decoded['material_name'] = self.materials.get(item['material_type'], f"Unknown Material ({item['material_type']})")
        decoded['item_type_name'] = self.item_types.get(item['item_type'], f"Unknown Item ({item['item_type']})")
        decoded['quality_name'] = self._get_quality_name(item['quality'])
        decoded['wear_description'] = self._get_wear_description(item['wear'])
        
        return decoded
        
    def _decode_personality(self, personality: Dict[str, Any]) -> Dict[str, Any]:
        """Decodifica personalidade"""
        decoded = personality.copy()
        
        decoded['stress_description'] = self._decode_stress(personality['stress_level'])
        decoded['focus_description'] = self._decode_focus(personality['focus_level'])
        
        # Decodificar traits principais (apenas os mais importantes)
        if 'traits' in personality:
            decoded['main_traits'] = self._decode_main_traits(personality['traits'])
            
        return decoded
        
    def _get_skill_level_name(self, level: int) -> str:
        """Converte nível numérico para nome"""
        if level == 0: return "Dabbling"
        elif level == 1: return "Novice"
        elif level == 2: return "Adequate"
        elif level == 3: return "Competent"
        elif level == 4: return "Skilled"
        elif level == 5: return "Proficient"
        elif level == 6: return "Talented"
        elif level == 7: return "Adept"
        elif level == 8: return "Expert"
        elif level == 9: return "Professional"
        elif level == 10: return "Accomplished"
        elif level == 11: return "Great"
        elif level == 12: return "Master"
        elif level == 13: return "High Master"
        elif level == 14: return "Grand Master"
        elif level >= 15: return "Legendary"
        else: return f"Level {level}"
        
    def _calculate_exp_percentage(self, level: int, experience: int) -> float:
        """Calcula percentual de experiência no nível atual"""
        # Experiência necessária por nível (aproximado)
        exp_per_level = [0, 500, 1100, 1800, 2600, 3500, 4500, 5600, 6800, 8100, 9500, 11000, 12600, 14300, 16100, 18000]
        
        if level >= len(exp_per_level) - 1:
            return 100.0
            
        current_level_exp = exp_per_level[level] if level < len(exp_per_level) else level * 1000
        next_level_exp = exp_per_level[level + 1] if level + 1 < len(exp_per_level) else (level + 1) * 1000
        
        if next_level_exp <= current_level_exp:
            return 100.0
            
        progress = ((experience - current_level_exp) / (next_level_exp - current_level_exp)) * 100
        return max(0, min(100, progress))
        
    def _decode_happiness(self, happiness: int) -> str:
        """Decodifica nível de felicidade"""
        if happiness >= 200: return "Ecstatic"
        elif happiness >= 150: return "Very Happy"
        elif happiness >= 100: return "Happy"
        elif happiness >= 50: return "Content"
        elif happiness >= 0: return "Neutral"
        elif happiness >= -50: return "Unhappy"
        elif happiness >= -100: return "Very Unhappy"
        else: return "Miserable"
        
    def _decode_stress(self, stress: int) -> str:
        """Decodifica nível de stress"""
        if stress <= 10000: return "No Stress"
        elif stress <= 25000: return "Low Stress"
        elif stress <= 50000: return "Some Stress"
        elif stress <= 75000: return "Moderate Stress"
        elif stress <= 100000: return "High Stress"
        elif stress <= 150000: return "Very High Stress"
        else: return "Extreme Stress"
        
    def _decode_focus(self, focus: int) -> str:
        """Decodifica nível de foco"""
        if focus >= 5000: return "Very Focused"
        elif focus >= 2500: return "Focused"
        elif focus >= 1000: return "Somewhat Focused"
        elif focus >= 0: return "Normal Focus"
        else: return "Unfocused"
        
    def _get_attribute_description(self, value: int) -> str:
        """Descrição do valor do atributo"""
        if value >= 5000: return "Incredible"
        elif value >= 4500: return "Amazing"
        elif value >= 4000: return "Extraordinary"
        elif value >= 3500: return "Fantastic"
        elif value >= 3000: return "Excellent"
        elif value >= 2500: return "Very Good"
        elif value >= 2000: return "Good"
        elif value >= 1500: return "Above Average"
        elif value >= 1000: return "Average"
        elif value >= 750: return "Below Average"
        elif value >= 500: return "Poor"
        elif value >= 250: return "Very Poor"
        else: return "Abysmal"
        
    def _get_wound_severity(self, pain: int, bleeding: int) -> str:
        """Determina severidade do ferimento"""
        total = pain + bleeding
        if total >= 100: return "Critical"
        elif total >= 50: return "Severe"
        elif total >= 25: return "Moderate"
        elif total >= 10: return "Minor"
        else: return "Negligible"
        
    def _get_quality_name(self, quality: int) -> str:
        """Nome da qualidade do item"""
        qualities = {
            0: "Basic",
            1: "Well-crafted", 
            2: "Finely-crafted",
            3: "Superior",
            4: "Exceptional",
            5: "Masterwork",
            6: "Artifact"
        }
        return qualities.get(quality, f"Quality {quality}")
        
    def _get_wear_description(self, wear: int) -> str:
        """Descrição do desgaste"""
        if wear == 0: return "No Wear"
        elif wear <= 1: return "x"
        elif wear <= 2: return "X"
        elif wear <= 3: return "XX"
        else: return "XXX"
        
    def _decode_main_traits(self, traits: Dict[int, int]) -> List[Dict[str, Any]]:
        """Decodifica os principais traits de personalidade"""
        trait_names = {
            0: "Anxiety", 1: "Courage", 2: "Curiosity", 3: "Excitement-seeking",
            4: "Immoderation", 5: "Violent", 6: "Perseverance", 7: "Pride",
            8: "Vengeful", 9: "Compassion", 10: "Forgiveness", 11: "Honor",
            12: "Justice", 13: "Mercy", 14: "Modesty", 15: "Temperance",
            16: "Chastity", 17: "Greed", 18: "Envy", 19: "Lust",
            20: "Gluttony", 21: "Wrath", 22: "Laziness", 23: "Vanity",
            24: "Ambition"
        }
        
        main_traits = []
        for trait_id, value in traits.items():
            if abs(value - 50) >= 25:  # Apenas traits significativos
                trait_name = trait_names.get(trait_id, f"Trait_{trait_id}")
                tendency = "High" if value > 75 else "Very High" if value > 90 else "Low" if value < 25 else "Very Low" if value < 10 else "Moderate"
                main_traits.append({
                    'name': trait_name,
                    'value': value,
                    'tendency': tendency
                })
                
        return sorted(main_traits, key=lambda x: abs(x['value'] - 50), reverse=True)[:5]  # Top 5 traits

def decode_complete_export(input_file: str, output_file: str = None) -> bool:
    """Decodifica um arquivo JSON completo de export"""
    try:
        input_path = Path(input_file)
        if not input_path.exists():
            print(f"ERRO: Arquivo não encontrado: {input_file}")
            return False
            
        # Definir arquivo de saída
        if output_file is None:
            output_file = input_path.parent / f"{input_path.stem}_decoded{input_path.suffix}"
        
        print(f"Decodificando: {input_file}")
        print(f"Salvando em: {output_file}")
        
        # Carregar dados
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Inicializar decodificador
        decoder = DwarfDataDecoder()
        
        # Decodificar todos os dwarves
        print(f"Decodificando {len(data['dwarves'])} dwarves...")
        decoded_dwarves = []
        
        for i, dwarf in enumerate(data['dwarves']):
            if i % 50 == 0:
                print(f"  Processando dwarf {i+1}/{len(data['dwarves'])}")
            decoded_dwarf = decoder.decode_dwarf(dwarf)
            decoded_dwarves.append(decoded_dwarf)
            
        # Criar dados decodificados
        decoded_data = data.copy()
        decoded_data['dwarves'] = decoded_dwarves
        decoded_data['metadata']['decoded'] = True
        decoded_data['metadata']['decoder_version'] = '1.0'
        
        # Salvar arquivo decodificado
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(decoded_data, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Decodificação concluída: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Erro na decodificação: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Teste com o último arquivo exportado
    from pathlib import Path
    
    exports_dir = Path(__file__).parent.parent.parent / "exports"
    if exports_dir.exists():
        json_files = list(exports_dir.glob("complete_dwarves_data_*.json"))
        if json_files:
            latest_file = sorted(json_files)[-1]
            print(f"Decodificando o arquivo mais recente: {latest_file.name}")
            decode_complete_export(str(latest_file))
        else:
            print("Nenhum arquivo de export encontrado na pasta exports/")
    else:
        print("Pasta exports/ não encontrada")