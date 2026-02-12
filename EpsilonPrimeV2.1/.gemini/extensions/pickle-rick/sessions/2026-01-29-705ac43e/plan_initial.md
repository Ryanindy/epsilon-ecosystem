# Epsilon Prime Portable - Implementation Plan

## Overview
We are creating the "Epsilon Prime Portable" module. This system allows the entire Epsilon AI ecosystem to be deployed onto a removable drive (MicroSD/USB) and run on any Windows or Linux host without installation ("Zero-Footprint").
**Constraint**: The original source files in `C:\Users\Media Server\` MUST NOT be modified.

## Current State Analysis
- **Hardcoded Paths**: Found 65+ instances of `C:\Users\Media Server\` in `BOOT.py`, `gemini.bat`, `daily_backup.py`, etc.
- **Dependencies**: Relies on system Python or specific venv paths.

## Implementation Approach: "Read-Modify-Write" (Hot-Patching)
The `deploy_portable.py` script will act as a "compiler." It will read source files, replace hardcoded paths with portable logic *in memory*, and write the sanitized versions to the drive.

## Phase 1: The Deployment Engine (Hot-Patcher)
### Overview
Create `deploy_portable.py` to recursively copy and sanitize the codebase.
### Changes Required:
#### 1. `deploy_portable.py` (New File)
**Logic**:
- **Source**: `C:/Users/Media Server`
- **Dest**: User-defined (e.g., `E:/EpsilonPrime`)
- **Ignore List**: `.git`, `.blackbox`, `.blackboxcli`, `__pycache__`, `venv`, `node_modules`, `tmp`.
- **Transformation Logic**:
    - If file is `BOOT.py`: Replace `SYSTEM_ROOT = "..."` with `SYSTEM_ROOT = os.path.dirname(os.path.abspath(__file__))`.
    - If file is `.bat`: Replace absolute paths with `%~dp0`.
    - If file is `.py`: Replace `C:\\Users\\Media Server` with `.` or relative path logic.

## Phase 2: The Portable Bootloader
### Overview
Since `BOOT.py` is hot-patched during deployment, we don't need a separate `BOOT_PORTABLE.py`. The deployed `BOOT.py` will already be portable.
### Changes Required:
- None (Handled by Phase 1 logic).

## Phase 3: Environment Setup
### Overview
Prepare the drive to run Python without installation.
### Changes Required:
#### 1. `deploy_portable.py` (Additions)
- Create folder `python_embed`.
- **Instruction**: Script will prompt user: "Please download 'Windows x86-64 embeddable package' from python.org and extract to [Drive]/python_embed/".
- (Scope Limit: We will not automate the download to avoid breaking the script if URLs change, but we will create the structure).

#### 2. `launch_epsilon.bat` (New File)
- **Logic**:
    - Sets `PYTHONHOME=%~dp0python_embed`
    - Sets `PATH=%~dp0python_embed;%PATH%`
    - Runs `python_embed\python.exe BOOT.py`

#### 3. `launch_epsilon.sh` (New File - Linux)
- **Logic**:
    - Checks for local python or `python3`.
    - Runs `python3 BOOT.py`.

## Phase 4: Portable Node.js (MCP Support)
### Overview
Enable MCP servers (and optionally n8n) by providing a portable Node.js environment.
### Changes Required:
#### 1. `deploy_portable.py` (Additions)
- Create folder `node_embed`.
- **Instruction**: "Download Node.js Windows Binary (.zip) and extract to [Drive]/node_embed/".
#### 2. `launch_epsilon.bat` (Update)
- Add `node_embed` to `%PATH%`.
- Set `N8N_USER_FOLDER=%~dp0n8n_data` (Pre-configuration for n8n if user installs it).

## Phase 5: Execution & Verification
### Overview
Run the deployer to build the artifact in `C:\Users\Media Server\.gemini\tmp\epsilon_portable_build` for verification.
### Success Criteria:
#### Automated:
- [ ] `deploy_portable.py` runs successfully.
- [ ] `grep "C:/Users/Media Server" [Build_Dir]/BOOT.py` returns 0 matches.
#### Manual:
- [ ] Verify `BOOT.py` in build folder has dynamic path logic.
- [ ] Verify `python_embed` and `node_embed` folders exist.

## Review Criteria
- **Integrity**: Original files must remain untouched.
- **Safety**: No Blackbox files in the build output.

