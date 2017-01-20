import queue

a = queue.Queue()
a.put("aaaaa")
while True:
    print("yooo")

    print("ga")
    data = a.get()
    print(data)
