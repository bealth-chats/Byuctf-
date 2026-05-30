# Write-up for "easy mode is turned on" CTF Challenge

## Challenge Description
The challenge provides the description:
> Okay, easy mode is turned on. You know how to use bash, right?
> chals.cyberjousting.com:1370

This indicates we need to connect to a server that likely gives us a bash (Linux command line) interface, but with some restrictions ("easy mode... With... some modifications, anyways").

## Step-by-Step Solution

### 1. Connecting to the Server
First, we need to interact with the server. We can do this using a Python script that connects to `chals.cyberjousting.com` on port `1370`.

When we connect, the server greets us with:
```
Run anything you want! With... some modifications, anyways
$
```

### 2. Testing the Waters
Let's try sending a simple command like `ls` to list the files.
If we send `ls`, the server replies:
```
Input:
ls
Error:
bash: line 1: ls: command not found
```
This tells us that common commands like `ls` and `cat` have been removed or the path has been restricted so we can't find them.
We also noticed that if we send commands with spaces, the spaces are stripped out! For example, `echo *` becomes `echo*`.

### 3. Finding the Files
We can still use built-in bash features. One built-in feature is wildcard expansion (`*`), which replaces `*` with all filenames in the current directory.
Since spaces are removed, we can't use `echo *`. However, we can use an internal bash variable called `IFS` (Internal Field Separator) which contains a space by default. Let's try `echo${IFS}*`.
The server responds with:
```
Input:
echo${IFS}*
Output:
bash flag.txt run
```
Aha! There is a file named `flag.txt`! We need to read its contents.

### 4. Reading the Flag
We need to read `flag.txt`, but we don't have the `cat` command, and spaces get removed.
We can use a bash feature called command substitution. If we write `$(<flag.txt)`, bash will read the contents of `flag.txt` and substitute it into our command.

Let's try sending the command `echo $(<flag.txt)`.
When the server receives this, it strips the space, turning it into:
`echo$(<flag.txt)`

Bash will then read `flag.txt` and place its contents right next to `echo`.
The server responds with an error:
```
Input:
echo$(<flag.txt)
Error:
bash: line 1: echobyuctf{g0_t0_j41l_a60941}: command not found
```

### 5. Success!
Even though it was an error, the error message reveals the flag!
The command bash tried to run was `echobyuctf{g0_t0_j41l_a60941}`, which means the contents of `flag.txt` is `byuctf{g0_t0_j41l_a60941}`.

**Flag:** `byuctf{g0_t0_j41l_a60941}`
