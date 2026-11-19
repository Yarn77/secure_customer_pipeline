import re
import html

class InvalidCustomerError(Exception):
    pass

CID_REGEX = re.compile(r"C[0-9]{3}")
PIN_REGEX = re.compile(r"[0-9]{6}")

def validate_record(raw_rec: dict) -> dict:
    cid = raw_rec.get("cid", "").strip().upper()
    email = raw_rec.get("email", "").strip().lower()
    pin = raw_rec.get("pin", "").strip()
    name = html.escape(raw_rec.get("name", "").strip())
    
    if not CID_REGEX.fullmatch(cid):
        raise InvalidCustomerError(f"Invalid CID pattern: {cid}")
    if "@" not in email or "." not in email.split("@")[-1]:
        raise InvalidCustomerError(f"Malformed email format: {email}")
    if not PIN_REGEX.fullmatch(pin):
        raise InvalidCustomerError(f"Invalid pincode format: {pin}")
        
    try:
        spend = float(raw_rec.get("spend", 0))
    except ValueError:
        raise InvalidCustomerError("Spend must be a valid number")
        
    if spend < 0.0:
        raise InvalidCustomerError(f"Negative spend rejected: {spend}")
        
    return {"cid": cid, "name": name, "email": email, "pin": pin, "spend": spend}