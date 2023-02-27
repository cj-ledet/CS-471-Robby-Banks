from things.actors import actor
import json
import random

from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

sia = SentimentIntensityAnalyzer()



MY_GAME_LOGIC = {}
with open('robber_dialog.json', 'r') as myfile:
    MY_GAME_LOGIC = json.loads(myfile.read())

class robber(actor):
    def __init__(self, phone_number):
        super().__init__(phone_number)
        self.score = 0

        self.paranoid = False #bool(random.getrandbits(1))
        if self.paranoid :
            self.state =  "init_copper"



    def get_output(self,msg_input):


        sent = sia.polarity_scores(msg_input)
        if sent['neg'] > .4:
            self.state =  "init_copper"

        found_match = False
        output = [  ]
        if type( MY_GAME_LOGIC[ self.state ]['next_state'] ) != str: # we have choices
            for next_state in MY_GAME_LOGIC[ self.state ]['next_state']:
                if msg_input.lower() ==  next_state['input'].lower():
                    self.state = next_state['next_state']
                    if 'point_delta' in  next_state:
                        self.score += next_state['point_delta']
                    found_match = True
                    break

            if found_match == False:
                if 'input_not_found' in MY_GAME_LOGIC[ self.state ]:
                    self.state = MY_GAME_LOGIC[ self.state ]['input_not_found']['next_state']
                else:
                    return [random.choice ( MY_GAME_LOGIC['misc corpus'] )] 

        while True:
            if type( MY_GAME_LOGIC[ self.state ]['content'] ) == str:
                output.append( MY_GAME_LOGIC[ self.state ]['content'])
            else:
                output.append( random.choice ( MY_GAME_LOGIC[ self.state ]['content']) )
            if 'next_state' not in MY_GAME_LOGIC[ self.state ] or type( MY_GAME_LOGIC[ self.state ]['next_state'] ) != str:
                break
            self.state = MY_GAME_LOGIC[ self.state ]['next_state']
        
        return output

