def setup():
    print(10*'=' + ' Notas SIGAA setup ' + 10*'=')

    username = str(input('SIGAA username: '))
    password = str(input('SIGAA password: '))
    webdriver_path = str(input('Webdriver path (always use / and, if in the same dir, use ./): '))
    csv_output = str(input('CSV output path (always use / and, if in the same dir, use ./): '))
    g_credentials_path = str(input(
        'Google Cloud credentials.json path (always use / and, if in the same dir, use ./): '))
    g_sheet = str(input("Google Sheet's sheet name: "))
    downloads_path = str(input('Downloads folder path (always use / and, if in the same dir, use ./): '))

    with open('./.env', 'w') as file:
        file.write(f"""MY_USERNAME="{username}"
MY_PASSWORD="{password}"
DRIVER_PATH="{webdriver_path}"
CSV_OUTPUT="{csv_output}"
G_CREDENTIALS="{g_credentials_path}"
G_SHEET="{g_sheet}"
DOWNLOADS_PATH="{downloads_path}"
""")


if __name__ == '__main__':
    setup()
