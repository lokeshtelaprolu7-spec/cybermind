.PHONY: help install test run-backend run-frontend docker-up docker-down

help:
	@echo "CyberMIND Management Commands:"
	@echo "  make install        Install backend and frontend dependencies"
	@echo "  make test           Run all automated pytest suites"
	@echo "  make run-backend    Start the FastAPI backend server on port 8000"
	@echo "  make run-frontend   Start the Next.js frontend dev server on port 3000"
	@echo "  make docker-up      Start all services with Docker Compose"
	@echo "  make docker-down    Stop Docker Compose containers"

install:
	cd backend && python -m venv .venv && ./.venv/Scripts/pip install -r requirements.txt
	cd frontend && npm install

test:
	cd backend && ./.venv/Scripts/pytest tests/ -v

run-backend:
	cd backend && ./.venv/Scripts/uvicorn app.main:app --reload --port 8000

run-frontend:
	cd frontend && npm run dev

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down
