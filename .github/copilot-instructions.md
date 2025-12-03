# Dwarf Therapist - AI Coding Agent Instructions

## Project Overview
Qt5/C++14 application for external dwarf management in Dwarf Fortress. Reads/writes DF memory directly via platform-specific implementations.

## Architecture

### Core Data Flow
```
DFInstance (memory) → MemoryLayout (offsets) → Dwarf/Model objects → GridView (UI)
```

### Key Singletons
```cpp
DT->get_DFInstance()       // Memory interface (via DT macro from dwarftherapist.h)
DT->get_main_window()      // UI access
DT->user_settings()        // QSettings config
```

### Platform Memory Implementations
- `src/dfinstancewindows.cpp` - Win32 API (ReadProcessMemory)
- `src/dfinstancelinux.cpp` - ptrace syscalls  
- `src/dfinstanceosx.mm` - Mach VM APIs

### Column System (Extensible)
All column types inherit `ViewColumn` and implement:
```cpp
QStandardItem* build_cell(Dwarf *d) override;        // Per-dwarf cell
QStandardItem* build_aggregate(...) override;        // Group summary
```
Register in `src/columntypes.h` enum + `init_column_types()`. See `src/laborcolumn.cpp` as reference.

## Build Commands

```bash
# Windows (VS 2017+, Qt 5.9+)
mkdir build && cd build
cmake -DCMAKE_PREFIX_PATH=C:/Qt/5.15.2/msvc2019_64 -G "Visual Studio 16 2019" ..
cmake --build . --config Release

# Dev mode (data from source dir, no install)
cmake -DBUILD_DEVMODE=ON ..

# Portable (all files relative to exe)
cmake -DBUILD_PORTABLE=ON ..
```
Windows deployment: `windeployqt.exe` then copy `share/*` to `data/`

## Memory Layout System

INI files in `share/memory_layouts/<platform>/` map DF version offsets:
```ini
[info]
checksum=0x68d64ce7          # DF executable checksum
version_name=v0.52.05 win64 STEAM

[addresses]
creature_vector=0x14234d370  # Global vectors
dwarf_race_index=0x1422fbb2c

[dwarf_offsets]
first_name=0x0000            # Struct field offsets
happiness=0x0ABC
```
**New DF version?** Copy latest INI, update checksum + changed offsets.

## Critical Files

| File | Purpose |
|------|---------|
| `src/dfinstance.h/cpp` | Memory read/write API, `read_mem<T>()` template |
| `src/memorylayout.h` | Offset parsing from INI files |
| `src/dwarf.cpp` | Dwarf data model (skills, attributes, labor flags) |
| `src/dwarfmodel.cpp` | Qt model for main table, `DR_*` data roles |
| `resources/game_data.ini` | 8K+ lines: skill names, professions, labor defs |

## Logging
```cpp
LOGE << "Error message";     // LL_ERROR
LOGW << "Warning";           // LL_WARN  
LOGI << "Info";              // LL_INFO
LOGD << "Debug";             // LL_DEBUG
TRACE << "Verbose trace";    // LL_TRACE
```
Output: `log/log.txt` (Windows/macOS) or stderr (Linux)

## Connection States
Check `DFInstance::m_status`:
- `DFS_DISCONNECTED` - No DF process
- `DFS_CONNECTED` - Process attached
- `DFS_LAYOUT_OK` - Memory layout matched
- `DFS_GAME_LOADED` - Fortress loaded, dwarves readable

## Testing Approach
No automated tests. Manual testing with live DF saves. Use `DFInstance::pprint()` for hex dumps when debugging memory reads.

## Python Implementation
`python_implementation/` contains a parallel Python codebase for memory analysis/extraction. Separate from main Qt app - useful for prototyping offset discovery.