#!/usr/bin/env python3
'''A class that processes scripts for star trek radio theater'''
import re
import sys

class script_process:
    '''A class that processes scripts for star trek radio theater'''
    def __init__(self):
        ''' initalize variables '''
        self.final_list = []
        self.s_counter = 0
        self.t_counter = 0
        self.b_counter = 0
        self.script, self.script_file = self.open_file('410.txt')
        self.transcript, self.transcript_file = self.open_file('tapestry')
        #self.transcript_done, self.transcript_file = self.open_file('final_dialog')
        self.transcript_done = []
        self.script_done = []
        self.brackets_list = []
    def open_file(self, filename, mode='r'):
        ''' open files '''
        with open(filename, mode) as f:
            return f.readlines(), f
    def process_script(self):
        ''' strips the dialoge and other cruft
            out of the script '''
        for i in range(len(self.script)):
            if self.script[i][0].isdigit():
                if ('INT.' in self.script[i] or
                    'EXT.' in self.script[i]
                ):
                    self.script[i] = self.script[i].replace('INT.','')
                    self.script[i] = self.script[i].replace('EXT.','')
                for j in self.script[i]:
                    if j.isspace():
                        self.script[i] =(
                        self.script[i][:self.script[i].index(j) + 1] +
                        'WE FOCUS ON' +
                        self.script[i][self.script[i].index(j) + 2:])
                        break
        #    if self.script[i].startswith('\t\t\t'):
                #brackets = re.findall(r'\([^)]*\)',self.script[i])
                #self.brackets_list.extend(brackets)
            if (
                self.script[i].startswith('\t\t\t')
                or 'ACT'in self.script[i]
                or 'CONTINUED' in self.script[i]
                or 'TEASER' in self.script[i]
                or 'OMITTED'in self.script[i]
                ):
                continue
            #else:
            self.script_done.append(self.script[i])
        self.save_script()

    def process_transcript(self):
        ''' Captures only the dialoge, strips out everything else
            and formats like the script '''
        for i in self.transcript:
            #i = re.sub(r'\([^)]*\)','',i)
            #if(
            #    i.startswith('(')
            #    or i.startswith('[')
            #    or i.isspace()
            #    ):
            #    continue
            #else:
            #i = i.replace('LAFORGE','GEORDI')
            if i.startswith('['):
                i = 'WE FOCUS ON '+i
                i = i.replace('[','')
                i = i.replace(']','')
                i = i.upper()
            elif i.startswith('('):
                i = i.replace('(','')
                i = i.replace(')','')
                i = '\n\t' + i 
                count = 0
                for j in range(len(i)):
                    if count > 60 and i[j].isspace():
                        i = i[:j] + '\n\t' + i[j+1:]
                        count = 0
                    else:
                        count += 1
            elif ':' in i:
                i = '\n\t\t\t\t' + i + '\n'
        #        i = '\t\t ' + i
                i = i.replace(': ','\n\t\t')
                #i = i.replace('. ','.\n\t\t')
                count = 0
                for j in range(len(i)):
                    if i[j] == '\n':
                        count = 0
                    if count > 30 and i[j].isspace():
                        i = i[:j] + '\n\t\t' + i[j+1:]
                    #    i = i.replace('\t ','\t')
                        count = 0
                    else:
                        count += 1
            else:
                i = '\t\t' + i + '\n'
                count = 0
                for j in range(len(i)):
                    if count > 30 and i[j].isspace():
                        i = i[:j] + '\n\t\t' + i[j+1:]
                        count = 0
                    else:
                        count += 1


            #i.replace('\t ','\t')
            i = i.replace('\n\n','\n')
            self.transcript_done.append(i)
    def scroll_script(self):
        try:
            self.final_list.append(self.script_done[self.s_counter])
            self.s_counter += 1
        except:
            self.save_to_file()
            print('File Saved !!!')
    def script_back(self):
        self.final_list.pop(-1)
        self.s_counter -= 1
        for i in self.final_list:
            print(i)
    def scroll_transcript(self):
        self.final_list.append(self.transcript_done[self.t_counter])
        self.t_counter += 1
    def transcript_back(self):
        self.final_list.pop(-1)
        self.t_counter -= 1
    def ui(self):
        print('-'*80)
        try:
            print(self.transcript_done[self.t_counter])
            print(self.script_done[self.s_counter])
        except:
            print('done')
    def discard(self):
        self.s_counter += 1
    def save_to_file(self):
        with open('final.txt', 'w+') as f:
            for i in self.final_list:
                f.write(i)
    def process_brackets(self):
        transcript = []
        while True:
            try:
                i = self.transcript_done[self.t_counter]
            except IndexError:
                break
            i = i.split('\n')
            dialog = []
            count = 0
            while True:
                try:
                    j = i[count]
                except IndexError:
                    break
                for k in transcript:
                    print (k)
                for l in range(10):
                    print()
                print('-'*80)
                try:
                    print(self.brackets_list[self.b_counter])
                except IndexError:
                    pass
                print(j)
                x = input()
                if x == 'i':
                    try:
                        dialog.append('\t\t\t'+self.brackets_list[self.b_counter])
                    except IndexError:
                        pass
                    self.b_counter +=1
                if x == 'd':
                    self.b_counter += 1
                if x == '':
                    dialog.append(j)
                    count += 1
            self.t_counter += 1
            dialog1 = '\n'.join(dialog)
            transcript.append(dialog1)
        self.t_counter = 0
        self.transcript_done = transcript
    def save_script(self):
        with open('final_script','+w') as f:
            for i in self.script_done:
                f.write(i)
    def save_dialog(self):
        with open('final_dialog1','+w') as f:
            for i in self.transcript_done:
                f.write(i)
    def get_brackets(self):
        dialog = []
        for i in self.script:
            if i.startswith('\t\t\t'):
                i = i.strip('\t')
                i = i.replace('\n','\n\t\t\t')
                dialog.append(i)

        dialog = ''.join(dialog)
        brackets = re.findall(r'\([^)]*\)',dialog)

        self.brackets_list.extend(brackets)

s = script_process()
#s.process_script()
s.process_transcript()
#s.get_brackets()
#s.process_brackets()
s.save_dialog()
print (s.transcript_done)
'''
while True:
    x = input()
    if x == '':
        s.scroll_script()
        s.ui()
    if x == 'sb' and not s.final_list[-1].startswith('-'):
        s.script_back()
        s.ui()
    if x == 'i':
        s.scroll_transcript()
        s.ui()
    if x == 'tb' and s.final_list[-1].startswith('-'):
        s.transcript_back()
        s.ui()
    if x == 'd':
        s.discard()
        s.ui()
    if x == 's':
        s.save_to_file()
    if x == 'q':
        break
'''
