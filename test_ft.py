from fine_turning import Qwen3PhysicsTester
import re


def clean_email_icons_simple(text: str) -> str:
    """
    Loại bỏ emoji và icons khỏi text email, xử lý xuống dòng
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Pattern mở rộng để bắt nhiều loại emoji hơn
    emoji_pattern = re.compile(r'[\U0001F000-\U0001F9FF\u2600-\u26FF\u2700-\u27BF\u200d\ufe0f]')
    text = emoji_pattern.sub(" ", text)
    
    # Xử lý xuống dòng - Option 1: Giữ format nhưng giới hạn dòng trống
    # Thay thế nhiều xuống dòng liên tiếp bằng tối đa 2 xuống dòng
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Tối đa 2 dòng trống
    text = re.sub(r'[ \t]+', ' ', text)  # Thay nhiều space/tab bằng 1 space
    text = re.sub(r'[ \t]*\n[ \t]*', '\n', text)  # Loại space thừa quanh xuống dòng
    
    return text.strip()


tester = Qwen3PhysicsTester("Qwen/Qwen3-0.6B")
tester.setup_device(force_cpu=True)
tester.load_model_from_fold("fine_turning/model_LLM_email/fold_4", use_quantization=False)

system_prompt = """
Bạn là hệ thống phân loại email chính xác.

Phân loại mỗi email vào 1 trong 5 nhãn:
- Giả mạo: Lừa đảo, giả danh ngân hàng/dịch vụ, đòi thông tin nhạy cảm
- Khuyến mãi: Quảng cáo hợp lệ từ công ty/thương hiệu
- Spam: Email rác, không mong muốn, nội dung vô nghĩa  
- Bình thường: Email giao tiếp thông thường, hợp pháp

Quy tắc:
1. Chỉ trả lời 1 từ: Giả mạo/Khuyến mãi/Spam/Bình thường
2. Không giải thích
3. Phân tích: người gửi, tiêu đề, nội dung, link
4. Ưu tiên an toàn: nếu nghi ngờ → Giả mạo

Dấu hiệu giả mạo: link lạ, yêu cầu gấp, đe dọa, domain giả
Dấu hiệu khuyến mãi: giảm giá, sản phẩm mới, từ brand thật
Dấu hiệu spam: VIẾT HOA, ký tự lạ, hứa hẹn vô lý
""".strip()

# email : str = input("Bạn hãy nhập email: ")

emails = [
    """Người gửi: support@appleid-secure.com
Người nhận: nguyen.thanh@gmail.com
Thời gian: 2025-07-23 07:43:11
Tiêu đề: Apple ID của bạn đã bị đăng nhập tại Trung Quốc
Nội dung:
Chúng tôi phát hiện một phiên đăng nhập mới từ thiết bị không xác định tại Trung Quốc.
Nếu đây không phải bạn, vui lòng xác minh tài khoản tại:
https://appleid-secure.com/verify-now

Apple Security Center""",

    """Người gửi: technews@vnexpress.net
Người nhận: nguyen.thanh@gmail.com
Thời gian: 2025-07-23 08:05:01
Tiêu đề: Tin công nghệ mới nhất: OpenAI ra mắt AI mới cực mạnh
Nội dung:
Kính gửi bạn đọc,

Hôm nay, OpenAI đã chính thức công bố mô hình AI thế hệ tiếp theo có khả năng lập trình, dịch ngôn ngữ và phân tích hình ảnh vượt trội.

Đọc thêm: https://vnexpress.net/tin-cong-nghe/openai-ai-moi

Cảm ơn bạn đã theo dõi VnExpress""",

    """Người gửi: hr@tuyendung-fpt.com.vn
Người nhận: nguyen.thanh@gmail.com
Thời gian: 2025-07-22 21:15:55
Tiêu đề: Bạn đã được chọn vào vòng phỏng vấn – xác nhận ngay
Nội dung:
Xin chào Nguyễn Thanh,

Chúng tôi rất ấn tượng với hồ sơ của bạn. Để xác nhận tham gia vòng phỏng vấn tại FPT Software, vui lòng đăng nhập vào cổng xác thực sau:

https://fpt-confirm-interview.site/login

Chúng tôi chờ đợi bạn!

HR Team""",

    """Người gửi: my.bank@tpbank.vn
Người nhận: nguyen.thanh@gmail.com
Thời gian: 2025-07-23 02:22:30
Tiêu đề: Giao dịch trên 10 triệu đồng cần xác minh
Nội dung:
Quý khách thân mến,

Tài khoản của quý khách vừa thực hiện giao dịch chuyển khoản 12,800,000 VND vào 01:47 AM.

Nếu đây không phải giao dịch của quý khách, vui lòng KHÔNG trả lời email này. Hãy đăng nhập TPBank app để kiểm tra và liên hệ tổng đài nếu cần.

Trân trọng,
TPBank""",

    """Người gửi: giftcenter@tiki.vn
Người nhận: nguyen.thanh@gmail.com
Thời gian: 2025-07-21 14:30:42
Tiêu đề: Bạn có 1 phần quà chưa nhận – Chỉ còn 24h!
Nội dung:
Xin chào Nguyễn Thanh,

Bạn đã tích đủ 10 điểm thưởng Tiki Xu và được nhận phần quà đặc biệt.

Nhấn vào đây để xem quà và xác nhận nhận hàng:
https://tiki.vn/khuyenmai/phanqua123

Chúc bạn một ngày vui vẻ!"""
]


for email in emails:
    email_clean = clean_email_icons_simple(email)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": email_clean}
    ]
    thinking, result = tester.Gen_Asne_Optimized(messages, target_tokens=700, enable_thinking=True)
    print("-" * 20)
    print(f"Kết quả model trả lời: {result}")