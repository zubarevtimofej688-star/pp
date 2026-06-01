file_in = open ("INPUT.TXT", "r", encoding="utf-8")
file_out = open ("OUTPUT.TXT", "r", encoding="utf-8")

N = int(input("ведите номер месяца от 1-12 "))

if N < 1 or N > 12:
    print("Error: месяцы только от 1 and 12.")
else:
    if N in [12, 1, 2]:
        file_out.write = "Winter"
    elif N in [3, 4, 5]:
        file_out.write  =  "Spring"
    elif N in [6, 7, 8]:
        file_out.write  =   "Summer"
    elif N in [9, 10, 11]:
        file_out.write  =   "Autumn"
                   



