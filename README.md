# UniAmigo Model

This is a model for [UniAmigo](https://github.com/JDDMR03/UniAmigo) trained with [Rasa Open Source](https://github.com/RasaHQ/rasa).

## Installation and Environment Setup

Follow these steps to install and test the model:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/JDDMR03/UniAmigoModel
    ```

2. **Navigate to the project directory:**
    ```bash
    cd UniAmigoModel
    ```

> 💡 **Note:**  
> You need Python 3.10 for this project. We recommend using [Pyenv](https://github.com/pyenv/pyenv) for managing Python versions.

3. **Create a Virtual Environment:**
    ```bash
    python3 -m venv uniamigo
    source uniamigo/bin/activate
    ```
    If you are using Windows:
    ```bash
    .\venv\Scripts\activate
    ```

4. **Install Rasa:**
    ```bash
    pip install rasa
    ```

5. **Navigate to the model directory:**
    ```bash
    cd model
    ```

6. **Train the model:**
    ```bash
    rasa train
    ```

7. **Open another terminal**

8. **Navigate to the model directory:**
    ```bash
    cd UniAmigoModel/model/
    ```

9. **Enable the API:**
    ```bash
    rasa run --enable-api
    ```

10. **Open another terminal**

11. **Navigate to the actions directory:**
    ```bash
    cd UniAmigoModel/model/actions
    ```

12. **Run the actions:**
    ```bash
    rasa run actions
    ```

13. **Test the chatbot in the console:**
    ```bash
    rasa shell
    ```

## API Usage for LINUX

### Send a Message to the model

To perform this operation, define the username and the message for the model:
  ```bash
  curl -X POST http://model.uniamigomodel.com/api/model/send \
     -H "Authorization: Bearer <JWT_TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{"sender": "{username}", "message": "{message}"}'
  ```

### Create User

To perform this operation, define the username, the password and if it is an admin for the model:
 ```bash
curl -X POST http://model.uniamigomodel.com/api/users \
     -H "Authorization: Bearer <MASTER_TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{"username": "{username}", "password": "{pasword}", "is_admin": {true,false} }'
 ```
 > 💡 **Note:**  
> The password must be 8 digits as minimun, contain a Number and a capital letter

### Delete User

To perform this operation, define the user_id for the model:
 ```bash
 curl -X POST http://model.uniamigomodel.com/api/login \
     -H "Authorization: Bearer <MASTER_TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{"username": "{username}", "password": "{password}"}'
 ```

 ### Login

To perform this operation, define the username and the password
 ```bash
 curl -X DELETE http://model.uniamigomodel.com/api/users/{user_id} \
     -H "Authorization: Bearer <JWT_TOKEN>"
 ```

### Get All Users

 ```bash
 curl -X GET http://model.uniamigomodel.com/api/users \
     -H "Authorization: Bearer <JWT_TOKEN>"
 ```

### Get a Specific User by Username

To perform this operation, define the username
 ```bash
 curl -X GET http://model.uniamigomodel.com/api/users/username/{username} \
     -H "Authorization: Bearer <JWT_TOKEN>"
 ```

### Get a Specific User by ID

To perform this operation, define the user_id
 ```bash
 curl -X GET http://model.uniamigomodel.com/api/users/{user_id} \
     -H "Authorization: Bearer <JWT_TOKEN>"
 ```

### Create a Message

To perform this operation, define the user_id and the message
 ```bash
 curl -X POST http://model.uniamigomodel.com/api/messages \
     -H "Authorization: Bearer <JWT_TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{"user_id": {user_id}, "message_text": "{Message}"}'
 ```

### Delete a Message

To perform this operation, define the messsage_id
 ```bash
 curl -X DELETE http://model.uniamigomodel.com/api/messages/{message_id} \
     -H "Authorization: Bearer <JWT_TOKEN>"
 ```

### Get all Messages

 ```bash
 curl -X GET http://model.uniamigomodel.com/api/messages \
     -H "Authorization: Bearer <JWT_TOKEN>"
 ```

### Get a Specific Message by ID

To perform this operation, define the messsage_id
 ```bash
 curl -X GET http://model.uniamigomodel.com/api/messages/{message_id} \
     -H "Authorization: Bearer <JWT_TOKEN>"
 ```

### Get Messages by User ID

To perform this operation, define the user_id
 ```bash
 curl -X GET http://model.uniamigomodel.com/api/messages/user/{user_id} \
     -H "Authorization: Bearer <JWT_TOKEN>"
 ```

## API Usage for WINDOWS

### Send a Message to the model

To perform this operation, define the username and the message for the model:
  ```cmd
  curl -X POST http://model.uniamigomodel.com/api/model/send ^
     -H "Authorization: Bearer <JWT_TOKEN>" ^
     -H "Content-Type: application/json" ^
     -d "{\"sender\": \"{username}\", \"message\": \"{message}\"}"
  ```

### Create User

To perform this operation, define the username, the password, and if it is an admin for the model:
 ```cmd
curl -X POST http://model.uniamigomodel.com/api/users ^
     -H "Authorization: Bearer <MASTER_TOKEN>" ^
     -H "Content-Type: application/json" ^
     -d "{\"username\": \"{username}\", \"password\": \"{password}\", \"is_admin\": {true,false} }"
 ```

 > 💡 **Note:**  
 > The password must be 8 digits as minimum, contain a Number and a capital letter

### Delete User

To perform this operation, define the user_id for the model:
 ```cmd
 curl -X POST http://model.uniamigomodel.com/api/login ^
     -H "Authorization: Bearer <MASTER_TOKEN>" ^
     -H "Content-Type: application/json" ^
     -d "{\"username\": \"{username}\", \"password\": \"{password}\"}"
 ```

 ### Login

To perform this operation, define the username and the password
 ```cmd
 curl -X DELETE http://model.uniamigomodel.com/api/users/{user_id} ^
     -H "Authorization: Bearer <JWT_TOKEN>"
 ```

### Get All Users

 ```cmd
 curl -X GET http://model.uniamigomodel.com/api/users ^
     -H "Authorization: Bearer <JWT_TOKEN>"
 ```

### Get a Specific User by Username

To perform this operation, define the username
 ```cmd
 curl -X GET http://model.uniamigomodel.com/api/users/username/{username} ^
     -H "Authorization: Bearer <JWT_TOKEN>"
 ```

### Get a Specific User by ID

To perform this operation, define the user_id
 ```cmd
 curl -X GET http://model.uniamigomodel.com/api/users/{user_id} ^
     -H "Authorization: Bearer <JWT_TOKEN>"
 ```

### Create a Message

To perform this operation, define the user_id and the message
 ```cmd
 curl -X POST http://model.uniamigomodel.com/api/messages ^
     -H "Authorization: Bearer <JWT_TOKEN>" ^
     -H "Content-Type: application/json" ^
     -d "{\"user_id\": {user_id}, \"message_text\": \"{Message}\"}"
 ```

### Delete a Message

To perform this operation, define the message_id
 ```cmd
 curl -X DELETE http://model.uniamigomodel.com/api/messages/{message_id} ^
     -H "Authorization: Bearer <JWT_TOKEN>"
 ```

### Get all Messages

 ```cmd
 curl -X GET http://model.uniamigomodel.com/api/messages ^
     -H "Authorization: Bearer <JWT_TOKEN>"
 ```

### Get a Specific Message by ID

To perform this operation, define the message_id
 ```cmd
 curl -X GET http://model.uniamigomodel.com/api/messages/{message_id} ^
     -H "Authorization: Bearer <JWT_TOKEN>"
 ```

### Get Messages by User ID

To perform this operation, define the user_id
 ```cmd
 curl -X GET http://model.uniamigomodel.com/api/messages/user/{user_id} ^
     -H "Authorization: Bearer <JWT_TOKEN>"
 ```