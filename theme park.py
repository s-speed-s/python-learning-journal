from queue import Queue
import heapq

#Used https://www.geeksforgeeks.org/queue-in-python/ for queue functions

class ElevatorRide:
    def __init__(self):
        self.stack = []

    def board_guest(self, guest_name):
        self.stack.append(guest_name)
        print(f"{guest_name} has joined the line for the elevator.")

    def start_ride(self, capacity):
        if len(self.stack) == 0:
            print("There is no one in this line.")
            return
        
        print(f"Starting elevator ride with {min(capacity, len(self.stack))} people.")
        for person in range(min(capacity, len(self.stack))):
            guest = self.stack.pop()
            print(f"{guest} has exited the elevator.")
        print("Elevator ride has finished.")

class RollerCoasterRide:
    def __init__(self):
        self.queue = Queue()
    
    def join_queue(self, guest_name):
        self.queue.put(guest_name)
        print(f"{guest_name} joined the line for the roller coaster.")
    
    def start_ride(self, capacity):
        if self.queue.qsize() == 0:
            print("There is no one in this line.")
            return
        
        print(f"Starting roller coaster ride with {min(capacity, self.queue.qsize())} people.")
        for person in range(min(capacity, self.queue.qsize())):
            guest = self.queue.get()
            print(f"{guest} has gotten on the roller coaster.")
        print("Roller coaster ride has completed.")

class VIPRide:
    def __init__(self):
        self.priority_queue = []

    def add_guest(self, guest_name, priority):
        heapq.heappush(self.priority_queue, (priority, guest_name))
        print(f"{guest_name} with priority {priority} has joined the VIP line.")

    def start_ride(self, capacity):
        if len(self.priority_queue) == 0:
            print("There is no one in this line.")
            return
        
        print(f"Starting VIP ride with {min(capacity, len(self.priority_queue))} people.")
        for person in range(min(capacity, len(self.priority_queue))):
            priority, guest = heapq.heappop(self.priority_queue)
            print(f"{guest} (priority {priority}) has gotten on the VIP ride.")
        print("VIP ride has finished.")


#Testing
if __name__ == '__main__':
    #Testing Elevator
    elevator = ElevatorRide()
    print("\nElevator:")
    elevator.board_guest("a")
    elevator.board_guest("b")
    elevator.board_guest("c")
    elevator.start_ride(2)
    
    #Testing Roller Coaster
    rcoaster = RollerCoasterRide()
    print("\nRoller Coaster Simulation:")
    rcoaster.join_queue("a")
    rcoaster.join_queue("b")
    rcoaster.join_queue("c")
    rcoaster.start_ride(4)
    
    #Testing VIP
    vipr = VIPRide()
    print("\nVIP Ride Simulation")
    vipr.start_ride(2)
