### CTF Write-up: Blastoise, use Skull Bash!!

**The Goal:**
In this challenge, we connect to a remote computer and are dropped into a highly restricted environment known as a "jail." Our mission is to find and run a hidden script in our current folder to reveal a secret password (the "flag").

**The Obstacles (The Jail Rules):**
The computer uses a custom setup called "sbash" (Safe Bourne Again Shell). It acts like an extremely strict bouncer at a club, checking everything we type against a rigid list of rules before letting it through:
1. **No Lowercase Letters:** We cannot type any lowercase letters (a, b, c, etc.).
2. **No Common Symbols:** We can't type spaces, dots (`.`), stars (`*`), or many other standard punctuation marks.
3. **Strict Length Limit:** Our command cannot be longer than 20 characters.

Usually, to run a program in your current folder on this kind of system, you would type something like `./program_name`. However, we are forbidden from using the dot (`.`), and we certainly can't type out a lowercase name!

**The Solution: Thinking Outside the Box**
To beat the bouncer, we have to use clever loopholes built into the computer's language itself.

**Step 1: Pointing to our location without a dot**
Since we can't type the dot (`.`) to tell the computer "look in my current folder", we need another way. Luckily, the system has a built-in shortcut: `~+`.
Whenever we type `~+`, the computer automatically replaces it with the full, true name of the folder we are currently standing in (acting like a "You Are Here" pin on a map).

**Step 2: Naming the file without letters**
We know there is a file we need to run, but we can't type any letters! Instead of spelling its name, we can use wildcards. Think of a wildcard like a blank tile in Scrabble.
In this system, the question mark (`?`) acts as a wildcard for *exactly one character*. So, typing `???` means "any file name that is exactly three characters long."

**Step 3: Putting it all together**
By doing a little bit of trial and error (testing different lengths of wildcards), we found that the hidden script's name was exactly 8 characters long.

We combine our two tricks into one short code:
`~+/????????`

Here is how the computer translates this code:
1. **`~+`** tells it: "Start in my current folder."
2. **`/`** separates the folder from the file.
3. **`????????`** tells it: "Find and run the file here that has exactly 8 characters in its name."

**The Result:**
Because our command (`~+/????????`) contains no lowercase letters, uses no forbidden symbols, and is only 11 characters long, the "bouncer" lets it right through!

The system successfully translates our command, finds the hidden script, runs it, and rewards us with the winning flag:

**`byuctf{funky_bu1lt1n_j1uj1tsu_ba8c3e44}`**
