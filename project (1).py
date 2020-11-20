
#test_data is outside of the classes

def test_data(infileName, category, day):
    
    infile = open(infileName, 'r')
    
    
    linenum = -1
    price = 0
    for line in infile:
        Date, Open, High, Low, Close, adj_close, Volume = line.split(",")
        
        linenum = linenum+1
        if linenum == day and category == "close" :
            price = float(Close)
        elif linenum == day and category == "open":
            price = float(Open)
        
        elif linenum == day and category == "high":
            price = float(High)
        elif linenum == day and category == "low":
            price = float(Low)
    #close file to avoid memory issues   
    infile.close()
    return price

#I have divided my work up into two classes, one class to open and parse the file, and another that has all the algorithms.
#class Filereadandparse takes the file and opens and parses it
#class algorithm has all the trading algorithms and the functions that are used in them.
#there is a main method that tests the trading algorithms.
#class Filereadandparse has all the file parsing functions (used to open and read the file)
#there are two classes of objects: File parsers and algorithms and I have used object oriented design to divide them as such
class Filereadandparse:
#constructive for the Filereadandparse
    def __init__(self):
        self.filename = self.get_filename()
        self.file = self.open()
        self.data = self.parse()
        
    def get_filename(self):
        infile = input('Which file would you like to use? ')
        return infile

    def open(self):
        try:
            file = open(self.filename, 'r')
            return file
        except FileNotFoundError:
            exit()
            
    def parse(self):
        data = []
        for lines in self.file.readlines():
            line = lines.strip().split(',')
            data.append(line)
        return data


#The class algorithm has all the trading functions that were outside of a class in the last milstone 
class Algorithms:
#constructive for the Algorithm class 
    def __init__(self):

        self.file = Filereadandparse()
        self.data = self.file.data
        self.open = self.values(1)
        self.close = self.values(4)
        self.low = self.values(3)
        self.high = self.values(2)
        self.cash_balance = 0
        self.stocks_owned = 0



#bookkeeping function 
    def transact(self, qty, price, buy=False, sell=False):
        Qty = int(qty)
        price = float(price)
        total = price*Qty
        if (buy):
            if (sell):
                #print("Ambigious transaction! Can't determine whether to buy or sell. No action performed.")
                pass
     
                
            elif (self.cash_balance < total):
                #print("Ambigious transaction! Can't determine whether to buy or sell. No action performed.")
                pass
  

            else:
                self.stocks_owned = self.stocks_owned + Qty
                self.cash_balance = self.cash_balance - total
             
        elif (sell):
            if (self.stocks_owned < Qty):
              #print("Ambigious transaction! Can't determine whether to buy or sell. No action performed.")
                pass
            else:
                self.stocks_owned = self.stocks_owned - Qty
                self.cash_balance = self.cash_balance + total
        else:
            print("Ambigious transaction! Can't determine whether to buy or sell. No action performed.")

#moving average algorithm 
    def alg_moving_average(self):
        self.cash_balance = 1000
        self.stocks_owned = 0 
        
        curr_average = 0
        open_vals = self.open
        for i in range(len(open_vals)):
            

            if (i >= 19):
                
                curr_average = sum(open_vals[i-19:i])/20
                curr_price = open_vals[i]
                
                if ((curr_average >= (1.05*curr_price)) and (self.stocks_owned >= 10)):
                    self.transact(10, curr_price, False, True)
                if (curr_average <= (0.95*curr_price)):
                    self.transact(10, curr_price, True, False)
            if (i == (len(open_vals)-1)):
                self.transact(self.stocks_owned, curr_price, False, True)
#below method is used to get particular columns of values from the data 
    def values(self, col):
        values = []
        data = self.data
        del data[0]
        for i in range(len(data)):
            values.append(float(data[i][col]))
        return values
#my trading algorithm 
    def alg_mine(self):
        self.cash_balance = 1000
        self.stocks_owned = 0

        high_so_far = 0
        low_so_far = 2000
    
        for value in range(len(self.high)):
            highstockprice = self.high[value]
            lowstockprice = self.low[value]
            
            stock_buy_max = (self.cash_balance//lowstockprice)
            if (lowstockprice < low_so_far):
                
                low_so_far = lowstockprice
            if (highstockprice > high_so_far):
                
                high_so_far = highstockprice
           
            if (value >= 6):
                
                weekaverage_low = sum(self.low[value-6:value])/7
                weekaverage_high = sum(self.low[value-6:value])/7
            if (value >= 29):
                
                monthaverage_low = sum(self.high[value-29:value])/30
                monthaverage_high = sum(self.high[value-29:value])/30
              
                if (weekaverage_low <= (0.90*monthaverage_low)):
                    
                    self.transact(stock_buy_max, lowstockprice, True, False)
                elif ((weekaverage_high >= (1.1*monthaverage_high)) and (self.stocks_owned >= 5)):
                    
                    self.transact(5, highstockprice, False, True)
            if (value >= 50):
                 
                if (highstockprice == high_so_far):
                    
                    self.transact(self.stocks_owned, highstockprice, False, True)
                    
                if (lowstockprice == low_so_far):
                    
                    self.transact(stock_buy_max, highstockprice,True, False)
                    
            if (value == (len(self.high))-1):
                
                self.transact(self.stocks_owned, highstockprice, False, True)






#main method uses the two classes to tp find the number of stocks and amount of cash left in each algorithm
def main():
  
#creating a new instance of the Algorithm class so that we can use it
    algorithm = Algorithms()
#testing the alg_moving_average 
    print('Testing for alg_moving_average()')
    algorithm.alg_moving_average()
   
    print("The number of stocks left is ", algorithm.stocks_owned, ". The amount of money left is ", algorithm.cash_balance)

    print('Testing for alg_mine()')
    algorithm.alg_mine()
    print("The number of stocks left is  ", algorithm.stocks_owned, ". The amount of money left is ", algorithm.cash_balance)



if __name__ == '__main__':
    main()
