import requests
import hashlib
import getpass


def request_pwned_data(query):
    url = 'https://api.pwnedpasswords.com/range/' + query
    req = requests.get(url)
    # print(req.encoding)
    if req.status_code != 200:
        raise RuntimeError("Sorry please enter the correct url")
    return req


def pwned_api_check(password_to_check):
    # checking if the pasword exists in the pwned passwords
    hashed = hashlib.sha1(password_to_check.encode("utf-8"))
    sha1pass = hashed.hexdigest().upper()
    head, tail = sha1pass[:5], sha1pass[5:]
    response = request_pwned_data(head)
    return no_of_breaches(response.text, tail)


def no_of_breaches(response_in_str, tail):
    # creating a generator object
    response_object = (line.split(":") for line in response_in_str.splitlines())
    for h, no in response_object:
        if h == tail:
            return no
    return 0


def main():
    while True:
        try:
            prompt=getpass.getpass("Password: ")
            count = pwned_api_check(prompt)
            if count:
                print(f"Your password has been found in {count} data breaches.You should change your password")
            else:
                print(f'Your password NOT found!!')
        except KeyboardInterrupt:
            break



if __name__=="__main__":
    main()
