# IO
a = list(map(int, open("input.txt").read().replace("\n", "")))
width, height = 25,6
chunk_len = (width*height)
chunk_number = len(a) // chunk_len
chunks = [a[(i*chunk_len):(i+1)*chunk_len] for i in range(chunk_number)]

# 1st 
b = min(chunks, key=lambda c: c.count(0))
print(b.count(1)*b.count(2))

# 2nd
s = ""
for y in range(height):
    for x in range(width):
        for layer in chunks:
            pixel = layer[x+y*width]
            if pixel == 0:
                s+=" "
                break
            elif pixel == 1:
                s+="*"
                break
    s+="\n"
print(s)