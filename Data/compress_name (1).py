# Compress all names into single csv - new entry for each year/name pair
# Ethan Cline-Cole Jan 29 2024

filename = "names/yob"
firstyear = 1880
lastyear = 2022

file = open("all_years.txt","w")
file.write("year,name,sex,count \n")
for year in range(firstyear, lastyear + 1):
    f = open(filename + str(year) + ".txt")
    for line in f.readlines():
        file.write(str(year)+ ","+ line)
    f.close()
file.close()