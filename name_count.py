

with open("links_file.txt", "r") as file:
    lines = file.readlines()
    clip_label = {}
    for line in lines:
        if line.strip() == "":
            continue

        elif line.startswith("https://"):
            continue

        else:
            line = line.strip()
            line = line.split(',')
            name = line[0]
            name = name.split(" ")[0].strip()
            if name not in clip_label:
                clip_label[name] = 1
            else:
                clip_label[name] += 1
    print(clip_label)
            
        
