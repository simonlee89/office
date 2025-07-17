# 네이버 지도 연동 시스템 사용 가이드

## 📋 개요
이 시스템은 네이버 지도 API와 슈퍼베이스를 연동하여 부동산 매물 정보를 지도에 표시하는 웹 애플리케이션입니다.

## 🛠️ 시스템 구성

### 파일 구조
```
프로젝트 폴더/
├── create_naver_map_table.py    # 슈퍼베이스 테이블 생성 스크립트
├── config.js                    # API 설정 파일
├── naver_map_app.html          # 메인 웹 애플리케이션
├── start_server.py             # 웹 서버 실행 스크립트
└── NAVER_MAP_GUIDE.md          # 이 가이드 문서
```

### 주요 기능
- 슈퍼베이스 '네이버지도실험' 테이블에서 매물 데이터 로드
- 주소를 지도 좌표로 변환하여 마커 표시
- 마커 클릭 시 매물 정보 팝업 표시
- 정보창에서 외부 링크 열기 기능
- 매물 목록에서 지도 위치로 이동

## 🚀 설치 및 설정

### 1. 네이버 지도 API 설정

1. **네이버 클라우드 플랫폼 접속**
   - https://console.ncloud.com 접속
   - 계정 로그인 또는 회원가입

2. **지도 API 서비스 신청**
   - AI·Application Service > Maps 선택
   - Web Dynamic Map 선택
   - 애플리케이션 등록

3. **클라이언트 ID 발급**
   - 서비스 URL: `http://localhost:8000` 입력
   - 클라이언트 ID 복사

4. **config.js 파일 수정**
   ```javascript
   NAVER_MAP: {
       CLIENT_ID: '여기에_발급받은_클라이언트_ID_입력',
       // ...
   }
   ```

### 2. 슈퍼베이스 설정

1. **슈퍼베이스 프로젝트 확인**
   - https://supabase.com/dashboard 접속
   - 기존 프로젝트 URL과 API 키 확인

2. **테이블 생성**
   ```bash
   python create_naver_map_table.py
   ```

3. **config.js 파일 확인**
   - 슈퍼베이스 URL과 ANON_KEY가 올바른지 확인

### 3. 웹 서버 실행

```bash
python start_server.py
```

## 📊 데이터베이스 구조

### '네이버지도실험' 테이블 스키마
| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| id | BIGSERIAL | 기본키 (자동 증가) |
| 매물명 | TEXT | 매물 이름 |
| 주소 | TEXT | 매물 주소 (지도 마커 위치) |
| 링크 | TEXT | 매물 상세 페이지 URL |
| 가격 | TEXT | 매물 가격 정보 |
| 면적 | TEXT | 매물 면적 정보 |
| 상세정보 | TEXT | 매물 상세 설명 |
| created_at | TIMESTAMPTZ | 생성 시간 |

### 테스트 데이터 예시
```sql
INSERT INTO "네이버지도실험" (매물명, 주소, 링크, 가격, 면적, 상세정보) VALUES
('강남역 인근 사무실', '서울특별시 강남구 강남대로 396', 'https://land.naver.com/article/info/32424230', '월세 500/50', '33㎡', '강남역 도보 5분, 신축 건물');
```

## 🖥️ 사용 방법

### 1. 시스템 시작
1. `python start_server.py` 실행
2. 브라우저에서 자동으로 `http://localhost:8000/naver_map_app.html` 열림

### 2. 웹 인터페이스 사용
- **좌측 사이드바**: 매물 목록 표시
- **우측 지도**: 매물 위치 마커 표시
- **매물 클릭**: 해당 위치로 지도 이동
- **마커 클릭**: 매물 정보 팝업 표시
- **링크 열기**: 정보창에서 외부 링크 접속

### 3. 데이터 새로고침
- 좌측 상단 "🔄 데이터 새로고침" 버튼 클릭
- 슈퍼베이스에서 최신 데이터 로드

## 🔧 커스터마이징

### 지도 설정 변경
```javascript
// config.js
NAVER_MAP: {
    CENTER: {
        lat: 37.5665,  // 초기 지도 중심 위도
        lng: 126.9780  // 초기 지도 중심 경도
    },
    ZOOM: 13  // 초기 줌 레벨
}
```

### 마커 스타일 변경
```javascript
// naver_map_app.html의 createMarker 함수에서
icon: {
    content: `<div style="background: #ff4444; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: bold; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);">${index + 1}</div>`,
    size: new naver.maps.Size(30, 30),
    anchor: new naver.maps.Point(15, 15)
}
```

### 정보창 내용 변경
```javascript
// naver_map_app.html의 createInfoWindowContent 함수 수정
function createInfoWindowContent(property) {
    return `
        <div style="padding: 15px;">
            <h3>${property.매물명}</h3>
            <p>📍 ${property.주소}</p>
            <p>💰 ${property.가격}</p>
            // 추가 정보 표시
        </div>
    `;
}
```

## 🐛 문제 해결

### 일반적인 문제

1. **지도가 표시되지 않는 경우**
   - 네이버 지도 API 클라이언트 ID 확인
   - 브라우저 개발자 도구에서 오류 메시지 확인
   - 네트워크 연결 상태 확인

2. **마커가 표시되지 않는 경우**
   - 슈퍼베이스 연결 상태 확인
   - '네이버지도실험' 테이블 존재 여부 확인
   - 테이블에 데이터가 있는지 확인

3. **주소 변환 실패**
   - 주소 형식이 올바른지 확인
   - 네이버 지도 API의 Geocoding 서비스 상태 확인

### 오류 메시지별 해결 방법

**"설정 오류: 네이버 지도 API 클라이언트 ID를 설정해주세요"**
- `config.js`에서 `CLIENT_ID` 값을 실제 발급받은 ID로 변경

**"데이터 로드 중 오류가 발생했습니다"**
- 슈퍼베이스 URL과 API 키 확인
- 네트워크 연결 상태 확인
- 테이블 존재 여부 확인

**"포트 8000가 이미 사용 중입니다"**
- 다른 프로그램이 포트 8000을 사용하고 있음
- 해당 프로그램 종료 후 다시 시도

## 📱 모바일 지원

- 반응형 디자인으로 모바일 기기에서도 사용 가능
- 모바일에서는 사이드바가 상단으로 이동
- 터치 제스처로 지도 조작 가능

## 🔒 보안 주의사항

1. **API 키 보안**
   - 클라이언트 측에서 사용되는 API 키는 브라우저에서 확인 가능
   - 네이버 클라우드 플랫폼에서 도메인 제한 설정 권장

2. **슈퍼베이스 보안**
   - ANON KEY는 읽기 전용 권한만 부여
   - Row Level Security (RLS) 설정 권장

3. **서버 보안**
   - 개발 환경에서만 사용
   - 운영 환경에서는 HTTPS 사용 권장

## 🆕 업데이트 및 확장

### 새로운 매물 추가
1. 슈퍼베이스 대시보드에서 직접 추가
2. 또는 별도의 관리 도구 개발

### 기능 확장 아이디어
- 매물 필터링 기능
- 즐겨찾기 기능
- 매물 비교 기능
- 길찾기 연동
- 주변 시설 정보 표시

## 📞 지원

문제가 발생하거나 추가 기능이 필요한 경우:
1. 브라우저 개발자 도구에서 오류 메시지 확인
2. 네이버 클라우드 플랫폼 지원 센터 문의
3. 슈퍼베이스 공식 문서 참조

---

**📝 참고 문서**
- [네이버 지도 API 문서](https://navermaps.github.io/maps.js.ncp/)
- [슈퍼베이스 JavaScript 가이드](https://supabase.com/docs/reference/javascript)
- [네이버 클라우드 플랫폼 콘솔](https://console.ncloud.com) 