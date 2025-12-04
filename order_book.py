class Order:
    def __init__(self, id, side, order_type, price, quantity):
        self.id = id
        self.side = side
        self.order_type = order_type
        self.price = price
        self.quantity = quantity
    
    def __repr__(self):
        return (
            f"Order(id={self.id}, side='{self.side}', "
            f"type='{self.order_type}', price={self.price}, qty={self.quantity})"
        )

def random_order():
    pass

class OrderBook:
    def __init__(self):
        self.bids = {}
        self.bid_prices = []
        self.asks = {}
        self.ask_prices = []

    def __str__(self):
        return (
            "\n------ ORDER BOOK ------\n"
            f"BID PRICES: {self.bid_prices}\n"
            f"BIDS: {self.bids}\n\n"
            f"ASK PRICES: {self.ask_prices}\n"
            f"ASKS: {self.asks}\n"
            "----------------------------\n"
        )


    def place_order(self, order):
        self.order_match(order)             # match only once

        if order.quantity > 0:              # if it's not empty
            if order.side == "buy":         
                self.place_bid(order)
            else:
                self.place_ask(order)

    def place_bid(self, order):
        if order.price not in self.bid_prices:
            self.bids[order.price] = []
            self.bids[order.price].append(order)
            self.bid_prices.append(order.price)
            self.bid_prices.sort(reverse=True)
        else:
            self.bids[order.price].append(order)

    def place_ask(self, order):
        if order.price not in self.ask_prices:
            self.asks[order.price] = []
            self.asks[order.price].append(order)
            self.ask_prices.append(order.price)
            self.ask_prices.sort()
        else:
            self.asks[order.price].append(order)

    def order_match(self, order):
        # compare the incoming order with the opposite side's best order etc
        # check if it's empty

        if order.side == "buy":
            # make sure the ask prices list is not empty 
            if self.ask_prices == []:
                return

            best_ask_price = self.ask_prices[0]             # find the best sell price
            best_ask_order = self.asks[best_ask_price][0]   # get the first order in the best sell price queue (first one)
            qty = best_ask_order.quantity                   # get the quantity of that order

            if order.price >= best_ask_price:                   # first order at price
                buy_matched_quantity = min(order.quantity, qty)     # find the minimum of qty
                order.quantity -= buy_matched_quantity              # subtract the min from the order qty for the incoming order
                best_ask_order.quantity -= buy_matched_quantity     # subtract quantity from existing order
                if best_ask_order.quantity == 0:
                    self.asks[best_ask_price].pop(0)             # remove order from list
                    if self.asks[best_ask_price] == []:
                        self.ask_prices.remove(best_ask_price)
                        self.asks.pop(best_ask_price)
            # do something if there are leftover shares

            else:
                return

        elif order.side == "sell":
            if self.bid_prices == []:
                return
            best_bid_price = self.bid_prices[0]
            best_bid_order = self.bids[best_bid_price][0]
            sell_qty = best_bid_order.quantity

            if order.price <= best_bid_price:
                sell_matched_quantity = min(order.quantity, sell_qty)
                order.quantity -= sell_matched_quantity
                best_bid_order.quantity -= sell_matched_quantity
                if best_bid_order.quantity == 0:
                    self.bids[best_bid_price].pop(0)
                    if self.bids[best_bid_price] == []:
                        self.bid_prices.remove(best_bid_price)
                        self.bids.pop(best_bid_price)
            # do something if there are leftover shares
                        
            else:
                return

def main():
    ob = OrderBook()

    print("Order Book Commands:")
    print("     buy <quantity> <price>")
    print("     sell <quantity> <price>")
    print("     show")
    print("     quit")

    while True:
        command = input("Enter command: ").strip().lower()
        if command == "quit":                               # quit the loop
            print("Existing Order Book...")
            print("BIDS: ", ob.bids)
            print("ASKS: ", ob.asks)
            break
        elif command == "show":                             # show the order book
            print("BIDS: ", ob.bids)
            print("ASKS: ", ob.asks)
            continue

        parts = command.split()         # split into 3 --> action (buy), quantity, price
        if len(parts) != 3:
            print("Invalid format. Example: buy 5 100")
            continue

        side = parts[0]                                 # the word 'buy' or 'sell'
        quantity = int(parts[1])                        # convert quantity to integer
        price = float(parts[2])                         # convert price to float

        order = Order(                                  # create a new Order object
            id = len(ob.bids) + len(ob.asks) + 1,       # num of bids + num of asks + 1
            side=side,
            order_type="limit",
            quantity=quantity,
            price=price
        )

        ob.place_order(order)           # send the order into the OrderBook class

        print(f"Placed {side.upper()} order: qty={quantity}, price={price}")       

if __name__ == "__main__":
    main()          