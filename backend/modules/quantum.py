from fastapi import APIRouter
from pydantic import BaseModel
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np

router = APIRouter()

class QuantumRequest(BaseModel):
    num_values: int = 10
    max_value: int = 100

@router.post("/quantum/generate")
async def generate_quantum_random(request: QuantumRequest) -> dict:
    """Generate quantum random numbers using Qiskit QRNG."""
    try:
        qc = QuantumCircuit(8, 8)
        qc.h(range(8))
        qc.measure(range(8), range(8))
        
        simulator = AerSimulator()
        job = simulator.run(qc, shots=request.num_values)
        result = job.result()
        counts = result.get_counts()
        
        random_values = [
            int(list(counts.keys())[i % len(counts)], 2) % request.max_value
            for i in range(request.num_values)
        ]
        
        return {
            "success": True,
            "data": {"values": random_values, "method": "qiskit_qrng"},
            "error": None
        }
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}
