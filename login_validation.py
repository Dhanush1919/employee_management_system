def authenticate_user():

    user_id = input("Enter User ID : ")
    password = input("Enter Password : ")
    
    if user_id == "nineleaps" and password == "nineleaps":
        return True
    else:
        return False