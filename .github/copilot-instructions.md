# Dwarf Therapist - AI Coding Agent Instructions

## Project Overview
Qt5/C++14 external memory editor for Dwarf Fortress. Reads/writes DF process memory via platform-specific APIs to manage dwarf labors, professions, and statistics.

## Architecture

### Data Flow
```
DFInstance → MemoryLayout (INI offsets) → Dwarf objects → DwarfModel → GridView UI
```

### Global Access Pattern
Use the `DT` macro (defined in `src/dwarftherapist.h`) for singleton access:
```cpp
DT->get_DFInstance()       // Memory interface
DT->get_main_window()      // MainWindow*
DT->user_settings()        // QSettings*
```

### Platform Implementations
Memory reading is platform-specific via virtual methods in DFInstance:
- `src/dfinstancewindows.cpp` - ReadProcessMemory/WriteProcessMemory
- `src/dfinstancelinux.cpp` - ptrace  
- `src/dfinstanceosx.mm` - Mach VM APIs

### Column System
To add a new column type:
1. Add enum to `src/columntypes.h` (`CT_YOURTYPE`)
2. Register string mapping in `init_column_types()`
3. Create class inheriting `ViewColumn`, implement `build_cell()` and `build_aggregate()`
4. Use `DR_*` data roles from `src/dwarfmodel.h` for cell data

Example pattern in `src/laborcolumn.cpp`:
```cpp
item->setData(CT_LABOR, DwarfModel::DR_COL_TYPE);
item->setData(d->get_skill_level(m_skill_id), DwarfModel::DR_RATING);
```

## Build Commands

```bash
# Windows (VS 2017+, Qt 5.9+) - use forward slashes in CMAKE_PREFIX_PATH
mkdir build && cd build
cmake -DCMAKE_PREFIX_PATH=C:/Qt/5.15.2/msvc2019_64 -G "Visual Studio 16 2019" ..
cmake --build . --config Release

# Dev mode - reads data files from source tree without install
cmake -DBUILD_DEVMODE=ON ..

# Portable - all paths relative to exe
cmake -DBUILD_PORTABLE=ON ..
```
Deployment: run `windeployqt.exe` on output, then copy `share/*` to `data/`

## Memory Layout System

INI files in `share/memory_layouts/<platform>/` define offsets per DF version:
```ini
[info]
checksum=0x68d64ce7           # DF executable checksum (identifies version)
version_name=v0.52.05 win64 STEAM

[addresses]
creature_vector=0x14234d370   # Global pointers
dwarf_race_index=0x1422fbb2c

[dwarf_offsets]
first_name=0x0000             # Struct field offsets
```

**Supporting new DF version:** Copy latest INI for platform, update `checksum` from new DF executable, adjust changed offsets. Use `python_implementation/` tools for offset discovery.

## Key Files

| Path | Purpose |
|------|---------|
| `src/dfinstance.h` | Memory API: `read_mem<T>()`, `enum_vec<T>()`, `read_string()` |
| `src/memorylayout.h` | Parses offset INI files |
| `src/dwarf.cpp` | Dwarf model (skills, attributes, labors, moods) |
| `src/dwarfmodel.h` | `DR_*` data roles enum for Qt model items |
| `resources/game_data.ini` | 8K+ lines of game definitions (skills, professions, labors) |
| `share/memory_layouts/` | Per-platform offset definitions |

## Logging
```cpp
LOGE << "Error";    LOGW << "Warning";    LOGI << "Info";
LOGD << "Debug";    TRACE << "Verbose";
```
Output: `log/log.txt` (Windows/macOS) or stderr (Linux). Use `DFInstance::pprint()` for hex dumps.

## Connection States (`DFInstance::m_status`)
- `DFS_DISCONNECTED` → `DFS_CONNECTED` → `DFS_LAYOUT_OK` → `DFS_GAME_LOADED`

## Testing
No automated tests. Test manually with running DF and save files. Check `status_err_msg()` for connection diagnostics.

## Python Implementation
`python_implementation/` is a separate Python codebase for memory analysis and offset discovery. Not part of the Qt build - use for prototyping new offset mappings.