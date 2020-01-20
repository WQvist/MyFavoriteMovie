import csv
import mysql.connector

## Connect to MySQL
try:
    mydb = mysql.connector.connect(
        user='$USER', 
        password='$PASS',
        host='$HOST', 
        auth_plugin='mysql_native_password',
        database='mymovies'
    )
    mycursor = mydb.cursor()
except:
    print("MySQL is not running.")


# # Insert movies into db
# mycursor.execute("CREATE TABLE movies (title VARCHAR(255), rating INT, sorted BIT)")
# with open('C:\\Users\\William\\Desktop\\ratings.csv', 'r') as csvfile:
#     MovieReader = csv.reader(csvfile, delimiter=',')
#     next(csvfile)
#     for row in MovieReader:
#         if int(row[1]) > 6: # if rating > 6
#             if row[5] != "movie": # exclude all but movies
#                 mycursor.execute("INSERT INTO movies (title, rating, sorted) VALUES (%s, %s, %s)", (row[3], int(row[1]), 0))
# 
# mycursor.execute("ALTER TABLE movies ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY") 

# mydb.commit()

mycursor.execute("SELECT * FROM movies WHERE sorted = 0")
AllMovies = mycursor.fetchall()
MovieA = AllMovies.pop()
MovieB = AllMovies.pop()
previousA = None
previousB = None
print(len(AllMovies), "movies to go!")
while len(AllMovies)>0:
    response = input("Which do you prefer?\nA: " + MovieA[0] + "\nB: " + MovieB[0] + "\n")
    print()
    if response.lower() == "a":
        try:
            mycursor.execute("UPDATE movies SET sorted = %s WHERE id = %s", (1, int(MovieB[2])))
            previousB = MovieB[2]
            MovieB = AllMovies.pop()
        except:
            print("Could not update database")
            break
    elif response.lower() == "b":
        try:
            mycursor.execute("UPDATE movies SET sorted = %s WHERE id = %s", (1, int(MovieA[2])))
            previousA = MovieA[2]
            MovieA = AllMovies.pop()
        except:
            print("Could not update database")
            break
    elif response.lower() == "z":
        print("Regretting previous choice and shutting down!")
        try:
            mycursor.execute("UPDATE unsorted_movies SET sorted = %s WHERE id = %s", (0, previousA))
            mycursor.execute("SELECT title FROM unsorted_movies WHERE id = %s", (previousA,))
            for row in mycursor.fetchall():
                AllMovies.append(row)
            mycursor.execute("UPDATE unsorted_movies SET sorted = %s WHERE id = %s", (0, previousB))
            mycursor.execute("SELECT title FROM unsorted_movies WHERE id = %s", (previousB,))
            for row in mycursor.fetchall():
                AllMovies.append(row)
            break
        except:
            print("Could not update database")
            break
    elif response.lower() == "q":
        print("Quitting")
        break
    else:
        print("Wrong button?\nq = quit\nz = undo")
        input("Press Enter to continue...")
        print("---")

mydb.commit()
mydb.close()
