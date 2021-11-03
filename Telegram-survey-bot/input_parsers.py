import re

# --------------------------------------------------------------------
# use to this to identify what an incoming message is 
def parse_result(result):
    if "text" in result:
        if "entities" in result:
            return "command"
        return "text_message"
    elif "voice" in result:
        return "voice_message"
    elif "audio" in result:
        return "audio_file"
    elif "document" in result:
        return "document"
    elif "sticker" in result:
        return "sticker"
    elif "document" in result and "animation" in result:
        return "animation" 
# --------------------------------------------------------------------
# this block of code verifies formatted inout from user for creating a survey
CREATE_SURVEY_REGEX = re.compile(r"""(name)?\s*:?\s*(.+)
(number of questions)?\s*:?\s*(\d+)
(amount of people)?\s*:?\s*(\d+)""", re.UNICODE)

def create_survey_parser(regex, message):
    message = "\n".join([string for string in message.lower().strip().splitlines() if string])
    if regex.fullmatch(message):
        result = regex.findall(message)[0]
        return {result[group]:result[group+1] for group in range(0,len(result),2)}
    return False

# --------------------------------------------------------------------
# this block of code verifies formatted inout from user for inputting questions 
# needs more work tho
QUESTION_REGEX = re.compile(r"question?\s*\d+?\s*:?\s*(.*)", re.UNICODE)
CHOICE_REGEX = re.compile(r"choice?\s*\d+?\s*:?\s*(.*)", re.UNICODE)

def add_question_parse(question_regex, choice_regex, message):
    message = [string for string in message.lower().strip().splitlines() if string]
    final_dictionary = []
    temp_dictionary = {}
    choices = []
    for line in message:
        if question_regex.fullmatch(line):
            temp_dictionary.update({"choices" : choices})
            final_dictionary.append(temp_dictionary)
            temp_dictionary = {}
            choices = []
            temp_dictionary.update({"question" : question_regex.findall(line)[0]})
        elif choice_regex.fullmatch(line):
            choices.append(choice_regex.findall(line)[0])
        else:
            return False
    temp_dictionary.update({"choices" : choices})
    final_dictionary.append(temp_dictionary)
    final_dictionary.pop(0)
    return dict(enumerate(final_dictionary))