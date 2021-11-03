# ============================ imports =========================
import json
from bot import Bot
from survey_object import *
from constants import *
from json_tools import *
from input_parsers import *

# ========================== Globals =========================
update_id = None
my_bot = Bot("config.ini")
#------------------------------------------------------
flag = None # current process
#------------------------------------------------------
current_survey = None # Current Survey being operated on 
current_questions = []
answers = []
#------------------------------------------------------
chat_id = None # used for updating questions
message_id = None

# ========================= main loop ======================
while True:
    print("Running ...")
    updates = my_bot.get_updates(offset=update_id)
    updates = updates["result"]
    
    if updates:
        for update in updates:
            update_id = update["update_id"]
            # every update is processed based on it's type, specifically whether it's a message or a callback_query(returned from a button press)
            if "message" in update:
                try:
                    sender = update["message"]["chat"]["id"]
                    result_type = parse_result(update["message"])

                    # ==================================== Choose process based on commands and set flags================================================ #
                    if result_type == COMMAND:
                        recieved_command = update["message"]["text"]
                        
                        if recieved_command == "/start":
                            reply_keyboard = my_bot.get_custom_keyboard([["/create_survey"], ["/fill_a_survey"]])
                            send_welcome_message = my_bot.send_message(sender, WELCOME_MESSAGE, ReplyKeyboardMarkup = reply_keyboard)

                        elif recieved_command == "/create_survey":
                            send_create_prompt = my_bot.send_message(sender, CREATE_SURVEY)
                            flag = CREATING_SURVEY
                        
                        elif recieved_command == "/fill_a_survey":
                            send_search_prompt = my_bot.send_message(sender, SEARCH_FOR_A_SURVEY)
                            flag = SEARCHING_SURVEY
                            
                    # ===============================Process response from users based on flags set by commands===================================== #
                    if result_type == TEXT_MESSAGE:
                        reply = update["message"]["text"]

                        if flag == CREATING_SURVEY:
                            processed_reply = create_survey_parser(CREATE_SURVEY_REGEX, reply) # Validate input and send processed reply
                            # processed_reply = {"name":name, "number of questions" : number, "amount of people" : number}
                            if processed_reply:
                                new_survey = survey(processed_reply["name"].strip().lower(), int(processed_reply["number of questions"]), int(processed_reply["amount of people"]), sender)
                                register_survey(new_survey.get_survey()) 
                                register_submission(new_survey.get_submission_format()) # create and register empty surveys 
                                send_question_prompt = my_bot.send_message(sender, REGISTER_QUESTIONS) # send prompt to user to send questions
                                
                                flag = REGISTERING_QUESTIONS # set flag, and active survey
                                current_survey = processed_reply["name"].strip().lower()
                            else:
                                send_input_error = my_bot.send_message(sender, INPUT_ERROR) # send error message if input not valid 
                        
                        elif flag == REGISTERING_QUESTIONS:
                            processed_reply = add_question_parse(QUESTION_REGEX, CHOICE_REGEX, reply) # Validate input and send processed reply
                            # {index_0:{question: question, choices:[]}, index_1..}
                            if processed_reply:
                                # ---------------- register questions and set flags back to they were ---------------------------
                                number_of_questions = len(processed_reply.keys())
                                for question_index in range(number_of_questions):
                                    add_question(question_index, processed_reply[question_index]["question"], processed_reply[question_index]["choices"], current_survey) 
                                reply_keyboard = my_bot.get_custom_keyboard([["/create_survey"], ["/fill_a_survey"]])
                                send_success_message = my_bot.send_message(sender, INPUT_SUCCESS, ReplyKeyboardMarkup=reply_keyboard)
                                
                                flag = None
                                current_survey = None
                            else:
                                send_input_error = my_bot.send_message(sender, INPUT_ERROR) # send error message if input not valid 

                        elif flag == SEARCHING_SURVEY:
                            result = search_available_survey(reply.lower().strip()) # search for a survey from user reply
                            if result: 
                                
                                if not has_already_submitted(sender, reply.lower().strip()): # start filling in survey if user hasn't filled in the survey before 
                                    current_survey = reply.lower().strip() #set active survey and set flags
                                    flag = FILLING_SURVEY
                                    current_questions = list(result["questions"].values())
                                    
                                    reply_keyboard = my_bot.get_inline_keyboard([{"text":"Start", "callback_data":"start"}])
                                    send_search_success = my_bot.send_message(sender, SEARCH_SUCCESS, InlineKeyboardMarkup=reply_keyboard)
                                    message_id, chat_id = send_search_success.json()["result"]["message_id"], send_search_success.json()["result"]["chat"]["id"]
                                
                                else:
                                    send_already_filled = my_bot.send_message(sender, DOUBLE_SUBMISSION_ERROR) # send error message if user has filled in the survey before

                            else:
                                send_search_not_found = my_bot.send_message(sender, SEARCH_ERROR) # send error if the survey wasn't found
                except:
                    pass
            #===================== process button presses ====================================
            elif "callback_query" in update:                
                try:
                    query_id = update["callback_query"]["id"]
                    sender = update["callback_query"]["message"]["chat"]["id"]
                    data = update["callback_query"]["data"]
    # =========== The whole process below is very techinical, so I can't explain with comments, just know it displays questions and recieves answers=========#
                    if data == "start": 
                        my_bot.answer_callback_query(query_id)
                        reply_keyboard = my_bot.get_inline_keyboard([{"text":str(choice), "callback_data":str(choice)} for choice in current_questions[0][1]])
                        edit_message = my_bot.edit_message_text(chat_id, message_id, current_questions[0][0], reply_keyboard)
                        message_id, chat_id = edit_message.json()["result"]["message_id"], edit_message.json()["result"]["chat"]["id"]
                        current_questions.pop(0)
                    else:
                        answers.append(data)
                        my_bot.answer_callback_query(query_id)
                        
                        try:
                            reply_keyboard = my_bot.get_inline_keyboard([{"text":str(choice), "callback_data":str(choice)} for choice in current_questions[0][1]])
                            edit_message = my_bot.edit_message_text(chat_id, message_id, current_questions[0][0], reply_keyboard)
                            message_id, chat_id = edit_message.json()["result"]["message_id"], edit_message.json()["result"]["chat"]["id"]
                            current_questions.pop(0)
                        except:
                            add_submission(answers,sender,current_survey) # add submission when survey is complete
                             # send results to owner if limit of people has been reached,and delete the survey 
                            if has_limit_reached(current_survey): 
                                my_bot.send_message(find_owner(current_survey), return_results(current_survey))
                                delete_survey(current_survey)

                            send_survey_complete_message = my_bot.send_message(sender, SURVEY_COMPLETE)

                            #set every flag and stuff back to normal
                            flag = None
                            current_survey = None
                            current_questions = []
                            chat_id = None
                            message_id = None
                            answers = []
                except:
                    pass

# I used multiple try, except blocks to stop the bot from crashing as much as possible 
