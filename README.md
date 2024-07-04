# UniAmigo Model

This is a model for [UniAmigo](https://github.com/JDDMR03/UniAmigo) trained with [Rasa Open Source](https://github.com/RasaHQ/rasa).

## Installation and Environment Setup

Here are several commands for installing and testing the model:

1. Clone the repository:
    ```bash
    https://github.com/JDDMR03/UniAmigoModel
    ```

2. Navigate to the project directory:
    ```bash
    cd UniAmigoModel
    ```

> 💡 **Note:**
> 
> You have to install python 3.10 for this project, we recommend you to use [Pyenv](https://github.com/pyenv/pyenv)

3. Creating Virtual Enviroment
    ```bash
    python3 -m venv uniamigo
    source uniamigo/bin/activate
    ```

4. Install the rasa:
    ```bash
    pip3 install rasa
    ```

> 💡 **Note:**
> 
> You have to write `model` as the model directory

5. Navigate to the model directory
    ```bash
    cd model

5. Train the model:
    ```bash
    rasa train
    ```

6. Test the chatbot in the console:
    ```bash
    rasa shell
    ```

