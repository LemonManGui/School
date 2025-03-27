def load_data(filename):
    """ Print the elements stored in the text file. """
    # Open file to read
    with open(filename) as f: # f is a file opject
        for line in f: # Read each line as text
            print(int(line)) # Convert to int and append to the list
            
def store_data(filename):
    """ Allows the user to store data to the text file named filename """
    with open(filename, 'w') as f: # f is a file object
        number = 0
        while number != 999: # Loop until user provides magic number
            number = int(input("Please enter number (999 to quit): "))
            if number != 999:
                f.write(str(number) + '\n') # Convert int to str to save
            else:
                break # Exit loop
            
def capitalice(filename):
    with open(filename, 'r') as infile:
        with open('upper_' + filename, 'w') as outfile:
            for line in infile:
                line = line.strip().upper()
                print(line, file=outfile)
                      
            
def main():
        """ Interactive function that allows user to 
            create or consume files of numbers. """
        done = False
        while not done:
            cmd = input("S)ave L)oad Q)uit: ")
            if cmd == 's' or cmd == 'S':
                store_data(input("Enter file name: "))
            elif cmd == 'l' or cmd =='L':
                load_data(input("Enter name of file: "))
            elif cmd == 'q' or cmd =='Q':
                done = True
            else:
                print("ValueError") 

if __name__ == '__main__':
    main()