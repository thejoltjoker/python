def main(question):
    while "the answer is invalid":
        reply = str(input(question + ' (y/n): ')).lower().strip()
        print(reply)
        if reply[:1] in ['yes', 'y']:
            return True
        if reply[:1] in ['no', 'n']:
            return False
        else:
            break

    main("Please answer yes or no")


if __name__ == "__main__":
    print(main("Is this a question?"))
