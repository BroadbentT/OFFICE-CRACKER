#!/usr/bin/python3
# coding:UTF-8

# -------------------------------------------------------------------------------------
#                 PYTHON UTILITY FILE TO CRACK ENCRYPTED OFFICE FILES
#                BY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)
# -------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 3.0                                                               
# Details : Load required imports.
# Modified: N/A
# -------------------------------------------------------------------------------------

import os
import sys
import pyfiglet
import fileinput

from termcolor import colored

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 3.0                                                               
# Details : Conduct simple and routine tests on supplied arguements.   
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

if os.geteuid() != 0:
   print("Please run this python script as root...")
   exit()

if len(sys.argv) < 2:
   print("Use the command python3 office-cracker.py topsecret.docx...")
   exit()

fileName = sys.argv[1]

if os.path.exists(fileName) == 0:
   print("File " + fileName + " was not found, did you spell it correctly?...")
   exit()

filextends = fileName[-4:]
officelist = ["docx", ".doc", ".xls", "xlsx", ".ppt", "ccdb", ".pub"]

if filextends not in officelist:
   print("This is not a Microsoft Office file...\n")
   exit()

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 3.0                                                               
# Details : Create a function to display my universal banner.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

def display(fileName):
   os.system("clear")
   ascii_banner = pyfiglet.figlet_format("OFFICE CRACKER").upper()
   print((colored(ascii_banner.rstrip("\n"), 'red', attrs=['bold'])))
   print((colored("     BY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)     \n", 'yellow', attrs=['bold'])))
   print("Selected fileName : " + fileName + "\n")

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 3.0                                                               
# Details : Check all required dependencies are installed on the system.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

checklist = ["/usr/bin/hashcat"]
installed = True

display(fileName)
for check in checklist:
   cmd = "locate -i " + check + " > /dev/null"
   checked = os.system(cmd)
   if checked != 0:
      print("I could not find " + check + "...")
      installed = False

if installed == False:
   print("\nInstall the above missing dependencies before you begin...\n")
   exit()  
   
# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 3.0                                                               
# Details : User changeable dependencies.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------
   
hashcrack = "/usr/share/john/office2john.py"									# USER CHANGEABLE LOCATION OF OFFICETOJOHN
if not os.path.exists(hashcrack):
  print("The identified file on line 99 of this script, was not found!!...\n")
  exit()   
  
dictionary = "/usr/share/wordlists/rockyou.txt"									# USER CHANGEABLE LOCATION OF DICTIONARY
if not os.path.exists(dictionary):
   print("The identified dictionary on line 104 of this script, was not found!!...\n")
   exit()

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 3.0                                                               
# Details : The main menu system.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

menu = {}
menu['1']="Dictionary Attack."
menu['2']="Hash Attack."
menu['3']="Exit"

while True: 
   display(fileName)
   options=list(menu.keys())
   options.sort()
   for entry in options: 
      print(entry, menu[entry])
   print(colored("\n[?] Please select an option: ",'green'),end='')
   selection=input()

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 3.0                                                               
# Details : Menu option selected - Dictionary attack.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='1':
      print("\n[+] Crack Status : Using dictionary " + dictionary + "...")             
      print("[+] Crack Status : Using words in dictionary as password, please wait...")   
      os.system("python2.7 " + hashcrack + " '" + fileName + "' > F1.tmp")					# NOTE PYTHON 2.7 REQUIRED HERE!!
      os.system("john --encoding=UTF-8 --wordlist=" + dictionary + " F1.tmp > F2.tmp 2>&1")
      os.system("john --show F1.tmp > F2.tmp")
      os.system("sed -i '$d' F2.tmp")      
      password = open("F2.tmp").readline().replace(fileName + ":","")
      if password == "Could not find password":
         print("[-] Crack Status      : Dictionary exhausted...")
      else:      
         print(colored("\n[!] Found password '" + password.rstrip("\n") + "'\n",'green'))         
      os.system("rm *.tmp")        
      exit()

# ------------------------------------------------------------------------------------- 
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version: 2.0                                                                
# Details: Menu option selected - Hash attack.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection == '2':
      os.system("python2.7 " + hashcrack + " '" + fileName + "' > F1.tmp")
      hashdata = open("F1.tmp").readline().replace(fileName + ":","")
      os.system("sed -i 's/" + fileName + "://g' F1.tmp")
      print("\nHash Extracted    : " + hashdata[:55] + "...")
      hashdata = hashdata[:13]
      hashdata = hashdata[-4:]
      print("MS Office Version : " + hashdata)
      if hashdata == "2013":
         level = "9600"
      elif hashdata == "2010":
         level = "9500"
      elif hashdata == "2007":
          level = "9400"
      elif hashdata == "2003":
         level = "9700"
      else:
         print("\n[-] Crack Status      : Unknown year...")
         os.system("rm *.tmp")
         exit()
      print("Using Hashcat Mode: " + level)
      print("Crack Status      : Cracking hash values, please wait...")
      os.system("hashcat -m " + level + " -a 3 F1.tmp -i ?d?d?d?d?d?d --force > F2.tmp 2>&1")
      os.system("hashcat --show -m " + level + " F1.tmp --force > F3.tmp")
      os.system("awk -F: '{ print $2 }' F3.tmp > F4.tmp")
      password = open("F4.tmp").readline().replace("\n","")
      if password == "":
         print("Crack Status      : Hash values exhausted...\n")
      else:
         print(colored("\n[!] Found password '" + password.rstrip("\n") + "'\n",'green'))
      os.system("rm *.tmp")
      exit()
 
# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 3.0                                                               
# Details : Menu option selected - Quit program.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection == '3': 
      print("\n")
      quit()

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 3.0                                                               
# Details : Catch all other entries.
# Modified: N/A
# -------------------------------------------------------------------------------------

   else:
      pass

#Eof
