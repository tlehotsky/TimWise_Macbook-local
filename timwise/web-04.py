#!/usr/bin/python
# -*- coding:UTF-8 -*-
import os, sys, re,requests, warnings, argparse, time  
from bs4 import BeautifulSoup, SoupStrainer
from colorama import Fore, Back, Style

warnings.filterwarnings("ignore", category=UserWarning)

os.system('clear')
print (Fore.WHITE + "test webscrape 1.2")


def command_line_parser():
	parser = argparse.ArgumentParser(description='Short sample app')

	parser.add_argument('-s', action='store_false', default=False,
	                    dest='fast_switch',
	                    help='Set a switch to false')

	parser.add_argument('-f', action='store_true', default=False,
	                    dest='fast_switch',
	                    help='Set a switch to true')
	results = parser.parse_args()

	if results.fast_switch:
		run_fast=True
		print ("The program will run fast")

	else:
		run_fast=False
		print ("The program will run SLOW, use the -f flag  to run FAST")
		time.sleep(2)

	return run_fast

def donothing():
	return

def check_all_good(directory, file_list):

	html_count=0 #for counting html fils in directory
	try:
		if not os.path.exists("html_source"):
			os.makedirs("html_source")

	except:
		preflight=False


	if len(os.listdir(directory))==0:
		print (Fore.RED + 'the directory is empyt, exiting')
		print (Fore.WHITE + '************ program terminated  ************')
		sys.exit()

	else:
		print(Fore.GREEN + 'directory is populated ', end="" +Fore.WHITE)


	for filename in file_list:
		f = os.path.join(directory, filename)

		if filename.endswith(".html"):
			html_count=html_count+1

	if html_count==0:
		print (Fore.RED + 'the directory has no html files')
		print (Fore.WHITE + '************ program terminated  ************')
		sys.exit()				

	print ('the number of files in directory is', len(os.listdir(directory)), 'and there is/are', html_count, '.html file(s)' )

	preflight=True

	return preflight

def build_file_list(directory):
	file_list_start=os.listdir(directory) #Building file list

	final_file_list=[]

	for filename in file_list_start:

		if filename.endswith(".html"):
			final_file_list.append(filename)

	if len(final_file_list)==0:
		print (Fore.RED + 'the directory has no html files')
		print (Fore.WHITE + '************ program terminated  ************')
		sys.exit()		

	return final_file_list

def clean_text(text):
	text=text.rstrip('\n')
	text=text.lstrip('\n')

	return text


#####################
##### constants #####
#####################

directory = '/Users/tlehotsky/Mac Code/html_source' #starting directory
speed=command_line_parser() #check if running fast or slow
page_info=""

#####################
###### program ######
#####################

file_list=build_file_list(directory)
if not check_all_good(directory, file_list):
	sys.exit()


for filename in file_list:
	f = os.path.join(directory, filename)
	


	with open(f) as hdoc:
		strainer = SoupStrainer('div')
		content = hdoc.read()
		soup = BeautifulSoup(content, features="html5lib", parse_only=strainer)

	book_title=soup.find(class_ = "bookTitle")
	author=soup.find(class_ = "authors")

	book_name=clean_text(book_title.text)
	author_name=clean_text(author.text)
	print (Fore.WHITE + 'The books TITLE to process is ', end='' )
	print (Fore.GREEN +  book_name, end='')
	print (Fore.WHITE + ' The authors is NAME is:', author_name)
	print ("last name is", author_name.split(',')[0])
	print ("first name is", author_name.split(', ')[1])


	divs = soup.findAll('div', class_='sectionHeading')  
	print ("the number of section Headings or chapters is:", len(divs))

	div_section_sourcelines=[]
	div_sections={}

	for sh in divs:

		name=clean_text(sh.text)
		div_sections[name]=sh.sourceline
		div_section_sourcelines.append(sh.sourceline)

	for x,y in div_sections.items(): 
		print ("section number", y, "chapter name:", x)

	print('\n')



	notes = soup.findAll('div', class_='noteText')  

	for note in notes:
		last_sourceline=note.sourceline



	x = range(0, len(div_section_sourcelines))
	y=1
	for line in x:
		try:
			end_sourceline=div_section_sourcelines[line + 1]

		except:
			end_sourceline=last_sourceline

		start_sourceline=div_section_sourcelines[line]

		for note in notes:

			if note.sourceline>start_sourceline and note.sourceline<end_sourceline:
				text=note.text.strip()
				target_sourceline=note.sourceline-3
				notesheading = soup.findAll('div', class_='noteHeading')
				for head in notesheading:
					if head.sourceline==target_sourceline:
						page_info=head.text
						head, sep, tail = page_info.partition('Page ')
						page_number=clean_text(tail)
						start = '('
						end = ')'
						s = page_info
						highlight_color=(s.split(start))[1].split(end)[0]

				print (Fore.GREEN + 'SECTION:',y, end="")
				print (Fore.RED+' LINE:', note.sourceline, end="")

				if highlight_color=="yellow":
					print (Fore.YELLOW+' HIGHLIGHT COLOR:', highlight_color, end="")

				if highlight_color=="blue":
					print (Fore.BLUE+' HIGHLIGHT COLOR:', highlight_color, end="")
					
				if highlight_color=="pink":
					print (Fore.LIGHTMAGENTA_EX+' HIGHLIGHT COLOR:', highlight_color, end="")

					
				print (Fore.CYAN+' PAGE NUMBER:', page_number, end="")
				print (Fore.WHITE+' NOTE:', text, '\n')


		y=y+1










sys.exit()



# the number of sectionHeadings is: 3
# section number 143 chapter name: PART ONE: HOW TO INTRIGUE EVERYONE WITHOUT SAYING A WORD: YOU ONLY HAVE TEN SECONDS TO SHOW YOU'RE A SOMEBODY
# section number 182 chapter name: PART TWO: HOW TO KNOW WHAT TO SAY AFTER YOU SAY "HI"
# section number 203 chapter name: PART THREE: HOW TO TALK LIKE A VIP



