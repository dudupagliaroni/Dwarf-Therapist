# Dwarf Therapist - AI Coding Agent Instructions

## Project Overview
Dwarf Therapist is a Qt5/C++14 application that provides external management of dwarfs in the game Dwarf Fortress. It reads/writes Dwarf Fortress memory directly using platform-specific implementations (`dfinstancewindows.cpp`, `dfinstancelinux.cpp`, `dfinstanceosx.mm`).

## Architecture Overview

### Core Components
- **DFInstance**: Platform-specific memory interface for Dwarf Fortress process
- **DwarfTherapist**: Main application singleton (access via `DT` macro)
- **MemoryLayout**: INI-based memory offsets for different DF versions (`share/memory_layouts/`)
- **Dwarf**: Individual dwarf data model with skills, attributes, beliefs, emotions
- **GridView**: Customizable data table views with column types (labor, skill, attribute, etc.)

### Memory System Pattern
All DF data access follows: `DFInstance::read_mem<T>(address)` → parse via MemoryLayout offsets → populate model objects. Critical files:
- `src/dfinstance.h` - Abstract memory interface
- `src/memorylayout.h` - Version-specific memory maps
- Platform implementations handle process attachment/memory reading

### Column System Architecture
Extensible column types in `src/*column.cpp`:
- Inherit from `ViewColumn` base class
- Override `build_cell()` for data display
- Use `cell_data()` pattern for dwarf-specific data extraction
- Color coding via `CellColorDef` system

## Build System

### CMake Configuration
```bash
# Standard build
mkdir build && cd build
cmake -DCMAKE_PREFIX_PATH=/path/to/qt5 ..
cmake --build . --config Release

# Development mode (uses current source dir for data)
cmake -DBUILD_DEVMODE=ON ..

# Portable build (looks for files relative to executable)
cmake -DBUILD_PORTABLE=ON ..
```

### Platform-Specific Requirements
- **Windows**: MSVC 2017+, Qt 5.9+, use `scripts/windeployqt.sh` for deployment
- **Linux**: GCC 5+, check ptrace permissions (`dist/ptrace_scope/README.md`)
- **macOS**: Clang 3.4+, Homebrew Qt installation

## Data Files & Configuration

### Game Data Structure
- `resources/game_data.ini` - Skills, professions, labors definitions (8K+ lines)
- `share/memory_layouts/` - Platform-specific DF memory offsets
- `resources/default_gridviews.dtg` - Default column layouts

### Memory Layout System
Memory layouts are INI files mapping DF structures:
```ini
[globals]
current_year = 0x01234567
dwarf_race_id = 0x02345678

[dwarf]
size = 0x1000
first_name = 0x0000
happiness = 0x0ABC
```

## Development Patterns

### Singleton Access Pattern
```cpp
// Access main application
DT->get_main_window()
DT->get_DFInstance()
DT->user_settings()

// Access game data
DFInstance *df = DT->get_DFInstance();
df->get_dwarf_by_id(id);
df->read_mem<int>(address);
```

### Qt Model/View Integration
- `DwarfModel` provides QAbstractItemModel for main dwarf table
- `DwarfModelProxy` adds filtering/sorting
- Custom delegates handle complex cell rendering

### Error Handling Convention
Use `LOGE`, `LOGW`, `LOGI`, `LOGD`, `TRACE` macros for consistent logging to `log/log.txt`.

## Common Tasks

### Adding New Column Types
1. Create `src/newcolumn.h/.cpp` inheriting from `ViewColumn`
2. Add to `columntypes.h` enum and `ViewColumnFactory`
3. Implement `build_cell()` method for data extraction
4. Add CMakeLists.txt entry

### Memory Layout Updates
DF version changes require updating `share/memory_layouts/<platform>/` with new offsets. Use debugging tools to find structure changes.

### Custom Professions
Stored in user settings, managed via `CustomProfession` class. Use `DT->add_custom_profession()` pattern.

## Debugging & Testing

### Memory Debugging
- Use `DFInstance::pprint()` for hex dump analysis
- Check `m_status` for connection state (DISCONNECTED/CONNECTED/LAYOUT_OK/GAME_LOADED)
- Platform-specific process attachment in `dfinstance*.cpp`

### No Automated Tests
Project relies on manual testing with live Dwarf Fortress saves. Focus on data integrity and memory safety.

## External Dependencies
- Qt5 (Widgets, QML, Network, Concurrent modules)
- Platform APIs for process memory access
- Dwarf Fortress game process (external)

## Key Files to Understand
- `src/dwarftherapist.cpp` - Application lifecycle
- `src/dfinstance.cpp` - Core memory reading logic  
- `src/dwarf.cpp` - Individual dwarf data model
- `src/gridview.cpp` - Main UI table management
- `CMakeLists.txt` - Build configuration and file organization