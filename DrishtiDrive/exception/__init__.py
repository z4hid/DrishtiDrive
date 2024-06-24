import sys


# This function generates a detailed error message based on the provided error and error detail.
# It takes in an error message and an error detail object, which contains information about the error.
# The function extracts the file name and line number from the error detail object and constructs
# a detailed error message in the format "Error occurred in python script name [file_name] line number [line_number] error message [error_message]".
def error_message_detail(error, error_detail:sys):
    """
    Generate a detailed error message based on the provided error and error detail.

    Args:
        error (Exception): The error that occurred.
        error_detail (sys): The error detail object containing information about the error.

    Returns:
        str: The detailed error message in the format "Error occurred in python script name [file_name] line number [line_number] error message [error_message]".
    """
    # Get the traceback object from the error detail.
    _, _, exc_tb = error_detail.exc_info()

    # Get the file name from the traceback object.
    file_name = exc_tb.tb_frame.f_code.co_filename

    # Construct the detailed error message.
    error_message = "Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )

    return error_message


# This class represents an application exception.
# It takes in an error message and an error detail object, which contains information about the error.
# The class initializes a new instance of the AppException class with the specified error message and error detail.
# It also defines a __str__ method to return a string representation of the error message.
class AppException(Exception):
    def __init__(self, error_message, error_detail:sys):
        """
        Initializes a new instance of the AppException class with the specified error message and error detail.

        Args:
            error_message (str): The error message to be displayed.
            error_detail (sys): The error detail object containing information about the error.

        Returns:
            None
        """
        # Call the parent class constructor with the error message.
        super().__init__(error_message)

        # Generate the detailed error message using the error_message_detail function.
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        """
        Returns a string representation of the error message.

        :return: A string representing the error message.
        :rtype: str
        """
        # Return the detailed error message.
        return self.error_message
    

