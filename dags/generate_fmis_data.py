import csv
import random
import os
import logging
import sys
from faker import Faker

# 1. Observability: Configure logging to track script progress and failures
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


def generate_fmis_transactions(count=10000, output_path="data/raw/transactions.csv"):
    """
    Generates synthetic FMIS transaction data with relational integrity.
    """
    fake = Faker()

    try:
        # 2. Idempotency & Environment Safety: Ensure directories exist before writing
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # 3. Relational Integrity: Pre-defined keys to allow SQL JOINs later
        account_codes = ["1000", "2100", "2200", "3100", "4100", "5000"]
        dept_ids = list(range(1, 16))  # Mocking 15 government departments

        logging.info(f"Starting generation of {count} transactions...")

        with open(output_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            # Header row
            writer.writerow(
                ["transaction_id", "date", "amount", "account_code", "department_id"]
            )

            for i in range(count):
                writer.writerow(
                    [
                        fake.uuid4(),  # Unique ID
                        fake.date_between(start_date="-1y"),  # Within last fiscal year
                        round(
                            random.uniform(10.0, 75000.0), 2
                        ),  # Realistic spend range
                        random.choice(account_codes),  # Valid account code
                        random.choice(dept_ids),  # Valid department ID
                    ]
                )

                # Progress logging for long-running scripts
                if (i + 1) % 2500 == 0:
                    logging.info(f"Progress: {i + 1}/{count} records generated.")

        logging.info(f"✅ Success! Data successfully written to: {output_path}")

    except Exception as e:
        # 4. Error Handling: Don't let the script fail silently
        logging.error(f"❌ Critical failure during data generation: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    # You can easily change the count here for local testing vs. stress testing
    generate_fmis_transactions(count=10000)
