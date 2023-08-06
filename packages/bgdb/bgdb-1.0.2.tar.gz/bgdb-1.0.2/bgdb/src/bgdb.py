from getpass import getpass
import requests
import json
from dotenv import dotenv_values


# Class which represents the overall blood group database client
class BGDBClient:
    def __init__(self, url):
        # URL of the database API
        self.url = url

        # Create a requests session
        self.session = requests.session()

        # Test the connection
        self.test_connection()

    def test_connection(self):

        # Check the database is alive
        response = self.session.get(self.url + "/")

        # Check the response is valid
        if response.status_code == 200:
            print(f"Server: {self.url} is alive.")
        else:
            raise Exception(f"Server: {self.url} is unresponsive.")

    def login(self, use_env=False):

        if use_env:
            config = dotenv_values()
            # Get the email and password from the environment
            self.email = config["EMAIL"]
            self.password = config["PASSWORD"]
        else:
            self.email = input("Enter your email: ")
            self.password = getpass("Enter your password: ")

        # Login to the database
        response = self.session.post(
            self.url + "/auth/login",
            json={"email": self.email, "password": self.password},
            headers={"Content-Type": "application/json"},
        )

        # Check the login was successful
        if response.status_code != 201:

            # load response as json
            response_json = json.loads(response.text)

            # Check if message is an array
            if isinstance(response_json["message"], list):
                error_messages = ", ".join(response_json["message"])
            else:
                error_messages = response_json["message"]

            # Print the errors
            print(f"Login failed: {error_messages}.")

        else:
            # Test that you are logged in
            logged_in_as = self.whoami()

            # Check if self.email matched logged_in_as
            if self.email == logged_in_as:
                print(f"Logged in successfuly as {self.email}")
            else:
                print(f"Login failed.")

    def whoami(self):
        response = self.session.get(self.url + "/auth/whoami")

        # Load response as json
        response_json = json.loads(response.text)

        # Check if response is 404
        if response.status_code == 404:
            return "Not logged in"

        # Check if response is 200
        if response.status_code == 200:
            return response_json["email"]


# Def main function
def main():
    BGDBClient("https://blood-group-database.herokuapp.com")


if __name__ == "__main__":
    main()
