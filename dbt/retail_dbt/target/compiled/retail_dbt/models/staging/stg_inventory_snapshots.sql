select
  snapshot_date::date as snapshot_date,
  store_id,
  product_id,
  on_hand_qty::number as on_hand_qty,
  ingested_at
from RETAIL_DW.RAW.INVENTORY_SNAPSHOTS_RAW