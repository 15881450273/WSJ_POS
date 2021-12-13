
with open('WSJ_02-21.pos','r') as f:
    line = f.read()
line = line.split()
likelihood = {}
allwords = []
for i in range(1,len(line),2):
    word = line[i]
    pos = line[i-1]
    allwords.append(word)
    if pos not in likelihood:
        likelihood[pos] = {}
        if word not in likelihood[pos]:
            likelihood[pos][word] = 1
        else:
            likelihood[pos][word] += 1
    else:
        if word not in likelihood[pos]:
            likelihood[pos][word] = 1
        else:
            likelihood[pos][word] += 1
likelihood['OOV'] = {}       
likelihood['OOV']['OOV'] = 0.0001

transition = {}
for i in range(1,len(line),2):
    prevpos = i - 2
    pos = line[i]
    nextpos = i + 2
    if i == 1 or line[prevpos] == '.':
        key = 'B'
    elif pos == '.':
        key = 'E'
    else:
        key = pos
    if key == 'B':
        if key not in transition:
            transition[key] = {}
            if pos not in transition[key]:
                transition[key][pos] = 1
            else:
                transition[key][pos] += 1
        else:
            if pos not in transition[key]:
                transition[key][pos] = 1
            else:
                transition[key][pos] += 1
    else:
        if line[prevpos] not in transition:
            transition[line[prevpos]] = {}
            if pos not in transition[line[prevpos]]:
                transition[line[prevpos]][pos] = 1
            else:
                transition[line[prevpos]][pos] += 1
        else:
            if pos not in transition[line[prevpos]]:
                transition[line[prevpos]][pos] = 1
            else:
                transition[line[prevpos]][pos] += 1
for i in likelihood:
    count = 0
    for j in likelihood[i]:
        count += likelihood[i][j]
    for k in likelihood[i]:
        likelihood[i][k] = likelihood[i][k]/count
for i in transition:
    count = 0
    for j in transition[i]:
        count += transition[i][j]
    for k in transition[i]:
        transition[i][k] = transition[i][k]/count
transition['OOV'] = {}
transition['OOV']['OOV'] = 0.0001
transition['.'] = {}
transition['.']['B'] = 1

sentence = []
realposition = 0
start = True
beginning = True
with open('WSJ_23.words','r') as file:
    line = file.read()
line = line.split()


answer = []
CORRECTPB = 0




for i in range(len(line)):
    word = line[i]
    if start == True:
        sentence.append('B')
        start = False
    if word != '.':
        sentence.append(word)
    elif word not in allwords:
        sentence.append('OOV')
    elif word == '.':
        sentence.append('.')

        for g in range(1,len(sentence)):

            word = sentence[g]


            if beginning == True:
                if word not in likelihood:
                    word = 'OOV'
                    CORRECTPOS = max(transition['B'], key = transition['B'].get)
            
                else:
                    
                    for j in likelihood[word]:
                        if j not in transition['B']:
                            PB = 0
                        else:
                            PB = likelihood[word][j] * transition['B'][j]
                        if PB > CORRECTPB:
                            CORRECTPB = PB
                            CORRECTPOS = j
                    CORRECTPB = 0
                answer.append(CORRECTPOS)
                            
                beginning = False
            elif word == '.':
                answer.append('.')
                
                beginning = True
            else:
                
                if word not in likelihood:
                    CORRECTPOS = max(transition[answer[len(answer)-1]], key = transition[answer[len(answer)-1]].get)

                else:
                    for state in likelihood[word]:

                        if state not in transition[answer[len(answer)-1]]:
                            PB = 0
                        else:
                            PB = likelihood[word][state] * transition[answer[len(answer)-1]][state]
                        if PB > CORRECTPB:
                            CORRECTPB = PB
                            CORRECTPOS = state
                    CORRECTPB = 0
                answer.append(CORRECTPOS)
                    

    
        start = True
        sentence = []


f = open('submission.pos','w')
for i in range(len(line)):
    count+=1
    f.write(line[i]+'\t'+answer[i]+'\n')
    #if answer[i] == '.':
        #f.write('\n')
f.close()


print(count)



with open('WSJ_23.words','r') as f:
    line = f.read()
line = line.split()
with open('submission.pos','r') as g:
    ans = g.read()
ans = ans.split()
print(len(line))
print(len(ans))

