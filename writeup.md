# Inception CTF Challenge Write-up

This was a fun and interesting challenge! The description mentioned finding a "weird file" that had some problems opening. Here is a step-by-step guide on how we found the flag, written so anyone can follow along.

## Step 1: Identifying the File Type
We started with a file named `inception` that had no extension. To figure out what it was, we used a command called `file` which tells us what kind of data is inside. It turned out to be a **PNG image**.

## Step 2: Extracting Part 1 (The Image Itself)
By adding a `.png` extension to the file, we could view it like a normal picture. Looking at the image (or using text recognition tools like Tesseract OCR), we found the first part of the flag written directly in the picture:
`byuctf{wh4t_`

## Step 3: Digging Deeper (Extracting Hidden Files)
Sometimes, files can hide other files inside them. This is often called "steganography". We used a tool called `binwalk` to scan the image for hidden data. `binwalk` found a few hidden files:
- A Zip archive
- A PDF document

We told `binwalk` to extract all of these hidden files so we could examine them.

## Step 4: Extracting Part 2 (The Zip Archive)
Inside the extracted files, there was a Zip archive containing a file named `data.bin`. Opening this file in a text editor revealed the second part of the flag:
`th3`

## Step 5: Extracting Part 3 (The PDF Document)
Next, we looked at the extracted PDF document data. By reading the raw text of this document file, we found the third and final part of the flag:
`_fr3ak}`

## Conclusion
By putting all three pieces together, we found the complete hidden message!

**The Flag:** `byuctf{wh4t_th3_fr3ak}`
