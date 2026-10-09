from __future__ import annotations
import httpx
from app.config import get_settings
from app.models.order import Order

settings = get_settings()

def send_telegram_message(chat_id: str, message: str) -> bool:
    if not settings.TELEGRAM_BOT_TOKEN: return False
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    try:
        httpx.post(url, json=payload)
        return True
    except:
        return False

def send_sms(phone: str, message: str) -> bool:
    if not settings.SMS_API_URL or not settings.SMS_API_KEY: return False
    try:
        httpx.post(settings.SMS_API_URL, json={"api_key": settings.SMS_API_KEY, "phone": phone, "msg": message})
        return True
    except:
        return False

def format_new_order_message(order: Order) -> str:
    return f"New Order {order.order_number}! Total: {order.total_amount}"

def format_reorder_alert_message(product_name: str, current_stock: int, threshold: int) -> str:
    return f"ALERT: Stock for {product_name} is low ({current_stock}). Threshold is {threshold}."
