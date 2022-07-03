# Tutorial
AVim is a lightweight and simple text editor inspired by Vim and Sublime text LOL

There are 2 available mode in AVim

``Command Mode``
  Used to manage everything related to the file
  
``Insert Mode``
  Used to edit file content

Tutorial
  1. Download AVim folder from this github page
  2. Run ``avim.exe``
  3. Command mode is the first mode that active after the program is started. What you can do in this mode is passing some command to the text editor.
     
     Command template:  ``<Command Name> <Param>``
     
     Command Name:
     
     a. `:build` ->   `<Param>` : None
                      
            To build the current opened file
     b. `:cd`    ->   `<Param>` : Directory name
                      
            Display the name of or changes the current directory 
     c. `:e`     ->   `<Param>` : File to be opened
                      
            To open file
     d. `:help`  ->   `<Param>` : None
                      
            Show all available command
     e. `:ls`    ->   `<Param>` : None
                      
            Disply a list of files or subdirectories in a current directory
     f. `:mkdir` ->   `<Param>` : directory name
                      
            To make new subdirectory in the current directory
     g. `:pwd`   ->   `<Param>` : None
                      
            Display the path of the current directory
     h. `:q`     ->   `<Param>` : None
                      
            Exit program
     i. `:run`   ->  `<Param>` : None
                      
             Run the current opened file
     j. `:sav`   ->  `<Param>` : File name
                      
             Save the current opened file
  4. To enter ``Insert Mode``, press ``i``
  5. After finish editing the file, if you want to enter ``Command Mode``, press ``Esc``
