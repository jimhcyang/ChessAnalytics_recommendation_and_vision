## Working with GitHub repo ## 


Clone repo locally in dir of your choice (example personal_github is dir)

```
➜  personal_github git clone https://github.com/nankivel/capstone.git 
Cloning into 'capstone'...
remote: Enumerating objects: 325, done.
remote: Counting objects: 100% (157/157), done.
remote: Compressing objects: 100% (121/121), done.
Receiving objects: 100% (325/325), 142.90 MiB | 6.33 MiB/s, done.
remote: Total 325 (delta 42), reused 108 (delta 32), pack-reused 168
Resolving deltas: 100% (79/79), done.
```

Change to cloned repo dir

```
➜  personal_github cd capstone       
➜  capstone git:(main) 
```

Look at repo contents

```
➜  capstone git:(main) ls -l
total 48
-rw-r--r--   1 nankivel  staff   1088 Mar 18 10:04 LICENSE
-rw-r--r--   1 nankivel  staff   3324 Mar 18 10:04 README.md
-rw-r--r--   1 nankivel  staff  10562 Mar 18 10:04 action_encoder_decoder.ipynb
drwxr-xr-x  10 nankivel  staff    320 Mar 18 10:06 chesscog
drwxr-xr-x   8 nankivel  staff    256 Mar 18 10:06 data
drwxr-xr-x   3 nankivel  staff     96 Mar 18 10:05 models
drwxr-xr-x  10 nankivel  staff    320 Mar 18 10:05 notebooks
-rw-r--r--   1 nankivel  staff    103 Mar 18 10:04 requirements.txt
```

See current git status

```
➜  capstone git:(main) git status                                        
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

Added/updated file, check git status

```
➜  capstone git:(main) git status                                        
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
➜  capstone git:(main) git status
On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	github_notes.md

nothing added to commit but untracked files present (use "git add" to track)
```

Stage file

`➜  capstone git:(main) ✗ git add * `

Commit changes

```
➜  capstone git:(main) ✗ git commit -m "add github nodes readme"           
[main 6e3d292] add github nodes readme
 1 file changed, 67 insertions(+)
 create mode 100644 github_notes.md
 ```
 
 Push committed changes to remote repo
 
 ```
 ➜  capstone git:(main) ✗ git push                               
Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Delta compression using up to 10 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 1006 bytes | 1006.00 KiB/s, done.
Total 3 (delta 1), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
To https://github.com/nankivel/capstone.git
   6406221..6e3d292  main -> main
```
