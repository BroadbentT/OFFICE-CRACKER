#!/usr/bin/python

# -------------------------------------------------------------------------------------
#                 PYTHON UTILITY FILE TO CRACK ENCRYPTED OFFICE FILES
#                BY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)
# -------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------- 
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Load any required imports.
# Modified: N/A
# -------------------------------------------------------------------------------------

import os
import sys
import fileinput

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Show a universal header.    
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

print "  ___    _____   _____   ___    ____   _____    ____   ____       _       ____   _  __  _____   ____   "
print " / _ \  |  ___| |  ___| |_ _|  / ___| | ____|  / ___| |  _ \     / \     / ___| | |/ / | ____| |  _ \  "
print "| | | | | |_    | |_     | |  | |     |  _|   | |     | |_) |   / _ \   | |     | ' /  |  _|   | |_) | "
print "| |_| | |  _|   |  _|    | |  | |___  | |___  | |___  |  _ <   / ___ \  | |___  | . \  | |___  |  _ <  "
print " \___/  |_|     |_|     |___|  \____| |_____|  \____| |_| \_\ /_/   \_\  \____| |_|\_\ |_____| |_| \_\ "
print "                                                                                                       "
print "                         BY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)                         "

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Conduct simple and routine tests on supplied arguements.   
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

if os.geteuid() != 0:
    print "\nPlease run this python script as root..."
    exit(True)

if len(sys.argv) < 2:
    print "\nUse the command python office-cracker.py topsecret.docx\n"
    exit(True)

filename = sys.argv[1]

if os.path.exists(filename) == 0:
    print "\nFile " + filename + " was not found, did you spell it correctly?"
    exit(True)

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Check all required dependencies are installed on the system.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

install = False

print "\nChecking dependencies...."

if os.path.isfile('/usr/share/wordlists/rockyou.txt') != 1:
    print "Rockyou.txt - missing"
    install = True

if os.path.isfile('/root/Downloads/bleeding-jumbo/JohnTheRipper-bleeding-jumbo/run/office2john.py') != 1:
    print "John the ripper bleeding jumbo - missing"
    install = True

if os.path.isfile('/root/.hashcat/hashcat.potfile') != 1:
    print "Hashcat - missing"
    install = True

if install == False:
    print "All required dependencies are pre-installed...\n"
else:
    print "Install any missing dependencies before you begin...\n"
    exit (True)

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Check Microsoft Office File.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

typetest = filename[-4:]
office = False

if typetest == "docx":
    office = True
elif typetest == "xlsx":
    office = True
else:
    office = False

if office == False:
    print "Unknown office file...."
    exit (True)

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Main menu system.
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
    selection=raw_input("Please Select: ") 

# ------------------------------------------------------------------------------------- 
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Menu option one selected - Dictionary attack.
# Modified: N/A
# -------------------------------------------------------------------------------------

    if selection =='1':
        print "\nCrack Selected    : Dictionary Attack"
        print "Using Dictionary  : /usr/share/wordlists/rockyou.txt"
        print "Crack Status      : Cracking, please wait..."
        os.system("python /root/Downloads/bleeding-jumbo/JohnTheRipper-bleeding-jumbo/run/office2john.py " + filename + " > F1.txt")
        print('-' * 100)
        os.system("john --wordlist=/usr/share/wordlists/rockyou.txt F1.txt")
        os.system("john --show F1.txt > F2.txt")
        print('-' * 100)
	os.system("sed '$d' F2.txt > F3.txt")
	with open('F3.txt', 'r') as myfile:
            password = myfile.read().replace(filename + ":", '')
        if password == "Could not find password":	
            print "Crack Status      : Dictionary exhausted...\n"
        else:      
            print "File Password     : " + password	
        os.remove('./F1.txt')
        os.remove('./F2.txt')
        os.remove('./F3.txt')
        exit (False)

# ------------------------------------------------------------------------------------- 
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Menu option two selected - Hash attack.
# Modified: N/A
# -------------------------------------------------------------------------------------

    elif selection == '2':
        print "\nCrack Selected    : Hash Attack"
        os.system("perl ../../Downloads/bleeding-jumbo/JohnTheRipper-bleeding-jumbo/run/office2john.py " + filename + " > F1.txt")
        for line in fileinput.input('F1.txt', inplace=1):
            sys.stdout.write(line.replace(filename + ":", ''))
        with open('F1.txt', 'r') as myfile:
            hashdata = myfile.read().replace('\n', '')
        hashdata = hashdata[:25] + "..."     
        print "Hash Extracted    : " + hashdata
        os.system("sed -e 's/.*office$\*\(.*\)\*10000.*/\\1/' F1.txt > Year.txt")
        with open('Year.txt', 'r') as myfile:
            year = myfile.read().replace('\n', '')
        if year == "2013":
            level = "9600"
        elif year == "2010":
            level = "9500"
        elif year == "2007":
            level = "9400"
        else:
            print "Crack Status      :Unknown year, using defualt..."
            level = "9700"
        print "Hash Mode/Level   : " + level
        print "Crack Status      : Cracking, please wait..."
        os.system("hashcat -m " + level + " -a 3 F1.txt -i ?d?d?d?d?d?d --force > F2.txt") # Note - Currently set for six decimal password only
        os.system("hashcat --show -m " + level + " F1.txt --force > F3.txt")
        os.system("awk -F: '{ print $2 }' F3.txt > F4.txt")
        with open('F4.txt', 'r') as myfile:
            hashpass = myfile.read().replace('\n', '')
        if hashpass == "":
            print "Crack Status      : Algorithm exhausted...\n"
        else:
            print "Password          : " + hashpass
        os.remove('./Year.txt')
        os.remove('./F1.txt')
        os.remove('./F2.txt')
        os.remove('./F3.txt')
        os.remove('./F4.txt')
        exit (True)
 
# ------------------------------------------------------------------------------------- 
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Menu option three selected - Quit program.
# Modified: N/A
# -------------------------------------------------------------------------------------

    elif selection == '3': 
        break

# ------------------------------------------------------------------------------------- 
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Catch all other entries.
# Modified: N/A
# -------------------------------------------------------------------------------------

    else:
        print ""

#Eof
