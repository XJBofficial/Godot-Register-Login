extends Node


onready var UsernameField : LineEdit = get_node("Background/Form/UsernameField")
onready var PasswordField : LineEdit = get_node("Background/Form/PasswordField")
onready var Notification : Label = get_node("Background/Form/Notification")
onready var Request : HTTPRequest = get_node("HTTPRequest")


var Host = "http://127.0.0.1:3000"



func _on_Submit_pressed():
	if UsernameField.text.empty() or PasswordField.text.empty():
		Notification.set_text("Please fill in all the fields.")
		return
	
	
	# Send a request
	
	var Payload = {
		"Username": UsernameField.text,
		"Password": PasswordField.text
	}
	Request.request(Host + "/login", [], false, HTTPClient.METHOD_POST, to_json(Payload))



func _on_HTTPRequest_request_completed(result, response_code, headers, body):
	match response_code:
		200:
			Notification.set_text("Logged in!")
			
			var User = JSON.parse(body.get_string_from_utf8()).result["result"]
			print(User)
		
		404:
			Notification.set_text("User not found.")
		
		403:
			Notification.set_text("Invalid password.")
