from bot.services.title_translator import clean_raw_title, translate_full_title


def test_clean_raw_title_seo():
    raw = "GLB-클래스 X247 GLB200 d 경기 중고차 : 내차팔기·내차사기"
    assert clean_raw_title(raw) == "GLB-클래스 X247 GLB200 d"


def test_translate_full_title_examples():
    examples = {
        "Ford 익스플로러 6세대 2.3 리미티드 4WD": "Ford Explorer 6th Gen 2.3 Limited 4WD",
        "Audi A6 C8 45 TFSI 콰트로 Premium": "Audi A6 C8 45 TFSI quattro Premium",
        "BMW 5시리즈 G30 530i Luxury 플러스": "BMW 5-Series G30 530i Luxury Plus",
        "마세라티 기블리 3.0 그란스포츠 3세대": "Maserati Ghibli 3.0 GranSport 3rd Gen",
        "Jeep 랭글러 JL 2.0 오버랜드 4도어": "Jeep Wrangler JL 2.0 Overland 4-Door",
        "포르쉐 카이엔 PO536 3.0 E-Hybrid": "Porsche Cayenne PO536 3.0 E-Hybrid",
        "Volkswagen 골프 8세대 2.0 GTI": "Volkswagen Golf 8th Gen 2.0 GTI",
        "Volvo S60 3세대 T5 인스크립션": "Volvo S60 3rd Gen T5 Inscription",
        "MINI 쿠퍼 S JCW 3세대": "MINI Cooper S JCW 3rd Gen",
        "랜드로버 레인지로버 4세대 4.4 SDV8 AB LWB": "Land Rover Range Rover 4th Gen 4.4 SDV8 AB LWB",
        "Volkswagen 파사트 GT B8 2.0 TDI Premium": "Volkswagen Passat GT B8 2.0 TDI Premium",
        "Volkswagen 제타 7세대 1.4 TSI Prestige": "Volkswagen Jetta 7th Gen 1.4 TSI Prestige",
        "Ford 머스탱 7세대 2.3 에코부스트 Premium 컨버터블": "Ford Mustang 7th Gen 2.3 EcoBoost Premium Convertible",
        "MINI 쿠퍼 S 컨버터블 기본형 3세대": "MINI Cooper S Convertible Base 3rd Gen",
        "BMW 2시리즈 액티브 투어러 U06 220i 어드밴티지": "BMW 2-Series Active Tourer U06 220i Advantage",
        "Volkswagen 아테온 2.0 TDI Premium": "Volkswagen Arteon 2.0 TDI Premium",
        "Volkswagen 티구안 올스페이스 2.0 TSI Prestige": "Volkswagen Tiguan Allspace 2.0 TSI Prestige",
        "MINI 쿠퍼 컨트리맨 기본형 2세대": "MINI Cooper Countryman Base 2nd Gen",
        "포르쉐 911 992 카레라 카브리올레": "Porsche 911 992 Carrera Cabriolet",
        "테슬라 모델 S 플래드": "Tesla Model S Plaid",
        "Jeep 레니게이드 2.4 리미티드 AWD": "Jeep Renegade 2.4 Limited AWD",
        "쉐보레(GM대우) 트레일블레이저": "Chevrolet Trailblazer",
        "르노코리아(삼성) QM6": "Renault Samsung QM6",
        "E-클래스 W213 E300e 4MATIC 익스클루시브": "Mercedes-Benz E-Class W213 E300e 4MATIC Exclusive",
        "3시리즈 F30 330i M 스포츠": "BMW 3-Series F30 330i M-Sport",
        "스포티지 5세대 가솔린 1.6 터보 2WD 프레스티지": "Kia Sportage 5th Gen 1.6 Turbo 2WD Prestige",
    }

    for raw, expected in examples.items():
        assert translate_full_title(clean_raw_title(raw)) == expected
