from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)
FILE_NAME_CONTACTS = "contacts.json"
FILE_NAME_USERS = "users.json"
try:
    with open(FILE_NAME_CONTACTS, "r") as file:
        contacts = json.load(file)
except:
    contacts = []


try:
    with open(FILE_NAME_USERS, "r") as file:
        users = json.load(file)
except:
    users = []


# contacts = [
#     {
#         "id": 1,
#         "name": "Ran",
#         "age": 44,
#         "phone": "0521251236",
#         "email": "ran@gmail.com",
#     },
#     {
#         "id": 2,
#         "name": "Piotr",
#         "age": 28,
#         "phone": "0532851633",
#         "email": "piotr@gmail.com",
#     },
# ]


# @app.route("/")
# def welcome_page():
#     # html_str = f"""<h1>Hello World!</h1>
#     # <h2>testing this stuff</h2>
#     # <h3>this is the main page</h3>
#     # <a href="/contacts">contacts list</a><br>
#     # <a href="/add-contact">Add contact</a>
#     # """

#     # return html_str
#     return render_template("welcome.html")


@app.route("/welcome")
def welcome():
    return render_template("welcome.html")


@app.route("/contacts")
def contacts_list():
    # html_str = "<h1>this is a contacts list:</h1>"
    # html_str += "<ol>"
    # for contact in contacts:
    #     html_str += f"<li><a href='contacts/{contact['id']}'>{contact['name']}</a></li>"
    # html_str += "</ol>"
    # html_str += "<a href='/'>back</a>"
    # return html_str
    return render_template("contacts_list.html", contacts=contacts)


@app.route("/contacts/<int:id>")
def contact(id):
    for contact in contacts:
        if contact["id"] == id:
            return render_template("contact.html", contact=contact)


@app.route("/add_contact", methods=["POST", "GET"])
def add_contact():
    # html_str = """<form>
    # First Name:<input type="text">
    # Last Name:<input type="text">
    # <input value="submit" type="submit">
    # </form>
    # <a href='/'>back</a>
    # """
    # return html_str
    #       "id": 4,
    #     "name": "Sven",
    #     "age": 18,
    #     "phone": "0533854562",
    #     "email": "sven@gmail.com",
    #     "is_favorite": true
    #   }
    if request.method == "POST":
        contacts.append(
            {
                "id": contacts[-1]["id"] + 1,
                "name": request.form["contact_name"].capitalize(),
                "age": int(request.form["contact_age"]),
                "phone": request.form["phone_number"],
                "email": request.form["contact_email"],
                "is_favorite": bool(request.form["is_fav"]),
            }
        )
        with open(FILE_NAME_CONTACTS, "w") as file:
            json.dump(contacts, file)
        return redirect(url_for("contacts_list"))
    return render_template("add_contact.html")


@app.route("/contacts/favorites")
def get_favorites():
    # favorites = []
    # for contact in contacts:
    #     if contact["is_favorite"] == True:
    #         favorites.append(contact)
    # return render_template("favorites.html", favorites=favorites)
    return render_template("favorites.html", contacts=contacts)


@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        valid = False
        for user in users:
            if (
                request.form["user_name"] == user["user_name"]
                and request.form["password"] == user["password"]
            ):
                valid = True
                return redirect(url_for("welcome"))
        if not valid:
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        valid = False
        user_names = []
        for user in users:
            user_names.append(user["user_name"])
        if request.form["user_name"] in user_names:
            return redirect(url_for("register"))
        else:
            users.append(
                {
                    "id": users[-1]["id"] + 1,
                    "user_name": request.form["user_name"],
                    "password": request.form["password"],
                }
            )
            with open(FILE_NAME_USERS, "w") as file:
                json.dump(users, file)
            return redirect(url_for("welcome"))
    else:
        return render_template("register.html")


@app.route("/delete_contact/<int:id>")
def delete_contact(id):
    for contact in contacts:
        if contact["id"] == id:
            contacts.remove(contact)
            with open(FILE_NAME_CONTACTS, "w") as file:
                json.dump(contacts, file)
            return redirect(url_for("contacts_list"))


@app.route("/edit_contact/<int:id>", methods=["POST", "GET"])
def edit_contact(id):
    for contact in contacts:
        if contact["id"] == id:
            if request.method == "POST":
                index = contacts.index(contact)
                contacts.pop(index)
                contacts.insert(
                    index,
                    {
                        "id": id,
                        "name": request.form["contact_name"].capitalize(),
                        "age": int(request.form["contact_age"]),
                        "phone": request.form["phone_number"],
                        "email": request.form["contact_email"],
                        "is_favorite": bool(request.form["is_fav"]),
                    },
                )
                with open(FILE_NAME_CONTACTS, "w") as file:
                    json.dump(contacts, file)
                return redirect(url_for("contact", id=id))
            else:
                return render_template("edit_contact.html", contact=contact)


if __name__ == "__main__":
    app.run(debug=True, port=9000)
