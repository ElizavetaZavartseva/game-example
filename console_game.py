import copy
import random
import typing as t

VEHICLES = {
    "Car": 20,
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
        task_cost = 1.25*task_size
        task_distance = random.randrange(300)
        if task_size <= 3:
            task_vehicle = 'Car'
            task_time = task_distance / 120
        else:
            task_vehicle = 'Bus'
            task_time = task_distance / 80

    else:
        task_size = random.randrange(60)
        task_price = 10*task_size
        task_cost = 6.75 * task_size
        task_distance = random.randrange(1000)
        task_vehicle = 'Truck'
        task_time = task_distance / 100

    current_task = {
        "task_number": task_number,
        "task_size": task_size,
        "task_choice": task_choice,
        "task_price": task_price,
        "task_cost": task_cost,
        "task_vehicle": task_vehicle,
        "task_distance": task_distance,
        "task_time": task_time,
    }
    return current_task


def init_game(balance: int, autopark: list[str]) -> tuple[int, list[str]]:
    # init vars
    curren_balance = balance
    current_autopark = copy.deepcopy(autopark)

    greetings = (f"Hi there! Now, you are in the game. You have {curren_balance} "
                 f"gold coins and you need to create your own auto-park.")
    print(greetings)

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

    print(f"Congratulations! You built your own auto-park. Your balance is {curren_balance} gold coins. You own {current_autopark}.")
    # when I don't have enough money it gives me wrong choice of transport. I have 30 coins, I can buy only car, but it suggests me car and bus.
    
    return curren_balance, current_autopark

def play(balance: int, autopark: list[str]):
    # task_acceptance = input(f"Now, it's time to complete 1st task. Do you want to start?")
    # init vars
    curren_balance = balance
    current_autopark = copy.deepcopy(autopark)
    time_passed = 0
    tasks_in_progress: list[dict[str, t.Any]] = []

    task_number = 0

    # TODO: add a chance to buy more vehicles

    while True:
        task_number += 1
        tmp_tasks = []

        for task in tasks_in_progress:
            if task["task_time"] <= time_passed - task["start_time"]:
                print(f"Congrats! Task is completed! You earned {task["task_price"] - task["task_cost"]} coins")
                curren_balance += task["task_price"] - task["task_cost"]
                current_autopark.append(task["task_vehicle"])
            else:
                tmp_tasks.append(task)

        tasks_in_progress = copy.deepcopy(tmp_tasks)

        print(f"{len(tasks_in_progress)} tasks are in progress")
        print(f"Available vehicle are: {current_autopark}. Your balance is {curren_balance}")

        next_task = get_next_task(task_number)

        task = (
            f'This is your {next_task["task_number"]} task. '
            f'You have to deliver {next_task["task_size"]} {next_task["task_choice"]}.'
            f'You will earn {next_task["task_price"]} gold coins. '
            f'It will cost {next_task["task_cost"]}. '
            f'Your profit is {next_task["task_price"] - next_task["task_cost"]} gold coins.'
            f'You have to use {next_task["task_vehicle"]}, '
            f'delivery distance is {next_task["task_distance"]} and it will take {next_task["task_time"]} hours.'
        )
        print(task)
        task_acceptance = input(f"Do you want to accept this task? (type Exit to stop playing)")
        if task_acceptance == "Yes":
            next_task["start_time"] = time_passed
            if next_task["task_vehicle"] in current_autopark:
                current_autopark.remove(next_task["task_vehicle"])
                tasks_in_progress.append(next_task)
            else:
                print(f"Sorry, you don't have a necessary vehicle! You need a {next_task['task_vehicle']}")
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
    balance, autopark = init_game(balance, autopark)
    play(balance, autopark)
    print("Goodbye")


if __name__ == "__main__":
    start_game()

