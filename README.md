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

  * The default branch is `master`, you should now create your how development branch where to play and exercise with the code:

`git branch`

`git checkout -b DEV_BRANCH_NAME`

Now you `master` and `DEV_BRANCH_NAME` are the identical, work on the latter will tracked and later committed.

  * Define mzanetti79's repo as the upstream repository, check that actually succeeded and get (fetch) the updates that have been done on the remote repository:

`git remote add upstream https://github.com/mzanetti79/LaboratoryOfComputationalPhysics.git`

`git remote -v`

`git fetch upstream`
