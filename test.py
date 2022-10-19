data = 10000.255695

money_str = f"{data:.2f}"
dollar_str = money_str[:-3]
cents_str = money_str[-3:]
data_str = ''
for index, digit in enumerate(dollar_str[::-1], start=1):
    data_str += digit
    if index%3 == 0:
        data_str += ','

new_data = "$" + data_str.strip(',')[::-1] + cents_str

print(new_data)