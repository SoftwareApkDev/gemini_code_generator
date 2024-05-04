"""
This file contains code for the application "Gemini Code Generator".
Author: SoftwareApkDev
"""


# Importing necessary libraries


import google.generativeai as gemini
import sys
import os
from dotenv import load_dotenv
from mpmath import mp, mpf

mp.pretty = True


# Creating static functions to be used in this application.


def is_number(string: str) -> bool:
    try:
        mpf(string)
        return True
    except ValueError:
        return False


def clear():
    # type: () -> None
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows System
    else:
        os.system('clear')  # For Linux System


# Creating main function used to run the application.


def main() -> int:
    """
    This main function is used to run the application.
    :return: an integer
    """

    load_dotenv()
    gemini.configure(api_key=os.environ['GEMINI_API_KEY'])

    # Asking user input values for generation config
    temperature: str = input("Please enter temperature (0 - 1): ")
    while not is_number(temperature) or float(temperature) < 0 or float(temperature) > 1:
        temperature = input("Sorry, invalid input! Please re-enter temperature (0 - 1): ")

    float_temperature: float = float(temperature)

    top_p: str = input("Please enter Top P (0 - 1): ")
    while not is_number(top_p) or float(top_p) < 0 or float(top_p) > 1:
        top_p = input("Sorry, invalid input! Please re-enter Top P (0 - 1): ")

    float_top_p: float = float(top_p)

    top_k: str = input("Please enter Top K (at least 1): ")
    while not is_number(top_k) or int(top_k) < 1:
        top_k = input("Sorry, invalid input! Please re-enter Top K (at least 1): ")

    float_top_k: int = int(top_k)

    max_output_tokens: str = input("Please enter maximum input tokens (at least 1): ")
    while not is_number(max_output_tokens) or int(max_output_tokens) < 1:
        max_output_tokens = input("Sorry, invalid input! Please re-enter maximum input tokens (at least 1): ")

    int_max_output_tokens: int = int(max_output_tokens)

    # Set up the model
    generation_config = {
        "temperature": float_temperature,
        "top_p": float_top_p,
        "top_k": float_top_k,
        "max_output_tokens": int_max_output_tokens,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    model = gemini.GenerativeModel(model_name="gemini-1.0-pro",
                                   generation_config=generation_config,
                                   safety_settings=safety_settings)

    convo = model.start_chat(history=[
    ])

    while True:
        clear()
        language: str = input("What programming language do you want to generate code in? ")
        convo.send_message("Is " + str(language) + " a programming language (one word response only)?")
        language_from_check_answer: str = str(convo.last.text).upper()
        while language_from_check_answer != "YES":
            language = input("Sorry, invalid input! What programming language do you want to generate code in? ")
            convo.send_message("Is " + str(language) + " a programming language (one word response only)?")
            language_from_check_answer = str(convo.last.text).upper()

        code_file_name: str = input("Please enter the name of the file containing the code (include extension please): ")
        convo.send_message("Is " + str(code_file_name) + " a " + str(language).lower().capitalize() +
                           " file (one word response only)?")
        code_file_check_answer: str = str(convo.last.text).upper()
        while code_file_check_answer != "YES":
            code_file_name: str = input(
                "Sorry, invalid input! Please enter the name of the file containing the code (include extension "
                "please): ")
            convo.send_message("Is " + str(code_file_name) + " a " + str(language).lower().capitalize() +
                               " file (one word response only)?")
            code_file_check_answer = str(convo.last.text).upper()

        convo = model.start_chat(history=[
        ])
        prompt: str = """
Write a """ + str(language) + """ program with the following specifications (please include the code only in your response):

"""
        specifications: list = []  # initial value
        print("Enter \"Y\" for yes.")
        print("Enter anything else for no.")
        continue_loop: str = input("Are there any further specifications? ")
        while continue_loop == "Y":
            specification: str = input("Please enter a specification of the code to be generated: ")
            specifications.append(specification)
            continue_loop = input("Are there any further specifications? ")

        for i in range(len(specifications)):
            prompt += """
""" + str(i + 1) + """. """ + str(specifications[i]) + """"""

        convo.send_message(prompt)
        code_response: str = str(convo.last.text)
        code: str = '\n'.join(code_response.split('\n')[1:-1])
        code_file = open("../codes/" + str(code_file_name), "w")
        code_file.write(code)
        code_file.close()

        convo = model.start_chat(history=[
        ])
        convo.send_message("What is the command to run the file \"../codes/" + str(code_file_name)
                           + "\" (only include commands in your response)?")
        run_code_file_command: str = str(convo.last.text)
        print("Executing command: " + str(run_code_file_command))
        os.system(run_code_file_command)

        print("Enter \"Y\" for yes.")
        print("Enter anything else for no.")
        continue_using: str = input("Do you want to continue generating code? ")
        if continue_using != "Y":
            return 0


if __name__ == '__main__':
    main()
