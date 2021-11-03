#=========================== File for communication with the JSON files ===================================

# JSON Files organization 
"""
survey_list.json:

This file contains a simple list of all the survyes available
each survey object is defined by it's name, so no 2 surveys can't have the same name 
this is how the json file is structured:

{survey_1 : {questions: {question_index : [question, choices],...}, number_of_questions : number, owner = creator_id, limit = number_people}},...}
======================================================================================================================

submissions.json
This file contains the submissions for each survey, in the following format:

{survey_1 : {questions:{question_1: {choice_a: 0, choice_b: 0, choice_c: 0,...}, question_2....}, people_who_submitted: [id_1, id_2,...]}....}

each survey is identified by it's name as before..
"""

import json
# ========== simply opens a Json file and returns the whole thing, not sure if it's efficient ==============
def get_data(json_file):
    with open(json_file, "r") as json_file:
        data = json.load(json_file)
    return data

# ===========================Functions used for Updating and changing the JSON files ==================

def register_survey(survey_info):
    data = get_data("survey_list.json")
    with open("survey_list.json", "w") as survey_file:
        #needs further validation logic 
        data.update(survey_info)
        survey_file.write(json.dumps(data))

def register_submission(survey_info):
    data = get_data("submissions.json")
    with open("submissions.json", "w") as submission_file:
        #needs further validation logic 
        data.update(survey_info)
        submission_file.write(json.dumps(data))

def update_json(updated_json, json_file):
    with open(json_file, "w") as file:
        file.write(json.dumps(updated_json))

def add_question(index, question, choices, survey_name):
    survey_data = get_data("survey_list.json")
    submission_data = get_data("submissions.json")
    survey_data[survey_name]["questions"].update({index: [question,choices]})
    submission_data[survey_name]["questions"].update({index:{choice:0 for choice in choices}})
    update_json(survey_data, "survey_list.json")
    update_json(submission_data, "submissions.json")

def add_submission(answers, submitter, survey_name):
    submission_data = get_data("submissions.json")
    submission_data[survey_name]["people_who_submitted"].append(submitter)
    for question in submission_data[survey_name]["questions"]:
        submission_data[survey_name]["questions"][question][answers[0]]+=1
        answers.pop(0) 
    update_json(submission_data, "submissions.json")

def delete_survey(survey_name):
    survey_data = get_data("survey_list.json")
    submission_data = get_data("submissions.json")
    survey_data.pop(survey_name)
    submission_data.pop(survey_name)
    update_json(survey_data, "survey_list.json")
    update_json(submission_data, "submissions.json")

# ================== functions used for checking various stuff, the names are self explanatory ================ 
def find_owner(survey_name):
    return get_data("survey_list.json")[survey_name]["owner"]

def has_already_submitted(user_id, survey_name):
    submission_data = get_data("submissions.json")    
    if user_id in submission_data[survey_name]["people_who_submitted"]:
        return True
    else:
        return False

def has_limit_reached(survey_name):
    if len(get_data("submissions.json")[survey_name]["people_who_submitted"]) < get_data("survey_list.json")[survey_name]["limit"]:
        return False
    else:
        return True    

def search_available_survey(survey_name):
    survey_data = get_data("survey_list.json")
    try: 
        return(survey_data[survey_name])
    except:
        return False

# ================ returns final result of a survey with simple calculations=========================
def return_results(survey_name):
    survey_data = get_data("survey_list.json")[survey_name]
    submission_data = get_data("submissions.json")[survey_name]
    amount_of_people = survey_data["limit"]
    questions = submission_data["questions"]
    results = []
    for question in questions:
        question_result = []
        for choice in questions[question]:
            question_result.append("{0:.3g}%".format((questions[question][choice] / amount_of_people) * 100))
        results.append(question_result)

    # This works! don't touch
    string_questions = [f"Question {int(index)+1}: {question[0]}\n"+"\n".join([f"{result} answered {choice}" for result, choice in zip(results[int(index)], question[1])]) for index, question in survey_data["questions"].items()]
    
    
    return f"Here are the results of {survey_name}...\n\n"+"\n\n📊📊📊📊📊📊📊📊📊📊📊📊📊📊📊📊\n\n".join(string_questions)