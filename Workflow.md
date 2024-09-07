## Workflow
The best practice for contributing to this project is to develop locally and use a pull request (PR) to submit changes. This workflow ensures that you can make and test adjustments on your local machine before pushing them to the remote repository. Below are the detailed steps for setting up and working with the repository locally.

### Prerequisites
You need to have Git installed on your local system.
You need to have an account on GitHub.
An IDE or text editor of your choice (such as VSCode) to view and edit the project files locally.

### Step-by-Step Workflow
- **Fork the Repository**

Fork the project repository to create a copy under your GitHub account. To do this, visit the main project repository at:
 ```text
 https://github.com/natnew/Prompt-Engineering
```

Click the `Fork` button in the top-right corner of the page to create your own copy of the repository.

- **Clone the Fork Locally**

Open your terminal (or command prompt) and clone your forked repository to your local system:
 ```text
git clone https://github.com/YourAccount/Awesome-Prompt-Engineering.git
```
Replace `YourAccount` with your GitHub username. This command will create a local copy of the repository in a directory called `Awesome-Prompt-Engineering`.

- **Set Up Remote Tracking**

Next, you need to set up remote tracking so you can sync your fork with the original repository. This ensures that you always have the latest changes from the main project.
 ```text
cd Awesome-Prompt-Engineering
git remote add upstream https://github.com/natnew/Awesome-Prompt-Engineering.git
```
Verify that you have correctly set up the remote tracking with:
 ```text
git remote -v
```
The output should be:
 ```text
origin   https://github.com/YourAccount/Awesome-Prompt-Engineering.git (fetch)
origin   https://github.com/YourAccount/Awesome-Prompt-Engineering.git (push)
upstream https://github.com/natnew/Awesome-Prompt-Engineering.git (fetch)
upstream https://github.com/natnew/Awesome-Prompt-Engineering.git (push)
```
- **Synchronize Your Main Branch with Upstream**

Before you start making changes, it's important to sync your local `main` branch with the upstream main branch to ensure you're working with the latest version:
 ```text
git checkout main
git fetch upstream
git merge upstream/main
```
- **Create a New Branch for Your Work**

It's best practice to work on your own branch rather than directly editing the `main` branch. Create and switch to a new branch:
 ```text
git checkout -b my_new_feature_branch
```
You can replace `my_new_feature_branch` with a meaningful name that reflects the feature or change you're working on.

- **Make Changes Locally**

Open the project folder in your IDE or text editor. Make the necessary changes to the files. After making changes, test your project locally to ensure everything works correctly. You can view your changes immediately.

- **Stage and Commit Your Changes**

Once you're satisfied with the changes you've made, stage and commit the files:
 ```text
git add <modified_files>
git commit -m "Your descriptive commit message"
```

- **Sync with the Upstream Repository**
Before pushing your changes, make sure your branch is up to date with the latest changes from the main repository:
 ```text
git fetch upstream
git merge upstream/main
```
Resolve any merge conflicts if they arise.

- **Push Your Changes to GitHub**

Push your branch with the changes to your forked repository on GitHub:
 ```text
git push origin my_new_feature_branch
```

- **Create a Pull Request (PR)**

After pushing your changes, navigate to your repository on GitHub. You will see a notification prompting you to create a pull request. Click the "Compare & pull request" button to submit your changes for review.

You can find more detailed instructions on creating a pull request [here](https://github.com/natnew/Prompt-Engineering).

### Best Practices
- Use Meaningful Branch Names: When creating a new branch, use a name that describes the feature or fix you are working on. This makes it easier to manage and review.

- Commit Frequently: Make small, atomic commits. This makes it easier to track changes and roll back if needed.

- Write Descriptive Commit Messages: A clear commit message helps others understand what changes were made and why.

- Sync Regularly: Before pushing your changes or starting new work, always sync your branch with the upstream repository to ensure you have the latest changes.











