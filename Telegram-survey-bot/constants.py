#----------------------------success messages--------------------------#
INPUT_SUCCESS = "Your survey has been registered successfully!"
SEARCH_SUCCESS = """I have found the survey you're looking for ! 
Surveys are completely anonymous....so please fill it in responsibly! """
SURVEY_COMPLETE = "Thank you for completing the survey!"

WELCOME_MESSAGE = """Welcome to Komari survey bot ✌️

What would you like to do?"""
#---------------Flags-------------------#
TEXT_MESSAGE = "text_message"
COMMAND = "command"
CREATING_SURVEY = "creating"
REGISTERING_QUESTIONS = "registering_questions"
SEARCHING_SURVEY = "searching for a survey"
FILLING_SURVEY = "currently filling survey"
#---------------Prompts-------------------#
CREATE_SURVEY = """Please send the following:

✅ the name of the survey
✅ the number of questions in the survey 
✅ and the amount of people you want the survey to be filled by, in the following format 

name : the name you want for your survey
number of questions : a number 
amount of people : a number"""

REGISTER_QUESTIONS="""Please send questions in this format:

Question 1:  your question
choice 1 : a choice
choice 2 : a second choice
choice 3 : another choice
choice 4 : you get the point 

Question 2:  your question
choice 1 : choice A
choice 2 : choice B
choice 3 : and so on...

✅ You can add more choices in the same format
✅ The number of questions you send must be equal to the number of questions you specified when creating the survey
✅ all the questions and their choices must be sent in a single text"""

SEARCH_FOR_A_SURVEY = "Please send me the name of the survey you want to fill in"

#------------------------------error messages--------------------------#
INPUT_ERROR = "sorry I don't understand that format! Please use the format I sent you!"
SEARCH_ERROR = """Sorry I couldn't find the survey you asked for 
✅ It might have been deleted by the owner 
✅ It might have been submitted by enough people
✅ or maybe you made a typo ..."""
DOUBLE_SUBMISSION_ERROR = "You have already submitted this survey!"