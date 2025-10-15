from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from database.models import db_session, init_db, get_user, add_item_to_inventory, promocode_used, get_promocode
import random

app = Flask(__name__)
CORS(app)

CASE_ITEMS = [
    {"name": "🗡️ Неоновый меч", "rarity": "Epic", "chance": 5, "gif_url": "/static/assets/epic_sword.gif"},
    {"name": "🎧 Неоновые наушники", "rarity": "Rare", "chance": 15, "gif_url": "/static/assets/rare_headphones.gif"},
    {"name": "💾 USB-брелок", "rarity": "Common", "chance": 80, "gif_url": "/static/assets/common_usb.gif"},
]

@app.route("/open_case", methods=["POST"])
def open_case():
    data = request.get_json()
    user_id = data.get("initData")
    roll = random.randint(1, 100)
    cumulative = 0
    for item in CASE_ITEMS:
        cumulative += item["chance"]
        if roll <= cumulative:
            add_item_to_inventory(user_id, item["name"])
            return jsonify(item)
    return jsonify(CASE_ITEMS[-1])

@app.route("/promo", methods=["POST"])
def promo():
    data = request.get_json()
    user_id = data.get("initData")
    code = data.get("code").strip().upper()
    promo = get_promocode(code)
    if not promo:
        return jsonify({"message": "❌ Промокод не найден."})
    if user_id in (promo.used_by or "").split(","):
        return jsonify({"message": "⚠️ Вы уже использовали этот промокод."})
    if promo.reward_type == "balance":
        user = get_user(user_id)
        user.balance += int(promo.reward_value)
        db_session.commit()
        message = f"✅ Получено {promo.reward_value} монет!"
    elif promo.reward_type == "item":
        add_item_to_inventory(user_id, promo.reward_value)
        message = "🎁 Предмет добавлен в инвентарь!"
    else:
        message = "🎉 Промокод активирован!"
    promocode_used(code, user_id)
    return jsonify({"message": message})

@app.route("/static/assets/<path:filename>")
def serve_gif(filename):
    return send_from_directory("static/assets", filename)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
