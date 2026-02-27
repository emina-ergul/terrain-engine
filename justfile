backend:
    cd backend && uvicorn app.main:app --reload

frontend:
    cd frontend && npm run dev

dev:
    (cd backend && uvicorn app.main:app --reload) & (cd frontend && npm run dev) & \
    wait

stop-backend:
    pkill -f uvicorn