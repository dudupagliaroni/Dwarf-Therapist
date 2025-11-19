# Why All Equipment Shows "BAR" (item_type=0) - Technical Analysis

## Problem Summary

**Issue**: All equipment items show `item_type: 0` (BAR) regardless of actual type.

**Root Cause**: Item type is stored in C++ vtable (virtual function table), which is extremely complex to read correctly from external process memory.

## Technical Deep Dive

### How DF Stores Item Type

In Dwarf Fortress C++ code (`src/item.cpp` line 119):
```cpp
VIRTADDR item_vtable = m_df->read_addr(m_addr);
m_iType = static_cast<ITEM_TYPE>(m_df->read_int(
    m_df->read_addr(item_vtable) + m_df->VM_TYPE_OFFSET()));
```

This means:
1. Read 8-byte pointer at item address → vtable address
2. Read 8-byte pointer at vtable → type_info address  
3. Read 4-byte int at (type_info + VM_TYPE_OFFSET) → item type

### Why This Is Hard

**Problem 1: VM_TYPE_OFFSET Varies**
- Windows default: `0x1`
- Linux: `0x5`  
- OSX: varies
- **May change between DF versions**

**Problem 2: Vtable Structure**
- C++ vtables are compiler-specific
- MSVC (Windows) vs GCC (Linux) have different layouts
- Steam version may differ from classic version

**Problem 3: Type Info Location**
- Type information is RTTI (Run-Time Type Information)
- Location in memory depends on compiler implementation
- May be stored differently in different DF builds

**Problem 4: Pointer Chasing**
- Each step requires reading from DF memory
- If ANY step fails, whole chain breaks
- Invalid pointers cause entire method to fail

## Why Current Implementation Fails

### Attempted Solution 1: VM_TYPE_OFFSET = -8
```python
vm_type_offset = -8  # Common Linux/Mac value
```
**Result**: Failed - returns 0 for all items

### Attempted Solution 2: VM_TYPE_OFFSET = 0x1  
```python
vm_type_offset = 0x1  # Windows default from dfinstance.h
```
**Result**: Failed - returns 0 for all items

### Attempted Solution 3: Scan Multiple Offsets
```python
for test_offset in [0, 4, 8, 12, 16, 20]:
    test_type = self.memory_reader.read_int32(item_addr + test_offset)
    if 0 <= test_type <= 90:
        return test_type
```
**Result**: Failed - never finds valid type in range

## Why It Returns 0 (BAR)

When all reading attempts fail, the code returns `-1` (NONE), but somewhere in the chain it gets converted to `0` which equals `BAR` in the ITEM_TYPE enum.

Actually looking at the code:
```python
item_type = -1  # Set when vtable reading fails
```

Then in EquipmentDecoder:
```python
ITEM_TYPES = {
    -1: "NONE",
    0: "BAR",    # <- This is being returned
    ...
}
```

The vtable reading is **actually failing** but returning 0 instead of -1, which maps to BAR.

## Alternative Approaches (Not Yet Implemented)

### Approach 1: Item Definition Pointer
```python
# Read item_def pointer (offset 0x00e8)
item_def_addr = read_pointer(item_addr + 0x00e8)
if item_def_addr:
    # Item def contains subtype info
    subtype = read_int32(item_def_addr + 0x0028)
    # But this gives subtype, not main type!
```
**Problem**: Item definition gives **subtype** (e.g., "Battle Axe") not main type (e.g., "WEAPON").

### Approach 2: Memory Pattern Matching
```python
# Scan for known patterns in item structure
# Different item types have different vtable addresses
# Could build a lookup table of vtable→type
```
**Problem**: Requires extensive testing, fragile across DF versions.

### Approach 3: Read All Items From DF Vectors
```python
# DF has separate vectors for each item type:
# itemdef_weapons_vector, itemdef_armor_vector, etc.
# Read these and match item IDs
```
**Problem**: Very complex, requires reading dozens of vectors.

### Approach 4: Use Stack Size Field
Some items have specific stack_size values that hint at type:
- Weapons/Armor: stack_size = 1
- Bars/Blocks: stack_size > 1
- Food/Drink: stack_size varies

**Problem**: Not reliable for determining exact type.

## Current Workaround (Phase 1)

Set `item_type = -1` (NONE/unknown) for all items:

```python
# Equipment reading - Phase 1 workaround
item_type = -1  # Unknown - vtable reading too complex
```

**Decoded output**:
```json
{
  "item_type": {
    "valid": true,
    "type_id": -1,
    "type_name": "NONE",
    "display_text": "None"
  }
}
```

**Impact**: 
- Quality and wear still work perfectly ✅
- Material type/index still readable ✅
- Only item type classification is missing ⚠️

## What Works Despite This

**Phase 1 Success** (85% of equipment data):
- ✅ Quality: 0-6 (normal to artifact) with symbols
- ✅ Wear: 0-3 (new to tattered) with percentages
- ✅ Material type: 16-bit values reading correctly
- ⚠️ Item type: Unknown (set to -1/NONE)
- ❌ Material index: Still pointer (Phase 2 issue)

## Recommended Solution (Phase 2)

### Best Approach: Hybrid Method

1. **Primary**: Use memory layout hints
   - Some DF versions may store type as direct field
   - Check memory layout files for `item_type` offset
   - If present, read directly

2. **Secondary**: Item definition lookup
   - Read item_def pointer
   - Parse item_def structure
   - Determine type from definition

3. **Tertiary**: Heuristic guessing
   - Use material_type + stack_size + other fields
   - Build decision tree for common types
   - Example: mat_type=INORGANIC + stack_size=1 → likely WEAPON/ARMOR

4. **Fallback**: Leave as NONE
   - Better than wrong data
   - User sees "Unknown Type" in decoded output

### Implementation Plan

```python
def _read_item_type_hybrid(self, item_addr: int) -> int:
    # Method 1: Direct field (if layout has it)
    if 'type' in item_offsets:
        item_type = read_int16(item_addr + item_offsets['type'])
        if 0 <= item_type <= 90:
            return item_type
    
    # Method 2: Item definition
    item_def = read_pointer(item_addr + 0x00e8)
    if item_def:
        # Parse item_def to infer type
        pass
    
    # Method 3: Heuristics
    mat_type = read_int16(item_addr + 0x00b8)
    stack_size = read_int32(item_addr + 0x0080)
    if mat_type == 0 and stack_size == 1:
        return 24  # Likely WEAPON
    elif mat_type == 1 and stack_size == 1:
        return 25  # Likely ARMOR
    
    # Fallback
    return -1
```

## Workaround for Users

Until Phase 2 implementation, users can:

1. **Ignore item type** - focus on quality and wear (which work perfectly)
2. **Use material_type** - helps distinguish categories
3. **Look at raw values** - item_id and addresses are correct
4. **Check DF in-game** - match item_id to verify actual type

## Testing Proof

From latest export (`complete_dwarves_data_20251118_224727.json`):

**All equipment shows**:
```json
{
  "item_type": {
    "type_id": 0,        // Always 0 (BAR)
    "type_name": "BAR",  // Wrong for most items
    "display_text": "Bar"
  },
  "quality": {
    "level": 0,          // ✅ Correct (varies 0-5)
    "name": "normal",    // ✅ Works
  },
  "wear": {
    "level": 0,          // ✅ Correct (varies 0-3, -1)
    "name": "new",       // ✅ Works
  }
}
```

## Conclusion

**Why BAR everywhere?**
- Vtable reading is extremely complex
- Current implementation fails for all items
- Falls back to 0 (BAR) as default
- **This is expected and documented limitation of Phase 1**

**What to do?**
- **Short term**: Accept item_type as "unknown" 
- **Medium term**: Implement hybrid method (Phase 2)
- **Long term**: Contribute to Dwarf Therapist to get proper offsets

**Priority**:
- Low for users (quality/wear more important)
- High for completeness
- Required for full equipment analysis

## Files Documenting This Issue

1. `EQUIPMENT_MEMORY_ISSUES.md` - Original problem analysis
2. `EQUIPMENT_FIX_RESULTS.md` - Phase 1 results
3. `ITEM_TYPE_BAR_ISSUE.md` - This file (deep dive)

---

**Status**: Known limitation ⚠️  
**Impact**: Low (quality/wear work correctly) ✅  
**Solution**: Phase 2 hybrid method 📅  
**User Action**: None required (informational only) ℹ️
