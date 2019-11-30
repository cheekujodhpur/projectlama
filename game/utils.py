def plus_one(x): return x % 7 + 1

def prompter(text, options, validate=False):
    u_out = f"{text}\n"
    i = 1
    for option in options:
        u_out += f"{i}. {option}\n"
        i = i + 1
    response = input(f"{u_out}llama> ")

    # Basic validation for being an integer
    if not validate:
        return response
    else:
        if not response.isdigit() or int(response)-1 not in range(len(options)):
            return prompter(text,options,validate=validate)
        else:
            return int(response)
