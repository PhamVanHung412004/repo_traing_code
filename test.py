
import json

data_all = []
with open("/home/phamvanhung/SSD_512GB/repo_traing_code/dataset/dataset_10k.json", "r", encoding="utf-8") as file:
    data_final = json.load(file)
    
    for data in data_final:
        if (data["labels"] != "Spam"):
            data_all.append(data)
        # if (data["labels"] != "Spam"):
        #     data_all.append(data)




with open("data_final/dataset_tmp.json", "w", encoding="utf-8") as file:
    json.dump(data_all, file, indent=4, ensure_ascii=False)  
print(len(data_all))