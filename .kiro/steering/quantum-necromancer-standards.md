# Quantum Necromancer - Development Standards

## Code Style

### Python (Backend)
- Use type hints for all function signatures
- Follow PEP 8 naming conventions
- Keep functions under 50 lines
- Use async/await for I/O operations
- Add docstrings to all public functions

### TypeScript (Frontend)
- Use functional components with hooks
- Prefer const over let
- Use explicit types, avoid 'any'
- Keep components under 200 lines
- Use Tailwind classes, avoid inline styles

## Project Context

### Theme: Spooky Data Necromancy
- Use dark colors: blacks, purples, greens
- Add mystical/occult terminology in UI
- Animations should feel eerie and mysterious
- Data visualizations should have ghostly effects

### Quantum Module
- Always use Qiskit's AerSimulator for QRNG
- Generate at least 8 qubits for randomness
- Handle quantum circuit errors gracefully

### LDA Module
- Default to 5 topics unless specified
- Use TF-IDF vectorization before LDA
- Return top 10 keywords per topic

### Anomaly Module
- Use contamination=0.1 for isolation forest
- Flag anomalies with score > threshold
- Return both scores and binary flags

## Build & Test Instructions

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev  # Runs on port 3000
```

### Testing
- Backend: `pytest tests/`
- Frontend: `npm test`
- E2E: Manual testing of all pages

## API Conventions
- All endpoints under /api/
- Use POST for data processing
- Return JSON with {success, data, error} structure
- Include CORS headers for localhost:3000
