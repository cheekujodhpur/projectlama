def plus_one(x): return x % 7 + 1

def prompter(text, options):
    u_out = f"{text}\n"
    i = 1
    for option in options:
        u_out += f"{i}. {option}\n"
        i = i + 1
    return input(f"{u_out}llama> ")
