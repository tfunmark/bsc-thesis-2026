import json
import sqlite3
import time
import urllib.parse
import urllib.request

from config import BOT_TOKEN


DB_NAME = "transport.db"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


def get_connection():
    return sqlite3.connect(DB_NAME)


def api_request(method, params=None):
    if params is None:
        params = {}

    url = f"{API_URL}/{method}"

    data = urllib.parse.urlencode(params).encode("utf-8")

    request = urllib.request.Request(url, data=data)

    with urllib.request.urlopen(request, timeout=60) as response:
        result = response.read().decode("utf-8")
        return json.loads(result)


def send_message(chat_id, text):
    max_length = 3900

    if len(text) <= max_length:
        api_request("sendMessage", {
            "chat_id": chat_id,
            "text": text
        })
        return

    parts = [text[i:i + max_length] for i in range(0, len(text), max_length)]

    for part in parts:
        api_request("sendMessage", {
            "chat_id": chat_id,
            "text": part
        })


def register_user(message):
    user = message.get("from", {})
    telegram_id = user.get("id")
    username = user.get("username")

    if not telegram_id:
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO users (telegram_id, username)
        VALUES (?, ?)
    """, (telegram_id, username))

    conn.commit()
    conn.close()


def handle_start(chat_id):
    text = (
        "👋 Welcome to Fergana Transport Bot!\n\n"
        "This bot helps you find public transport information in Fergana.\n\n"
        "Available commands:\n"
        "/marshrut 1 - show route stops\n"
        "/marshrut 2 - show route stops\n"
        "/marshrut 4 - show route stops\n"
        "/poisk Stop A - Stop B - find route between stops\n"
        "/taxi - show taxi information\n"
        "/help - show help"
    )

    send_message(chat_id, text)


def handle_help(chat_id):
    text = (
        "📌 Help\n\n"
        "Commands:\n\n"
        "/start - start the bot\n"
        "/help - show all commands\n"
        "/marshrut 1 - show stops of route 1\n"
        "/marshrut 2 - show stops of route 2\n"
        "/marshrut 4 - show stops of route 4\n\n"
        "Search example:\n"
        "/poisk Истиклол - Аэропорт\n\n"
        "/taxi - show taxi services\n"
        "/dobavit - suggest new transport information"
    )

    send_message(chat_id, text)


def handle_route(chat_id, args):
    if not args:
        send_message(chat_id, "Please enter route number.\n\nExample:\n/marshrut 1")
        return

    route_number = args.strip()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, number, name, description
        FROM routes
        WHERE number = ?
    """, (route_number,))

    route = cursor.fetchone()

    if not route:
        conn.close()
        send_message(chat_id, f"Route {route_number} was not found.")
        return

    route_id, number, name, description = route

    cursor.execute("""
        SELECT stops.name
        FROM stops
        JOIN route_stops ON stops.id = route_stops.stop_id
        WHERE route_stops.route_id = ?
        ORDER BY route_stops.stop_order
    """, (route_id,))

    stops = cursor.fetchall()
    conn.close()

    if not stops:
        send_message(chat_id, f"No stops found for route {route_number}.")
        return

    stop_lines = []

    for index, stop in enumerate(stops, start=1):
        stop_lines.append(f"{index}. {stop[0]}")

    text = (
        f"🚌 Route {number}\n"
        f"{name}\n\n"
        f"Stops:\n"
        + "\n".join(stop_lines)
    )

    send_message(chat_id, text)


def handle_search(chat_id, args):
    if not args or "-" not in args:
        send_message(
            chat_id,
            "Please use this format:\n\n"
            "/poisk Stop A - Stop B\n\n"
            "Example:\n"
            "/poisk Истиклол - Аэропорт"
        )
        return

    parts = args.split("-", 1)
    from_stop = parts[0].strip()
    to_stop = parts[1].strip()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT r.number, r.name
        FROM routes r
        JOIN route_stops rs1 ON r.id = rs1.route_id
        JOIN stops s1 ON rs1.stop_id = s1.id
        JOIN route_stops rs2 ON r.id = rs2.route_id
        JOIN stops s2 ON rs2.stop_id = s2.id
        WHERE LOWER(s1.name) LIKE LOWER(?)
          AND LOWER(s2.name) LIKE LOWER(?)
    """, (f"%{from_stop}%", f"%{to_stop}%"))

    routes = cursor.fetchall()
    conn.close()

    if not routes:
        send_message(
            chat_id,
            "No direct route was found.\n\n"
            "Try to write stop names more simply.\n"
            "Example:\n"
            "/poisk Истиклол - Аэропорт"
        )
        return

    lines = []

    for route in routes:
        lines.append(f"🚌 Route {route[0]}: {route[1]}")

    text = (
        f"Search result:\n\n"
        f"From: {from_stop}\n"
        f"To: {to_stop}\n\n"
        + "\n".join(lines)
    )

    send_message(chat_id, text)


def handle_taxi(chat_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, phone, working_hours
        FROM taxi_services
        ORDER BY name
    """)

    taxis = cursor.fetchall()
    conn.close()

    if not taxis:
        send_message(
            chat_id,
            "Taxi information is not available yet.\n"
            "It can be added by the administrator later."
        )
        return

    lines = []

    for taxi in taxis:
        name, phone, working_hours = taxi
        lines.append(
            f"🚕 {name}\n"
            f"Phone: {phone}\n"
            f"Working hours: {working_hours}"
        )

    send_message(chat_id, "\n\n".join(lines))


def handle_add(chat_id):
    text = (
        "You can suggest new route or stop information.\n\n"
        "Please send it in this format:\n"
        "Route number: ...\n"
        "Stops: ...\n\n"
        "In this MVP version, suggestions are checked manually."
    )

    send_message(chat_id, text)


def handle_message(message):
    chat = message.get("chat", {})
    chat_id = chat.get("id")
    text = message.get("text", "")

    if not chat_id or not text:
        return

    register_user(message)

    if text.startswith("/start"):
        handle_start(chat_id)

    elif text.startswith("/help"):
        handle_help(chat_id)

    elif text.startswith("/marshrut"):
        args = text.replace("/marshrut", "", 1).strip()
        handle_route(chat_id, args)

    elif text.startswith("/poisk"):
        args = text.replace("/poisk", "", 1).strip()
        handle_search(chat_id, args)

    elif text.startswith("/taxi"):
        handle_taxi(chat_id)

    elif text.startswith("/dobavit"):
        handle_add(chat_id)

    else:
        send_message(
            chat_id,
            "Unknown command.\n\n"
            "Use /help to see available commands."
        )


def main():
    print("Fergana Transport Bot is running...")
    print("Press Ctrl+C to stop.")

    offset = None

    while True:
        try:
            params = {
                "timeout": 30
            }

            if offset is not None:
                params["offset"] = offset

            response = api_request("getUpdates", params)

            if not response.get("ok"):
                print("Telegram API error:", response)
                time.sleep(3)
                continue

            updates = response.get("result", [])

            for update in updates:
                offset = update["update_id"] + 1

                message = update.get("message")

                if message:
                    handle_message(message)

        except KeyboardInterrupt:
            print("Bot stopped.")
            break

        except Exception as error:
            print("Error:", error)
            time.sleep(5)


if __name__ == "__main__":
    main()