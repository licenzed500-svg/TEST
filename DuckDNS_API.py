import requests
import time

def get_user_input():
    token = input("Введите ваш токен DuckDNS: ")
    domain = input("Введите ваш домен DuckDNS: ")
    return token, domain

def update_ip(token, domain):
    duckdns_url = f"https://www.duckdns.org/update?domains={domain}&token={token}"
    try:
        response = requests.get(duckdns_url)
        if response.status_code == 200:
            print(f"IP для домена {domain} успешно обновлен.")
        else:
            print(f"Ошибка при обновлении IP: {response.status_code}")
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")

def main():
    token, domain = get_user_input()
    
    while True:
        update_ip(token, domain)
        change_domain = input("Хотите сменить домен? (y/n): ").lower()
        if change_domain == 'y':
            domain = input("Введите новый домен DuckDNS: ")
        time.sleep(300)

if __name__ == "__main__":
    main()
