# Git Tag Challenge Write-up

### Introduction
The challenge description mentions that the startup started "tagging" their code releases but accidentally tagged one with the wrong thing. In Git (a system used to track changes in code), a "tag" is like a bookmark or a sticky note that developers use to label specific versions of their project (like `v1.0`). We need to find the flag hidden in one of these tags.

### Step 1: Download the Repository
The first step is to download the project's history onto our computer using the provided link.
We do this by running the clone command in the terminal:
```bash
git clone git://chals.cyberjousting.com:1363/challenge
```
This gives us a local copy of the `challenge` folder along with all its hidden Git history.

### Step 2: Examine the Tags
Once we are inside the `challenge` folder, we can see a list of all the tags the startup created.
```bash
cd challenge
git tag
```
Running this command outputs a massive list of tags, ranging from `v1.0` all the way to `v1.1.24` and beyond. There are hundreds of them! Searching through them manually would take forever.

### Step 3: Search for the Flag in the Tag Descriptions
Tags in Git aren't just names; they can also have hidden descriptions or messages attached to them, known as annotations.

We can list all the tags along with their detailed descriptions using the command:
```bash
git tag -l -n99
```
Since we know from the `README.md` that the flag format starts with `byuctf{`, we can use a search tool called `grep` to filter out everything else and only show the line containing our flag:
```bash
git tag -l -n99 | grep byuctf
```

### The Result
Running that search command instantly reveals the hidden message attached to the tag named `v1.0.129`:
> `v1.0.129        sdasdkjgarjknakfndlvoaiutiqewrhqiwerqjewnqwebehfbwhbqeuorueoqrhqoewuirhnbadnabyuctf{that's_a_lot_of_tags_wow}bkmsldfvnjsdfgkjwhvdsklfvsjlfbgwglkjhjfvkg sfgjno eigudshfwjlqfwebekjbfhdav`

### The Flag
Nestled right in the middle of that random text is the flag:
**`byuctf{that's_a_lot_of_tags_wow}`**
