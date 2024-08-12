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

### Send a Message

To perform this operation, define the username and the message for the model:
  ```bash
  curl -X POST \
  http://model.uniamigomodel.com/webhooks/rest/webhook \
  -H "Content-Type: application/json" \
  -d '{"sender": "{username}", "message": "{message}"}'
  ```

### Admin Access

To perform this operation, define the username and the password for the model:
 ```bash
curl -X POST http://132.145.171.30:80/api/users \ 
     -H "Content-Type: application/json" \
     -d '{"username": "{username}", "password": "{password}", "is_admin": true}'
```



## API Usage for WINDOWS

### Send a Message

To perform this operation, define the username and the message for the model:
  ```bash
  curl -X POST http://model.uniamigomodel.com/webhooks/rest/webhook -H "Content-Type: application/json" -d "{\"sender\": \"{username}\", \"message\": \"{message}\"}"
  ```

### Admin Access

To perform this operation, define the username and the password for the model:
 ```bash
curl -X POST http://132.145.171.30:80/api/users -H "Content-Type: application/json" -d "{\"username\": \"{username}\", \"password\": \"{password}\", \"is_admin\": true}"
```


> 💡 **Note:**  
> The model saves the conversation from each user in their respective tracker.

### Get a User Tracker
  ```bash
  curl -X GET "http://model.uniamigomodel.com/conversations/{username}/tracker" \
  -H "Content-Type: application/json"
  ```

### Reset a User Tracker
  ```bash
  curl -X POST "http://model.uniamigomodel.com/conversations/{username}/tracker/events" \
  -H "Content-Type: application/json" \
  -d '{"event": "restart"}'
  ```