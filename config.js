// validateConfig 함수 정의
window.validateConfig = function() {
    const errors = [];
    
    if (!window.CONFIG) {
        errors.push('CONFIG 객체가 정의되지 않았습니다.');
        return errors;
    }
    
    if (!window.CONFIG.CLIENT_ID) {
        errors.push('네이버 지도 CLIENT_ID가 설정되지 않았습니다.');
    }
    if (!window.CONFIG.CLIENT_SECRET) {
        errors.push('네이버 지도 CLIENT_SECRET(시크릿값)이 설정되지 않았습니다.');
    }
    if (!window.CONFIG.SUPABASE || !window.CONFIG.SUPABASE.URL || !window.CONFIG.SUPABASE.ANON_KEY) {
        errors.push('슈퍼베이스 설정이 완전하지 않습니다.');
    }
    if (!window.CONFIG.NAVER_MAP || !window.CONFIG.NAVER_MAP.CENTER) {
        errors.push('네이버 지도 설정이 완전하지 않습니다.');
    }
    return errors;
};
