# RCaaS Writeup

This challenge provides a Linux executable binary called `rcaas`. The goal is to reverse engineer this program and discover the hidden flag.

## Step 1: Investigating the Binary

First, we checked what kind of file `rcaas` was using the `file` command, which told us it's a 64-bit Linux executable.

We then tried running it:
```bash
./rcaas
```
We received an error: `ERRO This script must be run as root`.

So, we ran it using `sudo`:
```bash
sudo ./rcaas
```
The output changed to: `INFO Service installed successfully.`

This suggested the program acts as a system service.

## Step 2: Tracking Down the Service

We used tools like `strace` (which traces system calls) and `systemctl` (which manages system services) to figure out what service was installed. We discovered a new systemd service called `atYourService`, whose description was "What is the flag?".

Starting this service ran the `rcaas` binary in the background. If we checked the system logs using `journalctl -u atYourService`, we could see what the program was doing. We also checked the system service definition and found it required a file at `/opt/atyourservice/flag.txt`.

This meant the challenge expected us to put our guess for the flag into a specific file, and the background service would check if our guess was correct.

## Step 3: Digging into the Code

Since we didn't know the flag, we had to look inside the `rcaas` program itself to see how it checks our guess. We used a tool provided by the Go programming language (which the program was written in) to disassemble the code:
```bash
go tool objdump -s main.main rcaas
```

The assembly code showed that the program reads the `/opt/atyourservice/flag.txt` file and does several checks:
1. It verifies that the file starts with the standard prefix `byuctf{`.
2. It expects the text inside the file to be exactly 46 characters long.
3. It specifically checks that the characters at indices 13, 21, 24, 26, 29, 31, 36, 37, and 39 are all the number `3`.

## Step 4: The Mathematical Equations

The core of the program's check was a series of mathematical equations. It loaded specific characters (bytes) from our flag guess, multiplied them together, and checked if the result matched a specific number.

For example, the code would load the 4th character and the 40th character, multiply their ASCII values together, and check if the result (when divided by 256 and taking the remainder) was exactly 80.

There were over 30 of these equations! Trying to solve them by hand would take forever.

## Step 5: Solving the Equations Automatically

To find the flag, we needed a way to solve this giant system of equations quickly. We used a powerful tool called `z3-solver`, which is a theorem prover from Microsoft Research.

We wrote a custom Python script that read the program's assembly code, automatically extracted all the multiplication equations, and translated them into constraints for `z3`.

We told `z3`:
* The flag is 46 characters long.
* It starts with `byuctf{` and ends with `}`.
* Every character must be a standard, printable letter or number.
* It must satisfy all the mathematical equations extracted from the code.

In less than a second, `z3` crunched the numbers and output the only possible solution that satisfies all the rules:

**`byuctf{s3rv1c3s_c4n_b3_r3v3rs3_3ng1n33r3d_t00}`**

## Step 6: Verification

To prove our solution was correct, we created the expected file and wrote our flag into it:
```bash
sudo mkdir -p /opt/atyourservice
echo 'byuctf{s3rv1c3s_c4n_b3_r3v3rs3_3ng1n33r3d_t00}' | sudo tee /opt/atyourservice/flag.txt
```

When we restarted the service and checked the logs, we were greeted with a success message: `INFO Correct!`
