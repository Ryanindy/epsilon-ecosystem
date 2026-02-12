# PLATE ENGINEER SKILL

## SKILL METADATA
- **Skill ID**: plate_engineer
- **Version**: 1.0
- **Domain**: Engineering / Computer Vision / ALPR
- **Risk Level**: LOW
- **Confidence Floor**: 80
- **Project Root**: `H:\Legal Legal\Jay New 10326\plate\PlateShapez`

---

## PURPOSE
Engineer adversarial datasets for License Plate Recognition (ALPR) research using the PlateShapez tool.

---

## CAPABILITIES

### 1. Generate Dataset
**Action**: `generate`
**Command**: 
```powershell
cd "H:\Legal Legal\Jay New 10326\plate\PlateShapez"
uv run advplate generate --config "{config_file}" --seed {seed}
```
**Description**: Generates a synthetic dataset of license plates with adversarial perturbations.
**Default Config**: `config.yaml` (in project root)

### 2. Configure Experiment
**Action**: `configure`
**Instruction**: Write a YAML file to the project root with specific perturbation parameters (shapes, noise, warp, texture).
**Example**:
```yaml
perturbations:
  - name: shapes
    params:
      num_shapes: 50
      intensity: 0.8
```

### 3. Run Demo
**Action**: `demo`
**Command**:
```powershell
cd "H:\Legal Legal\Jay New 10326\plate\PlateShapez"
uv run advplate demo
```
**Description**: Runs the interactive demo to verify the pipeline.

### 4. Install/Update
**Action**: `install`
**Command**:
```powershell
cd "H:\Legal Legal\Jay New 10326\plate\PlateShapez"
uv sync
```
**Description**: Installs dependencies.

---

## RAG DEPENDENCIES
- `engineering_collection`: Contains the source code (`plate_src_...`) and documentation (`plate_README_md`).
- Consult RAG for specific perturbation parameters and class definitions.

## USAGE EXAMPLES

**User**: "Generate a dataset with high noise intensity."
**Agent**:
1. Create `high_noise_config.yaml` in project root.
2. Run `uv run advplate generate --config high_noise_config.yaml`

**User**: "How does the warp perturbation work?"
**Agent**: Query RAG for `plate_src_plateshapez_perturbations_warp_py` to explain the algorithm.

**STATUS: ACTIVE**
