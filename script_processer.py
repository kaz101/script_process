#!/usr/bin/env python3
'''A class that processes scripts for star trek radio theater'''
import re
import sys
from selenium import webdriver
import time

class script_process:
    '''A class that processes scripts for star trek radio theater'''
    def __init__(self):
        ''' initalize variables '''
        self.browser = webdriver.Chrome()
        try:
            self.episode = ' '.join(sys.argv[1:])
        except:
            print('You must give an episode to find')
        self.transcript_done = []

    def get_transcript(self):
        self.browser.get('http://www.chakoteya.net/StarTrek/')
        self.link_elements = self.browser.find_elements_by_tag_name('a')
        self.links = []
        for i in self.link_elements:
            href = i.get_attribute('href')
            if href not in self.links:
                self.links.append(href)
            for j in range(len(self.links)):
                if 'fortyseven' in self.links[j]:
                    self.links.pop(j)
        for i in self.links:
        #    time.sleep(1)
            print(i)
            if (
            'StarTrek' in i or
            'NextGen' in i or
            'DS9' in i or
            'Voyager' in i or
            'Enterprise' in i or
            'movies' in i
            ):
                self.browser.get(i)
                series_elements = self.browser.find_elements_by_tag_name('a')
            else:
                continue
            for j in series_elements:
                print(self.episode)
                print(j.text)
                if self.episode.lower() in j.get_attribute('text').lower():
                    print('found it')
                    if 'Voyager' in i:
                        self.series = 'VOY'
                    elif 'NextGen' in i:
                        self.series = 'TNG'
                    elif 'DS9' in i:
                        self.series = 'DS9'
                    elif 'Enterprise' in i:
                        self.series = 'ENT'
                    elif 'StarTrek' in i:
                        self.series = 'TOS'
                    self.script_url = j.get_attribute('href')
                    break
        print(self.script_url)
        self.browser.get(self.script_url)
        self.body = self.browser.find_elements_by_tag_name('font')
        self.body_text = []
        for i in self.body:
            i = i.text.split('\n')
            self.body_text.extend(i)
        print(self.body_text)
    def process_transcript(self):
        ''' Captures only the dialoge, strips out everything else
            and formats like the script '''
        for i in self.body_text:
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
                i ='\n'+'WE FOCUS ON '+i+'\n'
                i = i.replace('[','')
                i = i.replace(']','')
                i = i.upper()
            elif i.startswith('('):
                i = i.replace('(','')
                i = i.replace(')','')
                i = '\n\t' + i +'\n'
                count = 0
                for j in range(len(i)):
                    if count > 60 and i[j].isspace():
                        i = i[:j] + '\n\t' + i[j+1:]
                        count = 0
                    else:
                        count += 1
            elif ':' in i or i.startswith('\t'):
                #print (i)
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
            elif i.startswith('<'):
                break
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
    def save_dialog(self):
        with open(f"C:\\Users\\kaz10\\Google Drive\\public\\scripts\\Star Trek Radio Theater {self.series} '{self.body_text[0]}' Script V1",'w') as f:
            for i in self.transcript_done:
                i
                f.write(i)
            f.close()

s = script_process()
s.get_transcript()
s.process_transcript()
s.save_dialog()
