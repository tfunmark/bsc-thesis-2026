import os
import re
import html
import sqlite3


DB_NAME = "transport.db"
DATA_DIR = "data"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS routes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT NOT NULL UNIQUE,
            name TEXT,
            type TEXT,
            description TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            latitude REAL,
            longitude REAL,
            district TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS route_stops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            route_id INTEGER NOT NULL,
            stop_id INTEGER NOT NULL,
            stop_order INTEGER NOT NULL,
            FOREIGN KEY (route_id) REFERENCES routes(id),
            FOREIGN KEY (stop_id) REFERENCES stops(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS taxi_services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            working_hours TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL UNIQUE,
            username TEXT,
            registered_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()


def clear_data(conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM route_stops")
    cursor.execute("DELETE FROM routes")
    cursor.execute("DELETE FROM stops")
    cursor.execute("DELETE FROM taxi_services")
    conn.commit()


def clean_text(value):
    value = html.unescape(value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def extract_route_number(filename, content):
    match = re.search(r'masstransit-card-header-view__number[^>]*title="([^"]+)"', content)
    if match:
        return clean_text(match.group(1))

    match = re.search(r"bus(\d+)", filename.lower())
    if match:
        return match.group(1)

    return None


def extract_essential_stops(content):
    pattern = r'masstransit-card-header-view__essential-stop[^>]*>(.*?)</'
    found = re.findall(pattern, content, flags=re.DOTALL)

    stops = []
    for item in found:
        item = re.sub(r"<.*?>", "", item)
        item = clean_text(item)
        if item:
            stops.append(item)

    return stops


def extract_all_stops(content):
    stops = []

    aria_matches = re.findall(
        r'<a[^>]*class="[^"]*masstransit-legend-group-view__item-link[^"]*"[^>]*aria-label="([^"]+)"',
        content,
        flags=re.DOTALL
    )

    for item in aria_matches:
        item = clean_text(item)
        if item and item not in stops:
            stops.append(item)

    if stops:
        return stops

    block_matches = re.findall(
        r'<a[^>]*class="[^"]*masstransit-legend-group-view__item-link[^"]*"[^>]*>(.*?)</a>',
        content,
        flags=re.DOTALL
    )

    for item in block_matches:
        item = re.sub(r"<.*?>", "", item)
        item = clean_text(item)
        if item and item not in stops:
            stops.append(item)

    return stops


def insert_route(conn, number, essential_stops):
    cursor = conn.cursor()

    if len(essential_stops) >= 2:
        name = f"{essential_stops[0]} - {essential_stops[-1]}"
        description = f"Route {number}: {essential_stops[0]} to {essential_stops[-1]}"
    else:
        name = f"Route {number}"
        description = f"Bus route {number} in Fergana"

    cursor.execute("""
        INSERT OR IGNORE INTO routes (number, name, type, description)
        VALUES (?, ?, ?, ?)
    """, (number, name, "bus", description))

    conn.commit()

    cursor.execute("SELECT id FROM routes WHERE number = ?", (number,))
    return cursor.fetchone()[0]


def insert_stop(conn, stop_name):
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO stops (name, latitude, longitude, district)
        VALUES (?, NULL, NULL, NULL)
    """, (stop_name,))

    conn.commit()

    cursor.execute("SELECT id FROM stops WHERE name = ?", (stop_name,))
    return cursor.fetchone()[0]


def insert_route_stop(conn, route_id, stop_id, stop_order):
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO route_stops (route_id, stop_id, stop_order)
        VALUES (?, ?, ?)
    """, (route_id, stop_id, stop_order))

    conn.commit()


def add_demo_taxi_services(conn):
    cursor = conn.cursor()

    taxi_data = [
        ("Taxi information", "Not available yet", "24/7"),
        ("Administrator can add taxi services later", "Not available yet", "24/7")
    ]

    for name, phone, hours in taxi_data:
        cursor.execute("""
            INSERT INTO taxi_services (name, phone, working_hours)
            VALUES (?, ?, ?)
        """, (name, phone, hours))

    conn.commit()


def import_routes_from_files(conn):
    if not os.path.exists(DATA_DIR):
        print("Folder 'data' was not found.")
        return

    files = sorted([
        file for file in os.listdir(DATA_DIR)
        if file.lower().startswith("bus") and file.lower().endswith(".txt")
    ])

    if not files:
        print("No bus files found in data folder.")
        return

    for filename in files:
        path = os.path.join(DATA_DIR, filename)

        with open(path, "r", encoding="utf-8") as file:
            content = file.read()

        route_number = extract_route_number(filename, content)
        essential_stops = extract_essential_stops(content)
        all_stops = extract_all_stops(content)

        if not route_number:
            print(f"Route number not found in {filename}")
            continue

        if not all_stops:
            print(f"No stops found in {filename}")
            continue

        route_id = insert_route(conn, route_number, essential_stops)

        for index, stop_name in enumerate(all_stops, start=1):
            stop_id = insert_stop(conn, stop_name)
            insert_route_stop(conn, route_id, stop_id, index)

        print(f"Imported route {route_number}: {len(all_stops)} stops")


def main():
    conn = get_connection()

    create_tables(conn)
    clear_data(conn)
    import_routes_from_files(conn)
    add_demo_taxi_services(conn)

    conn.close()

    print("Database created successfully.")


if __name__ == "__main__":
    main()