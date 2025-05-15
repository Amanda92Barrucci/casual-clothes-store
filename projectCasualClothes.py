'''
Programmed by Amanda Barrucci
Casual Clothes - The purpose of this program is to assist in managing the store's finances by calculating
sales, entry prices, final prices, profitability and inventory.
I - Get information from user: Email if is not a new customer, customer name, customer email, Item ID,
if the customer is enrolled in the loyalty plan and number of items sold.
P - Calculate final price for customer based on the information using mathematical calculations and random will generate
customer ID.
O - Display to the user, final price for the customer, including discounts based on the loyalty plan, profit and final
value in the inventory.
'''

import tkinter, random, re, sys
from webbrowser import open
from datetime import date, timedelta
from tkinter import messagebox, simpledialog

def main():

    #Declare variables
    custName = ""
    custID = 0
    custEmail = ""
    itemID = 0
    invInitial = 100
    invFinal = 0
    newCust = True
    loyal = True
    itemSold = 0
    discount = 0.0
    finalPrice = 0.0
    profit = 0.0
    header = "Casual Clothes"
    count = 0
    newTrans = True
    totalSpent = 0.0
    totalProfit = 0
    confirm = True
    customerData = {} #Create an empty dictionary for customer data - requirement #1

    #Get today's date and use in the welcome page and final message - requirement #6
    today = date.today()
    firstDayNextMonth = (today.replace(day=28) + timedelta(days=4)).replace(day=1)
    lastDayMonth = firstDayNextMonth - timedelta(days=1)
    daysLeft = (lastDayMonth - today).days

    tkinter.messagebox.showinfo(header,  f"Welcome to Casual Clothes!\nToday is {today}.\n"
                                         f"Let's help your customers find the perfect outfits!")


    newCust = tkinter.messagebox.askyesno(header, "Would you like to register a new customer?") #clean up program - requirement #7


    if (newCust):
        #Load existing customer IDs from the file function.
        usedIDs = existingID("file1.txt")
        while True:
            custID = random.randint(1000, 9000)
            if custID not in usedIDs:
                usedIDs.add(custID)
                break

        custName = tkinter.simpledialog.askstring(header, "What's the customer's name?" )
        if custName is None:  # User click "Cancel" sys ends the program - requirement #9
            tkinter.messagebox.showinfo(header, "You canceled the action. Goodbye!")
            sys.exit() #User input validate - requirement #5
        if custName:
            custName = custName.title()
        while (not re.match("^[A-Za-z ]+$", custName)):
            tkinter.messagebox.showerror(header, "That doesn't look like a valid name. Please try again!")
            custName = tkinter.simpledialog.askstring(header, "What's the customer's name?") #User input validate - requirement #5
            if custName:
                custName = custName.title()

        custEmail = tkinter.simpledialog.askstring(header, "What's the customer's email?")
        if custEmail is None:  # User click "Cancel" sys ends the program - requirement #9
            tkinter.messagebox.showinfo(header, "You canceled the action. Goodbye!")
            sys.exit()  #User input validate - requirement #5
        if custEmail:
            custEmail = custEmail.lower()     #clean up program - requirement #7
        while (custEmail == "" or "@" not in custEmail or "." not in custEmail):
            tkinter.messagebox.showerror(header, "Oops! That email doesn't seem right. Please check and try again.")
            custEmail = tkinter.simpledialog.askstring(header, "What's the customer's email?") #User input validate - requirement #5
            if custEmail:
                custEmail = custEmail.lower()   #clean up program - requirement #7

        # Add customer to the dictionary - requirement #1.
        customerData[custID] = {"custName": custName, "custEmail": custEmail, "totalSpent": 0.0, "purchases": []}

        try:                                              #clean up program - requirement #7
            #Save the customer data to file1.txt
            f1 = __builtins__.open("file1.txt", "a")
            f1.write(f"{custID}: Name: {custName}, Email: {custEmail}\n")
            f1.close()
        except FileNotFoundError:
            tkinter.messagebox.showerror(header, f"FILE NOT FOUND.")

    else:
        custEmail = simpledialog.askstring(header, "What's the customer's email?")
        if custEmail is None:  # User click "Cancel" sys ends the program - requirement #9
            tkinter.messagebox.showinfo(header, "You canceled the action. Goodbye!")
            sys.exit() #User input validate - requirement #5
        while (custEmail == "" or "@" not in custEmail or "." not in custEmail):
            tkinter.messagebox.showerror(header, "Oops! That email doesn't seem right. Please check and try again.")
            custEmail = tkinter.simpledialog.askstring(header, "What's the customer's email?") #User input validate - requirement #5

        #Call the get customer data function and use a validation loop until a valid customer is found.
        while True:
            custID, custName, custEmail = getCustomerData (custEmail)
            if custName != "Customer Not Found":
                confirm = tkinter.messagebox.askyesno(header, f"Is this the correct customer?\n {custID}: {custName}, "
                                                              f"{custEmail}")
                if confirm:
                    if custEmail not in customerData:
                        customerData[custID] = {"custName": custName, "custEmail": custEmail, "totalSpent": 0.0,
                                                 "purchases": []}
                    break
                else:
                    tkinter.messagebox.showinfo(header, "Customer email not found. Please try again.")
                    custEmail = simpledialog.askstring(header, "What's the customer's email?") #User input validate - requirement #5
                    if custEmail is None:  # User click "Cancel" sys ends the program - requirement #9
                        tkinter.messagebox.showinfo(header, "You canceled the action. Goodbye!")
                        sys.exit() #User input validate - requirement #5
            else:
                tkinter.messagebox.showerror(header, "We couldn't find a customer with that email. Please try another email.")
                custEmail = simpledialog.askstring(header, "What's the customer's email?") #User input validate - requirement #5
                if custEmail is None:  # User click "Cancel" sys ends the program - requirement #9
                    tkinter.messagebox.showinfo(header, "You canceled the action. Goodbye!")
                    sys.exit() #User input validate - requirement #5



    while(newTrans):
        count += 1

        itemID = tkinter.simpledialog.askinteger(header, "What item was sold?\n1 - Pants\n2 - Shirt\n3 - Dress\n4 - Skirt\n5 - Shorts")
        if itemID is None:  # User click "Cancel" sys ends the program - requirement #9
            tkinter.messagebox.showinfo(header, "You canceled the action. Goodbye!")
            sys.exit() #User input validate - requirement #5
        while (itemID not in [1, 2, 3, 4, 5]):  #User input validate - requirement #5
            tkinter.messagebox.showerror(header, "Invalid item ID. Please select a number between 1 and 5.")
            itemID = tkinter.simpledialog.askinteger(header,"What item was sold?\n1 - Pants\n2 - Shirt\n3 - Dress\n4 - Skirt\n5 - Shorts")

        match itemID:
            case 1:
                finalPrice = 45.00
            case 2:
                finalPrice = 25.00
            case 3:
                finalPrice = 60.00
            case 4:
                finalPrice = 35.00
            case 5:
                finalPrice = 30.00


        itemSold = tkinter.simpledialog.askinteger(header, "How many items were sold? ")
        if itemSold is None:  # User click "Cancel" sys ends the program - requirement #9
            tkinter.messagebox.showinfo(header, "You canceled the action. Goodbye!")
            sys.exit() #User input validate - requirement #5
        while itemSold <= 0:
            tkinter.messagebox.showerror(header, "Invalid entry. The number of items must be greater than zero. Please try again.")
            itemSold = tkinter.simpledialog.askinteger(header, "How many items were sold?") #User input validate - requirement #5


        loyal = tkinter.messagebox.askyesno(header, "Is the customer enrolled in the loyalty program?")

        #Call Function
        discount, finalPrice = applyDiscount(loyal, itemSold, finalPrice)


        entryPrice = (finalPrice / (1 - discount) * 0.7)
        profit = (finalPrice - entryPrice) * itemSold
        invFinal = invInitial - itemSold
        totalSpent += finalPrice * itemSold
        itemTotal = finalPrice * itemSold

        #Update dictionary - requirement #1
        customerData[custID]["purchases"].append({"itemID": itemID, "quantity": itemSold, "pricePerItem": finalPrice,
                                                  "totalPrice": itemTotal})
        customerData[custID]["totalSpent"] += itemTotal


        tkinter.messagebox.showinfo(header,  f"Transaction Details:\n"
                                                    f"- Item ID: {itemID}\n"
                                                    f"- Quantity Sold: {itemSold}\n"
                                                    f"- Discount: {discount * 100:.0f}%\n"
                                                    f"- Price per Item (After Discount): \U0001F4B2{finalPrice:.2f}\n"
                                                    f"- Total Sale: \U0001F4B2{itemTotal:.2f}\n"
                                                    f"- Profit: \U0001F4B2{profit:.2f}\n"
                                                    f"- Inventory Remaining: {invFinal}\n")


        newTrans = tkinter.messagebox.askyesno(header, "Do you want to make another transaction for this customer?")

    #Calculate sum of Profit using a generator expression - requirement #9
    totalProfit = sum((purchase["totalPrice"] - (purchase["pricePerItem"] / (1 - discount) * 0.7 * purchase["quantity"]))
        for purchase in customerData[custID]["purchases"])

    #Display summary at the end of the customer’s session using string concatenation and dictionary  - requirement #9
    summary = f"Summary for Customer {custName}:\n"
    summary += f"Total Spent: \U0001F4B2{customerData[custID]['totalSpent']:.2f}\n"
    summary += f"Total Profit: \U0001F4B2{totalProfit:.2f}\n"
    summary += "Items Purchased:\n"
    for purchase in customerData[custID]["purchases"]:
        summary += f"- Item ID: {purchase['itemID']}, Quantity: {purchase['quantity']}, "
        summary += f"Price: \U0001F4B2{purchase['pricePerItem']:.2f}, Total: \U0001F4B2{purchase['totalPrice']:.2f}\n"
    tkinter.messagebox.showinfo(header, summary)

    #Using the customerData dictionary to store customer details and purchases - requirement #1 and #9
    #Using today's date to create a dynamic filename - requirement #6
    try:                                                                       #clean up program - requirement #7
        f2 = __builtins__.open(f"summary_{today}.txt", "a")
        for custID, data in customerData.items():
                f2.write(f"Customer ID: {custID}, Name: {data['custName']}, Total Spent: ${data['totalSpent']:.2f}\n")
                f2.write("Items Purchased:\n")
                for purchase in data["purchases"]:
                    f2.write(f"- Item ID: {purchase['itemID']}, Quantity: {purchase['quantity']}, ")
                    f2.write(f"Price: ${purchase['pricePerItem']:.2f}, Total: ${purchase['totalPrice']:.2f}\n")
                f2.write("\n")
        f2.close()
    except FileNotFoundError:
        tkinter.messagebox.showerror(header, f"FILE NOT FOUND.")

    #Using the system date to calculation in final message - requirement #6
    tkinter.messagebox.showinfo(header, f"Great job today! There are {daysLeft} days left this month"
                                        f" to increase your sales. Keep it up!")


    url = "https://www.casualclothes.com"
    open(url)


#------------------------------------------FUNCTIONS
#Function to load the dictionary and check customer ID to avoid repeating numbers - requirements #2 and #3
def existingID (fileName = "file1.txt"):

    existID = set()   #Using set() as a new feature - requirement #9
    try:                                                          #clean up program - requirement #7
        file = __builtins__.open(fileName, "r")

        while True:
            line = file.readline()
            if line == "":
                break
            else:
                custID = line.split(":")[0].strip() #Use of new strings - requirement #4
                existID.add(custID)
        file.close()
    except FileNotFoundError:
        pass
    return existID

#Function to load the dictionary, find the customer in the file, and return data to the main function - requirements #2 and #3
def getCustomerData (custEmail1):

    customerFile = "file1.txt"

    try:                                                        #clean up program - requirement #7
        f2 = __builtins__.open(customerFile, "r")

        while True:
            line = f2.readline()
            if line == "":
                break
            else:
                line = line.strip()
                if f"Email: {custEmail1}" in line:
                        parts = line.split(",")
                        custName1 = parts[0].split(": ", 1)[-1].replace("Name: ", "").strip() #Use of new strings - requirement #4
                        custId1 = parts[0].split(":")[0].strip()    #Use of new strings - requirement #4
                        return int(custId1), custName1, custEmail1
        f2.close()
    except FileNotFoundError:
        pass
    return "Customer not Found", "Customer Not Found", "Customer Not Found"


def applyDiscount(loy, itSold, fPrice):

    #local variable
    disc = 0.0

    if (loy and itSold >= 5):
        disc = 0.10
        fPrice = fPrice * (1 - disc)
    elif (loy and itSold < 5):
        disc = 0.05
        fPrice = fPrice * (1 - disc)
    else:
        disc = 0.0

    return disc, fPrice


# Execute main function
main()
