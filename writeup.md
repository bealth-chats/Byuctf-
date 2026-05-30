# Writeup for YARA Rule CTF Challenge

In this challenge, we are provided with a YARA rule named `rule.yar` and need to figure out what string satisfies all of its conditions. The challenge description suggests using the `--no-warnings` flag. The format of the flag is `byuctf{...}`.

Let's break down the rule string by string to piece together the flag.

### Examining the Strings

YARA allows matching of strings using text, regular expressions, and byte patterns. We can decode and infer the expected string components from each of the declared strings in the rule.

1. **`$c = /byuctf.{33}/`**
   - This regular expression mandates that the string starts with `byuctf` followed by exactly 33 characters. This means the entire flag length is 39 characters.

2. **`$m = { 62 ?? ?? ?? ?? ?? ?? ?? 68 }`**
   - This translates to `b` (0x62), followed by 7 wildcard bytes, ending with `h` (0x68). This perfectly matches the start of the flag: `byuctf{wh`.

3. **`$d = { 77 ?8 79 }`**
   - `0x77` is `w`, `0x79` is `y`. With the wildcard `?8` in between matching `h` (0x68), this gives us `why`.

4. **`$k = { 6? 79 5F 64 }`**
   - `6?` matches `h` (0x68). The rest translates to `y_d`. So this gives `hy_d`.

5. **`$a = "\x76\x8d\xec" base64`**
   - The comment helpfully suggests `do3s`. When we take `\x76\x8d\xec` and base64 encode it, it literally becomes the string `do3s`!

6. **`$f = { 73 5? 79 }`**
   - `0x73` is `s`, `5?` matches `_` (0x5f), and `0x79` is `y`. This yields `s_y`.

7. **`$q = "yara"`**
   - This matches the literal string `yara`.

8. **`$b = { 5F 7? ?4 ?4 ?E 6? 5F }`**
   - Matching bytes against the ASCII table: `_` (0x5f), `s` (0x73), `t` (0x74), `4` (0x34), `n` (0x6e), `d` (0x64), `_` (0x5f). This matches the string `_st4nd_`.

9. **`$p = { 64 5f 66 }`**
   - Translates to `d_f`.

10. **`$h = { 6? 30 72 }`**
    - Translates to `f0r`.

11. **`$e = { 72 ?F 74 }`**
    - Translates to `r_t`.

12. **`$n = { 74 68 }`**
    - Translates to `th`.

13. **`$g = "EY\x05E\x0e" xor`**
    - The `xor` modifier tells YARA to check if the string matches this sequence XORed by a single byte. By XORing with the key `0x31`, the sequence becomes `th4t?`.

14. **`$j = /\?{3}\}/`**
    - This is a regex matching exactly three question marks followed by a closing curly brace: `???}`.

### Examining the Conditions

The condition block requires all these string segments to be present, and applies specific constraints on absolute character positions (using 0-based index offset).

```yara
uint32(21) == 0x6E347473 and
uint16(28) == 0x7230 and
uint16be(29) == 0x725F
```

- `uint32(21) == 0x6E347473`: Because it is read as a little-endian 32-bit unsigned integer, the byte sequence starting at index 21 is `0x73`, `0x74`, `0x34`, `0x6E` -> `st4n`.
- `uint16(28) == 0x7230`: Little-endian again. Byte sequence at index 28 is `0x30`, `0x72` -> `0r`.
- `uint16be(29) == 0x725F`: This uses big-endian. Byte sequence at index 29 is `0x72`, `0x5F` -> `r_`.

### Putting It All Together

Let's concatenate all the discovered overlaps into a single consecutive string:

- Starts with `byuctf{wh` (`$m`)
- Appending `y` -> `why` (`$d`)
- Appending `_d` -> `hy_d` (`$k`)
- Appending `o3s` -> `do3s` (`$a`)
- Appending `_y` -> `s_y` (`$f`)
- Appending `ara` -> `yara` (`$q`)
- Appending `_st4nd_` (`$b` and `$l`)
- Appending `f0r` (`$h`, `$p`)
- Appending `_th4t?` (`$e`, `$n`, `$g`, `$o`)
- Appending `??}` (`$j`)

Assembling all of these components yields the complete string that fits inside the 39 character limit required by the regex `$c`:

**Flag:** `byuctf{why_do3s_yara_st4nd_f0r_th4t???}`

When running `yara --no-warnings rule.yar test.txt` with a file containing this exact string, it evaluates successfully and confirms our solution.
