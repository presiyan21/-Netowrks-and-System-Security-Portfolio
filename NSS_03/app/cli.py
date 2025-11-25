from core.auth_system import AuthSystem

# Main auth system
auth = AuthSystem(require_totp=True)  

def run():
    print("1. Register")
    print("2. Login")

    choice = input("Select: ")

    if choice == "1":
        # User registration flow
        u = input("Username: ")
        p = input("Password: ")
        ok, msg = auth.register(u, p)
        print(msg)

        if ok:
            # Show TOTP URI 
            print("TOTP URI:", auth.get_totp_uri(u))

    elif choice == "2":
        # User login flow
        u = input("Username: ")
        p = input("Password: ")
        c = input("TOTP: ")
        ok, msg = auth.authenticate(u, p, c)
        print(msg)

if __name__ == "__main__":
    run()

