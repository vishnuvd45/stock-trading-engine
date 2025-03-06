 📈 Real-Time Stock Trading Engine

A real-time **Stock Trading Engine** for matching **Buy** and **Sell** orders efficiently.


Features
Supports Buy and Sell orders**  
Handles up to 1,024 stock transactions in a simulation**  
Implements a lock-free linked list to maintain the order book**  
Uses multi-threading to simulate multiple traders and execute trades**  
Ensures thread safety using synchronization**  



Language Used Python 🐍

Run the Program

python StockTrading.py

This will start real-time stock transactions and execute trade matching.

How It Works
Orders are randomly generated as Buy or Sell.
Order book maintains transactions using a lock-free linked list.
Matching orders execute instantly when conditions are met.
Multi-threading handles concurrent traders.
Trade summary is displayed at the end.



License
This project is open-source and available under the MIT License.