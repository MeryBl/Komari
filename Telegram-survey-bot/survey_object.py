class survey:
    def __init__(self, survey_name, number_of_questions, limit, owner):
        self.survey_name = survey_name
        self.number_of_questions = number_of_questions
        self.limit = limit
        self.owner = owner
        self.questions = {}

        self.submissions = {}
        self.submitter_ids = []
        
    def get_survey(self):
        return {self.survey_name: {"questions":self.questions,"numer_of_questions":self.number_of_questions,"owner":self.owner, "limit":self.limit}}
    
    def get_submission_format(self):
        return {self.survey_name: {"questions":{}, "people_who_submitted":self.submitter_ids}}
        
    def add_submission(self, answers, submitter):
        if submitter not in self.submitter_ids:
            for index in range(len(answers)):
                self.submissions[index][answers[index]] += 1
            self.submitter_ids.append(submitter)
        else:
            return False