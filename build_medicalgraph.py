
import pandas as pd
import json

#节点
diseases = [] #疾病名称
departments = [] #疾病科室
symptoms = [] #疾病症状
drugs = [] #疾病用药
checks = [] #疾病检查
cures = [] #治疗方法
producers =[]  #药品大类
foods = [] #食物

disease_info = []


#实体关系
rel_department = [] #科室-科室关系
rel_category = [] #疾病-室关系
rel_symptom = [] # 疾病-症状关系
rel_acompany = [] #疾病并发关系
rel_commondrug = [] #疾病-通用药品关系
rel_recommanddrug = [] # 疾病-推荐药品关系
rel_check = [] #疾病-检查关系
rel_drug_producer = [] #厂商-药物关系
rel_cureway = [] # 疾病-治疗方式关系
rel_noteat = [] #疾病-忌吃
rel_doeat = [] #疾病-宜吃
rel_recommandeat = [] #疾病-推荐吃

with open('data/medical.json', encoding='utf-8') as f:
    for line in f:
        disease_dic = {}
        obj = json.loads(line)
        disease = obj['name']
        diseases.append(disease)

        disease_dic['name'] = disease
        disease_dic['cause'] = ''
        disease_dic['get_prob'] = ''
        disease_dic['easy_get'] = ''
        disease_dic['prevent'] = ''
        disease_dic['cure_lasttime'] = ''
        disease_dic['cured_prob'] = ''

        if 'cause' in obj:
            disease_dic['cause'] = obj['cause']

        if 'get_prob' in obj:
            disease_dic['get_prob'] = obj['get_prob']

        if 'easy_get' in obj:
            disease_dic['easy_get'] = obj['easy_get']

        if 'prevent' in obj:
            disease_dic['prevent'] = obj['prevent']

        if 'cure_lasttime' in obj:
            disease_dic['cure_lasttime'] = obj['cure_lasttime']

        if 'cured_prob' in obj:
            disease_dic['cured_prob'] = obj['cured_prob']

        disease_info.append(disease_dic)

        if 'acompany' in obj:
            acompany = obj['acompany']
            for acomp in acompany:
                rel_acompany.append([disease, acomp])

        if 'cure_department' in obj:
            cure_department = obj['cure_department']
            if len(cure_department) == 1:
                rel_category.append([disease, cure_department[0]])
            if len(cure_department) == 2:
                big = cure_department[0]
                small = cure_department[1]
                rel_department.append([small, big])
                rel_category.append([disease, small])
            departments += cure_department

        if 'symptom' in obj:
            symptom = obj['symptom']
            for symp in symptom:
                rel_symptom.append([disease, symp])
            symptoms += obj['symptom']

        if 'common_drug' in obj:
            common_drug = obj['common_drug']
            for drug in common_drug:
                rel_commondrug.append([disease, drug])
            drugs += common_drug

        if 'recommand_drug' in obj:
            recommand_drug = obj['recommand_drug']
            for drug in recommand_drug:
                rel_recommanddrug.append([disease, drug])
            drugs += recommand_drug

        if 'check' in obj:
            check = obj['check']
            for che in check:
                rel_check.append([disease, che])
            checks += check

        if 'cure_way' in obj:
            cure_way = obj['cure_way']
            for cure in cure_way:
                rel_cureway.append([disease, cure])
            cures += cure_way

        if 'drug_detail' in obj:
            drug_detail = obj['drug_detail']
            producer = [i.split('(')[0] for i in drug_detail]
            rel_drug_producer += [[i.split('(')[0], i.split('(')[-1].replace(')', '')] for i in drug_detail]
            producers += producer

        if 'do_eat' in obj:
            do_eat = obj['do_eat']
            for do_ in do_eat:
                rel_doeat.append([disease, do_])
            foods += do_eat

        if 'not_eat' in obj:
            not_eat = obj['not_eat']
            for not_ in not_eat:
                rel_noteat.append([disease, not_])
            foods += not_eat

        if 'recommand_eat' in obj:
            recommand_eat = obj['recommand_eat']
            for recommand_ in recommand_eat:
                rel_recommandeat.append([disease, recommand_])
            foods += recommand_eat

diseases = set(diseases)  # 疾病名称
departments = set(departments)  # 疾病科室
symptoms = set(symptoms)  # 疾病症状
drugs = set(drugs)  # 疾病用药
checks = set(checks)  # 疾病检查
cures = set(cures)  # 治疗方法
producers = set(producers)  # 药品大类
foods = set(foods)  # 食物

# 写入entity2id.txt文件
with open('data/entity2id.txt', 'w') as f:
    # 写入实体总数
    f.write(str(len(diseases) + len(departments) + len(symptoms)
            + len(drugs) + len(checks) + len(cures) + len(producers) + len(foods)) + '\n')
    # 写入disease的id
    for i, disease in enumerate(diseases):
        f.write(disease + '\t' + str(i) + '\n')
    # 写入symptom的id
    for i, symptom in enumerate(symptoms):
        f.write(symptom + '\t' + str(len(diseases) + i) + '\n')
    # 写入department的id
    for i, department in enumerate(departments):
        f.write(department + '\t' + str(len(diseases) + len(symptoms) + i) + '\n')
    #写入drugs的id
    for i, drug in enumerate(drugs):
        f.write(drug + '\t' + str(len(diseases) + len(symptoms)
                                  + len(departments) + i) + '\n')
    #写入checks的id
    for i, check in enumerate(checks):
        f.write(check + '\t' + str(len(diseases) + len(symptoms)
                                  + len(departments) + len(drugs) + i) + '\n')
    #写入cures的id
    for i, cure in enumerate(cures):
        f.write(cure + '\t' + str(len(diseases) + len(symptoms)
                                  + len(departments) + len(drugs) + len(checks) + i) + '\n')

    #写入producers的id
    for i, producer in enumerate(producers):
        f.write(producer + '\t' + str(len(diseases) + len(symptoms)
                                  + len(departments) + len(drugs)
                                      + len(checks) + len(cures) + i) + '\n')
    #写入foods的id
    for i,food in enumerate(foods):
        f.write(food + '\t' + str(len(diseases) + len(symptoms)
                                  + len(departments) + len(drugs)
                                      + len(checks) + len(cures) + len(producers) + i) + '\n')

    # 写入relation2id.txt文件
    with open('data/relation2id.txt', 'w') as f:
        # 写入关系总数
        f.write('12\n')
        # 写入disease和symptom之间的关系
        f.write('disease_symptom\t0\n')
        # 写入disease和department之间的关系
        f.write('disease_department\t1\n')
        # 写入department之间的关系
        f.write('A_belongs_to_B\t2\n')
        # 写入disease并发关系
        f.write('acompany\t3\n')
        # 写入disease和commondrug之间的关系
        f.write('disease_commonDrug\t4\n')
        # 写入disease和recommanddrug之间的关系
        f.write('disease_recommandDrug\t5\n')
        # 写入disease和check之间的关系
        f.write('disease_check\t6\n')
        # 写入drug和producer之间的关系
        f.write('drug_producer\t7\n')
        # 写入disease和cureway之间的关系
        f.write('disease_cureway\t8\n')
        # 写入disease和noteat之间的关系
        f.write('disease_noteat\t9\n')
        # 写入disease和doeat之间的关系
        f.write('disease_doeat\t10\n')
        # 写入disease和recommandeat之间的关系
        f.write('disease_recommandeat\t11\n')

entity_id_df = pd.read_csv('data/entity2id.txt', sep='\t', header=None, names=['entity', 'id'], dtype={'id': str} ,encoding='gb18030')
entity_id_dict = dict(zip(entity_id_df['entity'], entity_id_df['id']))


with open('data/train2id.txt', 'w') as f:
    # 写入三元组总数
    f.write(str(len(rel_department)
                + len(rel_category)
                + len(rel_symptom)
                + len(rel_acompany)
                + len(rel_commondrug)
                + len(rel_recommanddrug)
                + len(rel_check)
                + len(rel_drug_producer)
                + len(rel_noteat)
                + len(rel_doeat)
                + len(rel_recommandeat)) + '\n')
    # 写入disease和symptom之间的三元组
    for disease, symptom in rel_symptom:
        f.write(entity_id_dict[disease] + '\t' + entity_id_dict[symptom] + '\t0\n')

    # 写入disease和symptom之间的三元组
    for disease, department in rel_category:
        f.write(entity_id_dict[disease] + '\t' + entity_id_dict[department] + '\t1\n')

    # 写入departments之间的三元组
    for department1, department2 in rel_department:
        f.write(entity_id_dict[department1] + '\t' + entity_id_dict[department2] + '\t2\n')

    # 写入disease之间并发的三元组
    for disease1, disease2 in rel_acompany:
        f.write(entity_id_dict[disease1] + '\t' + entity_id_dict[disease2] + '\t3\n')

    # 写入disaese和commonDrug之间的三元组
    for disease, commonDrug in rel_commondrug:
        f.write(entity_id_dict[disease] + '\t' + entity_id_dict[commonDrug] + '\t4\n')

    # 写入disease和recommandDrug之间的三元组
    for disease, recommandDrug in rel_recommanddrug:
        f.write(entity_id_dict[disease] + '\t' + entity_id_dict[recommandDrug] + '\t5\n')

    # 写入disease和check之间的三元组
    for disease, check in rel_check:
        f.write(entity_id_dict[disease] + '\t' + entity_id_dict[check] + '\t6\n')

    # 写入drug和producer之间的三元组
    for drug, producer in rel_drug_producer:
        f.write(entity_id_dict[drug] + '\t' + entity_id_dict[producer] + '\t7\n')

    # 写入disease和cure_way之间的三元组
    for disease, cure in rel_cureway:
        f.write(entity_id_dict[disease] + '\t' + entity_id_dict[cure] + '\t8\n')

    # 写入disease和symptom之间的三元组
    for disease, noteat in rel_noteat:
        f.write(entity_id_dict[disease] + '\t' + entity_id_dict[noteat] + '\t9\n')

    for disease, doeat in rel_doeat:
        f.write(entity_id_dict[disease] + '\t' + entity_id_dict[doeat] + '\t10\n')

    # 写入disease和drug之间的三元组
    for disease, recommandeat in rel_recommandeat:
        f.write(entity_id_dict[disease] + '\t' + entity_id_dict[recommandeat] + '\t11\n')


symptom_commondrug_dict = {}
# 遍历疾病-症状列表
for disease, symptom in rel_symptom:
    # 如果症状已经在字典中，则直接加入对应药物
    if symptom in symptom_commondrug_dict:
        symptom_commondrug_dict[symptom] += [disease_commondrug[1] for disease_commondrug in rel_commondrug if disease_commondrug[0] == disease]
    # 如果症状不在字典中，则创建新的症状-药物关系
    else:
        symptom_commondrug_dict[symptom] = [disease_commondrug[1] for disease_commondrug in rel_commondrug if disease_commondrug[0] == disease]

symptom_recommanddrug_dict = {}

for disease, symptom in rel_symptom:
    # 如果症状已经在字典中，则直接加入对应药物
    if symptom in symptom_recommanddrug_dict:
        symptom_recommanddrug_dict[symptom] += [disease_recommanddrug[1] for disease_recommanddrug in rel_recommanddrug  if disease_recommanddrug[0] == disease]
    # 如果症状不在字典中，则创建新的症状-药物关系
    else:
        symptom_recommanddrug_dict[symptom] = [disease_recommanddrug[1] for disease_recommanddrug in rel_recommanddrug  if disease_recommanddrug[0] == disease]

symptom_noteat_dic = {}
for disease, symptom in rel_symptom:
    # 如果症状已经在字典中，则直接加入对应药物
    if symptom in symptom_noteat_dic:
        symptom_noteat_dic[symptom] += [disease_noteat[1] for disease_noteat in rel_noteat  if  disease_noteat[0] == disease]
    # 如果症状不在字典中，则创建新的症状-药物关系
    else:
        symptom_noteat_dic[symptom] = [disease_noteat[1] for disease_noteat in rel_noteat  if  disease_noteat[0] == disease]

symptom_doeat_dic = {}
for disease, symptom in rel_symptom:
    # 如果症状已经在字典中，则直接加入对应药物
    if symptom in symptom_doeat_dic:
        symptom_doeat_dic[symptom] += [disease_doeat[1] for disease_doeat in rel_doeat  if  disease_doeat[0] == disease]
    # 如果症状不在字典中，则创建新的症状-药物关系
    else:
        symptom_doeat_dic[symptom] = [disease_doeat[1] for disease_doeat in rel_doeat  if  disease_doeat[0] == disease]

symptom_recommandeat_dic = {}
for disease, symptom in rel_symptom:
    # 如果症状已经在字典中，则直接加入对应药物
    if symptom in symptom_recommandeat_dic:
        symptom_recommandeat_dic[symptom] += [disease_recommandeat[1] for disease_recommandeat in rel_recommandeat  if  disease_recommandeat[0] == disease]
    # 如果症状不在字典中，则创建新的症状-药物关系
    else:
        symptom_recommandeat_dic[symptom] = [disease_recommandeat[1] for disease_recommandeat in rel_recommandeat  if  disease_recommandeat[0] == disease]

symptom_commondrug_data = []
symptom_recommanddrug_data = []
symptom_noteat_data = []
symptom_doeat_data = []
symptom_recommandeat_data = []

# 遍历字典中的每个键值对
for symptom, drugs in symptom_commondrug_dict.items():
    # 将每个药品和症状构成一个元组，并添加到列表中
    for drug in drugs:
        symptom_commondrug_data.append((symptom, drug))

for symptom, drugs in symptom_recommanddrug_dict.items():
    # 将每个药品和症状构成一个元组，并添加到列表中
    for drug in drugs:
        symptom_recommanddrug_data.append((symptom, drug))

for symptom, foods in symptom_noteat_dic.items():
    # 将每个药品和症状构成一个元组，并添加到列表中
    for food in foods:
        symptom_noteat_data.append((symptom, food ))

for symptom, foods in symptom_doeat_dic.items():
    # 将每个药品和症状构成一个元组，并添加到列表中
    for food in foods:
        symptom_doeat_data.append((symptom, food ))

for symptom, foods in symptom_recommandeat_dic.items():
    # 将每个药品和症状构成一个元组，并添加到列表中
    for food in foods:
        symptom_recommandeat_data.append((symptom, food ))

symptom_commondrug_df = pd.DataFrame(symptom_commondrug_data, columns=['Symptom', 'commonDrug'])
symptom_recommanddrug_df = pd.DataFrame(symptom_recommanddrug_data, columns=['Symptom', 'recommandDrug'])
symptom_noteat_df = pd.DataFrame(symptom_noteat_data, columns=['Symptom', 'noteatFood'])
symptom_doeat_df = pd.DataFrame(symptom_doeat_data, columns=['Symptom', 'doeatFood'])
symptom_recommandeat_df = pd.DataFrame(symptom_recommandeat_data, columns=['Symptom', 'recommandeatFood'])


symptom_commondrug_df.to_csv('data/symptom_commondrug_dict.csv', index=False)
symptom_recommanddrug_df.to_csv('data/symptom_recommanddrug_dict.csv', index=False)
symptom_noteat_df.to_csv('data/symptom_noteat_dict.csv', index=False)
symptom_doeat_df.to_csv('data/symptom_doeat.csv', index=False)
symptom_recommandeat_df.to_csv('data/symptom_recommandeat_dict.csv', index=False)

