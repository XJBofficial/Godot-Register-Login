from flask import Flask, request, jsonify
import json


Database = Flask(__name__)



@Database.route("/register", methods=["POST"])
def Register():
    Payload = json.loads(request.get_data())

    NewUser = {
        "Username": Payload["Username"],
        "Password": Payload["Password"],
        "Level": 0
    }

    with open("Users.json", "r") as FileRead:
        Users = json.loads(FileRead.read())

        # Check if this user exist

        if Payload["Username"] in Users:
            FileRead.close()
            Users.clear()
            
            return jsonify({
                "result": "This username is already used."
            }), 403

        # Register

        Users[Payload["Username"]] = NewUser

        # Save the users

        with open("Users.json", "w") as FileWrite:
            FileWrite.write(json.dumps(Users, indent=1))
            FileWrite.close()
        
        FileRead.close()
        Users.clear()
    
    return jsonify({
        "result": "A new account created!"
    }), 200



@Database.route("/login", methods=["POST"])
def Login():
    Payload = json.loads(request.get_data())

    with open("Users.json", "r") as FileRead:
        Users = json.loads(FileRead.read())

        # User not found

        if not Payload["Username"] in Users:
            FileRead.close()
            Users.clear()

            return jsonify({
                "result": "User not found"
            }), 404
        
        # Password validation

        User = Users[Payload["Username"]]

        if User["Password"] == Payload["Password"]:
            FileRead.close()
            Users.clear()

            return jsonify({
                "result": User
            }), 200
        else:
            FileRead.close()
            Users.clear()

            return jsonify({
                "result": "Invalid password."
            }), 403



if __name__ == "__main__":
    Database.run(port=3000, debug=True)
