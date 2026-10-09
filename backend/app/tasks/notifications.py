from __future__ import annotations
from app.tasks.celery_app import celery_app
from app.tasks.database import get_sync_db
from app.models.order import Order
from app.models.product import GlobalProduct
from app.services.notification_service import send_telegram_message, send_sms, format_new_order_message, format_reorder_alert_message

@celery_app.task
def notify_wholesaler_new_order(order_id: str):
    db = next(get_sync_db())
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        msg = format_new_order_message(order)
        send_telegram_message("wholesaler_chat_id", msg)

@celery_app.task
def notify_return_act(return_act_id: str):
    send_telegram_message("wholesaler_chat_id", f"New Return Act: {return_act_id}")

@celery_app.task
def send_reorder_alert(branch_id: str, product_id: str, current_stock: int, threshold: int):
    db = next(get_sync_db())
    prod = db.query(GlobalProduct).filter(GlobalProduct.id == product_id).first()
    if prod:
        msg = format_reorder_alert_message(prod.title, current_stock, threshold)
        send_telegram_message("retailer_chat_id", msg)

@celery_app.task
def send_sms_notification(phone: str, message: str):
    send_sms(phone, message)
