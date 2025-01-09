import copy
import random
import typing as t

# VEHICLES = {
#     "Car": 20,
#     "Van": 40,
#     "Bus": 50,
#     "Truck": 80,
# }
class Vehicle:
    price = 0
    capacity = 0
    cost_per1km = 0
    task_type = ''
    max_distance = 0
    earn_per_unit = 0
    vehicle_speed = 0

    def get_task_time(self, distance):
        task_time = distance / self.vehicle_speed
        return task_time

    def get_task_cost(self):
        task_cost = self.cost_per1km * self.capacity
        return task_cost

class Car(Vehicle):
    price = 20
    capacity = 3
    cost_per1km = 1.25
    task_type = 'passengers'
    max_distance = 300
    earn_per_unit = 3
    vehicle_speed = 120

class Van(Vehicle):
    price = 40
    capacity = 20
    cost_per1km = 6.75
    task_type = 'tons of goods'
    max_distance = 1000
    earn_per_unit = 10
    vehicle_speed = 110

class Bus(Vehicle):
    price = 50
    capacity = 60
    cost_per1km = 1.25
    task_type = 'passengers'
    max_distance = 1000
    earn_per_unit = 3
    vehicle_speed = 80

class Truck(Vehicle):
    price = 80
    capacity = 60
    cost_per1km = 6.75
    task_type = 'tons of goods'
    max_distance = 3000
    earn_per_unit = 10
    vehicle_speed = 80


ALL_VEHICLE_TYPES = {
    "Car": Car,
    "Van": Van,
    "Bus": Bus,
    "Truck": Truck
}

class Autopark:

    def __init__(self):
        self.__balance = 100
        self.__autopark: list[Vehicle] = []

    def add_vehicle(self, vehicle: Vehicle):
        self.__autopark.append(vehicle)
        return self.__autopark
    

    def get_balance(self):
        return self.__balance

    def get_autopark(self) -> list[Vehicle]:
        return copy.deepcopy(self.__autopark)

    def set_balance(self, new_balance):
        self.__balance = new_balance
        return self.__balance

    def set_autopark(self, new_autopark):
        self.__autopark = new_autopark
        return self.__autopark

def init_game(autopark):
    # init vars
    curren_balance = autopark.get_balance()
    current_autopark: list[Vehicle] = autopark.get_autopark()

    min_price = min(ALL_VEHICLE_TYPES.values(), key=lambda x: x.price)

    while curren_balance >= min_price.price:
        vehicle_choice = input(f"You can choose your vehicle from this list: {ALL_VEHICLE_TYPES}")

        if ALL_VEHICLE_TYPES[vehicle_choice].price > curren_balance:
            print("Sorry, too expensive!")
            affordable_vehicle = {}
            for k, v in ALL_VEHICLE_TYPES.items():
                if v.price <= curren_balance:
                    affordable_vehicle[k] = v
            print(
                f"Ops! You don't have enough gold coins. You can not buy {vehicle_choice}, "
                f"but you can choose vehicle from this list {affordable_vehicle}"
            )
            continue

        curren_balance -= ALL_VEHICLE_TYPES[vehicle_choice].price
        current_autopark.append(ALL_VEHICLE_TYPES[vehicle_choice]())
        if curren_balance >= min_price.price:
            vehicle_new = input(
                f'Good deal! Now, your curren_balance is {curren_balance} and you own {current_autopark}. Do you wanna buy something else?'
            )

            if vehicle_new == "No":
                break
            elif vehicle_new != 'Yes' and vehicle_new != 'No':
                vehicle_new = input(f'Sorry, I can not understand you:( Please enter "Yes" or "No"')
            # if yes we loop to the next iteration
        print(f"Congratulations! You own {current_autopark}. Your balance is {curren_balance} gold coins.")

    autopark.set_balance(curren_balance)
    autopark.set_autopark(current_autopark)

    return autopark


class Task:

    def __init__(self):
        self.task_type = ['passengers', 'tons of goods']

    def get_next_task(self, task_number):
        task_choice = random.choice(self.task_type)

        acceptable_vehicles = {k:v for k, v in ALL_VEHICLE_TYPES.items() if v.task_type == task_choice}
        max_capacity = max(acceptable_vehicles.values(), key=lambda x: x.price)
        task_size = random.randrange(1, max_capacity.capacity)
        max_distance = max(acceptable_vehicles.values(), key=lambda x: x.max_distance)
        task_distance = random.randrange(1, max_distance.max_distance)
        max_earning = max(acceptable_vehicles.values(), key=lambda x: x.earn_per_unit)
        task_price = max_earning.earn_per_unit * task_size


        current_task = {
            "task_number": task_number,
            "task_size": task_size,
            "task_choice": task_choice,
            "task_price": task_price,
            "acceptable_vehicles": acceptable_vehicles,
            "task_distance": task_distance,
        }

        return current_task

def play(autopark: Autopark):
    # init vars
    curren_balance = autopark.get_balance()
    current_autopark = autopark.get_autopark()
    time_passed = 0
    tasks_in_progress: list[dict[str, t.Any]] = []

    task_number = 0

    print('LOL LOL LOL')
    print('curren_balance', curren_balance)
    print('current_autopark', current_autopark)

    while True:
        task_number += 1
        tmp_tasks = []

        for task_message in tasks_in_progress:
            if task_message["task_time"] <= time_passed - task_message["start_time"]:
                print(f"Congrats! Task is completed! You earned {task_message["task_price"] - task_message["task_cost"]} coins")
                curren_balance += task_message["task_price"] - task_message["task_cost"]
                current_autopark.append(veh)
            else:
                tmp_tasks.append(task_message)

        tasks_in_progress = copy.deepcopy(tmp_tasks)

        print(f"{len(tasks_in_progress)} tasks are in progress")
        print(f"Available vehicle are: {current_autopark}. Your balance is {curren_balance}")

        min_price = min(ALL_VEHICLE_TYPES.values(), key=lambda x: x.price)
        if curren_balance >= min_price.price:
            new_vehicle = input(f"You earned enough money to buy new vehicle. Do you want to buy it?")
            if new_vehicle == "Yes":
                autopark.set_balance(curren_balance)
                autopark.set_autopark(current_autopark)
                autopark = init_game(autopark)

        next_task = Task().get_next_task(task_number)

        task_message = (
            f'This is your {next_task["task_number"]} task. '
            f'You have to deliver {next_task["task_size"]} {next_task["task_choice"]}.'
            f'You will earn {next_task["task_price"]} gold coins.'
            f'You have to use one of these: {next_task["acceptable_vehicles"]}, '
            f'delivery distance is {next_task["task_distance"]}.'
        )
        print(task_message)

        print("next_task[acceptable_vehicles]", next_task["acceptable_vehicles"])
        print("next_task[acceptable_vehicles].values()", next_task["acceptable_vehicles"].values())
        print("current_autopark", current_autopark)

        task_acceptance = input(f"Do you want to accept this task? (type Exit to stop playing)")
        if task_acceptance == "Yes":
            can_be_completed = False
            for acc_veh in next_task["acceptable_vehicles"].values():
                print(acc_veh.__name__)
                if acc_veh.__name__ in [type(x).__name__ for x in current_autopark]:
                    can_be_completed = True
                    break
            if not can_be_completed:
                print("Sorry, you don't have a necessary vehicle")
                continue

            while True:
                chosen_vehicle = input(f"Which vehicle {current_autopark} do you want to use for this task?")
                if chosen_vehicle in next_task["acceptable_vehicles"].keys():
                    break
                print("Sorry, this vehicle can't be used for this task")
            # break
    #
            # print("next_task:", next_task)
            # print("next_task['acceptable_vehicles'][chosen_vehicle]:", next_task['acceptable_vehicles'][chosen_vehicle])
            #
            # print("LOL", next_task['acceptable_vehicles'][chosen_vehicle].get_task_cost(100))

            next_task["start_time"] = time_passed
            veh = None
            for v in current_autopark:
                if type(v).__name__ == chosen_vehicle:
                    veh = v
                else:
                    "Sorry, you don't have a necessary vehicle."
            next_task["task_time"] = veh.get_task_time(next_task['task_distance'])
            next_task["task_cost"] = veh.get_task_cost()

            print(f"It will take {next_task["task_time"]} hours."
                  f'It will cost {next_task["task_cost"]}.'
                  f'Your profit is {next_task["task_price"] - next_task["task_cost"]} gold coins.'
                  )
        #
            current_autopark.remove(veh)
            tasks_in_progress.append(next_task)
        elif task_acceptance == "No":
            pass
        elif task_acceptance == "Exit":
            break
        else:
            print("What's that?")

        time_passed += 1



def start_game(autopark: Autopark):
    balance = autopark.get_balance()

    greeting = (f"Hi there! Now, you are in the game. You have {balance} "
                f"gold coins and you need to create your own auto-park.")
    print(greeting)


    autopark_game_init = init_game(autopark)

    print(f"Congratulations! You own {autopark_game_init.get_autopark()}. Your balance is {autopark_game_init.get_balance()} gold coins.")

    play(autopark_game_init)
    print("Goodbye")

if __name__ == "__main__":
    start_game(Autopark())


