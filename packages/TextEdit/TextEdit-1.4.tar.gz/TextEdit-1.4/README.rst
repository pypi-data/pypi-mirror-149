A small module for to display the letters at the sequence.  

New Releases
-------------
The new function Speed allow to change the speed of defilement for defile and defileInput

Installation
------------
For windows, you must install the folder TextEdit in C:\Users\your_account\AppData\Local\python\python-version\Lib\  
For Linux, you must install the folder TextEdit in /usr/local/lib/python/dist-packages/  
So, you import TextEdit for Linux with :
        
    pip3 TextEdit  
        
And, for Windows you import with :
        
    py -m pip install TextEdit
        
You must have pygame for use the fonction defileSound and defileInputSound.  
You can install it with this command for Linux :  

   pip3 install pygame;
        
And, for Windows :
        
    py -m pip install pygame
        
Importation and use
===================
Once you've installed, you can really quickly verified that it works with just this :  
        
    >>> import TextEdit
    >>> TextEdit.defile ("Hello world")
        
The TextEdit module contain for the moment 5 fonction : defile ; defileInput ; defileSound ; defileInputSound ; Speed.
It does not requires argument apart the function Speed.
You can put as many arguments as you want apart the function Speed
Example :  

    >>> TextEdit.defile ("Hello world",a,"Goodbye world")

The function Speed is different. You choose the speed of the function defile and defileInput.
You can write for argument a numberfor choose the time that elapses between each letter, "def" for reset the speed, and "reset" and "no_reset" for reset or no the speed at each line.
Example :

    >>> Speed("no_reset") #the speed don"t reset at each line
    >>> TextEdit.defile("Hello world") #it's the same speed for both lines.
    >>> TextEdit.defile("Goodbye world") 
        
Copyright
-----------
This software is Copyright © 2022 Corentin Perdry corentin.perdry@gmail.com  

See the bundled LICENSE file for more information.
