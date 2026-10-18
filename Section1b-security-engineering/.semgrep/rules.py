# ruleid: route-missing-auth
@app.get("/api/search")
def search(q: str):
    # ruleid: sqli-string-built-query
    # ruleid: order-query-missing-owner-filter
    rows = db.execute(f"select * from orders where item like '%{q}%'").fetchall()
    return {"results": rows}


@app.get("/api/orders/{order_id}")
def get_order_vulnerable(order_id: int, authorization: str = Header(None)):
    current_user(authorization)
    # ruleid: order-query-missing-owner-filter
    row = db.execute("select * from orders where id=?", (order_id,)).fetchone()
    return {"order": row}


# ok: route-missing-auth
@app.get("/api/orders/fixed/{order_id}")
def get_order_fixed(order_id: int, authorization: str = Header(None)):
    uid = current_user(authorization)
    # ok: order-query-missing-owner-filter
    # ok: sqli-string-built-query
    row = db.execute(
        "select * from orders where id=? and owner_id=?", (order_id, uid)
    ).fetchone()
    return {"order": row}
