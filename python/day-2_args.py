def show_information(*args,**kwargs):
    print("these are positional arguments:", args)
    print("these are keyword arguments:", kwargs)

result = show_information(2,4,5,5,'surenda',name="surendra")


def add_numbers(*args):
    return sum(args)

result = add_numbers(22,4)
print(result)


def print_user_info(**kwargs):
    for key,value in kwargs.items():
        print(f"{key}: {value}")
    
print_user_info(name="surendra", id=1)