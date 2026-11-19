import logging
from pathlib import Path
from pipeline_core.validation import validate_record, InvalidCustomerError
from pipeline_core.security import get_safe_path, compute_sha256
from pipeline_core.ingest import export_clean_csv, export_manifest

Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def main():
    raw_batch = [
        {"cid": "C101", "name": "Asha", "email": "asha@gmail.com", "pin": "201310", "spend": "1200.50"},
        {"cid": "101", "name": "Rohan", "email": "rohan@gmail.com", "pin": "201310", "spend": "500.00"},
        {"cid": "C102", "name": "Meera", "email": "user_invalid_domain", "pin": "201310", "spend": "900.00"},
        {"cid": "C103", "name": "Kabir", "email": "kabir@gmail.com", "pin": "20A310", "spend": "300.00"},
        {"cid": "C104", "name": "Dev", "email": "dev@gmail.com", "pin": "201310", "spend": "-150.00"}
    ]
    
    clean_records = []
    print("=== SECURE CUSTOMER DATA INTAKE PIPELINE ===")
    for rec in raw_batch:
        try:
            valid_rec = validate_record(rec)
            clean_records.append(valid_rec)
            logging.info("Accepted record: %s", valid_rec["cid"])
            print(f"ACCEPTED: {valid_rec['cid']} | {valid_rec['email']} | Pin: {valid_rec['pin']}")
        except InvalidCustomerError as err:
            logging.warning("Rejected record %s: %s", rec.get("cid"), err)
            print(f"REJECTED ({rec.get('cid')}): {err}")
            
    out_csv = get_safe_path("clean_customers.csv")
    export_clean_csv(out_csv, clean_records)
    
    digest = compute_sha256(out_csv)
    manifest_path = get_safe_path("manifest.json")
    export_manifest(manifest_path, len(clean_records), out_csv.name, digest)
    
    print(f"\nExported {len(clean_records)} clean record(s) to {out_csv.name}")
    print(f"SHA-256 Checksum: {digest[:16]}...")

if __name__ == "__main__":
    main()