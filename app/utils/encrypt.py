from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 암호화 설정
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# 입력된 평문과 암호화 비밀번호 비교
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)