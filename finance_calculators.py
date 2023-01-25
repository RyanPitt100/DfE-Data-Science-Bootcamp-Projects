import math


def main():
    # get calculator type from the user.
    print("Choose either 'investment' or 'bond' from the menu below to proceed:")
    print("\n")
    print("investment - to calculate the amount of interest you'll earn on your investment\n\nbond - to calculate the amount you'll have to pay on a home loan\n")
    choice = input("please enter choice: ").strip().lower()
    # check if user entered a valid responce, and run the calculator if they have.
    if choice == "investment":
        investment()
    elif choice == "bond":
        bond()
    else:
        print("error, invalid selection.")
        return


def investment():
    # get some information from the user, such as amount deposited, how long for, what is the interest rate and simple or compound interest.
    amount = float(input("How much are you depositing? "))
    interest_rate = int(input("What is the interest rate? "))
    years = int(
        input("How many years are you planning on investing this money for? "))
    interest_type = input(
        "Do you want to 'simple' or 'compound' interest to be calculated? ").strip().lower()
    # next based on the type of interest, calculate the total after the given number of years.
    if interest_type == "simple":
        # formula is  A = P(1 + r * t) where A = total, r = interest rate/100, t is time in years, P is amount deposited.
        total = amount * (1 + (interest_rate / 100) * years)
    elif interest_type == "compound":
        # formula for compound interest is A = P(1 + r) ** t
        total = amount * ((1 + (interest_rate / 100)) ** years)
    else:
        print("Sorry, invalid selection.\n")
        return

    # display total and parameters.
    print(f"Depositing ${amount:,.2f} for {years} years with an interest rate of {interest_rate:.2f}% will result in a total amount of ${total:,.2f} following {interest_type} interest.")


def bond():
    # ask user to present some information; the value of the house, interest rate, number of months they plan to repay the bond.
    house_value = int(
        input("What is the value of the house that you are purchasing? "))
    interest_rate = int(input("What is the interest rate? "))
    # dividing interest by 100 here helps us get it as a usable percentage. 5% of 100 is 5, which is 100 * 0.05. 100 * 5 is 500 which is very different from what we want.
    time_to_repay = int(
        input("Over how many months are you planning to repay this bond? "))
    # the repayment formula for a bond is x = (i.P)/(1 - (1 + i) ** (-n))
    # P is the current house value. i  is the interest rate divided by 12. n is the number of months.
    # we need to divide by 100 to get our functional interest for the formula. 5% == 0.05
    month_rate = (interest_rate / 100) / 12
    total = (house_value * month_rate)
    print(f"With a house valuing ${house_value:,}, an annual interest rate of {interest_rate}% over {time_to_repay} months, the monthly amount to be repaid will be ${total:,.2f}")


if __name__ == "__main__":
    main()
