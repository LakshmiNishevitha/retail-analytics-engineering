import os
from dotenv import load_dotenv
import great_expectations as gx

load_dotenv()  # loads retail-dw/.env

def snowflake_conn_str() -> str:
    user = os.environ["SNOWFLAKE_USER"]
    password = os.environ["SNOWFLAKE_PASSWORD"]
    account = os.environ["SNOWFLAKE_ACCOUNT"]
    db = os.environ["SNOWFLAKE_DATABASE"]
    schema = os.environ["SNOWFLAKE_SCHEMA"]
    wh = os.environ["SNOWFLAKE_WAREHOUSE"]
    role = os.environ.get("SNOWFLAKE_ROLE", "")

    role_part = f"&role={role}" if role else ""
    return f"snowflake://{user}:{password}@{account}/{db}/{schema}?warehouse={wh}{role_part}"

def main():
    # ✅ No CLI, no init. Ephemeral context in memory.
    context = gx.get_context()

    ds_name = "snowflake_retail_raw"
    conn = snowflake_conn_str()

    # GE 1.x fluent datasource manager
    try:
        datasource = context.data_sources.get(ds_name)
    except Exception:
        datasource = context.data_sources.add_sql(name=ds_name, connection_string=conn)

    def get_asset(table_name: str):
        # Avoid re-adding the same asset if script is run multiple times
        try:
            return datasource.get_asset(table_name)
        except Exception:
            return datasource.add_table_asset(name=table_name, table_name=table_name)

    def validate(table: str, suite_name: str, expectations_fn):
        suite = context.add_or_update_expectation_suite(suite_name)
        asset = get_asset(table)
        batch_request = asset.build_batch_request()
        validator = context.get_validator(batch_request=batch_request, expectation_suite=suite)

        expectations_fn(validator)

        # We don't need to "save" anything to disk for Phase 3 gate
        result = validator.validate()
        print(f"{table}: {'✅ PASS' if result.success else '❌ FAIL'}")
        return result.success

    # Expectations
    def orders(v):
        v.expect_column_values_to_not_be_null("ORDER_ID")
        v.expect_column_values_to_be_unique("ORDER_ID")
        v.expect_column_values_to_not_be_null("CUSTOMER_ID")
        v.expect_column_values_to_not_be_null("STORE_ID")
        v.expect_column_values_to_not_be_null("ORDER_TS")
        v.expect_column_values_to_be_in_set("STATUS", ["PLACED", "SHIPPED", "DELIVERED", "CANCELLED"])

    def items(v):
        v.expect_column_values_to_not_be_null("ORDER_ID")
        v.expect_column_values_to_not_be_null("PRODUCT_ID")
        v.expect_column_values_to_be_between("QTY", min_value=1, max_value=1000)
        v.expect_column_values_to_be_between("UNIT_PRICE", min_value=0, max_value=100000)
        v.expect_column_values_to_be_between("DISCOUNT_PCT", min_value=0, max_value=100)

    def customers(v):
        v.expect_column_values_to_not_be_null("CUSTOMER_ID")
        v.expect_column_values_to_be_unique("CUSTOMER_ID")
        v.expect_column_values_to_match_regex("EMAIL", r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
        v.expect_column_values_to_not_be_null("UPDATED_AT")

    def products(v):
        v.expect_column_values_to_not_be_null("PRODUCT_ID")
        v.expect_column_values_to_be_unique("PRODUCT_ID")
        v.expect_column_values_to_be_between("COST", min_value=0, max_value=100000)
        v.expect_column_values_to_be_in_set("ACTIVE_FLAG", ["Y", "N"])
        v.expect_column_values_to_not_be_null("UPDATED_AT")

    def stores(v):
        v.expect_column_values_to_not_be_null("STORE_ID")
        v.expect_column_values_to_be_unique("STORE_ID")
        v.expect_column_values_to_not_be_null("REGION")

    def inventory(v):
        v.expect_column_values_to_not_be_null("SNAPSHOT_DATE")
        v.expect_column_values_to_not_be_null("STORE_ID")
        v.expect_column_values_to_not_be_null("PRODUCT_ID")
        v.expect_column_values_to_be_between("ON_HAND_QTY", min_value=0, max_value=100000)

    print("\nRunning data quality checks...\n")

    results = [
        validate("ORDERS_RAW", "orders_raw_suite", orders),
        validate("ORDER_ITEMS_RAW", "order_items_raw_suite", items),
        validate("CUSTOMERS_RAW", "customers_raw_suite", customers),
        validate("PRODUCTS_RAW", "products_raw_suite", products),
        validate("STORES_RAW", "stores_raw_suite", stores),
        validate("INVENTORY_SNAPSHOTS_RAW", "inventory_snapshots_raw_suite", inventory),
    ]

    if not all(results):
        raise SystemExit("❌ One or more validations failed.")
    print("\n✅ All validations passed")

if __name__ == "__main__":
    main()
