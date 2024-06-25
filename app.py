from flask import Flask, render_template
import json

app = Flask(__name__)
FILE_NAME = "contacts.json"
try:
    with open(FILE_NAME, "r") as file:
        contacts = json.load(file)
except:
    contacts = []


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


@app.route("/")
def hello_world():
    html_str = f"""<h1>Hello World!</h1>
    <h2>testing this stuff</h2>
    <h3>this is the main page</h3>
    <a href="/contacts">contacts list</a><br>
    <a href="/add-contact">Add contact</a>
    """

    return html_str


@app.route("/contacts")
def contacts_list():
    # html_str = "<h1>this is a contacts list:</h1>"
    # html_str += "<ol>"
    # for contact in contacts:
    #     html_str += f"<li><a href='contacts/{contact['id']}'>{contact['name']}</a></li>"
    # html_str += "</ol>"
    # html_str += "<a href='/'>back</a>"
    # return html_str
    return render_template("contact_list.html", contacts=contacts)


@app.route("/contacts/<int:id>")
def contact(id):
    for contact in contacts:
        if contact["id"] == id:
            return render_template("contact.html", contact=contact)


@app.route("/add-contact")
def add_contact():
    html_str = """<form>
    First Name:<input type="text">
    Last Name:<input type="text">
    <input value="submit" type="submit">
    </form>
    <a href='/'>back</a> 
    """
    return html_str


@app.route("/contacts/favorites")
def get_favorites():
    # favorites = []
    # for contact in contacts:
    #     if contact["is_favorite"] == True:
    #         favorites.append(contact)
    # return render_template("favorites.html", favorites=favorites)
    return render_template("favorites.html", contacts=contacts)


if __name__ == "__main__":
    app.run(debug=True, port=9000)
