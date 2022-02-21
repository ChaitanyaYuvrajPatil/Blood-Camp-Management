import mysql.connector as mc

try:
    mydb = mc.connect(
        host="localhost",
        user='root',
        password='Lucifer@123',
        database='blood_camp'
    )

    total_A1 = 0
    total_A2 = 0
    total_B1 = 0
    total_B2 = 0
    total_AB1 = 0
    total_AB2 = 0
    total_O1 = 0
    total_O2 = 0
    mycursor = mydb.cursor()
    table_name = 'doner_data'
    mycursor.execute("SELECT Blood_Group,Blood_Donated FROM {}".format(table_name))
    result = mycursor.fetchall()


    for item in result:
        if item[0] == 'A+':
            total_A1 = total_A1 + int(item[1])
        if item[0] == 'A-':
            total_A1 = total_A2 + int(item[1])
        if item[0] == 'B+':
            total_B1 = total_B1 + int(item[1])
        if item[0] == 'B-':
            total_B2 = total_B2 + int(item[1])
        if item[0] == 'AB+':
            total_AB1 = total_AB1 + int(item[1])
        if item[0] == 'AB-':
            total_AB2 = total_AB2 + int(item[1])
        if item[0] == 'O+':
            total_O1 = total_O1 + int(item[1])
        if item[0] == 'O-':
            total_O2 = total_O2 + int(item[1])

    print(total_A1)


    mydb.commit()
    mycursor.close()
    mydb.close()
    # self.db_to_table_doner()
except mc.Error as e:
    print(e)
    pass