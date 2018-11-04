# LaboratoryOfComputationalPhysics

Notebooks guiding students through the world of data analysis with python.

This repo should be forked by each individual student. Exercises should be committed to the student's repo and notified to the professor by a pull request.
Such pull request should be made on this remote repo under the corresponding student branch (Dedicated branches will indeed be created in due time).

## Git Instructions

To start with, you need to have a github account. If you don't have one, go to [github](github.com) and follow instructions on how to create it.

Suggestion: use a reasonable username that resembles your actual name.  

Once you have your github, as first thing fork this repository, i.e. go [there](https://github.com/mzanetti79/LaboratoryOfComputationalPhysics) and click on the top-right button *fork*

### Setting up a local repository

What follows needs to be done any time a new local repository is created.
In particular, if you are working in a location where such repo already exist, what follows doesn't need to be repeated.
  * Clone your (forked) repository (i.e. create a local repository cloned from the remote one)

`git clone https://github.com/YOUR_GIT_ACCOUNT/LaboratoryOfComputationalPhysics.git`

 where YOUR_GIT_ACCOUNT it your account on github. Now you can get to your local working folder:

 `cd LaboratoryOfComputationalPhysics/`

   * Configure your username and email:

`git config --global user.name "YOUR_GIT_ACCOUNT"`

`git config --global user.email "YOUR_EMAIL_ADDRESS"`

(you must have understood what capital-letters-words stand for). Your git configuration is stored in `.gitconfig`, a file that you can alwasy edit by hand or via the `git config ..` commands.

* Define mzanetti79's repo as the upstream repository (you may need to set the url too), check that actually succeeded and get (fetch) the updates that have been done on the remote repository:

`git remote add upstream https://github.com/mzanetti79/LaboratoryOfComputationalPhysics.git`

`git remote set-url origin https://YOUR_GIT_ACCOUNT@github.com/YOUR_GIT_ACCOUNT/LaboratoryOfComputationalPhysics.git`

`git remote -v`

`git fetch upstream`

  * The default branch is `master`, you should now create your how development branch where to play and exercise with the code:

`git branch`

`git checkout -b DEV_BRANCH_NAME`

Now you `master` and `DEV_BRANCH_NAME` are the identical, work on the latter will tracked and later committed.


### Standard development cycle

  * Before starting with the development you could check whether the orginal repository (mzanetti79's one) have been updated with respect to your forked version (that's likely to be the case prior to every lab class). If it had, then merge the chances into your master:

  `git fetch upstream`

  `git checkout master`

  `git merge upstream/master`

this will update your local version, not the one on github. To update the latter you need to push the local version (see later)

  * From within your local repository choose your development branch and check it out (i.e. switch to it). :

`git checkout DEV_BRANCH_NAME`

  * Now do the real stuff, i.e. developing some code. Image you create a NEW_FILE. Add the file to your local repository and stages it for commit (To unstage a file, use 'git reset HEAD NEW_FILE)'

`git add NEW_FILE`

  * Commits the (tracked) changes you made to the file and prepares them to be pushed to your remote repository on github

`git commit -m "Add existing file"`

(what follows after `-m` is a comment to later remind what was that commit about)

 * Now you want to propagate (push) your local changes to your remote repository on github (`origin`)

 `git push origin DEV_BRANCH_NAME`

 * Finally you may want to propagate your development also to the repo you originally forked from, i.e. mzanetti79's one (this is likely to happen anytime you'll be asked to deliver your homework!). For that you need to go for a "pull request", which is done from github itself.

 * To close a development loop is a good habit to clean up, i.e. get rid of the development branch. Prior to that you may want to merge the `master` branch

 `git checkout master`

 `git merge DEV_BRANCH_NAME`  

 `git push origin master`

 `git commit -d DEV_BRANCH_NAME`
