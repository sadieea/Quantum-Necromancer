---
inclusion: manual
---

# Quantum Necromancer - Dependencies

## Backend Requirements (requirements.txt)
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
qiskit==0.45.0
qiskit-aer==0.13.0
scikit-learn==1.3.2
pandas==2.1.3
numpy==1.26.2
python-multipart==0.0.6
```

## Frontend Dependencies (package.json)
```json
{
  "dependencies": {
    "next": "^14.0.3",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "tailwindcss": "^3.3.5",
    "three": "^0.159.0",
    "@react-three/fiber": "^8.15.11",
    "@react-three/drei": "^9.88.17",
    "chart.js": "^4.4.0",
    "react-chartjs-2": "^5.2.0",
    "axios": "^1.6.2"
  },
  "devDependencies": {
    "@types/node": "^20.9.0",
    "@types/react": "^18.2.37",
    "@types/three": "^0.159.0",
    "typescript": "^5.2.2",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.31"
  }
}
```
