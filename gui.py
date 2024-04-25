import customtkinter
import re
from db_connection import Mongo

root = customtkinter.CTk()
loginFrame = customtkinter.CTkFrame(master=root)
registerFrame = customtkinter.CTkFrame(master=root)
mainFrame = customtkinter.CTkFrame(master=root)
informationFrame = customtkinter.CTkFrame(master=mainFrame, width=550, height=500)

loggedInUsername = None
loggedInUserId = None
alreadyError = False


def init():
    customtkinter.set_appearance_mode("system")
    customtkinter.set_default_color_theme("blue")
    root.geometry("700x500")  # Grösse Fenster
    root.title("Rent-A-Room")
    root.resizable(False, False)
    set_login()  # Erstellt zu begin des Programm das login Fenster
    root.mainloop()


# Erstellt ein Error Fenster mit der mitgegebenen Nachricht
def error_frame(error):
    global alreadyError
    if (not (alreadyError == True)):
        alreadyError = True
        errorFrame = customtkinter.CTkToplevel()
        errorFrame.title("Error")
        errorFrame.resizable(False, False)
        errorMessage = customtkinter.CTkLabel(master=errorFrame, text=error)
        errorMessage.pack(pady=10, padx=10)

        def close_error():
            errorFrame.destroy()
            global alreadyError
            alreadyError = False

        closeButton = customtkinter.CTkButton(master=errorFrame, text="Close", command=lambda: close_error())
        closeButton.pack(pady=10, padx=10)
        errorFrame.wm_transient(root)  # Verhindert das das Error Fenster hinter dem Hauptfenster erstellt wird


# Überprüft ob das Passwort "sicher" ist.
def secure_password(password):
    x = re.search("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$", password)
    # (?=.*\d) -> Checkt ob mindestens eine Zahl vorhanden ist
    # (?=.*[a-z]) -> Checkt ob es mindestens ein kleiner Buchstaben hat
    # (?=.*[A-Z]) -> Checkt ob es mindestens ein grossen Buchstaben hat
    # (?=.*[a-zA-Z]) -> Checkt ob es überhaupt ein Zeichen hat
    # {8,} -> Mindestens 8 Zeichen
    return x


def check_login(email, password):
    userInfo = Mongo.getLogin(email)
    if (not userInfo):
        error_frame("Email doesn't exit.")
    elif (userInfo["password"] == password):
        global loggedInUsername
        loggedInUsername = userInfo["name"]
        global loggedInUserId
        loggedInUserId = userInfo["email"]
        set_main()  # Erstellt das eingeloggte GUI
    else:
        error_frame("Wrong password.")


# Erstellt ein User und erkennt alle möglichen Fehler
def create_user(firstname, name, email, address, password, repassword, telnr):
    if (not (email == "")):
        if (not (password == "" or repassword == "")):
            if (password == repassword):
                if (not (secure_password(password) == None)):
                    feedbackCreate = Mongo.createLogin(name, firstname, email, password, telnr, address)
                    print(feedbackCreate)
                    if (not feedbackCreate):
                        error_frame("error: couldn't create user")
                    elif (feedbackCreate == "unique"):
                        error_frame("User already exists.")
                    else:
                        print(Mongo.getLogin(email))
                        registerFrame.pack_forget()
                        set_login()  # Leitet den User nach einem erfolgreichem regristrieren zur Login Seite
                else:
                    error_frame(
                        "The password needs atleast 8 letter. It must contain a small letter, a capital letter, and a number.")
            else:
                error_frame("The passwords don't match.")
        else:
            error_frame("Please enter a password.")
    else:
        error_frame("Please fill out Email, Firstname and Name.")



# Erstellt ein neues Login für einen bestimmten User. IN DER APP ALS S
# Erstellt eine neue Location
def create_room(name, desc, address, rooms, space):
    feedbackCreate = Mongo.createRoom(name, desc, address, rooms, space, loggedInUsername, loggedInUserId)
    if (not feedbackCreate):
        error_frame("error: couldn't create room")
    else:
        set_main()  # Erfrischt die gnaze Seite für das der neue Eintrag sichtbar ist
        set_login_frame(feedbackCreate)  # Zeigt direkt den Eintrag an, wenn dieser erfolgreich erstellt wurde


# Löscht ein Login
def delete_login(id):
    feedbackDelete = Mongo.deleteRoom(id)
    if (not feedbackDelete):
        error_frame("error: couldn't delete login")
    else:
        # Zerstört alle Komponenten auf dem Informations Frame
        for child in informationFrame.winfo_children():
            child.destroy()
        set_main()  # Refreshed die ganze Seite für das der Eintrag nicht mehr sichtbar ist.


# Bearbeitet ein Login
def edit_login(id, plattform, username, password):
    feedbackEdit = Mongo.updateRoomById(id, plattform, username, password)
    if (not feedbackEdit):
        error_frame("error: couldn't update Room")
    else:
        set_main()  # Refreshed die Seite falls es eine Änderung am Titel gäbe
        set_login_frame(id)  # Zeigt den neuen bearbeiteten Eintrag direkt an


# Switched zwischen dem Regristrieren und dem Login Frame
def switch_login_register(switch):
    if switch:
        loginFrame.pack_forget()
        set_register()
    else:
        registerFrame.pack_forget()
        set_login()


def book_room(id):
    room = Mongo.getRoomById(id)
    if room["owner_id"] != loggedInUserId:
        if room["is_booked"] == False:
            Mongo.book_room(id, loggedInUserId)
            P = Mongo.getRoomById(id)
            print(P["is_booked"])
            set_login_frame(id)
        else:
            error_frame("error: Room is already Booked")


def unbook_room(id):
    room = Mongo.getRoomById(id)
    if room["booker_id"] == loggedInUserId:
        if room["is_booked"] == True:
            Mongo.unbook_room(id)
            P = Mongo.getRoomById(id)
            print(P["is_booked"])
            set_login_frame(id)
        else:
            error_frame("error: Room is not booked")
    else:
        error_frame("error: Room is not booked by User")


# Zeigt das den Informations Frame an. Ähnlich wie wenn man den Frame nun sichtbar macht
def grid_information():
    informationFrame.pack_propagate(0)
    informationFrame.grid(pady=10, padx=(0, 10), row=0, rowspan=3, column=1, columnspan=5, sticky='w')


# Erstellt das "Bearbeiten von einem Login" Frame.
def set_edit_login_frame(id):
    login = Mongo.getRoomById(id)
    if (not login):
        error_frame("error: id doesn't match with database entry")
    else:
        informationFrame.grid_remove()
        for child in informationFrame.winfo_children():
            child.destroy()
        plattformEditInput = customtkinter.CTkEntry(master=informationFrame, placeholder_text="Plattform Name")
        plattformEditInput.insert(0, login["name"])  # Fügt in das Eingabefeld die jetzigen Daten ein
        plattformEditInput.pack(pady=10, padx=10)
        usernameEditInput = customtkinter.CTkEntry(master=informationFrame, placeholder_text="Username")
        usernameEditInput.insert(0, login["beschreibung"])  # Fügt in das Eingabefeld die jetzigen Daten ein
        usernameEditInput.pack(pady=10, padx=10)
        passwordEditInput = customtkinter.CTkEntry(master=informationFrame, placeholder_text="Password")
        passwordEditInput.insert(0, login["address"])  # Fügt in das Eingabefeld die jetzigen Daten ein
        passwordEditInput.pack(pady=10, padx=10)
        editButton = customtkinter.CTkButton(master=informationFrame, text="Edit",
                                             command=lambda: edit_login(id, plattformEditInput.get(),
                                                                        usernameEditInput.get(),
                                                                        passwordEditInput.get()))
        editButton.pack(pady=10, padx=10)
        grid_information()

    # Erstellt den Informations Frame für ein einzelnes Login


def set_login_frame(id):
    room = Mongo.getRoomById(id)
    print(room)
    if (not room):
        error_frame("error: id doesn't match with database entry")
    else:
        informationFrame.grid_remove()
        for child in informationFrame.winfo_children():
            child.destroy()
        name = customtkinter.CTkLabel(master=informationFrame, text=room["name"], font=("Roboto", 36))
        name.pack(pady=(10, 30), padx=10)
        desc = customtkinter.CTkLabel(master=informationFrame, text="Description: " + room["beschreibung"])
        desc.pack(pady=10, padx=10)
        owner = customtkinter.CTkLabel(master=informationFrame, text="Owner: " + room["owner"])
        owner.pack(pady=10, padx=10)
        lol = customtkinter.CTkLabel(master=informationFrame, text="Address: " + room["address"])
        lol.pack(pady=10, padx=10)
        lo = customtkinter.CTkLabel(master=informationFrame, text="Room amount: " + room["room_amount"])
        lo.pack(pady=10, padx=10)
        l = customtkinter.CTkLabel(master=informationFrame, text="Space: " + room["space"] + " Meters Squared")
        l.pack(pady=10, padx=10)
        curT = customtkinter.CTkLabel(master=informationFrame, text="Current Tennants: " + room["booker_id"])
        curT.pack(pady=10, padx=10)
        if room["owner"] == loggedInUsername:
            editButton = customtkinter.CTkButton(master=informationFrame, text="Edit Room",
                                                 command=lambda: set_edit_login_frame(id))
            editButton.pack(pady=10, padx=10)
            deleteButton = customtkinter.CTkButton(master=informationFrame, text="Delete Room",
                                                   command=lambda: delete_login(id))
            deleteButton.pack(pady=10, padx=10)
        elif room["is_booked"] == False:
            editButton = customtkinter.CTkButton(master=informationFrame, text="Book Room",
                                                 command=lambda: book_room(id))
            editButton.pack(pady=10, padx=10)
        elif room["is_booked"] == True and room["booker_id"] == loggedInUserId:
            editButton = customtkinter.CTkButton(master=informationFrame, text="unBook Room",
                                                 command=lambda: unbook_room(id))
            editButton.pack(pady=10, padx=10)

        else:
            editButton = customtkinter.CTkButton(master=informationFrame, text="Book Room", state="disabled",
                                                 command=lambda: book_room(id))
            editButton.pack(pady=10, padx=10)

        grid_information()


def show_all():
    informationFrame.grid_remove()
    for child in informationFrame.winfo_children():
        child.destroy()

    informationFrame.pack_propagate(0)
    informationFrame.grid(pady=10, padx=(0, 10), row=0, rowspan=3, column=1, columnspan=5, sticky='w')

    AllRoom = Mongo.getAllRoom("s")
    print(AllRoom)
    if (not AllRoom):
        set_start_frame(False)
    else:
        set_start_frame(True)
        for i in AllRoom:
            frame = customtkinter.CTkFrame(master=informationFrame)
            label = customtkinter.CTkLabel(master=frame, text=(i["name"] + "\n " + i["beschreibung"] + "\n " + i["address"] + "\n " + i["owner"]), font=("Roboto", 16), cursor="hand2")
            label.pack(pady=1, padx=1, fill="x")

            def make_lambda(x):
                return lambda e: set_login_frame(x)

            label.bind("<Button-1>", make_lambda(i["_id"]))  # Bindet das Klick Event auf das Frame
            frame.pack(pady=2, padx=2, fill="x")


# Erstellt das Frame für zum erstellen von einem Login
def set_create_login_frame():
    informationFrame.grid_remove()
    for child in informationFrame.winfo_children():
        child.destroy()
    name = customtkinter.CTkEntry(master=informationFrame, placeholder_text="name")
    name.pack(pady=10, padx=10)
    desc = customtkinter.CTkEntry(master=informationFrame, placeholder_text="desc")
    desc.pack(pady=10, padx=10)
    address = customtkinter.CTkEntry(master=informationFrame, placeholder_text="address")
    address.pack(pady=10, padx=10)
    rooms = customtkinter.CTkEntry(master=informationFrame, placeholder_text="rooms")
    rooms.pack(pady=10, padx=10)
    space = customtkinter.CTkEntry(master=informationFrame, placeholder_text="space")
    space.pack(pady=10, padx=10)
    createButton = customtkinter.CTkButton(master=informationFrame, text="List",
                                           command=lambda: create_room(name.get(), desc.get(), address.get(),
                                                                       rooms.get(), space.get()))
    createButton.pack(pady=10, padx=10)
    grid_information()


# Fügt je nach dem ob man schon Einträge erstellt hat ein anderes Anfangs Frame ein.
def set_start_frame(alreadyEntries):
    if (alreadyEntries):
        description = "Rent-A-Room 0.1 \n by Nicky Lopez"
    else:
        description = 'You currently have no Rooms. \nStart creating your own Rooms by pressing on the "Create Room" button or Search for a Room.'
    informationFrame.grid_remove()
    startTitle = customtkinter.CTkLabel(master=informationFrame,
                                        text="Welcome to Rent-A-Room\n" + loggedInUsername,
                                        font=("Roboto", 36))
    startTitle.pack(pady=(10, 30), padx=10)
    description = customtkinter.CTkLabel(master=informationFrame, text=description)
    description.pack(pady=10, padx=10)
    grid_information()


# Erstellt das einloggen Frame
def set_login():
    loginFrame.pack(pady=90, padx=210, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=loginFrame, text="Login", font=("Roboto", 24))
    label.pack(pady=(55, 20), padx=10)

    email = customtkinter.CTkEntry(master=loginFrame, placeholder_text="Email", width=200)
    email.pack(pady=(12, 5), padx=10)

    password = customtkinter.CTkEntry(master=loginFrame, placeholder_text="Password", show="*", width=200)
    password.pack(pady=(5, 12), padx=10)

    login = customtkinter.CTkButton(master=loginFrame, text="Login",
                                    command=(lambda: check_login(email.get(), password.get())), width=200)
    login.pack(pady=12, padx=10)

    link = customtkinter.CTkFont(family="Roboto", size=12, underline=True)
    register = customtkinter.CTkLabel(master=loginFrame, text="Don't have an account? Sign Up", font=link,
                                      cursor="hand2")
    register.pack(pady=12, padx=10)
    register.bind("<Button-1>", lambda e: switch_login_register(True))  # Bindet das Button-1 (Klick) Event an.


# Erstellt das registrieren Frame
def set_register():
    registerFrame.pack(pady=25, padx=200, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=registerFrame, text="Sign Up", font=("Roboto", 24))
    label.pack(pady=(25, 20), padx=10)

    email = customtkinter.CTkEntry(master=registerFrame, placeholder_text="email", width=200)
    email.pack(pady=(6, 6), padx=10)

    firstname = customtkinter.CTkEntry(master=registerFrame, placeholder_text="firstname", width=200)
    firstname.pack(pady=(6, 6), padx=10)

    name = customtkinter.CTkEntry(master=registerFrame, placeholder_text="name", width=200)
    name.pack(pady=(6, 5), padx=10)

    address = customtkinter.CTkEntry(master=registerFrame, placeholder_text="address", width=200)
    address.pack(pady=(6, 5), padx=10)

    telnr = customtkinter.CTkEntry(master=registerFrame, placeholder_text="Phonenumber", width=200)
    telnr.pack(pady=(6, 5), padx=10)

    password = customtkinter.CTkEntry(master=registerFrame, placeholder_text="Password", show="*", width=200)
    password.pack(pady=(12, 5), padx=10)

    verifyPassword = customtkinter.CTkEntry(master=registerFrame, placeholder_text="Repeat Password", show="*",
                                            width=200)
    verifyPassword.pack(pady=(5, 12), padx=10)

    login = customtkinter.CTkButton(master=registerFrame, text="Sign Up",
                                    command=lambda: create_user(firstname.get(), name.get(), email.get(), address.get(),
                                                                password.get(), verifyPassword.get(), telnr.get()),
                                    width=200)
    login.pack(pady=12, padx=10)

    link = customtkinter.CTkFont(family="Roboto", size=12, underline=True)
    register = customtkinter.CTkLabel(master=registerFrame, text="Already have an account? Login", font=link,
                                      cursor="hand2")
    register.pack(pady=(4, 12), padx=10)
    register.bind("<Button-1>", lambda e: switch_login_register(False))  # Bindet das Button-1 (Klick) Event an.


# Erstellt das Hauptframe nach einem erfolgreichem Login
def set_main():
    loginFrame.pack_forget()
    registerFrame.pack_forget()
    mainFrame.columnconfigure(0, weight=1)  # Einstellung für ein Raster Layout
    mainFrame.columnconfigure(1, weight=1)  # " "
    mainFrame.rowconfigure(1, weight=1)  # " "
    mainFrame.pack(pady=5, padx=5, fill="both", expand=True)

    listFrame = customtkinter.CTkScrollableFrame(master=mainFrame, width=100, height=380)
    listFrame.grid(pady=(10, 0), padx=10, row=0, column=0, sticky='w')

    addLoginButton = customtkinter.CTkButton(master=mainFrame, width=120, height=20, text="Create Room",
                                             command=lambda: set_create_login_frame())
    addLoginButton.grid(pady=(0, 0), padx=10, row=2, column=0, sticky='w')

    addShowAllButton = customtkinter.CTkButton(master=mainFrame, width=120, height=20, text="Show Room",
                                               command=lambda: show_all())
    addShowAllButton.grid(pady=(0, 60), padx=10, row=2, column=0, sticky='w')

    grid_information()

    # Hohlt alle akutellen Logins und zeigt diese am Rand an
    userInfo = Mongo.getRoomByOwner(loggedInUsername, loggedInUserId)
    if (not userInfo):
        set_start_frame(False)
    else:
        set_start_frame(True)
        for i in userInfo:
            frame = customtkinter.CTkFrame(master=listFrame)
            label = customtkinter.CTkLabel(master=frame, text=i["name"], font=("Roboto", 16), cursor="hand2")
            label.pack(pady=1, padx=1, fill="x")

            def make_lambda(x):
                return lambda e: set_login_frame(x)

            label.bind("<Button-1>", make_lambda(i["_id"]))  # Bindet das Klick Event auf das Frame
            frame.pack(pady=2, padx=2, fill="x")
