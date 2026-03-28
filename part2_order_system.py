# Assignment - Part 2: Data Structures
# Theme: Restaurant Menu & Order Management System

import copy

menu = {
    "Paneer Tikka":   {"category": "Starters",  "price": 180.0, "available": True},
    "Chicken Wings":  {"category": "Starters",  "price": 220.0, "available": False},
    "Veg Soup":       {"category": "Starters",  "price": 120.0, "available": True},
    "Butter Chicken": {"category": "Mains",     "price": 320.0, "available": True},
    "Dal Tadka":      {"category": "Mains",     "price": 180.0, "available": True},
    "Veg Biryani":    {"category": "Mains",     "price": 250.0, "available": True},
    "Garlic Naan":    {"category": "Mains",     "price":  40.0, "available": True},
    "Gulab Jamun":    {"category": "Desserts",  "price":  90.0, "available": True},
    "Rasgulla":       {"category": "Desserts",  "price":  80.0, "available": True},
    "Ice Cream":      {"category": "Desserts",  "price": 110.0, "available": False},
}

inventory = {
    "Paneer Tikka":   {"stock": 10, "reorder_level": 3},
    "Chicken Wings":  {"stock":  8, "reorder_level": 2},
    "Veg Soup":       {"stock": 15, "reorder_level": 5},
    "Butter Chicken": {"stock": 12, "reorder_level": 4},
    "Dal Tadka":      {"stock": 20, "reorder_level": 5},
    "Veg Biryani":    {"stock":  6, "reorder_level": 3},
    "Garlic Naan":    {"stock": 30, "reorder_level": 10},
    "Gulab Jamun":    {"stock":  5, "reorder_level": 2},
    "Rasgulla":       {"stock":  4, "reorder_level": 3},
    "Ice Cream":      {"stock":  7, "reorder_level": 4},
}

sales_log = {
    "2025-01-01": [
        {"order_id": 1,  "items": ["Paneer Tikka", "Garlic Naan"],          "total": 220.0},
        {"order_id": 2,  "items": ["Gulab Jamun", "Veg Soup"],              "total": 210.0},
        {"order_id": 3,  "items": ["Butter Chicken", "Garlic Naan"],        "total": 360.0},
    ],
    "2025-01-02": [
        {"order_id": 4,  "items": ["Dal Tadka", "Garlic Naan"],             "total": 220.0},
        {"order_id": 5,  "items": ["Veg Biryani", "Gulab Jamun"],           "total": 340.0},
    ],
    "2025-01-03": [
        {"order_id": 6,  "items": ["Paneer Tikka", "Rasgulla"],             "total": 260.0},
        {"order_id": 7,  "items": ["Butter Chicken", "Veg Biryani"],        "total": 570.0},
        {"order_id": 8,  "items": ["Garlic Naan", "Gulab Jamun"],           "total": 130.0},
    ],
    "2025-01-04": [
        {"order_id": 9,  "items": ["Dal Tadka", "Garlic Naan", "Rasgulla"], "total": 300.0},
        {"order_id": 10, "items": ["Paneer Tikka", "Gulab Jamun"],          "total": 270.0},
    ],
}


def print_cart(cart, title="Current Cart"):
    print(f"\n--- {title} ---")
    if not cart:
        print("Cart is empty.")
        return

    for entry in cart:
        line_total = entry["quantity"] * entry["price"]
        print(f'{entry["item"]:15} x{entry["quantity"]:<3} ₹{line_total:.2f}')


def print_inventory_snapshot(data, title):
    print(f"\n{title}")
    for item, details in data.items():
        print(f'{item:15} Stock: {details["stock"]:2}  Reorder Level: {details["reorder_level"]}')


def task_1():
    print("TASK 1 - EXPLORE THE MENU")
    print("-" * 50)

    categories = []
    for item_name, details in menu.items():
        if details["category"] not in categories:
            categories.append(details["category"])

    for category in categories:
        print(f"\n===== {category} =====")
        for item_name, details in menu.items():
            if details["category"] == category:
                status = "Available" if details["available"] else "Unavailable"
                print(f"{item_name:15} ₹{details['price']:7.2f}   [{status}]")

    total_items = len(menu)
    available_items = 0
    most_expensive_name = ""
    most_expensive_price = 0
    low_priced_items = []

    for item_name, details in menu.items():
        if details["available"]:
            available_items += 1

        if details["price"] > most_expensive_price:
            most_expensive_price = details["price"]
            most_expensive_name = item_name

        if details["price"] < 150:
            low_priced_items.append((item_name, details["price"]))

    print("\nMenu Summary")
    print(f"Total number of items     : {total_items}")
    print(f"Total available items     : {available_items}")
    print(f"Most expensive item       : {most_expensive_name} (₹{most_expensive_price:.2f})")
    print("Items priced under ₹150   :")
    for item_name, price in low_priced_items:
        print(f"  - {item_name} (₹{price:.2f})")


def add_to_cart(cart, item_name, quantity):
    if item_name not in menu:
        print(f"Cannot add '{item_name}': item does not exist in menu.")
        return

    if not menu[item_name]["available"]:
        print(f"Cannot add '{item_name}': item is currently unavailable.")
        return

    for entry in cart:
        if entry["item"] == item_name:
            entry["quantity"] += quantity
            print(f"Updated quantity of '{item_name}' to {entry['quantity']}.")
            return

    cart.append({
        "item": item_name,
        "quantity": quantity,
        "price": menu[item_name]["price"]
    })
    print(f"Added '{item_name}' x{quantity} to cart.")


def remove_from_cart(cart, item_name):
    for index, entry in enumerate(cart):
        if entry["item"] == item_name:
            cart.pop(index)
            print(f"Removed '{item_name}' from cart.")
            return
    print(f"Cannot remove '{item_name}': item not found in cart.")


def update_cart_quantity(cart, item_name, quantity):
    for entry in cart:
        if entry["item"] == item_name:
            entry["quantity"] = quantity
            print(f"Quantity of '{item_name}' updated to {quantity}.")
            return
    print(f"Cannot update '{item_name}': item not found in cart.")


def print_order_summary(cart):
    print("\n========== Order Summary ==========")
    subtotal = 0

    if not cart:
        print("Cart is empty.")
    else:
        for entry in cart:
            line_total = entry["quantity"] * entry["price"]
            subtotal += line_total
            print(f'{entry["item"]:18} x{entry["quantity"]:<3} ₹{line_total:7.2f}')

    gst = subtotal * 0.05
    total_payable = subtotal + gst

    print("------------------------------------")
    print(f"Subtotal:                ₹{subtotal:7.2f}")
    print(f"GST (5%):                ₹{gst:7.2f}")
    print(f"Total Payable:           ₹{total_payable:7.2f}")
    print("====================================")


def task_2():
    print("\nTASK 2 - CART OPERATIONS")
    print("-" * 50)

    cart = []

    add_to_cart(cart, "Paneer Tikka", 2)
    print_cart(cart, "After adding Paneer Tikka x2")

    add_to_cart(cart, "Gulab Jamun", 1)
    print_cart(cart, "After adding Gulab Jamun x1")

    add_to_cart(cart, "Paneer Tikka", 1)
    print_cart(cart, "After adding Paneer Tikka x1 again")

    add_to_cart(cart, "Mystery Burger", 1)
    print_cart(cart, "After trying to add Mystery Burger")

    add_to_cart(cart, "Chicken Wings", 1)
    print_cart(cart, "After trying to add Chicken Wings")

    remove_from_cart(cart, "Gulab Jamun")
    print_cart(cart, "After removing Gulab Jamun")

    print_order_summary(cart)
    return cart


def task_3(final_cart):
    print("\nTASK 3 - INVENTORY TRACKER WITH DEEP COPY")
    print("-" * 50)

    inventory_backup = copy.deepcopy(inventory)

    print("\nDeep copy created successfully.")

    original_stock = inventory["Paneer Tikka"]["stock"]
    inventory["Paneer Tikka"]["stock"] = 99

    print_inventory_snapshot(inventory, "Inventory after manual change")
    print_inventory_snapshot(inventory_backup, "Inventory backup after manual change")

    inventory["Paneer Tikka"]["stock"] = original_stock
    print("\nInventory restored to original state before fulfilment.")

    for entry in final_cart:
        item_name = entry["item"]
        quantity_needed = entry["quantity"]
        available_stock = inventory[item_name]["stock"]

        if available_stock >= quantity_needed:
            inventory[item_name]["stock"] -= quantity_needed
            print(f"Fulfilled {item_name}: deducted {quantity_needed} unit(s).")
        else:
            print(f"Warning: insufficient stock for {item_name}. Only {available_stock} unit(s) available.")
            inventory[item_name]["stock"] = 0

    print("\nReorder Alerts")
    alert_found = False
    for item_name, details in inventory.items():
        if details["stock"] <= details["reorder_level"]:
            alert_found = True
            print(f"⚠ Reorder Alert: {item_name} — Only {details['stock']} unit(s) left (reorder level: {details['reorder_level']})")

    if not alert_found:
        print("No reorder alerts at the moment.")

    print_inventory_snapshot(inventory, "Final inventory")
    print_inventory_snapshot(inventory_backup, "Inventory backup (unchanged)")


def calculate_daily_revenue(log_data):
    revenue_per_day = {}
    for date, orders in log_data.items():
        daily_total = 0
        for order in orders:
            daily_total += order["total"]
        revenue_per_day[date] = daily_total
    return revenue_per_day


def best_selling_day(revenue_per_day):
    best_day = ""
    best_amount = 0
    for date, revenue in revenue_per_day.items():
        if revenue > best_amount:
            best_amount = revenue
            best_day = date
    return best_day, best_amount


def most_ordered_item(log_data):
    item_counts = {}

    for date, orders in log_data.items():
        for order in orders:
            for item in order["items"]:
                if item not in item_counts:
                    item_counts[item] = 0
                item_counts[item] += 1

    top_item = ""
    top_count = 0

    for item, count in item_counts.items():
        if count > top_count:
            top_count = count
            top_item = item

    return top_item, top_count


def print_revenue_table(log_data, title):
    print(f"\n{title}")
    revenue_per_day = calculate_daily_revenue(log_data)
    for date, revenue in revenue_per_day.items():
        print(f"{date} : ₹{revenue:.2f}")

    best_day, best_amount = best_selling_day(revenue_per_day)
    print(f"Best-selling day: {best_day} (₹{best_amount:.2f})")


def task_4():
    print("\nTASK 4 - DAILY SALES LOG ANALYSIS")
    print("-" * 50)

    print_revenue_table(sales_log, "Revenue per day")

    item_name, count = most_ordered_item(sales_log)
    print(f"Most ordered item: {item_name} ({count} orders)")

    sales_log["2025-01-05"] = [
        {"order_id": 11, "items": ["Butter Chicken", "Gulab Jamun", "Garlic Naan"], "total": 490.0},
        {"order_id": 12, "items": ["Paneer Tikka", "Rasgulla"],                     "total": 260.0},
    ]

    print_revenue_table(sales_log, "Revenue per day after adding 2025-01-05")

    print("\nAll orders (numbered using enumerate)")
    order_number = 1
    all_orders = []

    for date, orders in sales_log.items():
        for order in orders:
            all_orders.append((date, order))

    for number, record in enumerate(all_orders, start=1):
        date = record[0]
        order = record[1]
        items_text = ", ".join(order["items"])
        print(f"{number}. [{date}] Order #{order['order_id']} — ₹{order['total']:.2f} — Items: {items_text}")


def main():
    task_1()
    final_cart = task_2()
    task_3(final_cart)
    task_4()


if __name__ == "__main__":
    main()
