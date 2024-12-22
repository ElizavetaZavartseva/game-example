import copy
import random
import typing as t

VEHICLES = {
    "Car": 20,
    "Van": 40,
    "Bus": 50,
    "Truck": 80,
}


def get_next_task(task_number: int) -> dict[str, t.Any]:
    # TODO: change it to generator (later)

    if task_number == 1:
        task_number = '1st'
    elif task_number == 2:
        task_number = '2nd'
    elif task_number == 3:
        task_number = '3rd'
    else:
        task_number = str(task_number)+ 'th'

    task_type = ['passengers', 'tons of goods']
    task_choice = random.choice(task_type)

    if task_choice == 'passengers':
        task_size = random.randrange(50)
        task_price = 3*task_size
        task_distance = random.randrange(300)
        if task_size <= 3:
            acceptable_vehicles = ["Car", "Bus"]
        else:
            acceptable_vehicles = ["Bus"]

    else:
        task_size = random.randrange(60)
        task_price = 10*task_size
        task_distance = random.randrange(1000)
        if task_size <= 20:
            acceptable_vehicles = ["Van", "Truck"]
        else:
            acceptable_vehicles = ["Truck"]

    current_task = {
        "task_number": task_number,
        "task_size": task_size,
        "task_choice": task_choice,
        "task_price": task_price,
        "acceptable_vehicles": acceptable_vehicles,
        "task_distance": task_distance,
    }
    return current_task


def init_game(balance: int, autopark: list[str]) -> tuple[int, list[str]]:
    # init vars
    curren_balance = balance
    current_autopark = copy.deepcopy(autopark)

    while curren_balance >= min(VEHICLES.values()):
        vehicle_choice = input(f"You can choose your vehicle from this list: {VEHICLES}")

        if VEHICLES[vehicle_choice] > curren_balance:
            print("Sorry, too expensive!")
            affordable_vehicle = {}
            for k, v in VEHICLES.items():
                if VEHICLES[k] <= curren_balance:
                    affordable_vehicle[k] = v
            print(
                f"Ops! You don't have enough gold coins. You can not buy {vehicle_new}, "
                f"but you can choose vehicle from this list {affordable_vehicle}"
            )
            continue

        curren_balance -= VEHICLES[vehicle_choice]
        current_autopark.append(vehicle_choice)
        vehicle_new = input(
            f'Good deal! Now, your curren_balance is {curren_balance} and you own {current_autopark}. Do you wanna buy something else?'
        )

        if vehicle_new == "No":
            break
        elif vehicle_new != 'Yes' and vehicle_new != 'No':
            vehicle_new = input(f'Sorry, I can not understand you:( Please enter "Yes" or "No"')
        # if yes we loop to the next iteration

    
    return curren_balance, current_autopark

def play(balance: int, autopark: list[str]):
    # init vars
    curren_balance = balance
    current_autopark = copy.deepcopy(autopark)
    time_passed = 0
    tasks_in_progress: list[dict[str, t.Any]] = []

    task_number = 0

    while True:
        task_number += 1
        tmp_tasks = []

        for task_message in tasks_in_progress:
            if task_message["task_time"] <= time_passed - task_message["start_time"]:
                print(f"Congrats! Task is completed! You earned {task_message["task_price"] - task_message["task_cost"]} coins")
                curren_balance += task_message["task_price"] - task_message["task_cost"]
                current_autopark.append(task_message["chosen_vehicle"])
            else:
                tmp_tasks.append(task_message)

        tasks_in_progress = copy.deepcopy(tmp_tasks)

        print(f"{len(tasks_in_progress)} tasks are in progress")
        print(f"Available vehicle are: {current_autopark}. Your balance is {curren_balance}")

        if curren_balance >= min(VEHICLES.values()):
            new_vehicle = input(f"You earned enough money to buy new vehicle. Do you want to buy it?")
            if new_vehicle == "Yes":
                curren_balance, current_autopark = init_game(curren_balance, current_autopark)

        next_task = get_next_task(task_number)

        task_message = (
            f'This is your {next_task["task_number"]} task. '
            f'You have to deliver {next_task["task_size"]} {next_task["task_choice"]}.'
            f'You will earn {next_task["task_price"]} gold coins. '
            f'You have to use one of these: {next_task["acceptable_vehicles"]}, '
            f'delivery distance is {next_task["task_distance"]}.'
        )
        print(task_message)

        task_acceptance = input(f"Do you want to accept this task? (type Exit to stop playing)")
        if task_acceptance == "Yes":
            can_be_completed = False
            for acc_veh in next_task["acceptable_vehicles"]:
                if acc_veh in current_autopark:
                    can_be_completed = True
                    break
            if not can_be_completed:
                print("Sorry, you don't have a necessary vehicle")
                continue

            while True:
                chosen_vehicle = input(f"Which vehicle {current_autopark} do you want to use for this task?")
                if chosen_vehicle in next_task["acceptable_vehicles"]:
                    break
                print("Sorry, this vehicle can't be used for this task")
                
            next_task["start_time"] = time_passed
            if chosen_vehicle == "Van":
                task_time = next_task["task_distance"] / 110
                task_cost = 6.75 * next_task["task_size"]
            elif chosen_vehicle == "Truck":
                task_time = next_task["task_distance"] / 80
                task_cost = 6.75 * next_task["task_size"]
            elif chosen_vehicle == "Car":
                task_time = next_task["task_distance"] / 120
                task_cost = 1.25 * next_task["task_size"]
            elif chosen_vehicle == "Bus":
                task_time = next_task["task_distance"] / 80
                task_cost = 1.25 * next_task["task_size"]
            else:
                raise Exception("shouldn't happen")
            next_task["chosen_vehicle"] = chosen_vehicle
            next_task["task_time"] = task_time
            next_task["task_cost"] = task_cost
            print(f"It will take {next_task["task_time"]} hours."
                  f'It will cost {next_task["task_cost"]}. '
                  f'Your profit is {next_task["task_price"] - next_task["task_cost"]} gold coins.'
                  )

            current_autopark.remove(next_task["chosen_vehicle"])
            tasks_in_progress.append(next_task)
        elif task_acceptance == "No":
            pass
        elif task_acceptance == "Exit":
            break
        else:
            print("What's that?")

        time_passed += 1


def start_game():
    balance = 100
    autopark = []

    greeting = (f"Hi there! Now, you are in the game. You have {balance} "
                f"gold coins and you need to create your own auto-park.")
    print(greeting)

    balance, autopark = init_game(balance, autopark)

    print(f"Congratulations! You own {autopark}. Your balance is {balance} gold coins.")

    play(balance, autopark)
    print("Goodbye")


if __name__ == "__main__":
    start_game()

