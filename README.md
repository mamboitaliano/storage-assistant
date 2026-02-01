# Storage Assistant

> ⚠️ **This project is currently under construction.** Features may be incomplete, and breaking changes are expected.

A Home Assistant add-on for managing home storage and inventory. Stop digging through boxes and bins—know exactly what's inside each container before you open it.

## What It Does

Storage Assistant helps you organize and track items throughout your home with a hierarchical structure:

```
Floors → Rooms → Containers → Items
```

**Key Features:**
- **Inventory Tracking** – Add items to rooms or containers and track quantities
- **QR Code Labels** – Generate QR codes for containers that link directly to their contents page
- **Hierarchical Organization** – Organize storage by floor, room, and container
- **Filtering** – Filter items by name, room, and container with paginated results
- **Quick Search** – Find items across your entire home (coming soon)
- **Mobile-Friendly** – Scan QR codes with your phone to instantly see what's in a box

**Use Cases:**
- Moving boxes – label and scan to know contents without unpacking
- Garage/attic storage – track seasonal items, holiday decorations, tools
- Pantry inventory – know what you have before going shopping
- Craft/hobby supplies – find that specific item buried in bins

## Tech Stack

- **Backend:** FastAPI + SQLite (Python 3.12+)
- **Frontend:** React + Vite + TypeScript + Tailwind CSS + shadcn/ui
- **Containerization:** Docker + Docker Compose

---

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Git

### Quick Start (Docker)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd storage-assistant
   ```

2. **Run the first-time setup:**
   ```bash
   make first-start
   ```
   This will:
   - Check out the `develop` branch and pull latest changes
   - Build and start the Docker containers
   - Install frontend dependencies
   - Seed the database with sample data

3. **Start the servers:**
   ```bash
   make run-all
   ```

4. **Access the app:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

---

## Make Commands

| Command | Description |
|---------|-------------|
| `make first-start` | Initial setup: pulls latest code, builds containers, installs deps, seeds data |
| `make rebuild` | Tear down and rebuild containers from scratch, reinstall deps, reseed data |
| `make run-backend` | Start the FastAPI backend server |
| `make run-frontend` | Start the Vite frontend dev server |
| `make run-all` | Start both backend and frontend servers |
| `make test-backend` | Run backend pytest suite |
| `make test-frontend` | Run frontend tests |
| `make test-all` | Run all tests (backend + frontend) |
| `make seed-data` | Reset and seed the database with sample data |
| `make install-backend-deps` | Install/update Python dependencies in container |
| `make install-frontend-deps` | Install/update Node dependencies in container |
| `make tail-logs` | Follow Docker container logs |

---

## Manual Setup (Without Docker)

If you prefer running without Docker:

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set data directory (optional, defaults to /data)
export DATA_DIR=./data

# Run the API
python -m uvicorn app.main:app --reload --app-dir .
```

- API: http://127.0.0.1:8000
- Docs: http://127.0.0.1:8000/docs
- Database: `${DATA_DIR}/storage.db`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

- Dev server: http://127.0.0.1:5173
- Proxies `/api` and `/static` to the backend automatically

### Seeding Data

```bash
cd backend
source venv/bin/activate
python -m app.seed.runner
```

This wipes existing data and seeds sample floors, rooms, containers, and items using Faker.

---

## Project Structure

```
storage-assistant/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app entry point
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── database.py      # DB connection and session
│   │   ├── routers/         # API route handlers
│   │   ├── services/        # Business logic layer
│   │   ├── schemas/         # Pydantic request/response schemas
│   │   └── seed/            # Database seeders
│   ├── tests/               # Pytest test suite
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/           # Route page components
│   │   ├── features/        # Feature-specific components (filters, tables, etc.)
│   │   ├── components/      # Shared components
│   │   │   └── ui/          # shadcn/ui primitives
│   │   ├── hooks/           # Custom React hooks
│   │   ├── utils/           # Utility functions
│   │   └── api/             # API client and types
│   └── package.json
├── docker-compose.dev.yml   # Development Docker config
├── Dockerfile.dev           # Development Dockerfile
└── Makefile                 # Developer commands
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATA_DIR` | `/data` | Directory for SQLite database and QR code images |

---

## Roadmap

- [x] Floor/Room/Container/Item CRUD
- [x] Pagination for list views
- [x] QR code generation for containers
- [x] Item filtering by name, room, and container
- [ ] Global search across all entities
- [ ] Item quantity tracking and history
- [ ] Barcode scanning for items
- [ ] Home Assistant integration
- [ ] Mobile-optimized UI
- [ ] Import/export functionality

---

## Contributing

This project is in early development. Contributions, bug reports, and feature suggestions are welcome!

---

## License

TBD
