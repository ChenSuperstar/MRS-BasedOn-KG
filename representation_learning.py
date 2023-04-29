from openke.config import Config
from openke.models import TransE
from openke.data import utils
import torch
import numpy as np

# Step 1: 准备数据集

train_dataloader = TrainDataLoader(
    in_path="./benchmarks/FB15K237/",
    batch_size=1024,
    threads=8,
    sampling_mode="normal",
    bern_flag=0,
    filter_flag=1,
    neg_ent=25,
    neg_rel=0
)

test_dataloader = TestDataLoader("./benchmarks/FB15K237/", "link")

# Step 2: 配置参数
config = Config()
config.set_in_path("./benchmarks/FB15K237/")
config.set_work_threads(8)
config.set_dimension(50)
config.set_margin(1.0)
config.set_ent_neg_rate(1)
config.set_rel_neg_rate(0)
config.set_opt_method("adagrad")
config.set_learning_rate(0.01)
config.set_batch_size(1024)
config.set_bern(0)
config.set_filter(1)
config.set_negative_ent(25)
config.set_negative_rel(0)
config.set_test_flag(True)
config.set_export_files("./res/model.vec.pt")
config.set_import_files("./res/model.vec.pt")

# Step 3: 初始化模型
model = TransE(config)
model.initialize_embeddings()

# Step 4: 训练模型
trainer = NegativeSampling(model=model,
                           data_loader=train_dataloader,
                           train_times=1000,
                           alpha=0.5,
                           use_gpu=False)

trainer.run()
model.save_checkpoint(config.export_files)

# Step 5: 保存嵌入向量
entity_embeddings = model.ent_embeddings.weight.cpu().data.numpy()
relation_embeddings = model.rel_embeddings.weight.cpu().data.numpy()
np.save("./res/entity_embeddings.npy", entity_embeddings)
np.save("./res/relation_embeddings.npy", relation_embeddings)
