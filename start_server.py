#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
네이버 지도 웹 애플리케이션 서버 실행 스크립트
"""

import os
import sys
import webbrowser
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse
# dotenv 추가
from dotenv import load_dotenv

class CORSRequestHandler(SimpleHTTPRequestHandler):
    """CORS 헤더를 추가한 HTTP 요청 핸들러"""
    
    def end_headers(self):
        # CORS 헤더 추가
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        # OPTIONS 요청 처리 (CORS preflight)
        self.send_response(200)
        self.end_headers()
    
    def log_message(self, format, *args):
        # 로그 메시지 한글 지원
        try:
            message = format % args
            sys.stdout.write(f"[{self.log_date_time_string()}] {message}\n")
        except:
            pass

def check_config_file():
    """config.js 파일 확인"""
    if not os.path.exists('config.js'):
        print("❌ config.js 파일이 없습니다.")
        print("💡 config.js 파일을 생성하고 네이버 지도 API 클라이언트 ID를 설정해주세요.")
        return False
    
    try:
        with open('config.js', 'r', encoding='utf-8') as f:
            content = f.read()
            # CLIENT_ID가 실제 값으로 설정되어 있는지 확인
            import re
            match = re.search(r"CLIENT_ID\s*:\s*['\"]([a-zA-Z0-9]+)['\"]", content)
            if not match or match.group(1) in ['YOUR_NAVER_MAP_CLIENT_ID', '', None]:
                print("⚠️ 네이버 지도 API 클라이언트 ID가 설정되지 않았습니다.")
                print("💡 config.js 파일에서 CLIENT_ID를 실제 값으로 변경해주세요.")
                print("📖 네이버 클라우드 플랫폼에서 지도 API 클라이언트 ID를 발급받으세요.")
                return False
    except Exception as e:
        print(f"❌ config.js 파일 읽기 오류: {e}")
        return False
    
    return True

def check_html_file():
    """HTML 파일 확인"""
    if not os.path.exists('index.html'):
        print("❌ index.html 파일이 없습니다.")
        return False
    return True

def open_browser(url, delay=2):
    """브라우저 열기 (딜레이 후)"""
    def open_url():
        time.sleep(delay)
        try:
            webbrowser.open(url)
            print(f"🌐 브라우저에서 {url} 열기 완료")
        except Exception as e:
            print(f"❌ 브라우저 열기 실패: {e}")
            print(f"💡 수동으로 {url} 에 접속해주세요.")
    
    thread = threading.Thread(target=open_url)
    thread.daemon = True
    thread.start()

def generate_config_js():
    print("config.js 생성 시도", flush=True)
    try:
        if os.path.exists('config.js'):
            print("config.js already exists", flush=True)
            return

        load_dotenv()
        client_id = os.getenv('NAVER_CLIENT_ID', '')
        client_secret = os.getenv('NAVER_MAP_CLIENT_SECRET', '')
        supabase_url = os.getenv('SUPABASE_URL', '')
        supabase_anon_key = os.getenv('SUPABASE_ANON_KEY', '')

        config_content = f"""
window.CONFIG = {{
    CLIENT_ID: '{client_id}',
    CLIENT_SECRET: '{client_secret}',
    SUPABASE: {{
        URL: '{supabase_url}',
        ANON_KEY: '{supabase_anon_key}'
    }}
}};
"""
        with open('config.js', 'w', encoding='utf-8') as f:
            f.write(config_content)
        print("config.js 생성 완료", flush=True)
    except Exception as e:
        print(f"config.js 생성 실패: {e}", flush=True)

def main():
    print("서버 시작", flush=True)
    print("🗺️ 네이버 지도 웹 애플리케이션 서버 시작")
    print("=" * 50)
    
    # config.js 자동 생성 활성화
    generate_config_js()
    
    # 파일 존재 확인
    if not check_html_file():
        print("❌ 필요한 파일이 없습니다.")
        input("아무 키나 눌러서 종료하세요...")
        return
    
    # 설정 파일 확인
    if not check_config_file():
        print("⚠️ 설정 파일에 문제가 있지만 서버를 시작합니다.")
        print("💡 웹 페이지에서 설정 오류 메시지를 확인하세요.")
    
    # 서버 설정
    HOST = '0.0.0.0'
    PORT = int(os.environ.get('PORT', 8000))
    
    try:
        # 포트 사용 가능 확인
        server = HTTPServer((HOST, PORT), CORSRequestHandler)
        
        print(f"✅ HTTP 서버 시작: http://{HOST}:{PORT}")
        print(f"📁 서빙 디렉토리: {os.getcwd()}")
        print(f"🌐 메인 페이지: http://{HOST}:{PORT}/index.html")
        print("=" * 50)
        print("🔧 사용 방법:")
        print("1. 네이버 클라우드 플랫폼에서 지도 API 클라이언트 ID 발급")
        print("2. config.js 파일에서 CLIENT_ID 설정")
        print("3. 슈퍼베이스 '네이버지도실험' 테이블에 데이터 확인")
        print("4. 웹 페이지에서 지도 및 마커 확인")
        print("=" * 50)
        print("⚠️ 서버 종료: Ctrl+C")
        print()
        
        # 브라우저 자동 열기
        main_url = f"http://{HOST}:{PORT}/index.html"
        open_browser(main_url)
        
        # 서버 실행
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\n🛑 서버 종료 중...")
        server.shutdown()
        print("✅ 서버가 정상적으로 종료되었습니다.")
        print("서버 종료", flush=True)
        
    except OSError as e:
        if e.errno == 10048:  # Windows: 포트 이미 사용 중
            print(f"❌ 포트 {PORT}가 이미 사용 중입니다.")
            print("💡 다른 프로그램이 해당 포트를 사용하고 있거나 이미 서버가 실행 중일 수 있습니다.")
        else:
            print(f"❌ 서버 시작 오류: {e}")
        print("서버 종료", flush=True)
        input("아무 키나 눌러서 종료하세요...")
        
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        print("서버 종료", flush=True)
        input("아무 키나 눌러서 종료하세요...")

if __name__ == "__main__":
    main() 
