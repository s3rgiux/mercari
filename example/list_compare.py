items_retreived = {}

items_retreived["5x"] = ["Name1", 5555, "Status"]
items_retreived["6x"] = ["Name2", 5255, "Status"]
items_retreived["7x"] = ["Name1", 5355, "Status"]
items_retreived["8x"] = ["Name1", 5555, "Status"]

print("items_retreived")
print(items_retreived)
print(items_retreived["7x"])
print(items_retreived["7x"][0])
print(items_retreived["7x"][1])
print(items_retreived["7x"][2])

items_new = {}

items_new["5x"] = ["Name1", 5555, "Status"]
items_new["6x"] = ["Name2", 5255, "Status"]
items_new["7x"] = ["Name1", 5355, "Status"]
items_new["9x"] = ["Name1", 5555, "Status"]
items_new["10x"] = ["Name1", 7777, "Status"]

#k = "5x"
shared_items = {id: items_retreived[id] for id in items_retreived if id in items_new and items_retreived[id] == items_new[id]}
print("Found the same")
print(shared_items)
print("test keys")
for element in shared_items.items():
    print(element)
    print(element[0]) # key
    print(element[1]) # values
    print(element[1][2])

print(len(shared_items))


print("Not shared items")

print("Found different")

found_different = False

for new_key in items_new.keys():
    print("test key ", new_key)
    found_in_prev_list = False
    for old_key in items_retreived.keys():
        if new_key == old_key:
            found_in_prev_list = True
            print("found same")
            break
    if not found_in_prev_list:
        print("not found!!! new elelemnt")
        found_different = True
        print(new_key, " ", items_new[new_key])
    # if not found_different:
    #     print("element ", new_key ," found")
    #     print(new_key)
if found_different:
    print("new Items!!!")
    items_retreived = items_new
    print("New list")
    print(items_retreived)
    print(len(items_retreived))
else:
    print("nothing new")


