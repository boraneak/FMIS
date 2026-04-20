INSERT INTO fact_transactions (transaction_id, date_key, amount, source_system)
SELECT 
    transaction_id::uuid,
    CAST(REPLACE(date, '-', '') AS INT),
    amount,
    'FMIS_BATCH_UPLOAD'
FROM stg_transactions
ON CONFLICT (transaction_id) DO NOTHING;

TRUNCATE TABLE stg_transactions;
