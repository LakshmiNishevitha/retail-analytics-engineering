import os
from datetime import datetime, timedelta
import random
import pandas as pd
from faker import Faker

fake = Faker()

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def gen_stores(n=10):
    regions = ["West", "Southwest", "Midwest", "Northeast", "South"]
    rows = []
    for i in range(1, n + 1):
        rows.append({
            "store_id": f"S{i:03d}",
            "store_name": f"{fake.company()} Store",
            "city": fake.city(),
            "state": fake.state_abbr(),
            "region": random.choice(regions),
            "updated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        })
    return pd.DataFrame(rows)

def gen_products(n=200):
    brands = ["Acme", "Nimbus", "Orion", "BluePeak", "Vertex", "Evergreen", "NovaCo"]
    categories = ["Electronics", "Grocery", "Home", "Beauty", "Apparel", "Sports"]
    rows = []
    for i in range(1, n + 1):
        cost = round(random.uniform(2, 200), 2)
        price = round(cost * random.uniform(1.2, 2.5), 2)
        rows.append({
            "product_id": f"P{i:05d}",
            "sku": f"SKU-{i:05d}",
            "product_name": fake.catch_phrase(),
            "brand": random.choice(brands),
            "category": random.choice(categories),
            "cost": cost,
            "list_price": price,
            "active_flag": "Y",
            "updated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        })
    return pd.DataFrame(rows)

def gen_customers(n=500):
    rows = []
    for i in range(1, n + 1):
        rows.append({
            "customer_id": f"C{i:06d}",
            "full_name": fake.name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "address_line1": fake.street_address(),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "zip": fake.postcode(),
            "updated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        })
    return pd.DataFrame(rows)

def gen_orders_and_items(customers_df, stores_df, products_df, n_orders=2000, max_items=5, start_date=None):
    if start_date is None:
        start_date = datetime.utcnow() - timedelta(days=7)

    order_rows = []
    item_rows = []
    statuses = ["PLACED", "SHIPPED", "DELIVERED", "CANCELLED"]

    for i in range(1, n_orders + 1):
        order_id = f"O{i:07d}"
        cust = customers_df.sample(1).iloc[0]
        store = stores_df.sample(1).iloc[0]
        order_ts = start_date + timedelta(minutes=random.randint(0, 7 * 24 * 60))
        status = random.choices(statuses, weights=[0.25, 0.25, 0.45, 0.05])[0]

        order_rows.append({
            "order_id": order_id,
            "customer_id": cust["customer_id"],
            "store_id": store["store_id"],
            "order_ts": order_ts.strftime("%Y-%m-%d %H:%M:%S"),
            "status": status
        })

        n_items = random.randint(1, max_items)
        picked = products_df.sample(n_items)
        for _, p in picked.iterrows():
            qty = random.randint(1, 4)
            discount_pct = random.choice([0, 0, 0, 5, 10, 15])
            item_rows.append({
                "order_id": order_id,
                "product_id": p["product_id"],
                "qty": qty,
                "unit_price": float(p["list_price"]),
                "discount_pct": discount_pct
            })

    return pd.DataFrame(order_rows), pd.DataFrame(item_rows)

def gen_inventory_snapshot(stores_df, products_df, snapshot_date):
    rows = []
    for _, s in stores_df.iterrows():
        sample_products = products_df.sample(100)
        for _, p in sample_products.iterrows():
            rows.append({
                "snapshot_date": snapshot_date.strftime("%Y-%m-%d"),
                "store_id": s["store_id"],
                "product_id": p["product_id"],
                "on_hand_qty": random.randint(0, 200)
            })
    return pd.DataFrame(rows)

def write_partitioned(df, base_path, entity, date_str, filename):
    out_dir = os.path.join(base_path, entity, f"date={date_str}")
    ensure_dir(out_dir)
    out_path = os.path.join(out_dir, filename)
    df.to_csv(out_path, index=False)
    return out_path

def main():
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    base_path = "data/raw"

    stores = gen_stores(10)
    products = gen_products(300)
    customers = gen_customers(800)
    orders, order_items = gen_orders_and_items(customers, stores, products, n_orders=2500)

    inventory = gen_inventory_snapshot(stores, products, datetime.utcnow().date())

    print(write_partitioned(orders, base_path, "orders", date_str, "orders.csv"))
    print(write_partitioned(order_items, base_path, "order_items", date_str, "order_items.csv"))
    print(write_partitioned(customers, base_path, "customers", date_str, "customers.csv"))
    print(write_partitioned(products.drop(columns=["list_price"]), base_path, "products", date_str, "products.csv"))
    print(write_partitioned(stores, base_path, "stores", date_str, "stores.csv"))
    print(write_partitioned(inventory, base_path, "inventory_snapshots", date_str, "inventory_snapshots.csv"))

    print("Done ✅")

if __name__ == "__main__":
    main()