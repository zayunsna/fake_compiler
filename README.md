# fake_compiler
> A drowsy weekday afternoon at 3 PM, you might need this. Prepare your terminal and this code. With a single execution, you can take a mental break during work without your boss noticing!

A very lazy holiday with nothing to do.
There was nothing interesting on YouTube, and I was too lazy to go out. On a day like that, I coded something while giggling to myself, thinking it would be fun.
I have taken my office time-wasting skills to a new level.

The name is 'Fake_Compiler'
The purpose is very simple: 'To pretend to be compiling something grand.'

If you look at the source code, it’s just child’s play coding.
Anyone can do it, but it’s the kind of task that no one would bother to do.
A holiday with nothing to do made me do it.

### The implemented features are as follows:

- Output the g++ compile printing format with plausible words filled in randomly.
- Output dependencies (the length of the path and words are also random).
- Colorful progress display.
- 0.1% chance of an error occurring, followed by a Make error message.
- If completed without errors, output the compile result and completion message.

[On Success]
![[./images/on_success.png]]

[On Failure]
![[./images/on_failure.png]]

The code is implemented in Python, but what gets printed is a C++ compilation, which is the funny part.
I tried to make it look as plausible as possible by adding everything I could remember.

With the compile error implemented, you can monitor the fake compiling with a bit of tension. It’s a meaningless fake compile screen, but if an error occurs, it’s inexplicably annoying. On the other hand, if it compiles without errors, it feels oddly satisfying yet uneasy.

It feels like you should be debugging, but there’s nothing to debug. :) 

With this, during those ambiguous weekday afternoons when you have a lot of work but your brain isn’t working and you don’t want to do anything, you can now slack off with some confidence.

> The number of output lines was initially an input value but was fixed later. Adjust num_files in the main code to slack off as much as you want. (The default is 119, reflecting the sentiment of "Please save me, I want to go home.")

> You can only slack off if there are no errors. You can reduce the error probability or set it to 0 with error_probability to proceed without errors. (The default is 0.01 [1%])

Any other ideas to increase realism are welcome!

You can clone the code from the GitHub repo below and run it with python3!

(The plausible words were collected with the help of the great GPT-4.)
