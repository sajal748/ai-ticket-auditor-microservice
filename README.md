# On-Premise AI Ticket Routing & Audit Microservice (R&D Prototype)

## 📌 Project Overview
An internal research and development prototype designed to eliminate ticket misrouting and optimize resolution SLAs. This system serves as a real-time validation gate: it intercepts incoming operational support descriptions and audits them against user-selected categories using an offline Large Language Model (LLM). 

By running completely on local infrastructure, this architecture eliminates cloud API costs and adheres strictly to corporate data privacy guidelines.

## 🛠️ System Architecture
- **Web Layer:** FastAPI (Python)
- **AI Infrastructure:** Ollama (Local Server Deployment)
- **Model:** Llama 3.2 (3B Parameters)
- **Validation Engine:** Pydantic (Strict JSON Schema Enforcement)

## 📊 Core Features & Resilience Guardrails
1. **Asynchronous Background Auditing:** Built to run as an independent microservice that can be called asynchronously by the primary ticketing platform, preventing web portal latency.
2. **Deterministic Output:** Forces a stochastic LLM to output rigid JSON structures using Pydantic validation schemas.
3. **Graceful Fallback Logic:** Protects operations from crashes. If an empty input is processed or the AI fails to meet formatting guidelines, the system catches the error and defaults the ticket to a manual triage queue.

## 📈 Performance Benchmarks
- **Average Inference Latency:** ~2.10 - 9.80 seconds per ticket (Hardware dependent)
- **Schema Validation Success Rate:** 100% via enforced Pydantic structures.