# GenZPy Keyword Guide

This is the official documentation for all keywords and syntax used in the GenZPy language.

---

### 🧾 Variables & Printing

**`vibe check <name> = <value>`**
* **Meaning**: Declares a new variable.
* **Usage**: Used to store data like numbers, strings, or lists.
* **Example**:
    ```
    vibe check my_rizz = 100
    vibe check user_name = 'The Main Character'
    ```

**`bro print <value>`**
* **Meaning**: Prints a value to the console.
* **Usage**: Used to display the value of a variable or a direct value.
* **Example**:
    ```
    vibe check message = 'Wassup fam'
    bro print message
    bro print 100
    ```

---

### 🧮 Conditionals

**`fr if <condition>`**
* **Meaning**: "For real, if..." - Starts an `if` block. The code inside only runs if the condition is true (`facts`).

**`mid fr <condition>`**
* **Meaning**: "It's mid, for real..." - The `else if` block. Runs if the previous `if`/`mid fr` was false, but this new condition is true.

**`lowkey`**
* **Meaning**: "Lowkey..." - The `else` block. Runs if all preceding `if` and `mid fr` conditions were false.

* **Example**:
    ```
    vibe check score = 75
    fr if score > 90
        bro print 'Top G'
    mid fr score > 50
        bro print 'Mid fr, but you passed'
    lowkey
        bro print 'Its giving L'
    fin
    ```

---

### 🔄 Control Flow (Loops)

**`no cap i from <start> to <end>`**
* **Meaning**: "No cap..." - A `for` loop that iterates a set number of times. The loop variable `i` will go from `start` up to (but not including) `end`.
* **Example**:
    ```
    no cap i from 0 to 5
        bro print i
    fin
    ```

**`keep it 100 <condition>`**
* **Meaning**: "Keep it 100..." - A `while` loop. The code inside will keep running as long as the condition is true.
* **Example**:
    ```
    vibe check x = 0
    keep it 100 x < 3
        bro print x
        vibe check x = x + 1
    fin
    ```

**`yeet`**
* **Meaning**: The `break` keyword. Immediately exits the current loop.
* **Example**:
    ```
    no cap i from 0 to 10
        fr if i == 3
            yeet
        fin
        bro print i
    fin
    # This will only print 0, 1, 2
    ```

**`bet`**
* **Meaning**: The `continue` keyword. Skips the rest of the current loop iteration and goes to the next one.
* **Example**:
    ```
    no cap i from 0 to 5
        fr if i == 2
            bet
        fin
        bro print i
    fin
    # This will print 0, 1, 3, 4 (it skips 2)
    ```

---

### ✨ Functions

**`glow_up <name>(<params>)`**
* **Meaning**: Defines a new function. This is how you create reusable blocks of code.
* **Usage**: `params` are optional variable names for the data you want to pass into the function.

**`spill <value>`**
* **Meaning**: The `return` keyword. Used inside a function to send a value back out.

* **Example**:
    ```
    glow_up add(a, b)
        spill a + b
    fin

    vibe check result = add(10, 5)
    bro print result # Prints 15
    ```

---

### 📦 Data Structures & Built-ins

**`squad[...]`**
* **Meaning**: A `list`. Used to store a collection of items in order.
* **Example**:
    ```
    vibe check my_squad = squad[1, 'facts', 100]
    ```

**`spill_tea()`**
* **Meaning**: A built-in function to get input from the user.
* **Example**:
    ```
    bro print 'Spill the tea (whats your name?)'
    vibe check user_name = spill_tea()
    bro print 'Wassup ' + user_name
    ```

**`sneaky_link(<list>)`**
* **Meaning**: A built-in function that gets the length of a `squad` (list).
* **Example**:
    ```
    vibe check my_squad = squad[1, 2, 3]
    bro print sneaky_link(my_squad) # Prints 3
    ```

---

### ⚖️ Logic & Values

* **`facts`**: Represents `True`.
* **`cap`**: Represents `False`.
* **`ghosted`**: Represents `None` or a null value.
* **`same_vibes`**: The `==` operator (equals).
* **`bad_vibes`**: The `!=` operator (not equals).
* **`plus_one`**, **`take_L`**, **`flex`**, **`split`**: Slang for `+`, `-`, `*`, `/`. (Note: Standard operators also work).

---

**`fin`**
* **Meaning**: Marks the end of a code block (like `end` or Python indentation block).
* **Usage**: Used after `if`, `loops`, and `functions`.

