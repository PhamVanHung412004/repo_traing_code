import torch
from torch import nn
from torchtext.vocab import build_vocab_from_iterator
from torchtext.data.utils import get_tokenizer
import pickle
from clean_data import preprocess_text

device = torch.device("cpu")

class TextClassificationModel(nn.Module):
    def __init__(self, vocab_size, embed_dim, num_class):
        super(TextClassificationModel, self).__init__()
        self.embedding = nn.EmbeddingBag(vocab_size, embed_dim, sparse=False)
        self.fc = nn.Linear(embed_dim, num_class)
        self.init_weights()

    def init_weights(self):
        initrange = 0.5
        self.embedding.weight.data.uniform_(-initrange, initrange)
        self.fc.weight.data.uniform_(-initrange, initrange)
        self.fc.bias.data.zero_()

    def forward(self, inputs, offsets):
        embedded = self.embedding(inputs, offsets)
        return self.fc(embedded)

# Load vocabulary từ file
with open('solution_train_with_nn/vocal/vocab.pkl', 'rb') as f:
    vocabulary = pickle.load(f)

# Đảm bảo có default index để tránh lỗi từ ngoài vocab
vocabulary.set_default_index(vocabulary["<unk>"])


# ----------- Khôi phục thông số mô hình -----------
vocab_size = len(vocabulary)       # Thay bằng kích thước vocab bạn dùng lúc huấn luyện
embed_dim = 100           # Số chiều embedding bạn dùng
num_class = 4            # Số lớp phân loại, ví dụ: 4 lớp

# ----------- Tải mô hình đã lưu -----------
model = TextClassificationModel(vocab_size, embed_dim, num_class).to(device)
model.load_state_dict(torch.load("solution_train_with_nn/model/model_state.pth"))
model.eval()

# ----------- Tiền xử lý văn bản -----------

tokenizer = get_tokenizer("basic_english")

# Dummy example, thay bằng vocab thật khi huấn luyện
def yield_tokens(data_iter):
    for text in data_iter:
        yield tokenizer(text)

def predict(text):
    with torch.no_grad():
        encoded = torch.tensor(vocabulary(tokenizer(text)), device=device)
        output = model(encoded, torch.tensor([0], device=device))
        return output.argmax(1).item()


def main() -> None:
    text = """
Chào bạn,
Đây là email nhắc nhở bạn hoàn thành và nộp bài tiểu luận tuần 4 trước 23h59 ngày 25/07.
Mọi thắc mắc vui lòng liên hệ trực tiếp với giảng viên phụ trách.
Trân trọng,
Lan Phạm 
"""
    print(predict(preprocess_text(text)))

if __name__ == '__main__':

    main()