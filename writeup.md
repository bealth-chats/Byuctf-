# Chromatic Challenge Write-up

## The Goal
The objective of this challenge is to find a hidden flag within a video file named `chromatic.mp4`. The description given to us is simply: "Red".

## The Solution Process

### Step 1: Examine the Video
If you watch the `chromatic.mp4` video, it looks like a series of solid red frames that might flicker slightly.

Every pixel on your screen is made up of three primary colors: **Red, Green, and Blue** (often called **RGB**). By mixing these three colors in different amounts, your computer can display any color imaginable.

The hint "Red" is a clue that we should look specifically at the "red" part of the video's colors.

### Step 2: Look Closer at the Colors
Since it's difficult to see exactly what's changing with the naked eye, we can use a small computer program to look at the exact color numbers for each frame of the video.

When we inspect the frames, we find that:
* The amount of **Green** is always exactly `0`.
* The amount of **Blue** is always exactly `0`.
* But the amount of **Red** changes from frame to frame!

### Step 3: Extract the Hidden Numbers
The video plays at 30 frames per second. If we look at the red color value exactly once every second (which means looking at frame 0, frame 30, frame 60, and so on), we get a list of numbers.

The first few numbers look like this: `98, 121, 117, 99, 116, 102, 123...`

### Step 4: Translate the Numbers
Computers use a standard system called **ASCII** (American Standard Code for Information Interchange) to turn numbers into text. Every letter, number, and symbol on your keyboard corresponds to a specific number.

If we take the numbers we found in the red color and translate them using the ASCII system:
* `98` translates to the letter `b`
* `121` translates to the letter `y`
* `117` translates to the letter `u`
* `99` translates to the letter `c`
* `116` translates to the letter `t`
* `102` translates to the letter `f`
* `123` translates to the symbol `{`

Following this pattern for all the numbers we extracted gives us the complete flag!

## The Flag
`byuctf{It's_all_red_I_really_thought_it_would_be_more}`