# Documentation Index

## Overview
This directory contains comprehensive documentation for the Dwarf Therapist Python implementation and its human-readable data decoding features.

## Available Documentation

### 1. FLAGS_AND_FIELDS_ANALYSIS.md
**Topic**: Analysis of flags and numeric field meanings  
**Size**: ~15KB  
**Created**: Phase 0 (Initial Analysis)

**Contents**:
- Detailed analysis of flags1, flags2, flags3 bitmasks
- Body size calculation and age categories
- Blood level percentage interpretation
- Historical figure ID validation
- Squad and pet ownership fields
- C++ source code validation
- Memory offset references

**Target Audience**: Developers understanding raw memory data

---

### 2. EQUIPMENT_DECODER.md
**Topic**: Equipment decoding system documentation  
**Size**: ~12KB  
**Created**: Phase 1 (Equipment Decoding)

**Contents**:
- `EquipmentDecoder` class architecture
- ITEM_TYPE enum mapping (91 item types)
- Quality system (0-6 levels with DF symbols)
- Wear system (0-3 levels with condition percentages)
- Method signatures and API reference
- Integration with JSON export
- Usage examples and code samples
- Known limitations and future enhancements

**Target Audience**: Developers implementing or extending equipment decoding

---

### 3. PHASE1_SUMMARY.md
**Topic**: Phase 1 implementation summary and results  
**Size**: ~8KB  
**Created**: Phase 1 (Equipment Decoding)

**Contents**:
- Completed tasks checklist
- Implementation statistics
- Before/after comparison examples
- Known limitations
- Next steps for Phase 2
- Success criteria validation
- Timeline and milestones

**Target Audience**: Project managers, code reviewers, stakeholders

---

## Documentation by Topic

### Memory Reading & Data Extraction
- `FLAGS_AND_FIELDS_ANALYSIS.md` - Sections: "Estrutura de Memória", "Offsets e Leitura"

### Human-Readable Decoding
- `FLAGS_AND_FIELDS_ANALYSIS.md` - Sections: "Interpretação de Flags", "Análise de Campos Numéricos"
- `EQUIPMENT_DECODER.md` - Complete equipment decoding guide

### API Reference
- `EQUIPMENT_DECODER.md` - Section: "API Reference Summary"
- All method signatures documented with input/output

### Usage Examples
- `EQUIPMENT_DECODER.md` - Section: "Usage Examples"
- `PHASE1_SUMMARY.md` - Section: "Usage Instructions"

### Testing
- `PHASE1_SUMMARY.md` - Section: "Testing & Validation"
- Test script: `../test_equipment_decoder.py`

### Future Development
- `EQUIPMENT_DECODER.md` - Section: "Future Enhancements (Phase 2+)"
- `PHASE1_SUMMARY.md` - Section: "Next Steps (Phase 2)"

## Quick Reference

### Item Type IDs (ITEM_TYPE enum)
```
-1: NONE
 0: BAR          24: WEAPON      60: PANTS
 1: SMALLGEM     25: ARMOR       86: TOOL
 2: BLOCKS       26: SHOES       87: SLAB
 5: WOOD         28: HELM        88: EGG
 6: DOOR         29: GLOVES      89: BOOK
25: ARMOR        30: BOX         90: SHEET
```
See `EQUIPMENT_DECODER.md` for complete list (91 types)

### Quality Levels
```
-1: none              0: normal
 1: well-crafted (-)  2: finely-crafted (+)
 3: superior (*)      4: exceptional (≡)
 5: masterwork (☼)    6: artifact (!)
```

### Wear Levels
```
0: new (100%)         1: worn (66%) x
2: threadbare (33%) X 3: tattered (10%) XX
```

### Flags Bitmasks
See `FLAGS_AND_FIELDS_ANALYSIS.md` for complete flag definitions:
- **flags1**: Labor and skill flags
- **flags2**: Health and status flags (blind, paralyzed, etc.)
- **flags3**: Emotional and trait flags

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 0.1 | 2024-11-15 | Initial FLAGS_AND_FIELDS_ANALYSIS.md |
| 0.2 | 2024-11-16 | Added HumanReadableDecoder to complete_dwarf_reader.py |
| 1.0 | 2024-11-18 | Phase 1 complete: Equipment decoder implementation |
| 1.1 | 2024-11-18 | Documentation update: EQUIPMENT_DECODER.md, PHASE1_SUMMARY.md |

## File Organization

```
docs/
├── README.md (this file)
├── FLAGS_AND_FIELDS_ANALYSIS.md    # Phase 0: Initial analysis
├── EQUIPMENT_DECODER.md             # Phase 1: Equipment system
└── PHASE1_SUMMARY.md                # Phase 1: Implementation summary
```

## Related Files

### Python Implementation
- `../src/complete_dwarf_reader.py` - Main implementation file
  - Lines 400-650: `HumanReadableDecoder` class
  - Lines 650-800: `EquipmentDecoder` class

### Test Scripts
- `../test_equipment_decoder.py` - Equipment decoder test suite
- `../view_decoded_data.py` - Visualization tool for decoded JSON

### Test Data
- `../exports/equipment_decoder_test_*.json` - Test results
- `../exports/complete_dwarves_data_*.json` - Full dwarf data exports

## Reading Guide

### For New Developers
1. Start with `PHASE1_SUMMARY.md` for overview
2. Read `FLAGS_AND_FIELDS_ANALYSIS.md` for data structure understanding
3. Review `EQUIPMENT_DECODER.md` for implementation details
4. Examine `../src/complete_dwarf_reader.py` source code
5. Run `../test_equipment_decoder.py` to see live examples

### For Code Reviewers
1. Check `PHASE1_SUMMARY.md` for what changed
2. Verify `EQUIPMENT_DECODER.md` API reference
3. Review test results in `../exports/`
4. Validate code in `complete_dwarf_reader.py` lines 650-800

### For End Users
1. Read `PHASE1_SUMMARY.md` - "Usage Instructions" section
2. Review "Output Example" to understand JSON structure
3. Run test script to see decoder in action
4. Use `view_decoded_data.py` for formatted output

## Contributing

### Adding New Decoders
1. Study existing decoder implementation in `EQUIPMENT_DECODER.md`
2. Follow the pattern: static methods, dictionary mappings, return structure
3. Add tests to test suite
4. Document in new markdown file following template
5. Update this README.md with new documentation

### Updating Documentation
- Keep version history updated
- Add usage examples for new features
- Cross-reference related sections
- Maintain consistent formatting

## Support

### Common Questions

**Q: How do I decode equipment fields?**  
A: See `EQUIPMENT_DECODER.md` - Section: "Usage Examples"

**Q: What do the large numbers in quality/wear fields mean?**  
A: See `EQUIPMENT_DECODER.md` - Section: "Known Limitations" > "Pointer Values"

**Q: How do I add material decoding?**  
A: See `EQUIPMENT_DECODER.md` - Section: "Future Enhancements" > "Material Decoding"

**Q: What are flags1, flags2, flags3?**  
A: See `FLAGS_AND_FIELDS_ANALYSIS.md` - Section: "Análise Detalhada dos Flags"

### Troubleshooting

**Problem**: Decoder returns `"valid": false`  
**Solution**: Check if input value is within expected range. See API reference for valid ranges.

**Problem**: Large numbers (> 1000000) in equipment fields  
**Solution**: These are likely memory pointers. Decoder handles them as sentinel values. See "Pointer Values" section.

**Problem**: Material fields show raw numbers  
**Solution**: Material decoding not yet implemented (Phase 2). See "Known Limitations" section.

## External References

### Dwarf Therapist C++ Source
- `../../src/global_enums.h` - ITEM_TYPE enum definition
- `../../src/item.h` - Item class structure
- `../../src/item.cpp` - Quality/wear display logic
- `../../src/dwarf.h` - Dwarf class and flag definitions

### Memory Layouts
- `../../share/memory_layouts/` - DF version-specific offsets

### Build Configuration
- `../../CMakeLists.txt` - Build system configuration
- `../../BUILDING.md` - Build instructions

## License
See `../../LICENSE.txt` for project license information.

## Last Updated
2024-11-18 - Phase 1 Complete
