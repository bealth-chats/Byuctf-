# CTF Write-up: Replaced Secrets

In this Capture The Flag (CTF) challenge, we were given a hint that "someone has replaced it [the `secrets.txt` file] with something else!". The goal was to find a hidden flag.

Here is the step-by-step process of how we uncovered the secret:

### Step 1: Getting the Files
First, we downloaded the project files (also known as a repository) to our local machine. Think of a repository like a folder that keeps track of every change ever made to the files inside it. We did this using a command line tool called Git.

### Step 2: Investigating the Clues
Looking at the current version of the `secrets.txt` file, it just had a generic message: "This is where we've already put our secrets!". This was a dead end. However, the challenge description gave us a very important clue: the word "replaced".

### Step 3: Uncovering the "Replace" Trick
In Git, there is an advanced feature that allows people to "replace" one piece of history with another without changing the rest of the project's timeline. This means that when you look at a file, you might be seeing a fake or "replaced" version instead of the original one.

To see if this trick was being used, we told Git to fetch any hidden "replace" references from the server:
`git fetch origin 'refs/replace/*:refs/replace/*'`

### Step 4: Revealing the Original File
Once we downloaded those hidden references, we asked Git to list any replaced items:
`git replace -l`

This revealed a specific point in time (called a commit) that had been replaced. By asking Git to show us the contents of that original, un-replaced commit, we finally saw what was hidden beneath the fake `secrets.txt` file.

### The Result
The original file contained the flag we were looking for!

**Flag:** `byuctf{I_lov3_s3cr3t_files}`
