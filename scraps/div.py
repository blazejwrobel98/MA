import os

while True:
    try:
        # clear cmd
        os.system('cls')
    except Exception as e:
        pass
    year_sum = 0
    rate = 1.93
    owned_rates = 50000/rate
    dividend = 0.45
    year = 0
    total_sum = 0

    while True:
        print("Year: " + str(year))
        print("Year sum: " + str(year_sum))
        print("Total sum: " + str(total_sum))
        owned_rates += (1000+year_sum) / rate
        year_sum = round((owned_rates * dividend), 2)
        total_sum = round(total_sum + year_sum, 2)
        year = year + 1
        if year_sum > 1000000:
            print("Year: " + str(year))
            print("Year sum: " + str(year_sum))
            print("Total sum: " + str(total_sum))
            break
    input("Press enter to continue")
