# Solving the "Mysterious Person" Git Challenge

This guide explains how to find the hidden "flag" in a Git repository challenge. We'll break it down step-by-step so anyone can follow along, even without a technical background!

## The Goal
In Capture The Flag (CTF) challenges, your goal is to find a specific string of text called a "flag".

For this challenge, we were given two important clues:
1.  **"Some mysterious person made a commit to our repo! Who's the odd one out?"**
2.  **"The flag format is in the readme."**

Let's find this mysterious person!

## Step 1: Downloading the Project
First, we need to get a copy of the project files on our computer. In Git, a project is called a "repository" or "repo". We do this by "cloning" the repository using the provided link.

```bash
git clone git://chals.cyberjousting.com:1363/challenge
```
This command downloads the entire project and all its history into a new folder called `challenge`.

## Step 2: Exploring the History
A Git repository doesn't just store files; it stores the entire history of every change ever made to those files. Each change is called a "commit". Every commit records *what* was changed, *when* it was changed, and *who* changed it.

Our clue asks "Who's the odd one out?", which means we should look at the people who made these changes (the authors).

To see a list of everyone who has ever made a change to this project, we can use a special Git command:

```bash
git log --all --format="%an <%ae>" | sort | uniq
```

Here is a breakdown of what this command does in simple terms:
*   `git log --all`: Look through the entire history of the project.
*   `--format="%an <%ae>"`: Instead of showing everything about a change, only show the **A**uthor **N**ame and **A**uthor **E**mail.
*   `| sort | uniq`: Take that big list of names, sort them alphabetically, and remove any duplicates so we only see each unique person once.

## Step 3: Finding the Mysterious Person
When we run that command, we get a list of names that looks like this:

```text
Zinko <zinkogamez@gmail.com>
byuctf{wh0s_th3_auth0r?} <zinkogamez@gmail.com>
sawyer <zinkogamez@gmail.com>
walker <zinkogamez@gmail.com>
walter <zinkogamez@gmail.com>
william <zinkogamez@gmail.com>
wyatt <zinkogamez@gmail.com>
zinkozapper <zinkogamez@gmail.com>
```

Look closely at that list. Most of them look like normal names or usernames: Zinko, sawyer, walker, etc.

But there is one odd one out!
`byuctf{wh0s_th3_auth0r?}`

## Step 4: Claiming the Flag!
This strange name perfectly matches what flags look like in these types of challenges (they often start with the name of the competition and have curly braces). It also directly answers the clue's question: "Who's the author?".

We have successfully found the mysterious person and the flag!

**The Flag is:** `byuctf{wh0s_th3_auth0r?}`
