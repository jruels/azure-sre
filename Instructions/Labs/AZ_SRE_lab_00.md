
# Activity: Creating and Managing a Repository on GitHub

## Objectives

- Learn how to create a repository on GitHub
- Clone the repository locally
- Add a new file containing key Git commands
- Commit and push changes to the GitHub repository

## Step-by-Step Instructions

### 1. Create a Repository on GitHub

1. **Sign in to GitHub:**
   - Go to [GitHub](https://github.com/) and sign in to your account.

2. **Create a New Repository:**
   - Click on the `+` icon at the top right corner and select `New repository`.
   - Enter a repository name, e.g., `git-commands-tutorial`.
   - Optionally, add a description.
   - Choose the repository visibility (Public or Private).
   - Check `Initialize this repository with a README`.
   - Click on `Create repository`.

### 2. Clone the Repository Locally

1. **Open Terminal/Command Prompt:**
   - Open your terminal (macOS/Linux) or Command Prompt (Windows).

2. **Clone the Repository:**
   - Navigate to the directory where you want to clone the repository.
   - Run the following command:
     ```git
     git clone https://github.com/your-username/git-commands-tutorial.git
     ```

3. **Navigate to the Cloned Repository:**
   - Change to the directory of the cloned repository:
     ```git
     cd git-commands-tutorial
     ```

### 3. Add a New File Containing Key Git Commands

1. **Create a New File:**
   - Use a text editor to create a new file named `git-commands.md` in the repository directory.

2. **Add Key Git Commands:**
   - Open the `git-commands.md` file and add the following content:
     ```text
     # Key Git Commands

     ## Configuring Git

     git config --global user.name "Your Name"
     git config --global user.email "your.email@example.com"
  

     ## Initializing a Repository

     git init


     ## Cloning a Repository

     git clone https://github.com/username/repository.git


     ## Staging and Committing Changes

     git add filename
     git commit -m "Commit message"
 

     ## Viewing History
 
     git log
 

     ## Branching

     git branch new-branch
     git checkout new-branch


     ## Merging
  
     git merge branch-name


     ## Deleting Branches
 
     git branch -d branch-name


     ## Handling Merge Conflicts
 
     # Edit conflicted files
     git add resolved-file
     git commit
 

     ## Stashing
 
     git stash
     git stash pop


     ## Rebasing
 
     git rebase branch-name


     ## Cherry-Picking

     git cherry-pick commit-hash
 
     ```

### 4. Commit and Push Changes to GitHub

1. **Stage the New File:**
   - Run the following command to stage the `git-commands.md` file:
     ```git
     git add git-commands.md
     ```

2. **Commit the Changes:**
   - Run the following command to commit the changes:
     ```git
     git commit -m "Add git-commands.md with key Git commands"
     ```

3. **Push the Changes to GitHub:**
   - Run the following command to push the changes to the GitHub repository:
     ```git
     git push origin main
     ```
