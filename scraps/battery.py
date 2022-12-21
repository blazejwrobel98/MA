import time
import psutil


def main():
    while True:
        battery = psutil.sensors_battery()
        plugged = battery.power_plugged
        percent = str(battery.percent)
        curr_time = time.strftime("%H:%M:%S")
        plugged = "Plugged In" if plugged else "Not Plugged In"
        if len(state) > 0:
            if state[-1][0] != percent:
                print(f"{curr_time} - {percent}% | {plugged}")
                state.append([percent, curr_time])
        else:
            print(f"{curr_time} - {percent}% | {plugged}")
            state.append([percent, curr_time])
        with open("battery.csv", "w") as f:
            for el in state:
                f.write(f"{el[0]},{el[1]}\n")
        time.sleep(1)


if __name__ == "__main__":
    state = []
    main()
