from fastapi import FastAPI, Header, HTTPException
import sqlite3

app = FastAPI()
TOKENS = {"token-a": 1, "token-b": 2}   # token -> user id

def current_user(authorization: str = Header(None)):
    uid = TOKENS.get((authorization or "").replace("Bearer ", ""))
    if not uid:
        raise HTTPException(401)
    return uid

db = sqlite3.connect(":memory:", check_same_thread=False)
db.execute("create table orders(id int, owner_id int, item text, price real)")
db.execute("insert into orders values (1,1,'laptop',900),(2,2,'phone',500)")

@app.get("/api/orders/{order_id}")
def get_order(order_id: int, authorization: str = Header(None)):
    current_user(authorization)
    # FLAW 1 (logic): authenticated, but no ownership check -> BOLA/IDOR
    row = db.execute("select * from orders where id=?", (order_id,)).fetchone()
    return {"order": row}

@app.get("/api/search")
def search(q: str):
    # FLAW 2 (classic): SQL injection, and no auth at all
    rows = db.execute(f"select * from orders where item like '%{q}%'").fetchall()
    return {"results": rows}
