"""
Test script for Equipment Decoder
Tests the new equipment decoding functionality on sample data
"""
import json
from datetime import datetime
from pathlib import Path

# Test sample equipment items
sample_items = [
    {
        "item_id": 12345,
        "item_type": 25,  # ARMOR
        "material_type": 1,
        "material_index": 0,
        "quality": 5,  # Masterwork
        "wear": 0  # New
    },
    {
        "item_id": 67890,
        "item_type": 24,  # WEAPON
        "material_type": 0,
        "material_index": 0,
        "quality": 3,  # Superior
        "wear": 1  # Worn
    },
    {
        "item_id": 11111,
        "item_type": 28,  # HELM
        "material_type": 1,
        "material_index": 2,
        "quality": 4294967295,  # Sentinel value (should become -1/none)
        "wear": 2  # Threadbare
    },
    {
        "item_id": 22222,
        "item_type": 60,  # PANTS
        "material_type": 2,
        "material_index": 1,
        "quality": 0,  # Normal
        "wear": 3  # Tattered
    }
]

def test_equipment_decoder():
    """Test equipment decoder with sample data"""
    try:
        from src.complete_dwarf_reader import EquipmentDecoder
        
        print("=" * 80)
        print("EQUIPMENT DECODER TEST")
        print("=" * 80)
        print()
        
        results = []
        for i, item in enumerate(sample_items, 1):
            print(f"\n{'=' * 40}")
            print(f"Item {i}: Raw Data")
            print(f"{'=' * 40}")
            print(json.dumps(item, indent=2))
            
            decoded = EquipmentDecoder.decode_equipment_item(item)
            results.append({
                "original": item,
                "decoded": decoded
            })
            
            print(f"\n{'=' * 40}")
            print(f"Item {i}: Decoded Data")
            print(f"{'=' * 40}")
            print(json.dumps(decoded, indent=2, ensure_ascii=False))
            
            # Summary display
            print(f"\n📦 Summary:")
            if "item_type" in decoded:
                print(f"  Type: {decoded['item_type']['display_text']}")
            if "quality" in decoded:
                print(f"  Quality: {decoded['quality']['display_text']}")
            if "wear" in decoded:
                print(f"  Condition: {decoded['wear']['display_text']}")
        
        # Save test results
        output_dir = Path("exports")
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"equipment_decoder_test_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'=' * 80}")
        print(f"✅ Test results saved to: {output_file}")
        print(f"{'=' * 80}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_individual_decoders():
    """Test individual decoder methods"""
    try:
        from src.complete_dwarf_reader import EquipmentDecoder
        
        print("\n" + "=" * 80)
        print("INDIVIDUAL DECODER TESTS")
        print("=" * 80)
        
        # Test item types
        print("\n--- Item Type Decoder ---")
        test_types = [0, 24, 25, 28, 60, 90, 999]  # BAR, WEAPON, ARMOR, HELM, PANTS, SHEET, invalid
        for t in test_types:
            result = EquipmentDecoder.decode_item_type(t)
            print(f"Type {t:3d}: {result['display_text']}")
        
        # Test quality levels
        print("\n--- Quality Decoder ---")
        test_qualities = [-1, 0, 1, 2, 3, 4, 5, 6, 4294967295]
        for q in test_qualities:
            result = EquipmentDecoder.decode_quality(q)
            print(f"Quality {q:10d}: {result['display_text']}")
        
        # Test wear levels
        print("\n--- Wear Decoder ---")
        test_wears = [0, 1, 2, 3, 4294967295]
        for w in test_wears:
            result = EquipmentDecoder.decode_wear(w)
            print(f"Wear {w:10d}: {result['display_text']}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during individual tests: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Starting Equipment Decoder Tests\n")
    
    # Run individual decoder tests
    success1 = test_individual_decoders()
    
    # Run full equipment item tests
    success2 = test_equipment_decoder()
    
    if success1 and success2:
        print("\n✅ All tests passed successfully!")
    else:
        print("\n❌ Some tests failed")
