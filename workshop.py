from flask import Flask, request, redirect, session
import os
import random

app = Flask(__name__)
app.env = 'development'
app.debug = True

# 소수찾기 함수
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

# 주민등록번호 검증 함수
def verify_jumin(serial):
    serial_list = []
    for i in serial:
        if i != '-':
            serial_list.append(int(i))
    
    sum_serial = serial_list[0] * 2 + serial_list[1] * 3 + serial_list[2] * 4 + serial_list[3] * 5 + serial_list[4] * 6 + serial_list[5] * 7 + serial_list[6] * 8 + serial_list[7] * 9 + serial_list[8] * 2 + serial_list[9] * 3 + serial_list[10] * 4 + serial_list[11] * 5 # 검증합계

    sum_serial_na = sum_serial % 11 # 검증나머지
    valid_num = 11 - sum_serial_na # 검증코드

    if serial_list[12] == valid_num: # 13째자리와 비교
        return True
    else:
        return False
    

    #for j in serial_list:
    #    count = 1
    #    sum_j = sum_j + j * (count+1)


    
    return serial_list

@app.route('/')
def index():
    return "work"

# 1번문제(구구단 출력)
@app.route('/gugu/<num>')
def gugu(num):

    if not num.isnumeric():
            return "not number"

    if int(num) < 2 or int(num) > 9:
        return "2~9까지 숫자만 입력해 주세요."

    gugus = []
    
    for i in range(1, 10):
        s = num + " * " + str(i) + " = " + (str(int(num)*i))
        gugus.append(s)

    
    return '<br>'.join(gugus)


#2번문제(N입력 받은 후 1~N까지 중 소수만 출력)
@app.route('/prime/')
def prime():

    n = request.args.get('num')
    num_n = int(n)

    primes = []
    
    # 사이값 소수 찾기
    for i in range(num_n + 1):
        if is_prime(i):
            primes.append(str(i))  

    #return primes
    return '<br>'.join(primes)

#3번문제(N입력 받은 후 N의 약수 구하기)
@app.route('/common_factor/')
def common_factor():

    n = request.args.get('num')
    num_n = int(n)

    common_factors = []
    
    # 약수 구하기
    for i in range(1, num_n + 1):
        if num_n % i ==0:
            common_factors.append(str(i))  

    #return common_factors
    return '<br>'.join(common_factors)


#4번문제(N,M 입력 받은 후 최대공약수/최소공배수 구하기)
@app.route('/commons/')
def commons():

    a = request.args.get('num1')
    b = request.args.get('num2')
    num_a = int(a)
    num_b = int(b)
    
    # 최대공약수/최소공배수 구하기
    num_a2 = num_a
    num_b2 = num_b

    if num_b2 > num_a2:
        tmp = num_a2
        num_a2 = num_b2
        num_b2 = tmp
    while num_b2 > 0:
        num_c2 = num_b2
        num_b2 = num_a2 % num_b2
        num_a2 = num_c2

    mx = "최대공약수 = " + str(num_a2)
    mn = "최소공배수 = " + str(round(num_a * num_b / num_a2))
    
    return str(mx + ' / ' + mn)


#5번문제(사용자로부터 숫자를 N을 입력받아, 1, 5, 10, 25, 50의 숫자를 이용하여 최소 갯수로 N을 표현)
@app.route('/coins/')
def coins():

    n = request.args.get('num')
    num_n = int(n)
    #list_n = [50, 25, 10, 5, 1]

    coins = {}
    
    # 몫 구하기

    m_a50 = num_n // 50 # 50으로 나눈 몫
    s_a50 = num_n - m_a50 * 50 # 50으로 나눈 나머지
    coins['50'] = str(m_a50)

    m_a25 = s_a50 // 25 # 25으로 나눈 몫
    s_a25 = s_a50 - m_a25 * 25 # 25으로 나눈 나머지
    coins['25'] = str(m_a25)

    m_a10 = s_a25 // 10 # 10으로 나눈 몫
    s_a10 = s_a25 - m_a10 * 10 # 10으로 나눈 나머지
    coins['10'] = str(m_a10)

    m_a5 = s_a10 // 5 # 5으로 나눈 몫
    s_a5 = s_a10 - m_a5 * 5 # 5으로 나눈 나머지
    coins['5'] = str(m_a5)

    m_a1 = s_a5  # 1로 나눈 몫
    coins['1'] = str(m_a1)

    #s = n + " = " + '50' + ' * ' + str(m_a50) + ' + 25' + ' * ' + str(m_a25) + ' + 10' + ' * ' + str(m_a10) + ' + 5' + ' * ' + str(m_a5) + ' +1' + ' * ' + str(m_a1) + ' => 총' + str(m_a50 + m_a25 + m_a10 + m_a5 + m_a1) + '개'
    
    r1 = ''
    r2 = ''
    sum_v = 0
    for key, value in coins.items():
        #print(key, value)
        #print(type(value))
        if value != '0':
            r1 = key + " * " + value
            sum_v = sum_v + int(value)
            r2 = r2 + r1 + " + "
        r3 = r2[:-2]

        

    # for i in list_n:
    #     if num_n % i ==0:
    #         common_factors.append(str(i))  

    return str(n) + ' = ' + str(r3) + " => 총 " + str(sum_v) + "개"
    #return str(coins)

#6번문제(주민등록번호)
@app.route('/jumin', methods=['get', 'post'])
def jumin():
    with open('./WEB_W/jumin.html', 'r', encoding='utf8') as f:
        template = f.read()

    ss = ''
    result = ''

    if request.method == 'POST':
        ss = request.form.get('text')

        if len(ss) != 14:
            return "주민번호 13자리를 - 포함하여 넣어주세요"


        result = str(verify_jumin(ss))
        #print(result)

    return template.format(result=result)

# 7번문제(원주율))
@app.route('/pi/<num>')
def pi(num):
    
    
    count = 0
    for i in range(int(num)):
        x = random.random()
        y = random.random()
        if (x * x + y * y < 1):
            count = count + 1
    
    a = 4 * count / int(num)

    return str(a)


app.run(port=5002)