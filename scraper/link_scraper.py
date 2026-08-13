
# extracts listing URLs from oferty.txt and saves them to linki.txt
def save_links():
    with open('data/oferty.txt', 'r') as readfile, open('data/linki.txt', 'w') as savefile:
        lines = readfile.readlines()
        count = 1
        for line in lines:
            line = line.strip()
            line = line.split("\n")
            if 'Link: ' in line[0]:
                try:
                    savefile.write(line[0] + "\n")
                    count += 1
                except FileNotFoundError:
                    print(FileNotFoundError)
        print(f"{count} links was saved")      

