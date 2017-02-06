#!/usr/bin/env python3

import subprocess, re

fn = 'ModernGreekFlashcards.pdf'

res = subprocess.run(['pdftotext', '-layout', fn, '-'], stdout=subprocess.PIPE)
lines = [l.strip() for l in res.stdout.decode().split("\n")]

eng_letters = 'aåbgde™zh¸uiº›klmnjoøprsqty¥‰fxcv√ -'
ell_letters = 'αάβγδεέζηήθιίϊκλμνξοόπρσςτυύϋφχψωώ -'

t = str.maketrans(eng_letters, ell_letters)

flash = []
for line in lines:
    # search for lines with squished numbers
    line = re.sub('(?<=\D)(\d)', ' \\1', line)

    if line == '':
        pass
    elif line.split() == ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
        pass
    elif line.startswith('Liberation') or line.startswith('Software'):
        pass
    else:
        words = line.split()
        sections = [[]]
        for word in words:
            if re.match('\d+', word):
                sections.append([])
            else:
                sections[-1].append(word)

        phrases = [' '.join(s) for s in sections]

        if phrases[-1] == '':
            phrases = phrases[0:-1]

        if len(phrases) == 4:
            for english, raw_greek in zip(phrases[::2], phrases[1::2]):
                greek = raw_greek.translate(t)

                if re.search('[^' + ell_letters + ']', greek):
                    raise RuntimeError('bad letters in raw {} = {} = {}'.format(raw_greek, greek, english))

                flash.append([english, greek])
        else:
            raise RuntimeError('Bad phrase length')

for x in flash:
    print(*x, sep='\t')
