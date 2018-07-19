# instead of clicking through all the electives to read descriptions, hours, prerequisites, would it not be better
# to have the computer put them all in one place....?

# Author Corey Koelewyn
# Created July 19, 2018
# Requires a list of courses in a called "courses.txt" to be in same folder
# "courses.txt" will have one field of study and course number seperated by a space
# per line. example "ASTR 101"

from bs4 import BeautifulSoup
import requests
import os

# this is the base URL for course descriptions as of July 2018
course_url_base = "https://web.uvic.ca/calendar2018-05/CDs/"

def course_list_builder():
	try:
		local_files = os.listdir()
		for local_file in local_files:
			if local_file.lower() == "courses.txt":
				course_file_name = local_file
				continue
		course_file = open(course_file_name, 'r')
	except:
		print("courses.txt is not found in the current directory. check file name")
		exit()
	courses = []
	for line in course_file:
		try:
			course_id = (line.split(' ')[0] , line.split(' ')[1].strip())
			courses.append(course_id)
		except:
			print("something goofy on this line " + line)
	return courses

def output_file_builder(file_name):
	local_files = os.listdir()
	count = 1
	if file_name not in local_files:
		output_file = open(file_name, 'w')
		return output_file
	output_name = file_name
	while output_name in local_files:
		output_name = file_name.split('.')[0] + "(" + str(count) + ")" + '.' +file_name.split('.')[1]
		count += 1
	print("creating " + output_name)
	output_file = open(output_name, 'w')
	return output_file

# meat and potatoes of program, this returns the data grabbed from the web URL in a readable friendly form for writing 
# into a file
def website_data(web_url):
	data = requests.get(web_url).text
	soup = BeautifulSoup(data)
	data = requests.get(web_url).text
	soup = BeautifulSoup(data)
	try:
		course_sub_num = soup.find('h1' ,"subject-and-number").text
		course_title = soup.find('h2', "course-title").text
		course_hours = soup.find('h3', "hours").text
		course_description = soup.find('p' ,"description").text
	except:
		print(web_url + " seems to not work, check spelling")
		return "nothing found for this."
	return ( course_sub_num , course_title , course_hours , course_description)

def make_url(course_ID):
	return course_url_base + course_ID[0].upper() + '/' + course_ID[1] + '.html'


def main():
	outputfile = output_file_builder("electives.txt")
	for url in course_list_builder():
		data = website_data(make_url(url))
		outputfile.writelines(data[0] + ' ' + data[1] + '\n')
		outputfile.writelines(data[2]+ '\n\n')
		outputfile.writelines(data[3]+ '\n\n')
	outputfile.close()

if __name__ == "__main__":
	main()
