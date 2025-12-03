class Order:
    def __init__(self, id, side, order_type, price, quantity):
        self.id = id
        self.side = side
        self.order_type = order_type
        self.price = price
        self.quantity = quantity

def random_order():
    pass

class OrderBook:
    def __init__(self):
        self.bids = {}
        self.bid_prices = []
        self.asks = {}
        self.ask_prices = []

    def place_order(self, order):
        if order.side == "buy":
            self.order_match(order)
            self.place_bid(order)   # call place bid
        elif order.side == "sell":
            self.order_match(order)
            self.place_ask(order)   # call place ask
            

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
                self.place_bid(order)
                return

            best_ask_price = self.ask_prices[0]             # find the best sell price
            best_ask_order = self.asks[best_ask_price][0]   # get the first order in the best sell price queue (first one)
            qty = best_ask_order.quantity                   # get the quantity of that order

            if order.price >= best_ask_price:                   # first order at price
                matched_quantity = min(order.quantity, qty)     # find the minimum of qty
                order.quantity -= matched_quantity              # subtract the min from the order qty for the incoming order
                best_ask_order.quantity -= matched_quantity     # subtract quantity from existing order
                if best_ask_order == 0:
                    self.asks[best_ask_price].pop(0)             # remove order from list
                    if self.asks[best_ask_price] == {}:
                        self.ask_prices.remove(best_ask_price)
                        self.asks.pop(0)

            else:
                pass
# ----------------------------------------------------------------------------------------------
        elif order.side == "sell":
            if order.price <= self.bid_prices[0]:
                pass
            else:
                pass



o1 = Order(1, "buy", "limit", 100, 5)
