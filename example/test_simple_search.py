import mercari
items = mercari.search("Hioki")
items_list = []

for item in items:
    print("{}, {}, {}, {}, {}, {}".format(item.id, item.status, item.soldOut,
             item.price, item.productName, item.productURL))
    items_list.append([item.id, item.productName, item.price, item.soldOut])

    # self.id = kwargs['productID']
    # self.productURL = "{}{}".format(rootProductURL, kwargs['productID'])
    # self.imageURL = kwargs['imageURL']
    # self.productName = kwargs['name']
    # self.price = kwargs['price']
    # self.status = kwargs['status']
    # self.soldOut = kwargs['status'] != "on_sale"

num_items = len(items_list)

print("Items : ", num_items)

print(items_list)
