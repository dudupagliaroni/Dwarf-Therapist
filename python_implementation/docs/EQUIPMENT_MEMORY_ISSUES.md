# Equipment Reading Analysis - Memory Structure Issues

## Problem Summary

The equipment fields show very large numbers that are clearly **memory addresses (pointers)** rather than actual data values:

```json
"raw_values": {
  "item_id": 2416336896,         // 0x900B3000 - Valid item ID
  "item_type": 0,                // Always 0 - NOT BEING READ
  "material_type": 1893811340,   // 0x70E5140C - POINTER/GARBAGE
  "material_index": 2282120448,  // 0x880300C0 - POINTER/GARBAGE  
  "quality": 19960142,           // 0x01308CCE - POINTER/GARBAGE
  "wear": 32759                  // 0x7FF7 - Could be valid or garbage
}
```

## Root Cause Analysis

### Issue 1: Wrong Data Types

**Current Code** (line 1299-1300):
```python
quality_raw = self.memory_reader.read_int32(item_addr + item_offsets.get('quality', 0))
wear_raw = self.memory_reader.read_int32(item_addr + item_offsets.get('wear', 0))
```

**Correct Types** (from `src/item.cpp` lines 123-127):
```cpp
m_wear = m_df->read_short(m_df->memory_layout()->item_field(m_addr, "wear"));
m_mat_type = m_df->read_short(m_df->memory_layout()->item_field(m_addr, "mat_type"));
m_quality = m_df->read_short(m_df->memory_layout()->item_field(m_addr, "quality"));
```

**Problem**: Reading 32 bits (4 bytes) when we should read 16 bits (2 bytes) causes us to read **extra garbage bytes** from adjacent memory.

**Example**:
```
Memory at quality offset (0x00c2):
[05 00] [XX XX]  <- quality=5 (2 bytes) + garbage (2 bytes)
   ^      ^
   |      |
   |      +-- Garbage bytes (part of next field)
   +--------- Actual quality value

Reading as int32: 0xXXXX0005 = huge garbage number
Reading as short:       0x0005 = 5 (correct!)
```

### Issue 2: Material Type Wrong Size

**Current Code** (line 1304):
```python
material_type=self.memory_reader.read_int32(item_addr + item_offsets.get('mat_type', 0))
```

**Correct Type**:
```cpp
m_mat_type = m_df->read_short(...)  // SHORT (16 bits), not int32!
```

**Effect**: Reading 32 bits instead of 16 bits causes reading into the next field's data.

### Issue 3: Item Type Not Being Read

**Current Code**: Field `item_type` is **hardcoded to 0** in Equipment dataclass initialization.

**Correct Method** (from `src/item.cpp` line 119):
```cpp
VIRTADDR item_vtable = m_df->read_addr(m_addr);
m_iType = static_cast<ITEM_TYPE>(m_df->read_int(m_df->read_addr(item_vtable) + m_df->VM_TYPE_OFFSET()));
```

**Explanation**: Item type is stored in the C++ object's **virtual function table (vtable)**, not as a direct field. This is a C++ polymorphism mechanism.

**Steps to read item_type**:
1. Read pointer at `item_addr` (8 bytes on 64-bit) → vtable address
2. Read int32 at `vtable_address + VM_TYPE_OFFSET` → type ID
3. Cast to ITEM_TYPE enum

**Alternative Method** (using item_def):
From memory layout: `item_def=0x00e8`
```cpp
VIRTADDR item_def_addr = m_df->read_addr(item_addr + 0x00e8);
// Then read subtype from item_def structure
```
This gives access to item definition which contains subtype and details.

## Memory Layout Offsets (from v0.52.05-steam_win64.ini)

```ini
[item_offsets]
item_def=0x00e8        # Pointer to item definition
id=0x001c              # Item ID (int32)
general_refs=0x0038    # Vector of references
stack_size=0x0080      # Stack count (int32)
wear=0x00a4            # Wear level (SHORT - 16 bits)
mat_type=0x00b8        # Material type (SHORT - 16 bits)
mat_index=0x00bc       # Material index (int32)
maker_race=0x00c0      # Maker race (short)
quality=0x00c2         # Quality level (SHORT - 16 bits)
```

## Correct Field Sizes

| Field | Type | Size | Current | Should Be |
|-------|------|------|---------|-----------|
| item_id | int32 | 4 bytes | read_int32 ✅ | read_int32 |
| item_type | via vtable | - | NOT READ ❌ | read_vtable_type |
| mat_type | short | 2 bytes | read_int32 ❌ | read_int16 |
| mat_index | int32 | 4 bytes | read_int32 ✅ | read_int32 |
| quality | short | 2 bytes | read_int32 ❌ | read_int16 |
| wear | short | 2 bytes | read_int32 ❌ | read_int16 |

## Example of Reading Error

### Current Output
```json
{
  "quality": 19960142,    // 0x01308CCE
  "wear": 32759           // 0x7FF7
}
```

### Memory Structure at quality offset (0x00c2)
```
Offset   Value     Field
0x00c0   [??] [??]   maker_race (short)
0x00c2   [05] [00]   quality (short) = 5
0x00c4   [CE] [8C]   ??? (garbage or next field)
0x00c6   [30] [01]   ??? (garbage or next field)

Reading quality as int32 from 0x00c2:
  Bytes: [05 00 CE 8C]
  Value: 0x8CCE0005 (little-endian) = 2,362,646,533 ❌

Reading quality as short from 0x00c2:
  Bytes: [05 00]
  Value: 0x0005 = 5 ✅
```

## Solution Implementation

### Step 1: Fix Data Type Reading

**File**: `complete_dwarf_reader.py` line ~1299-1310

**Current**:
```python
quality_raw = self.memory_reader.read_int32(item_addr + item_offsets.get('quality', 0))
wear_raw = self.memory_reader.read_int32(item_addr + item_offsets.get('wear', 0))

item = Equipment(
    item_id=self.memory_reader.read_int32(item_addr + item_offsets.get('id', 0)),
    material_type=self.memory_reader.read_int32(item_addr + item_offsets.get('mat_type', 0)),
    material_index=self.memory_reader.read_int32(item_addr + item_offsets.get('mat_index', 0)),
    quality=-1 if quality_raw == UINT32_MAX else quality_raw,
    wear=-1 if wear_raw == UINT32_MAX else wear_raw
)
```

**Fixed**:
```python
# Read with correct data types (shorts are 16-bit)
quality_raw = self.memory_reader.read_int16(item_addr + item_offsets.get('quality', 0))
wear_raw = self.memory_reader.read_int16(item_addr + item_offsets.get('wear', 0))
mat_type_raw = self.memory_reader.read_int16(item_addr + item_offsets.get('mat_type', 0))

# Sentinel value for 16-bit is 65535 (0xFFFF), not 4294967295
SHORT_MAX = 65535

item = Equipment(
    item_id=self.memory_reader.read_int32(item_addr + item_offsets.get('id', 0)),
    material_type=mat_type_raw,  # Now reading as short
    material_index=self.memory_reader.read_int32(item_addr + item_offsets.get('mat_index', 0)),
    quality=-1 if quality_raw == SHORT_MAX else quality_raw,
    wear=-1 if wear_raw == SHORT_MAX else wear_raw,
    item_type=self._read_item_type(item_addr)  # New method
)
```

### Step 2: Add Item Type Reading Method

**New method** (add to CompleteDFInstance class):
```python
def _read_item_type(self, item_addr: int) -> int:
    """
    Read item type from vtable (C++ polymorphism)
    Based on src/item.cpp line 119:
        VIRTADDR item_vtable = m_df->read_addr(m_addr);
        m_iType = static_cast<ITEM_TYPE>(m_df->read_int(
            m_df->read_addr(item_vtable) + m_df->VM_TYPE_OFFSET()));
    """
    try:
        # Step 1: Read vtable pointer at item address
        vtable_addr = self.memory_reader.read_pointer(item_addr, self.pointer_size)
        
        if vtable_addr == 0:
            return -1  # NONE
        
        # Step 2: Read type info pointer from vtable
        # VM_TYPE_OFFSET is typically -0x08 (8 bytes before vtable on x64)
        vm_type_offset = self.layout.offsets.get('vm_type', -8)
        type_info_addr = self.memory_reader.read_pointer(vtable_addr + vm_type_offset, self.pointer_size)
        
        if type_info_addr == 0:
            return -1
        
        # Step 3: Read actual type ID (int32)
        item_type = self.memory_reader.read_int32(type_info_addr)
        
        return item_type
    except Exception as e:
        logger.debug(f"Failed to read item type: {e}")
        return -1  # NONE
```

### Step 3: Add Missing Memory Reader Method

**File**: `complete_dwarf_reader.py` MemoryReader class

**Add method**:
```python
def read_int16(self, address: int) -> int:
    """Read unsigned 16-bit integer from memory"""
    data = self.read_memory(address, 2)
    return struct.unpack('<H', data)[0] if len(data) == 2 else 0
```

(Note: This method already exists as `read_int16_signed` but we need unsigned version)

## Expected Results After Fix

### Before (Current - WRONG)
```json
{
  "item_id": 2416336896,
  "item_type": 0,              // Wrong - not being read
  "material_type": 1893811340, // Wrong - reading 32 bits instead of 16
  "material_index": 2282120448,
  "quality": 19960142,         // Wrong - reading 32 bits instead of 16
  "wear": 32759                // Wrong - reading 32 bits instead of 16
}
```

### After (Fixed - CORRECT)
```json
{
  "item_id": 2416336896,
  "item_type": 25,             // Correct - ARMOR from vtable
  "material_type": 1,          // Correct - 16-bit value (INORGANIC)
  "material_index": 12,        // Correct - steel or iron index
  "quality": 5,                // Correct - masterwork (☼)
  "wear": 0                    // Correct - new condition
}
```

### Decoded Output (After Fix)
```json
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
        "display_text": "☼masterwork☼"
      },
      "wear": {
        "valid": true,
        "level": 0,
        "name": "new",
        "condition_percentage": 100,
        "display_text": "new (100%)"
      }
    }
  ]
}
```

## Additional Issues

### Material Names
Material type and index need to be resolved to actual material names (e.g., "steel", "iron", "oak wood"). This requires:
1. Reading material vectors from DF memory
2. Mapping material_type to material category
3. Looking up material name from appropriate vector using material_index

This is **Phase 2** work - material decoding system.

### VM_TYPE_OFFSET
The `VM_TYPE_OFFSET` may vary by DF version. Common values:
- Windows x64: -8 (0xFFFFFFFFFFFFFFF8)
- Linux x64: -8
- May need to be in memory layout file

If not in layout, can try:
1. Reading at offset -8 from vtable
2. Validating result is reasonable ITEM_TYPE (0-90 range)
3. Fallback to reading item_def if vtable method fails

## Priority

**Critical** (Phase 1):
1. ✅ Fix quality/wear/mat_type to use read_int16 instead of read_int32
2. ✅ Add read_int16 method if missing
3. ⚠️ Implement item_type reading via vtable

**Important** (Phase 1.5):
4. Test with real DF data
5. Validate decoded values are in expected ranges
6. Handle edge cases (NULL pointers, invalid types)

**Future** (Phase 2):
7. Material name resolution
8. Item subtype decoding
9. Item maker information

## Testing Strategy

1. **Before fix**: Export current JSON, examine raw values
2. **After fix**: Export new JSON, verify:
   - quality values in range 0-6 (not millions)
   - wear values in range 0-3 (not thousands)
   - mat_type values in range 0-30 (material categories)
   - item_type values in range 0-90 (ITEM_TYPE enum)
3. **Validation**: Check decoded display_text makes sense

## Summary

**Problem**: Reading wrong data types (32-bit instead of 16-bit) causes reading garbage bytes from adjacent memory fields.

**Solution**: Use correct read functions (read_int16 for short fields) and implement vtable reading for item_type.

**Impact**: Once fixed, all equipment data will show correct values and human-readable decoding will work properly.
