"""
    Module Name: Response

    Description:
        HTTP Response module.

    Author: Liav Barsheshet [312429269] Elshan Getdarov [313735136].
    Date: 09/10/2024.
"""

# Imports
from datetime import datetime
from flask import jsonify
from typing import List


class Response:
    """
        Represents HTTP Response object.
    """

    def __init__(self):
        self.message: str = ""
        self.output: [] = []
        self.completed: bool = True
        self.status_code = 200
        self.arrival = datetime.now()
        self.relative_time = datetime.now()
        self.elapsed = datetime.now() - self.arrival

    def to_dict(self):
        """
            Converts HTTP Response object to dictionary.
        """
        return jsonify({
            "message": self.message,
            "output": self.output,
            "completed": self.completed,
            "status_code": self.status_code,
            "elapsed": (datetime.now() - self.arrival).total_seconds(),
            "arrival": self.arrival.strftime("%H:%M:%S"),
        }), 200

    def success(self, message: str, output: List[str]):
        """
            Creates a success HTTP response.
            :param message: The success message to include in the response.
            :param output: The list of output data to include in the response.
            :return: A success HTTP response object.
        """
        self.message = message
        self.output = output
        self.completed = True
        self.status_code = 200
        return self.to_dict()

    def failed(self, message: str, output: List[str]):
        """
            Creates a failure HTTP response.
            :param message: The error message to include in the response.
            :param output: The list of output data to include in the response.
            :return: A failure HTTP response object.
        """
        self.message = message
        self.output = output
        self.completed = False
        self.status_code = 400
        return self.to_dict()

    def delta_seconds(self) -> float:
        """
            Returns the time difference (delta) in seconds between consecutive calls to this method.
            :return: The delta time in seconds.
        """
        stamp = datetime.now()
        result = (stamp - self.relative_time).total_seconds()
        self.relative_time = stamp
        return result
