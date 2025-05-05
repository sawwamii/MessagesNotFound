<<<<<<< HEAD
**HOW TO SETUP:**  
make sure you have git, https://git-scm.com/downloads

create a python venv (py -m venv venv_name) (anywhere will do)  
next, activate it (run activate.bat in Scripts)

at this point, create a new folder inside of the venv folder (technically it doesnt have to be inside the venv, but i made it like that so its easy to manage)  
PREFERABLY name it "MessagesNotFound", cause thats the name of the project (idk if not following this will break anything)  
go into the folder, and run "git init"  
now you will pull from this repository

first, run "git remote add origin https://github.com/sawwamii/MessagesNotFound"  
this adds a remote link or smth to this repository, and here it is referred to as "origin" (cause thats what you put)  

now you can run "git pull origin main", and it SHOULD put the latest version of this project onto your pc  
one last thing, you'll notice a file named "requirements.txt", you're gonna wanna run "pip install -r requirements.txt"

**HOW TO USE GIT:**  
like mentioned before, you need to run "git init" in the project folder, and then "git remote add origin https://github.com/sawwamii/MessagesNotFound" to connect to the repository  
after you make some changes, you can run "git add ." (basically "stages" ALL files for committing, i think u can also add individual files also but idk this might be better when u dont know what will be changed)

"git status" will show you what files have been changed  
running "git commit -m MessageHere" will basically stage these files for the next step (required if you want to push)  
running "git push" will push all of the files you committed, and now the repository will be updated accordingly  
>btw, if you are pushing for the first time, you do "git push -u origin main" (doing it this way will basically push, and also make git remember to push it to main) (BASICALLY, after running this longer command, you can just run "git push" from now on)

**BTW**:  
if you happen to add new libraries for whatever reason, make sure you update **requirements.txt**! just run "pip freeze > requirements.txt" in the ORIGINAL directory of the requirements.txt file, and it should update when you commit and push

i think thats all? hopefully this is clear enough

**OH YEAH**:  
if you wanna test this by using another device to connect or smth, make sure you know the ip of the host machine + the port (usually 8000) (u need to know this cause you gotta connect to the correct address on the other device), and also ensure that when you do runserver you do it like this "py manage.py runserver 0.0.0.0:8000" (0.0.0.0:8000 is to allow other devices to connect to the host's ip)
=======
# MessagesNotFound
computer science 5 elective project
>>>>>>> 842df3fb94cfffa7d986de884a1452305052d7f7
