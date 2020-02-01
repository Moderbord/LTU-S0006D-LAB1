__LOG = "./logs/output.txt"


def log(msg):
    with open(__LOG, "a") as f:
        f.write(str(msg) + "\n")
    
