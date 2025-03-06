import threading
import random
import time

class Order:
    def __init__(self, order_type, ticker, quantity, price):
        self.order_type = order_type
        self.ticker = ticker
        self.quantity = quantity
        self.price = price
        self.next = None  # Pointer for linked list

class OrderBook:
    def __init__(self):
        self.head = None
        self.lock = threading.Lock()

    def add_order(self, order):
        with self.lock:
            if not self.head:
                self.head = order
            else:
                current = self.head
                while current.next:
                    current = current.next
                current.next = order

    def get_orders(self):
        orders = []
        current = self.head
        while current:
            if current.quantity > 0:  # Ignore zero-quantity orders
                orders.append(current)
            current = current.next
        return orders

    def remove_filled_orders(self):
        """Removes fully matched orders from the order book"""
        with self.lock:
            prev = None
            current = self.head
            while current:
                if current.quantity == 0:
                    if prev:
                        prev.next = current.next
                    else:
                        self.head = current.next
                    temp = current
                    current = current.next
                    del temp
                else:
                    prev = current
                    current = current.next

class StockTradingEngine:
    def __init__(self):
        self.order_books = [OrderBook() for _ in range(1024)]
        self.matched_trades = []  # Store matched trades for logging

    def addOrder(self, order_type, ticker, quantity, price):
        if quantity <= 0:
            print(f"⚠ Invalid order quantity: {quantity}. Order not added.")
            return
        
        order = Order(order_type, ticker, quantity, price)
        ticker_index = self.getTickerIndex(ticker)
        self.order_books[ticker_index].add_order(order)
        print(f" Added Order: {order_type} {ticker} {quantity} @ {price:.2f}")
        self.matchOrder(ticker_index)

    def matchOrder(self, ticker_index):
        order_book = self.order_books[ticker_index]
        orders = order_book.get_orders()

        buy_orders = [o for o in orders if o.order_type == 'Buy']
        sell_orders = [o for o in orders if o.order_type == 'Sell']

        buy_orders.sort(key=lambda x: x.price, reverse=True)
        sell_orders.sort(key=lambda x: x.price)

        print(f" Buy Orders for {ticker_index}: {[f'{o.quantity} @ {o.price:.2f}' for o in buy_orders]}")
        print(f" Sell Orders for {ticker_index}: {[f'{o.quantity} @ {o.price:.2f}' for o in sell_orders]}")

        i, j = 0, 0
        while i < len(buy_orders) and j < len(sell_orders):
            buy_order = buy_orders[i]
            sell_order = sell_orders[j]

            print(f" Trying to match Buy {buy_order.quantity} @ {buy_order.price:.2f} with Sell {sell_order.quantity} @ {sell_order.price:.2f}")

            if buy_order.price >= sell_order.price:
                matched_quantity = min(buy_order.quantity, sell_order.quantity)
                print(f" Matched: {matched_quantity} of {buy_order.ticker} at {sell_order.price:.2f}")
                
                self.matched_trades.append((buy_order.ticker, matched_quantity, sell_order.price))

                buy_order.quantity -= matched_quantity
                sell_order.quantity -= matched_quantity

                if buy_order.quantity == 0:
                    i += 1
                if sell_order.quantity == 0:
                    j += 1
            else:
                print(f" No match: Buy price {buy_order.price:.2f} < Sell price {sell_order.price:.2f}")
                break

        order_book.remove_filled_orders()

    def getTickerIndex(self, ticker):
        return sum(ord(c) for c in ticker) % 1024

    def simulate_orders(self, order_limit=100):
        order_types = ['Buy', 'Sell']
        tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
        for _ in range(order_limit):
            order_type = random.choice(order_types)
            ticker = random.choice(tickers)
            quantity = random.randint(1, 100)
            price = round(random.uniform(100, 1000), 2)
            self.addOrder(order_type, ticker, quantity, price)
            time.sleep(random.uniform(0.1, 0.5))
        
        print("\n Order simulation complete.")
        self.print_trade_summary()

    def print_trade_summary(self):
        """Prints a summary of all matched trades"""
        print("\n **Trade Summary** ")
        if not self.matched_trades:
            print("No trades were executed.")
        else:
            for ticker, quantity, price in self.matched_trades:
                print(f" {quantity} shares of {ticker} traded at {price:.2f}")
        print("\n")

if __name__ == "__main__":
    trading_engine = StockTradingEngine()
    
    simulation_thread = threading.Thread(target=trading_engine.simulate_orders, args=(100,))
    simulation_thread.start()
    simulation_thread.join()
