# Quantum Necromancer - Design

## Architecture

### System Overview
```
┌─────────────────┐         ┌──────────────────┐
│   Next.js App   │ ◄─────► │  FastAPI Backend │
│   (Frontend)    │  HTTP   │    (Python)      │
└─────────────────┘         └──────────────────┘
        │                            │
        │                    ┌───────┴────────┐
        │                    │                │
        ▼                    ▼                ▼
┌─────────────┐    ┌──────────────┐  ┌──────────────┐
│  Tailwind   │    │   Quantum    │  │     LDA      │
│   + Dark    │    │   (Qiskit)   │  │   (sklearn)  │
│   Theme     │    └──────────────┘  └──────────────┘
└─────────────┘            │
                           ▼
                  ┌──────────────┐
                  │   Anomaly    │
                  │  Detection   │
                  └──────────────┘
```

## Correctness Properties

### P1: Project Structure Integrity (AC1)
- PROPERTY: All required Kiro directories exist
- VERIFICATION: Directory structure check passes
- COVERS: AC1

### P2: API Availability (AC2)
- PROPERTY: FastAPI server responds to health checks
- VERIFICATION: GET /health returns 200
- COVERS: AC2

### P3: Quantum Randomness (AC3)
- PROPERTY: QRNG produces non-deterministic values
- VERIFICATION: Multiple calls produce different sequences
- COVERS: AC3

### P4: Topic Extraction (AC4)
- PROPERTY: LDA returns valid topic distributions
- VERIFICATION: Topic probabilities sum to 1.0
- COVERS: AC4

### P5: Anomaly Identification (AC5)
- PROPERTY: Anomaly scores are bounded and meaningful
- VERIFICATION: Scores in valid range, outliers flagged
- COVERS: AC5

### P6: Page Routing (AC6, AC7, AC8, AC9, AC10, AC11, AC12, AC13)
- PROPERTY: All pages are accessible and render
- VERIFICATION: Navigation to each route succeeds
- COVERS: AC6, AC7, AC8, AC9, AC10, AC11, AC12, AC13

## Backend Module Design

### Quantum Module (`backend/modules/quantum.py`)
```python
# Uses Qiskit to generate quantum random numbers
# Simulates quantum circuit for true randomness
# Returns random values for dataset selection
```

### LDA Module (`backend/modules/lda.py`)
```python
# Implements Latent Dirichlet Allocation
# Extracts topics from text data
# Returns topic keywords and distributions
```

### Anomaly Module (`backend/modules/anomaly.py`)
```python
# Uses Isolation Forest or similar algorithm
# Detects outliers in numerical data
# Returns anomaly scores and flagged indices
```

## Frontend Design

### Dark Theme
- Background: #0a0a0a to #1a1a1a gradient
- Accent: Purple (#8b5cf6) and green (#10b981) for spooky effect
- Typography: Monospace fonts for technical feel

### Page Responsibilities
- `/`: Landing page with navigation
- `/summon`: Dataset upload and quantum selection
- `/ritual`: LDA topic modeling visualization
- `/visualizer`: Interactive data charts
- `/ar`: WebXR AR experience
- `/anomalies`: Anomaly detection results
- `/kiro-logs`: Development metadata display

## Data Flow
1. User uploads dataset on `/summon`
2. Quantum module selects random subset
3. Backend processes with LDA and anomaly detection
4. Results stored in session/state
5. Frontend pages visualize different aspects
6. AR page renders 3D representation
