# 공실클럽 사무실 월세 크롤러 (수퍼베이스 버전)

공실클럽 웹사이트에서 강남구 사무실 월세 정보를 크롤링하여 수퍼베이스 데이터베이스에 저장하는 프로그램입니다.

## 주요 변경사항

- ✅ **구글시트 → 수퍼베이스 변경**: 더 안정적이고 확장 가능한 데이터베이스 사용
- ✅ **환경변수 관리**: 민감한 정보를 환경변수로 관리
- ✅ **중복 데이터 방지**: 동일한 매물 정보 중복 저장 방지
- ✅ **백업 기능**: 수퍼베이스 연결 실패 시 CSV 파일로 백업 저장

## 설치 및 설정

### 1. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 환경변수 설정

`env_example.txt` 파일을 참고하여 `.env` 파일을 생성하고 다음 정보를 입력하세요:

```env
# 수퍼베이스 설정
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key

# 로그인 정보
USER_ID=your_user_id
USER_PW=your_user_password
```

### 3. 수퍼베이스 테이블 생성

수퍼베이스 대시보드에서 다음 SQL을 실행하여 테이블을 생성하세요:

```sql
CREATE TABLE gangnam_office_monthly (
    id SERIAL PRIMARY KEY,
    page INTEGER,
    label TEXT,
    gu TEXT,
    dong_beonji TEXT,
    building_etc TEXT,
    deposit TEXT,
    monthly_rent TEXT,
    management_fee TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 중복 방지를 위한 인덱스 생성
CREATE INDEX idx_unique_property ON gangnam_office_monthly (gu, dong_beonji, building_etc, monthly_rent);
```

## 사용법

### 수퍼베이스 버전 실행

```bash
python supabase_office_crawler.py
```

### 기존 구글시트 버전 실행

```bash
python "25.4.10[강남월세][사무실][공클] .py"
```

## 파일 구조

```
공실클럽사무실월세/
├── supabase_office_crawler.py     # 수퍼베이스 버전 크롤러 (새로 추가)
├── requirements.txt               # 필요한 패키지 목록
├── env_example.txt               # 환경변수 예시 파일
├── README.md                     # 프로젝트 설명서
├── 25.4.10[강남월세][사무실][공클] .py          # 기존 구글시트 버전
├── 25.4.10[강남월세][사무실][공클] 누적.py      # 기존 구글시트 버전 (누적)
├── 25.4.10[송파월세][사무실][공클]  copy.py    # 송파 버전
└── 25.4.10[송파월세][사무실][공클] 누적 .py    # 송파 버전 (누적)
```

## 주요 기능

1. **자동 로그인**: 공실클럽 웹사이트에 자동으로 로그인
2. **검색 조건 설정**: 강남구 사무실 월세 조건으로 자동 설정
3. **데이터 수집**: 모든 페이지의 매물 정보를 자동으로 수집
4. **데이터 저장**: 수퍼베이스 데이터베이스에 자동 저장
5. **중복 방지**: 이미 저장된 매물 정보는 중복 저장하지 않음
6. **백업 기능**: 수퍼베이스 연결 실패 시 CSV 파일로 백업

## 수집되는 데이터

- 페이지 번호
- 매물 라벨 (예: "월세")
- 구 (예: "강남구")
- 동과 번지 정보
- 건물명 등 추가 정보
- 전세 금액
- 월세 금액 (보증금/월세)
- 관리비
- 수집 날짜/시간

## 주의사항

- Edge 브라우저가 설치되어 있어야 합니다.
- 수퍼베이스 프로젝트 URL과 API 키가 필요합니다.
- 공실클럽 로그인 정보가 필요합니다.
- 웹사이트 구조 변경 시 코드 수정이 필요할 수 있습니다.

## 문제 해결

### 수퍼베이스 연결 오류
- `.env` 파일의 URL과 KEY가 올바른지 확인
- 수퍼베이스 프로젝트가 활성화되어 있는지 확인

### 로그인 실패
- `.env` 파일의 사용자 ID와 비밀번호 확인
- 공실클럽 웹사이트 접속 상태 확인

### 크롤링 실패
- 인터넷 연결 상태 확인
- 웹사이트 구조 변경 여부 확인 

## 환경설정 파일 사용법

1. `config.example.js` 파일을 복사해서 같은 위치에 `config.js`로 이름을 바꿉니다.
2. 각 항목에 실제 네이버 지도 API Client ID, Supabase URL, Supabase ANON KEY 값을 입력합니다.
3. `config.js` 파일은 절대 git에 올리지 마세요! 