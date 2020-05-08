def human_file_size(num, suffix="B"):
    """Readable file size
    Based on this snippet https://gist.github.com/cbwar/d2dfbc19b140bd599daccbe0fe925597
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, "Yi", suffix)

if __name__ == '__main__':
    print(human_file_size(214300124))