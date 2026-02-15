# ============================================================
# Dual AI Chat — Makefile (Monorepo)
# ============================================================

.DEFAULT_GOAL := help

# ---- Local Development -----------------------------------

.PHONY: dev-backend
dev-backend: ## Start backend (FastAPI + uvicorn) in dev mode
	cd apps/backend && python run.py

.PHONY: dev-frontend
dev-frontend: ## Start frontend (Vite) in dev mode
	cd apps/frontend && npm run dev

.PHONY: dev
dev: ## Start both backend and frontend (requires two terminals)
	@echo "Run 'make dev-backend' in one terminal and 'make dev-frontend' in another."

.PHONY: install
install: install-backend install-frontend ## Install all dependencies

.PHONY: install-backend
install-backend: ## Install Python dependencies
	cd apps/backend && pip install -r requirements.txt

.PHONY: install-frontend
install-frontend: ## Install Node dependencies
	npm install

# ---- Docker ----------------------------------------------

.PHONY: docker-up
docker-up: ## Build & start all services via Docker Compose
	docker compose up --build -d

.PHONY: docker-down
docker-down: ## Stop all Docker services
	docker compose down

.PHONY: docker-logs
docker-logs: ## Tail Docker logs
	docker compose logs -f

# ---- Quality / Testing -----------------------------------

.PHONY: lint-backend
lint-backend: ## Lint Python code
	cd apps/backend && python -m flake8 app/ --max-line-length=120

.PHONY: lint-frontend
lint-frontend: ## Lint TypeScript/React code
	cd apps/frontend && npm run lint

.PHONY: test-backend
test-backend: ## Run backend tests
	cd apps/backend && python -m pytest tests/ -v

.PHONY: test-frontend
test-frontend: ## Run frontend tests
	cd apps/frontend && npm test

.PHONY: test
test: test-backend test-frontend ## Run all tests

# ---- Utilities -------------------------------------------

.PHONY: clean
clean: ## Remove generated files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name node_modules -exec rm -rf {} + 2>/dev/null || true
	rm -rf apps/backend/.pytest_cache apps/frontend/dist

.PHONY: help
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
