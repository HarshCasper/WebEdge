from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt
from pyfiglet import Figlet
from colorama import Fore, Style
import json
import clanimate
import yaml

jsonData = ['emptyData']
loadingAnim = clanimate.Animator('scroll_text', 10, name = " => WebEdge Is Scrapping Your Website ", animation_frames="===============")

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#00ff00 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#0000ff bold',
    Token.Question: '',
})    

def shouldc2(answers):
    check1 = answers['c1']
    if check1 != 'site':
        return True
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
    global jsonData #skipcq PYL-W0603
    jsonData = json.loads(jsonValue)
    options = []
    for i in jsonData.keys():
        options.append(i)
    print()
    questions = [
        {
            'type': 'list',
            'name': 'c1',
            'message': 'What do you want to check first ?',
            'choices': options
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
        },
        {
            'type':'list',
            'name':'c4',
            'message':'See them all at once or one by one',
            'choices':['All at Once', 'One by One'] 
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
    allAtOnce = False
    fullList = ""
    if answers['c4'] is 'All at Once':
        allAtOnce = True
    for i in li:
        no = no + 1
        ivalue = str(i['value'])
        message = "Point - "+str(no)+"\n Label : "+i[k1]+"\n Current : "+ivalue;
        fullList = fullList+message+"\n\n"
        if allAtOnce is False:
            qn = [
                {
                    'type': 'confirm',
                    'name': 'forward',
                    'message': message+'\n Go to next?',
                    'default': True
                }
            ]
            a = prompt(qn, style=style)
            if a['forward'] is False:
                didBreak = True
                break;
        else:
            if no%2 == 1:
                print(Fore.BLUE+Style.BRIGHT+message+"\n"+Style.RESET_ALL)
            else:
                print(Fore.CYAN+Style.BRIGHT+message+"\n"+Style.RESET_ALL)

    if didBreak is False and allAtOnce is False:
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
        saveFile = [
            {
                'type': 'confirm',
                'name': 'fileSave',
                'message': 'Do you want to save your analysis in a file?',
                'default': True
            }
        ]
        isFileSaved = prompt(saveFile, style = style)
        if isFileSaved['fileSave'] is True:
            filename = str(jsonData['pages'][0]['url'] + '_webedge_analysis.yaml')
            bad_chars = ['/', ':', '\\']
            for i in bad_chars:
                filename = filename.replace(i,'')
            with open(filename, 'w+') as f:
                f.write(yaml.dump(yaml.load(json.dumps(json.loads(jsonValue)),yaml.Loader)))
            print(filename+" saved")
            
        print(Fore.GREEN+Style.BRIGHT+"=====================\nWebEdge Analysis Done\n====================="+Style.RESET_ALL)

def outputName(name):
    f = Figlet(font='slant')
    print(Style.RESET_ALL)
    print(Fore.GREEN + Style.BRIGHT + f.renderText(name))
    print(Style.RESET_ALL)

def startLoading():
    print(Fore.GREEN + Style.BRIGHT , end='')
    loadingAnim.start_animation()

def endLoading():
    loadingAnim.end_animation()
    print(Style.RESET_ALL, end='')

def outputError():
    catsay("WebEdge Couldn't Parse Your Website")

def printError(errMessage):
    print(Style.RESET_ALL+Fore.RED+Style.BRIGHT+"\nERROR => "+errMessage+Style.RESET_ALL)

def exitError():
    catsay("Unexpected Exit By User")

def catsay(message):
    space = (len(message)+4)
    upBlock = "  "+"_"*space+"\n "+ "/"+" "*space+"\\ \n |< "
    downBlock = " >|\n \\"+"_"*space+"/\n "
    catStr = "	      \\ \n "+"	       \\    /\\_/\\           ___\n "+"		\\  = o_o =_______    \\ \\ \n "+ "		    __^      __(  \\.__) )\n "+"		(@)<_____>__(_____)____/\n"
    print(Style.RESET_ALL + Fore.YELLOW + Style.BRIGHT + upBlock + message + downBlock + catStr + Style.RESET_ALL)