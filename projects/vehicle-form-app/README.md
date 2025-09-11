
### File structure for backend/

```backend/
├── main.py                # FastAPI app entry point (very lightweight)
├── database.py            # DB engine, session, Base
├── models/
│   └── vehicle.py         # SQLAlchemy models (Vehicle, User)
├── schemas/
│   └── vehicle.py         # Pydantic schemas (VehicleCreate, VehicleOut)
├── routers/
│   └── vehicles.py        # Routes related to vehicles
│   └── users.py           # Routes related to users
├── crud/
│   └── vehicle.py         # DB logic: create, read, update vehicles
│   └── user.py            # DB logic: create, read users
├── alembic/               # Alembic migration folder
│   └── ...                # Auto-generated
└── requirements.txt       # Your dependencies

frontend/
├── src/
│   └── components/
│       └── VehicleStats.tsx  # React component for stats
│   └── App.tsx
└── package.json
```


### File structure for backend/
```src/
├── App.tsx              // Routing + global layout
├── pages/
│   ├── Dashboard.tsx    // Main dashboard page
│   ├── AddData.tsx      // Another page/tab
│   └── Reports.tsx      // (example extra page)
├── components/
│   ├── Dashboard/
│   │   ├── TotalVehicle.tsx
│   │   ├── SalesChart.tsx
│   │   ├── StatsCard.tsx
│   │   └── Dashboard.module.css
│   └── Shared/
│       ├── Navbar.tsx
│       └── Footer.tsx
```