import os
import re
import json
import pymupdf

def clean_ocr_text(text):
    if not text:
        return ""
    # Remove soft hyphens
    text = text.replace("\xad", "-")
    # CamScanner artifact filter
    text = re.sub(r"CS\s*CamScanner", "", text, flags=re.IGNORECASE)
    text = re.sub(r"CamScanner", "", text, flags=re.IGNORECASE)
    
    # Common OCR typo normalization in Vietnamese educational context
    replacements = [
        ("bải học", "bài học"),
        ("tinh huống", "tình huống"),
        ("cùa", "của"),
        ("vỉ du", "ví dụ"),
        ("đế hổ trợ", "để hỗ trợ"),
        ("can người", "con người"),
        ("mô lả", "mô tả"),
        ("hĩnh thành", "hình thành"),
        ("sắn", "sẵn"),
        ("chiêc", "chiếc"),
        ("cỏ logic", "có logic"),
        ("mấy tinh", "máy tính"),
        ("no­ron", "nơ-ron"),
        ("tich chập", "tích chập"),
        ("mỏt", "một"),
        ("láng thời gian", "tăng thời gian"),
        ("phủ hợp", "phù hợp"),
        ("sứ dụng", "sử dụng"),
        ("kì thuật", "kĩ thuật"),
        ("Intelligencs", "Intelligence"),
        ("vấn dề", "vấn đề"),
        ("tư học", "tự học"),
        ("người gia", "người già"),
        ("sự cổ", "sự cố"),
        ("linh hoại", "linh hoạt"),
        ("ẠI TẠO SINH", "AI TẠO SINH"),
        ("Al tạo sinh", "AI tạo sinh"),
        ("Al hẹp", "AI hẹp"),
        ("Al tổng quát", "AI tổng quát"),
        ("Al Agent", "AI Agent"),
        ("Al ", "AI "),
        (" Al", " AI"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
        
    return text.strip()

print("clean_ocr_text defined")
