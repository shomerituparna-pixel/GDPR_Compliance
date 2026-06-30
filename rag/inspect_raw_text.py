with open(
    "data/gdpr.txt",
    "r",
    encoding="utf-8"
) as f:

    text = f.read()

index = text.find("CHAPTER I")

print(text[index:index+5000])