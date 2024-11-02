def fp8_encode(value):
    """
    실수형 숫자를 FP8 형식으로 변환하는 함수.
    :param value: 변환할 실수(float) 값
    :return: FP8 형식의 8비트 정수값
    """
    # 부호 비트 설정 (0: 양수, 1: 음수)
    sign_bit = 0 if value >= 0 else 1
    value = abs(value)

    # 지수 계산 (비정상적 방법을 사용하여 3비트 지수 범위에 맞춤)
    exponent = 0
    if value >= 1:
        while value >= 2 and exponent < 7:
            value /= 2
            exponent += 1
    else:
        while value < 1 and exponent > -7:
            value *= 2
            exponent -= 1
    exponent += 7  # FP8 지수 바이어스

    # 가수 계산 (4비트로 맞추기 위해 정수형 변환 후 절단)
    mantissa = int((value - 1) * 16) & 0xF

    # FP8 값 생성
    fp8_value = (sign_bit << 7) | (exponent << 4) | mantissa
    return fp8_value


def fp8_decode(fp8_value):
    """
    FP8 형식의 값을 실수로 변환하는 함수.
    :param fp8_value: FP8 형식의 8비트 정수값
    :return: 실수(float) 값
    """
    # 부호, 지수, 가수 추출
    sign_bit = (fp8_value >> 7) & 0x1
    exponent = ((fp8_value >> 4) & 0x7) - 7  # 바이어스 제거
    mantissa = fp8_value & 0xF

    # 실수 값 계산
    value = (1 + mantissa / 16.0) * (2 ** exponent)
    return -value if sign_bit else value


def fp8_add(fp8_a, fp8_b):
    # FP8 형식의 두 수를 실수로 디코딩
    a = fp8_decode(fp8_a)
    b = fp8_decode(fp8_b)
    
    # 실수 덧셈 후 FP8으로 재변환
    result = a + b
    return fp8_encode(result)


def fp8_multiply(fp8_a, fp8_b):
    # FP8 형식의 두 수를 실수로 디코딩
    a = fp8_decode(fp8_a)
    b = fp8_decode(fp8_b)
    
    # 실수 곱셈 후 FP8으로 재변환
    result = a * b
    return fp8_encode(result)


def fp8_matrix_mult(A, B):
    # 2x2 결과 행렬 초기화
    C = [[0, 0], [0, 0]]
    
    for i in range(2):
        for j in range(2):
            sum_fp8 = fp8_encode(0.0)  # 0을 FP8로 초기화
            for k in range(2):
                # FP8 곱셈 및 덧셈 수행
                product_fp8 = fp8_multiply(A[i][k], B[k][j])
                sum_fp8 = fp8_add(sum_fp8, product_fp8)
            C[i][j] = sum_fp8
    return C


# 테스트용 행렬 초기화
A = [[fp8_encode(3.75), fp8_encode(-4.0)],
     [fp8_encode(4.25), fp8_encode(3.5)]]

B = [[fp8_encode(-3.5), fp8_encode(4.1)],
     [fp8_encode(3.75), fp8_encode(-3.6)]]

# FP8 형식의 행렬 곱셈 수행
C = fp8_matrix_mult(A, B)

# 결과 디코딩하여 출력
print("Result matrix C:")
for row in C:
    print([fp8_decode(value) for value in row])
