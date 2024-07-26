def authentication():

    user_id = input("Enter User ID : ")
    password = input("Enter Password : ")
    
    if user_id == "nineleaps" and password == "nineleaps":
        return True
    else:
        return False

if __name__ == "__main__":
    authentication()