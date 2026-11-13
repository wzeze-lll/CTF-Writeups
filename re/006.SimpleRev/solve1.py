"""Same inverse as the user's solve2.py, with a forward check."""
text = "killshadow"
key = "adsfkndcls"
answer = []
for index, expected in enumerate(text):
    matches = [value for value in range(ord("A"), ord("z") + 1)
               if (value - 39 - ord(key[index % len(key)]) + 97) % 26 + 97 == ord(expected)]
    assert matches
    answer.append(matches[0])
forward = "".join(chr((value - 39 - ord(key[index % len(key)]) + 97) % 26 + 97)
                  for index, value in enumerate(answer))
assert forward == text
print(bytes(answer).decode("ascii"))
