import threading
import time

class FittingRoom:
    def __init__(self, n):
        self.n = n
        self.room_lock = threading.Lock()
        self.blue_count = 0
        self.green_count = 0
        self.blue_available = threading.Condition(self.room_lock)
        self.green_available = threading.Condition(self.room_lock)

    def enter_room(self, thread_id, color):
        with self.room_lock:
            #once threads enter here, they cannot proceed if either  the fitting room contains the opposing color or its full
            while (color == 'blue' and self.green_count > 0) or (color == 'green' and self.blue_count > 0) or \
                    (color == 'blue' and self.blue_count >= self.n) or (color == 'green' and self.green_count >= self.n):
                if color == 'blue':
                    self.blue_available.wait() #the threads will wait here until the state changes
                elif color == 'green':
                    self.green_available.wait()
            print(f"{color} Thread {thread_id} entered fitting room")
            if color == 'blue': #print that only their color is allowed
                self.blue_count += 1
                if self.blue_count == 1:
                    print("Blue only.")
                time.sleep(1)
            elif color == 'green':
                self.green_count += 1
                if self.green_count == 1:
                    print("Green only.")
   
                time.sleep(1)

    def exit_room(self, thread_id, color):
        global blueCustomers, greenCustomers
        with self.room_lock:
            print(f"{color} Thread {thread_id} left the fitting room")
            if color == 'blue':
                self.blue_count -= 1
                blueCustomers -= 1
                time.sleep(1)
                if self.blue_count == 0:
                    print("Empty fitting room.")
                    #ensure blue and green taking turns but if no more green customers then blue can finish
                    self.green_available.notify_all() if greenCustomers > 0 else self.blue_available.notify_all()  
            elif color == 'green':
                self.green_count -= 1
                greenCustomers -= 1
                time.sleep(1)
                if self.green_count == 0:
                    print("Empty fitting room.")
                    #same concept for taking turns
                    self.blue_available.notify_all() if blueCustomers > 0 else self.green_available.notify_all()

def simulate_fitting_room(n, b, g):
    fitting_room = FittingRoom(n)
    threads = []
    global greenCustomers, blueCustomers #keep track of the total customers of each color, to be used in the exit function
    greenCustomers = g
    blueCustomers = b

    for i in range(b + g):
        color = 'blue' if i < b else 'green'
        t = threading.Thread(target=fitting_room_simulation, args=(fitting_room, i+1, color))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

def fitting_room_simulation(fitting_room, thread_id, color):
        # lifecycle of the threads where they enter the room, spend a second, then exit the room
        fitting_room.enter_room(thread_id, color)
        time.sleep(1)
        fitting_room.exit_room(thread_id, color)

if __name__ == "__main__":
    n = int(input("Enter the number of slots inside the fitting room: "))
    b = int(input("Enter the number of blue threads: "))
    g = int(input("Enter the number of green threads: "))

    simulate_fitting_room(n, b, g)
