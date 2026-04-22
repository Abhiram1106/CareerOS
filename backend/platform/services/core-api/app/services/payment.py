from __future__ import annotations

import hmac
import json
from hashlib import sha256
from typing import Any

import razorpay
import stripe

from ..config import (
    RAZORPAY_CALLBACK_URL,
    RAZORPAY_KEY_ID,
    RAZORPAY_KEY_SECRET,
    RAZORPAY_WEBHOOK_SECRET,
    STRIPE_CANCEL_URL,
    STRIPE_SECRET_KEY,
    STRIPE_SUCCESS_URL,
    STRIPE_WEBHOOK_SECRET,
)

PLANS = {
    "free": {"name": "Free", "price_inr_month": 0},
    "pro": {"name": "Pro", "price_inr_month": 299},
    "premium": {"name": "Premium", "price_inr_month": 799},
}


class PaymentError(ValueError):
    pass


def get_plans():
    return [{"code": code, **data} for code, data in PLANS.items()]


def plan_amount_inr(plan_code: str) -> int:
    if plan_code not in PLANS:
        raise PaymentError("Invalid plan")
    return int(PLANS[plan_code]["price_inr_month"])


def _require(value: str, message: str) -> None:
    if not value:
        raise PaymentError(message)


def _create_stripe_checkout(plan_code: str, transaction_id: int, amount_inr: int, email: str) -> dict[str, Any]:
    _require(STRIPE_SECRET_KEY, "Stripe is not configured")
    stripe.api_key = STRIPE_SECRET_KEY

    session = stripe.checkout.Session.create(
        mode="payment",
        success_url=STRIPE_SUCCESS_URL,
        cancel_url=STRIPE_CANCEL_URL,
        customer_email=email or None,
        line_items=[
            {
                "price_data": {
                    "currency": "inr",
                    "product_data": {"name": f"CareerOS {plan_code.capitalize()} Plan"},
                    "unit_amount": int(amount_inr * 100),
                },
                "quantity": 1,
            }
        ],
        metadata={"transaction_id": str(transaction_id), "plan_code": plan_code},
        payment_intent_data={"metadata": {"transaction_id": str(transaction_id), "plan_code": plan_code}},
    )
    return {
        "provider": "stripe",
        "external_ref": session["id"],
        "checkout_url": session.get("url", ""),
    }


def _create_razorpay_checkout(plan_code: str, transaction_id: int, amount_inr: int, email: str, full_name: str) -> dict[str, Any]:
    _require(RAZORPAY_KEY_ID, "Razorpay key id is not configured")
    _require(RAZORPAY_KEY_SECRET, "Razorpay key secret is not configured")
    client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

    payload: dict[str, Any] = {
        "amount": int(amount_inr * 100),
        "currency": "INR",
        "description": f"CareerOS {plan_code.capitalize()} Plan",
        "reference_id": str(transaction_id),
        "callback_url": RAZORPAY_CALLBACK_URL,
        "callback_method": "get",
        "notes": {"transaction_id": str(transaction_id), "plan_code": plan_code},
    }
    if email:
        payload["customer"] = {"name": full_name or "CareerOS User", "email": email}

    payment_link = client.payment_link.create(payload)
    checkout_url = payment_link.get("short_url") or payment_link.get("url", "")
    return {
        "provider": "razorpay",
        "external_ref": payment_link.get("id", ""),
        "checkout_url": checkout_url,
    }


def create_checkout(provider: str, plan_code: str, transaction_id: int, amount_inr: int, email: str, full_name: str) -> dict[str, Any]:
    if provider == "stripe":
        return _create_stripe_checkout(plan_code=plan_code, transaction_id=transaction_id, amount_inr=amount_inr, email=email)
    if provider == "razorpay":
        return _create_razorpay_checkout(
            plan_code=plan_code,
            transaction_id=transaction_id,
            amount_inr=amount_inr,
            email=email,
            full_name=full_name,
        )
    raise PaymentError("Unsupported provider")


def _verify_razorpay_signature(raw_body: bytes, signature: str) -> None:
    _require(RAZORPAY_WEBHOOK_SECRET, "Razorpay webhook secret is not configured")
    expected = hmac.new(RAZORPAY_WEBHOOK_SECRET.encode("utf-8"), raw_body, sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise PaymentError("Invalid Razorpay webhook signature")


def parse_razorpay_webhook(raw_body: bytes, headers: dict[str, str]) -> dict[str, Any]:
    signature = headers.get("x-razorpay-signature", "")
    if not signature:
        raise PaymentError("Missing Razorpay signature")
    _verify_razorpay_signature(raw_body, signature)

    event = json.loads(raw_body.decode("utf-8"))
    event_name = event.get("event", "")
    if event_name not in {"payment_link.paid", "payment.captured"}:
        return {"ignore": True, "reason": f"Unhandled Razorpay event: {event_name}"}

    payload = event.get("payload", {})
    payment_link_entity = payload.get("payment_link", {}).get("entity", {})
    payment_entity = payload.get("payment", {}).get("entity", {})

    tx_id = (
        payment_link_entity.get("reference_id")
        or payment_entity.get("notes", {}).get("transaction_id")
        or payload.get("payment_link", {}).get("entity", {}).get("notes", {}).get("transaction_id")
    )
    plan_code = (
        payment_entity.get("notes", {}).get("plan_code")
        or payment_link_entity.get("notes", {}).get("plan_code")
        or ""
    )
    external_ref = payment_link_entity.get("id") or payment_entity.get("id") or ""
    status = "captured" if payment_entity.get("status") == "captured" else "paid"

    return {
        "ignore": False,
        "transaction_id": int(tx_id) if str(tx_id).isdigit() else None,
        "external_ref": external_ref,
        "plan_code": plan_code,
        "status": status,
        "event": event_name,
    }


def parse_stripe_webhook(raw_body: bytes, headers: dict[str, str]) -> dict[str, Any]:
    _require(STRIPE_WEBHOOK_SECRET, "Stripe webhook secret is not configured")
    signature = headers.get("stripe-signature", "")
    if not signature:
        raise PaymentError("Missing Stripe signature")

    event = stripe.Webhook.construct_event(raw_body, signature, STRIPE_WEBHOOK_SECRET)
    event_type = event.get("type", "")
    if event_type not in {"checkout.session.completed", "checkout.session.async_payment_succeeded"}:
        return {"ignore": True, "reason": f"Unhandled Stripe event: {event_type}"}

    obj = event.get("data", {}).get("object", {})
    metadata = obj.get("metadata", {}) or {}
    tx_id = metadata.get("transaction_id")
    plan_code = metadata.get("plan_code", "")
    external_ref = obj.get("id", "")
    payment_status = obj.get("payment_status", "")
    status = "succeeded" if payment_status in {"paid", "no_payment_required"} else payment_status or "completed"

    return {
        "ignore": False,
        "transaction_id": int(tx_id) if str(tx_id).isdigit() else None,
        "external_ref": external_ref,
        "plan_code": plan_code,
        "status": status,
        "event": event_type,
    }

