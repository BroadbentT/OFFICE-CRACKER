#!/usr/bin/python
# coding:UTF-8

# -------------------------------------------------------------------------------------
#                 PYTHON UTILITY FILE TO CRACK ENCRYPTED OFFICE FILES
#                BY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)
# -------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Load required imports.
# Modified: N/A
# -------------------------------------------------------------------------------------

import os
import sys
import fileinput

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Display my universal banner.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

os.system("clear")

print "  ___  _____ _____ ___ ____ _____       ____ ____      _    ____ _  _______ ____   "
print " / _ \|  ___|  ___|_ _/ ___| ____|     / ___|  _ \    / \  / ___| |/ / ____|  _ \  "
print "| | | | |_  | |_   | | |   |  _| _____| |   | |_) |  / _ \| |   | ' /|  _| | |_) | "
print "| |_| |  _| |  _|  | | |___| |__|_____| |___|  _ <  / ___ \ |___| . \| |___|  _ <  "
print " \___/|_|   |_|   |___\____|_____|     \____|_| \_\/_/   \_\____|_|\_\_____|_| \_\ "
print "                                                                                   "
print "             BY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)                 "
print "                                                                                   "

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Conduct simple and routine tests on supplied arguements.   
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

if os.geteuid() != 0:
    print "Please run this python script as root..."
    exit(True)

if len(sys.argv) < 2:
    print "Use the command python office-cracker.py microsoft.docx..."
    exit(True)

filename = sys.argv[1]

if os.path.exists(filename) == 0:
    print "File " + filename + " was not found, did you spell it correctly?..."
    exit(True)

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Check that the specified file is a Microsoft Office file.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

filextends = filename[-4:]
officelist = ["docx", ".doc", ".xls", "xlsx", ".ppt", "ccdb", ".pub"]

if filextends not in officelist:
    print "Unknown Microsoft Office file format...."
    exit (True)

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Check all required dependencies are installed on the system.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

checklist = ["rockyou", "office2john", "hashcat"]
installed = True

for check in checklist:
    cmd = "locate " + check + " > /dev/null"
    checked = os.system(cmd)
    if checked != 0:
        print check + " is missing..."
        installed = False

if installed == True:
    print "All required dependencies are pre-installed...\n"
else:
    print "Install missing dependencies before you begin..."
    exit (True)

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : The main menu system.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

menu = {}
menu['1']="Dictionary Attack."
menu['2']="Hash Attack."
menu['3']="Exit"

while True: 
    options=menu.keys()
    options.sort()
    for entry in options: 
        print entry, menu[entry]
    selection=raw_input("\nPlease Select: ")
    print ""

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Menu option selected - Dictionary attack.
# Modified: N/A
# -------------------------------------------------------------------------------------

    if selection =='1':
        print "Crack Selected    : Dictionary attack..."
        dictionary = "/usr/share/wordlists/rockyou.txt"
        if os.path.isfile(dictionary):
            print "Using Dictionary  : " + dictionary + "..."
        else:
            print "System Error      : Dictionary not found..."
            exit(True)
        os.system("office2john.py " + filename + " > Hash.txt")
        os.system("john --encoding=UTF-8 --wordlist=" + dictionary + " Hash.txt > Temp.txt")
        os.system("john --show Hash.txt > Answer.txt")
	os.system("sed '$d' Answer.txt > Password.txt")
	with open('Password.txt', 'r') as myfile:
            password = myfile.read().replace(filename + ":", '')
        if password == "Could not find password":
            print "Crack Status      : Dictionary exhausted..."
        else:      
            print "File Password     : " + password
        os.remove('Hash.txt')
        os.remove('Answer.txt')
        os.remove('Password.txt')
        os.remove('Temp.txt')
        exit (False)

# ------------------------------------------------------------------------------------- 
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version: 2.0                                                                
# Details: Menu option selected - Hash attack.
# Modified: N/A
# -------------------------------------------------------------------------------------

    elif selection == '2':
        print "Crack Selected    : Hash attack..."
        os.system("office2john.py " + filename + " > Hash.txt")
	with open('Hash.txt', 'r') as myfile:
            hashdata = myfile.read().replace(filename + ":", '')
	for line in fileinput.input('Hash.txt', inplace=1):
            sys.stdout.write(line.replace(filename + ":", ''))
        hashdata = hashdata[:55]    
        print "Hash Extracted    : " + hashdata + "..."
	hashdata = hashdata[:13]    
        hashdata = hashdata[-4:]
        print "MS Office Version : " + hashdata
        if hashdata == "2013":
            level = "9600"
        elif hashdata == "2010":
            level = "9500"
        elif hashdata == "2007":
            level = "9400"
	elif hashdata == "2003":
            level = "9700"
        else:
            print "Crack Status      :Unknown year..."
            os.remove("Hash.txt")
            exit (True)
        print "Using Hashcat Mode: " + level
        os.system("hashcat -m " + level + " -a 3 Hash.txt -i ?d?d?d?d?d?d --force > Temp.txt")
        os.system("hashcat --show -m " + level + " Hash.txt --force > Answer.txt")
        os.system("awk -F: '{ print $2 }' Answer.txt > Password.txt")
        with open('Password.txt', 'r') as myfile:
            password = myfile.read().replace('\n', '')
        if password == "":
            print "Crack Status      : Algorithm exhausted...\n"
        else:
            print "Found Password    : " + password + "..."
        os.remove('Hash.txt')
        os.remove('Answer.txt')
        os.remove('Password.txt')
        os.remove('Temp.txt')
        exit (True)
 
# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Menu option selected - Quit program.
# Modified: N/A
# -------------------------------------------------------------------------------------

    elif selection == '3': 
        break

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Catch all other entries.
# Modified: N/A
# -------------------------------------------------------------------------------------

    else:
        print ""

#Eof
