# Equipment Decoder Documentation

## Overview
The `EquipmentDecoder` class provides human-readable interpretation of equipment-related numeric fields in Dwarf Fortress memory data. It translates raw numeric values into meaningful information about item types, quality levels, and wear conditions.

## Implementation Details

### Location
- **File**: `python_implementation/src/complete_dwarf_reader.py`
- **Lines**: ~650-800 (after `HumanReadableDecoder` class)
- **Integration**: Used in `CompletelyDwarfData.to_dict()` method when `human_readable=True`

### Data Sources
All mappings are based on official Dwarf Therapist C++ source code:
- **ITEM_TYPE enum**: `src/global_enums.h` (lines 60-170)
- **Quality system**: `src/item.cpp` `get_quality_symbol()` (lines 200-300)
- **Wear system**: `src/item.cpp` `build_display_name()` (lines 200-300)

## Class Structure

### ITEM_TYPES Dictionary
Maps numeric IDs (0-90+) to item type names from the `ITEM_TYPE` enum.

**Key Examples**:
```python
-1: "NONE"      # No item / invalid
0: "BAR"        # Metal bar
24: "WEAPON"    # Any weapon
25: "ARMOR"     # Body armor
28: "HELM"      # Helmet
60: "PANTS"     # Trousers
90: "SHEET"     # Paper/parchment
```

**Total**: ~91 item types covering all DF items from materials to equipment to consumables.

### QUALITY_LEVELS Dictionary
Maps quality values (-1 to 6) to descriptive information.

**Structure**:
```python
{
    level: {
        "name": str,         # Quality name
        "symbol": str,       # DF display symbol
        "description": str   # Full description
    }
}
```

**Levels**:
| Level | Name | Symbol | Display |
|-------|------|--------|---------|
| -1 | none | | none |
| 0 | normal | | normal |
| 1 | well-crafted | - | -well-crafted- |
| 2 | finely-crafted | + | +finely-crafted+ |
| 3 | superior | * | *superior* |
| 4 | exceptional | ≡ | ≡exceptional≡ |
| 5 | masterwork | ☼ | ☼masterwork☼ |
| 6 | artifact | ! | !artifact! |

**Special Cases**:
- Sentinel value `4294967295` (0xFFFFFFFF) → treated as `-1` (none)
- Values > 100 → treated as `-1` (likely invalid pointers)

### WEAR_LEVELS Dictionary
Maps wear values (0-3) to condition information.

**Structure**:
```python
{
    level: {
        "name": str,           # Condition name
        "symbol": str,         # DF wear marker
        "description": str,    # Full description
        "percentage": int      # Estimated condition %
    }
}
```

**Levels**:
| Level | Name | Symbol | Condition | Description |
|-------|------|--------|-----------|-------------|
| 0 | new | | 100% | New condition |
| 1 | worn | x | 66% | Worn |
| 2 | threadbare | X | 33% | Threadbare |
| 3 | tattered | XX | 10% | Tattered (nearly destroyed) |

**Special Cases**:
- Sentinel value `4294967295` → treated as `0` (new)
- Values > 100 → treated as `0` (default to new condition)

## Methods

### decode_item_type(item_type: int) → Dict[str, Any]
Translates ITEM_TYPE enum value to readable type information.

**Returns**:
```python
{
    "valid": bool,           # True if type is recognized
    "type_id": int,          # Original numeric ID
    "type_name": str,        # Enum constant name (e.g., "ARMOR")
    "display_text": str      # Formatted display name (e.g., "Armor")
}
```

**Example**:
```python
decode_item_type(25)
# Returns: {"valid": true, "type_id": 25, "type_name": "ARMOR", "display_text": "Armor"}

decode_item_type(999)
# Returns: {"valid": false, "type_id": 999, "type_name": "UNKNOWN", "display_text": "Unknown Type (999)"}
```

### decode_quality(quality: int) → Dict[str, Any]
Interprets quality level (0-6 scale) with sentinel handling.

**Returns**:
```python
{
    "valid": bool,           # True if quality is valid
    "level": int,            # Normalized quality level
    "name": str,             # Quality name
    "symbol": str,           # DF symbol (e.g., "☼")
    "description": str,      # Full description
    "display_text": str      # Formatted display (e.g., "☼masterwork☼")
}
```

**Example**:
```python
decode_quality(5)
# Returns: {
#     "valid": true,
#     "level": 5,
#     "name": "masterwork",
#     "symbol": "☼",
#     "description": "Masterwork",
#     "display_text": "☼masterwork☼"
# }

decode_quality(4294967295)  # Sentinel value
# Returns: {"valid": true, "level": -1, "name": "none", ...}
```

### decode_wear(wear: int) → Dict[str, Any]
Interprets wear/condition level (0-3 scale) with percentage estimation.

**Returns**:
```python
{
    "valid": bool,                # True if wear level is valid
    "level": int,                 # Normalized wear level
    "name": str,                  # Condition name
    "symbol": str,                # DF wear symbol (e.g., "X")
    "description": str,           # Full description
    "condition_percentage": int,  # Estimated condition %
    "display_text": str           # Formatted display (e.g., "X threadbare (33%)")
}
```

**Example**:
```python
decode_wear(2)
# Returns: {
#     "valid": true,
#     "level": 2,
#     "name": "threadbare",
#     "symbol": "X",
#     "description": "Threadbare",
#     "condition_percentage": 33,
#     "display_text": "X threadbare (33%)"
# }
```

### decode_equipment_item(item: Dict[str, Any]) → Dict[str, Any]
High-level method that decodes all equipment fields for a single item.

**Input**: Equipment dictionary with fields:
```python
{
    "item_id": int,
    "item_type": int,
    "material_type": int,
    "material_index": int,
    "quality": int,
    "wear": int
}
```

**Returns**:
```python
{
    "item_type": {...},      # Decoded item type info
    "quality": {...},        # Decoded quality info
    "wear": {...},           # Decoded wear info
    "raw_values": {          # Original values for reference
        "item_id": int,
        "item_type": int,
        "material_type": int,
        "material_index": int,
        "quality": int,
        "wear": int
    }
}
```

**Example**:
```python
item = {
    "item_id": 12345,
    "item_type": 25,      # ARMOR
    "material_type": 1,
    "material_index": 0,
    "quality": 5,         # Masterwork
    "wear": 0             # New
}

decoded = decode_equipment_item(item)
# Returns full decoded structure with all three decoders applied
```

## Integration with JSON Export

### Usage in CompletelyDwarfData.to_dict()
When `human_readable=True`, equipment decoding is automatically applied:

```python
def to_dict(self, human_readable: bool = False):
    # ... existing code ...
    
    if human_readable:
        result['_decoded'] = {
            'flags': HumanReadableDecoder.decode_flags(...),
            'body': HumanReadableDecoder.interpret_body_size(...),
            'blood': HumanReadableDecoder.analyze_blood_level(...),
            'history': HumanReadableDecoder.validate_hist_id(...),
            'squad': HumanReadableDecoder.decode_squad_info(...),
            'pet': HumanReadableDecoder.decode_pet_owner(...),
            'equipment': [EquipmentDecoder.decode_equipment_item(item) 
                         for item in result.get('equipment', [])]  # NEW!
        }
    
    return result
```

### JSON Output Structure
Each dwarf's equipment list will have decoded entries:

```json
{
  "name": "Urist McArmorsmith",
  "equipment": [
    {
      "item_id": 12345,
      "item_type": 25,
      "quality": 5,
      "wear": 0,
      "material_type": 1,
      "material_index": 0
    }
  ],
  "_decoded": {
    "equipment": [
      {
        "item_type": {
          "valid": true,
          "type_id": 25,
          "type_name": "ARMOR",
          "display_text": "Armor"
        },
        "quality": {
          "valid": true,
          "level": 5,
          "name": "masterwork",
          "symbol": "☼",
          "description": "Masterwork",
          "display_text": "☼masterwork☼"
        },
        "wear": {
          "valid": true,
          "level": 0,
          "name": "new",
          "condition_percentage": 100,
          "display_text": "new (100%)"
        },
        "raw_values": {
          "item_id": 12345,
          "item_type": 25,
          "material_type": 1,
          "material_index": 0,
          "quality": 5,
          "wear": 0
        }
      }
    ]
  }
}
```

## Testing

### Test Script
**File**: `python_implementation/test_equipment_decoder.py`

**Features**:
- Individual decoder tests for each method
- Full equipment item decoding tests
- Sentinel value handling verification
- Sample data covering all quality/wear levels
- JSON export of test results to `exports/`

**Usage**:
```bash
cd python_implementation
python test_equipment_decoder.py
```

**Test Coverage**:
- ✅ All 91 ITEM_TYPE values (-1 to 90)
- ✅ All 8 quality levels (-1 to 6)
- ✅ All 4 wear levels (0 to 3)
- ✅ Sentinel value conversion (4294967295 → -1 or 0)
- ✅ Invalid value handling

### Test Results
All tests pass with expected output. See `exports/equipment_decoder_test_*.json` for detailed results.

## Known Limitations

### Material System (Not Yet Implemented)
The `material_type` and `material_index` fields are NOT decoded in Phase 1.

**Reason**: Material system is complex:
- Materials stored in separate vectors in memory
- Requires reading material definitions from memory layout
- Material names depend on material type (metal, stone, wood, cloth, etc.)
- Each material type has its own index mapping

**Future Work**: Phase 2 will implement material decoding by:
1. Reading material vector addresses from memory layout
2. Mapping material_type to material category
3. Looking up material_index in appropriate vector
4. Extracting material name string

**Current Behavior**: Raw numeric values preserved in `raw_values` section.

### Pointer Values in Data
Some equipment fields may contain memory addresses instead of actual data:
- Very large numbers (> 1,000,000) likely pointers
- Quality values like `4294901760` appear to be addresses
- Decoder handles these as sentinel values (converts to -1 or 0)

**Mitigation**: 
- Sentinel detection: values > 100 treated as invalid
- Default fallbacks: -1 for quality, 0 for wear
- `valid` flag in output indicates detection success

## API Reference Summary

### EquipmentDecoder Class Methods

| Method | Input | Output | Purpose |
|--------|-------|--------|---------|
| `decode_item_type(int)` | Item type ID | Type info dict | ITEM_TYPE enum lookup |
| `decode_quality(int)` | Quality level | Quality info dict | Quality 0-6 interpretation |
| `decode_wear(int)` | Wear level | Wear info dict | Condition 0-3 interpretation |
| `decode_equipment_item(dict)` | Equipment item | Full decoded dict | All-in-one decoder |

### Output Dictionary Keys

**All methods return**:
- `valid`: Boolean indicating successful decoding
- `display_text`: Human-readable formatted string (primary display field)

**Type-specific fields**:
- Item type: `type_id`, `type_name`
- Quality: `level`, `name`, `symbol`, `description`
- Wear: `level`, `name`, `symbol`, `description`, `condition_percentage`

## Usage Examples

### Example 1: Decode Single Item Type
```python
from complete_dwarf_reader import EquipmentDecoder

result = EquipmentDecoder.decode_item_type(25)
print(result['display_text'])  # Output: "Armor"
```

### Example 2: Check Quality Level
```python
result = EquipmentDecoder.decode_quality(5)
print(f"{result['symbol']} {result['name']}")  # Output: "☼ masterwork"
```

### Example 3: Get Condition Percentage
```python
result = EquipmentDecoder.decode_wear(2)
print(f"Condition: {result['condition_percentage']}%")  # Output: "Condition: 33%"
```

### Example 4: Decode Full Equipment Item
```python
item = {
    "item_id": 999,
    "item_type": 24,  # WEAPON
    "quality": 3,      # Superior
    "wear": 1,         # Worn
    "material_type": 0,
    "material_index": 0
}

decoded = EquipmentDecoder.decode_equipment_item(item)
print(decoded['item_type']['display_text'])  # "Weapon"
print(decoded['quality']['display_text'])    # "*superior*"
print(decoded['wear']['display_text'])       # "x worn (66%)"
```

## Version History

- **Phase 1 (2024-11-18)**: Initial implementation
  - Item type decoding (ITEM_TYPE enum)
  - Quality level decoding (0-6 scale)
  - Wear condition decoding (0-3 scale)
  - Sentinel value handling
  - Integration with to_dict() method
  - Test suite creation

## Future Enhancements (Phase 2+)

### Planned Features
1. **Material Decoding** (High Priority)
   - Read material vectors from DF memory
   - Map material_type/material_index to actual material names
   - Support all material categories (metals, stones, woods, cloths, etc.)

2. **Material Quality Context**
   - Interpret quality differently based on material
   - Example: Masterwork steel vs masterwork wood
   - Material value modifiers

3. **Item Subtype Decoding**
   - Weapon/armor subtype identification
   - Specific item names (e.g., "Iron Battle Axe" not just "Weapon")
   - Tool type identification

4. **Maker Information**
   - Decode item maker/creator ID
   - Link to historical figure who crafted item
   - Display crafter name in item description

5. **Enchantments/Improvements**
   - Decode item decorations/improvements
   - Artifact powers and descriptions
   - Named items and their histories

## References

### Source Code Files
- `src/global_enums.h` - ITEM_TYPE enum definition
- `src/item.h` - Item class structure
- `src/item.cpp` - Quality/wear display logic
- `src/uniform.cpp` - Equipment handling
- `share/memory_layouts/` - Memory offset definitions

### Related Documentation
- `FLAGS_AND_FIELDS_ANALYSIS.md` - General field analysis
- `python_implementation/README.md` - Python implementation overview
- Test results in `exports/equipment_decoder_test_*.json`
