import requests
from bs4 import BeautifulSoup
from json import dump
from time import time_ns
from sys import exit




# NEED TO ADD:
# 1) Multiple page of commits
# 2) Whole person scanner
# 3) Ligma ballz suckers!











class patch:
	def __init__(self,commitID:str,author:str,url:str,date:str,fromName=None,fromEmail:str=None):
		self.commitID=commitID
		self.author=author
		self.url=url
		self.date=date
		self.fromName=fromName
		self.fromEmail=fromEmail

	def printInfo(self):
		print(f"Commit ID: {self.commitID}\nAuthor: {self.author} \nURL: {self.url} \nDate: {self.date}\nFrom: {self.fromName} <{self.fromEmail}>\n")
			


def save(REPONAME,REPOURL,detailedPatches):
	if detailedPatches==[]:
		print("Nothing to save. Shutting down.\nSee you later!")
	else:
		jsonOutput={}

		jsonOutput[REPONAME]={'URL': REPOURL,'patches':[]}
		for detailedPatch in detailedPatches:
			jsonOutput[REPONAME]['patches'].append({'Commit ID':detailedPatch.commitID,'Author':detailedPatch.author,'URL':detailedPatch.url,'Date':detailedPatch.date,'From':f'{detailedPatch.fromName} <{detailedPatch.fromEmail}>'})


		while True:
			answer=input("Save results in json file?(y/n)\n>>>")
			if answer.lower() not in ["y","n"]:
				print("Wrong answer.\n")
			else:
				break

		if answer=="y":
			filename=f"results-{REPONAME.split('/')[1]}-{time_ns()}.json"
			with open(filename,"w") as f:
				dump(jsonOutput,f)
			print(f"Results saved as {filename}")
			print("Have a nice day!")
		else:
			print("Have a nice day!")


def investigate(REPOURL):
	try:
		REPONAME=REPOURL.replace('https://github.com/','')
		print(f"Starting repo analyze for {REPONAME}")

		repoHtml=requests.get(REPOURL).text
		mainSoup=BeautifulSoup(repoHtml, 'html.parser')


		spanlist=mainSoup.find_all('span',attrs={'class':'css-truncate-target'})
		branch=""
		for span in spanlist:
			if span.get("data-menu-button")!=None:
				branch=span.text
				print(f"Searching for branch {branch}")
	except KeyboardInterrupt:
		print("Exitting. Nothing to display or save.")
		exit()

	try:
		commitHtml=requests.get(f"{REPOURL}/commits/{branch}").text
		commitSoup=BeautifulSoup(commitHtml,'html.parser')
		commitBtns=commitSoup.find_all("a",{'class':'tooltipped tooltipped-sw btn-outline btn BtnGroup-item text-mono f6'})
		commitAuthors=[]
		possibleTags=commitSoup.find_all(["a",'span'])

		for tag in possibleTags:
			try:
				if tag['class']==['commit-author','user-mention']:
					commitAuthors.append(tag.text)
				elif tag['class']==['text-bold']:
					commitAuthors.append(tag['title'])
			except:
				pass


		commitDates=commitSoup.find_all("relative-time")

		patches=[]
		detailedPatches=[]
		index=0
		for btn in commitBtns:
			commitURL=btn.get('href')[1:]
			commitID=btn.get('href').split("/")[-1]
			patches.append(patch(commitID,commitAuthors[index],f"https://github.com/{commitURL}.patch",commitDates[index].get("datetime")))
			repoPatch=patches[index]
			rawPatch=requests.get(repoPatch.url).text
			for line in rawPatch.splitlines():
				if line.startswith("From:") and "@" in line:
					line=line.replace("From: ","")
					detailedPatch=patch(repoPatch.commitID,repoPatch.author,repoPatch.url,repoPatch.date,line.split("<")[0][:-1],line.split("<")[1][:-1])
					detailedPatches.append(detailedPatch)
					detailedPatch.printInfo()
			index+=1
		save(REPONAME,REPOURL,detailedPatches)
	except KeyboardInterrupt:
		print("Canceled by user.")
		save(REPONAME,REPOURL,detailedPatches)

if __name__=="__main__":
	from pyfiglet import Figlet
	fig=Figlet("colossal",width=180)
	print(fig.renderText("GitSpector"))
	print("\t\t\t\tA GitHub commit analynzer. For noobs, by noobs.")
	try:
		while True:
			RepoURL=input("Enter repository URL (https://github.com/Test/TestRepo):\n>>>")
			if RepoURL.startswith("https://github.com/"):
				print("Checking repo link...")
				if requests.get(RepoURL).status_code!=200:
					print("Error: Invalid URL. Repository either doesn't exist or private.")
				else:
					print("Valid link!")
					break
		investigate(RepoURL)
	except KeyboardInterrupt:
		print("Canceled by user.")