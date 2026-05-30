# CTF Challenge Write-up

### Challenge Description
We were told that a user named Walker accidentally pushed an API key to a public repository (a place where code is stored). Walker quickly deleted it and thought everything was safe. The flag was hidden within that deleted API key.

### Step 1: Downloading the Code
The first step was to get a copy of the repository. Think of a repository like a folder that tracks every single change made to files over time. We used the provided link to download (or "clone") the repository onto our computer using the terminal. The command we used was:
`git clone git://chals.cyberjousting.com:1363/challenge`

### Step 2: Looking at the History
In the tool Git, which manages these repositories, nothing is ever truly deleted once it's been saved. Even if a file is removed, a record of its existence and its contents at the time remains in the repository's history. We can look at this history, which shows a list of all "commits" (or saved changes) made by anyone who worked on the code.
We used a command to view the history of the repository:
`git log --all --stat`

This command essentially tells Git: "Show me the full history of every change made to every branch (version) of this project, and give me a summary of which files were changed."

### Step 3: Finding the Deleted File
As we scrolled through the history, we looked for anything suspicious or related to an "API key," since that was our clue.
We noticed a change made by a user named Walker with the comment: "Forgot to commit skull skull".
More importantly, we found another set of changes where a file named `apikey.txt` was added in one update, and then seemingly deleted in a subsequent update. This perfectly matches the story from the challenge description.

### Step 4: Extracting the Secret
Now that we knew the file `apikey.txt` existed at some point, we needed to see exactly what was inside it when it was added. We asked Git to show us the exact lines of code that were added or removed in the `apikey.txt` file throughout its history.
We ran:
`git log --all -p -- apikey.txt`

This command showed us the "diff" (difference) of that specific file over time. In the output, we saw the exact moment the file was created and the content that was put inside it:
```
+byuctf{But_th3s_was_d3l3t3d?}
```
The plus sign means this line was added. And right there, we found our secret flag!

### Conclusion
Even if you delete a file in a Git repository and upload those changes, the history of that file is still accessible to anyone who downloads the repository. This is why you should never commit sensitive information like passwords or API keys to a Git repository, even temporarily!

**Flag:** `byuctf{But_th3s_was_d3l3t3d?}`