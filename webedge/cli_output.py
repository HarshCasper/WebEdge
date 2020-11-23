from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint
from pyfiglet import Figlet
from colorama import Fore, Back, Style
import json

jsonData = ['emptyData']


style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#00ff00 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#0000ff bold',
    Token.Question: '',
})

def getc1(answers):
    options = []
    for i in jsonData.keys():
        options.append(i)
    return options

def shouldc2(answers):
    if answers['c1'] != 'site':
        return True
    else:
        return False

def getm2(answers):
    m2 = "Which "+str(answers['c1']+" you want to review?")
    return m2

def getc2(answers):
    options = []
    if answers['c1'] != 'pages':
        options.append("no pages")
        return options
    for i in jsonData[answers['c1']]:
        options.append(i['url'])
    if not options:
        options.append("no pages")
    return options

def filterc2(val):
    m = 0
    for i in jsonData['pages']:
        if i['url'] == val:
            return m;
        m = m+1

def filterc3(val):
    if val[0] == 'I':
        return 'issues'
    return 'achieved'

    
def outputJson(jsonValue):
    global jsonData
    jsonData = json.loads(jsonValue)
    questions = [
        {
            'type': 'list',
            'name': 'c1',
            'message': 'What do you want to check first ?',
            'choices': getc1
        },
        {
            'type': 'list',
            'name': 'c2',
            'message': 'Which page do you want to review ?',
            'choices': getc2,
            'filter': filterc2,
            'when': shouldc2
        },
        {
            'type': 'list',
            'name': 'c3',
            'message': 'Issues or Achievements?',
            'choices': ['Issues','Achievements'],
            'filter': filterc3
        }
    ]
    answers = prompt(questions, style=style)
    k1 = 'warning'
    if(answers['c3'] == 'achieved'):
        k1 = 'achievement'
    
    if answers['c1'] == 'pages':
        li = jsonData[answers['c1']][answers['c2']][answers['c3']]
    else:
        li = jsonData[answers['c1']][answers['c3']]

    no = 0
    didBreak = False
    for i in li:
        no = no + 1
        ivalue = str(i['value'])
        message = "Point - "+str(no)+"\n Label : "+i[k1]+"\n Current : "+ivalue;
        qn = [
            {
                'type': 'confirm',
                'name': 'forward',
                'message': message+'\n Go to next?',
                'default': True
            }
        ]
        a = prompt(qn, style=style)
        if a['forward'] == False:
            didBreak = True
            break;

    if didBreak == False:
        print('List Ended')

    retry = [
        {
            'type': 'confirm',
            'name': 'again',
            'message': 'Do you want to check other things?',
            'default': True
        }
    ]
    res = prompt(retry, style=style)
    if res['again'] is True:
        outputJson(jsonValue)
    else:
        print(Fore.GREEN+Style.BRIGHT+"=====================\nWebEdge Analysis Done\n====================="+Style.RESET_ALL)

def outputName(name):
    f = Figlet(font='slant')
    print(Style.RESET_ALL)
    print(Fore.GREEN + Style.BRIGHT + f.renderText(name))
    print(Style.RESET_ALL)
