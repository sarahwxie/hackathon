

def sentiment(text):
    posnum = 0
    negnum = 0
    neunum = 0
    with open("negative-words.txt", "r") as f:
        neg = set(f.read().split("\n"))
    with open("positive-words.txt", "r") as f:
        pos = set(f.read().split("\n"))
    for i in text.split(" "):
        if i in neg: negnum+=1
        elif i in pos: posnum+=1
        else: neunum+=1
    print(posnum, negnum, neunum)


sentiment("My entire world is crashing. My best friend left me. I feel so alone.")
