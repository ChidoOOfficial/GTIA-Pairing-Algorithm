import load_data
import random
import math


def get_scores_matrix(data_ambs, data_stud):
    res = [[0 for i in range(len(data_stud))] for i in range(len(data_ambs))]
    possible_results = {0}
    for i in range(len(data_ambs)):
        for j in range(len(data_stud)):
            res[i][j] = 0
            if data_ambs[i]['Country Preference 1'] == data_stud[j]['Primary Citizenship']:
                res[i][j] += 22
            if data_ambs[i]['Country Preference 2'] == data_stud[j]['Primary Citizenship']:
                res[i][j] += 12
            if data_ambs[i]['Country Preference 3'] == data_stud[j]['Primary Citizenship']:
                res[i][j] += 7
            if data_ambs[i]['Major Preference 1'] == data_stud[j]['Major-Primary']:
                res[i][j] += 20
            if data_ambs[i]['Major Preference 2'] == data_stud[j]['Major-Primary']:
                res[i][j] += 10
            possible_results.add(res[i][j])

    possible_results = list(possible_results)
    possible_results.sort()
    return res, possible_results

def run_match(data_ambs, data_stud, score_matrix, poss_scores, max_assignment='auto', initial_max_assignment='auto'):
    excess = 0
    if max_assignment=='auto':
        max_assignment = math.ceil(len(data_stud)/len(data_ambs))
        initial_max_assignment = len(data_stud)//len(data_ambs)
        excess = len(data_stud) - initial_max_assignment * len(data_ambs)


    ambs = {}
    for i in range(len(data_ambs)):
        ambs[i] = []

    excess_assigned = 0

    amb_orders = list(range(len(data_ambs)))
    stud_orders = list(range(len(data_stud)))

    assigned = [False] * len(data_stud)
    curr_score = poss_scores[::-1]
    while len(curr_score) > 0:
        random.shuffle(amb_orders)
        random.shuffle(stud_orders)

        found_match = False

        for i in amb_orders:
            for j in stud_orders:
                if score_matrix[i][j] == curr_score[0] and not assigned[j] and (len(ambs[i]) < initial_max_assignment or (len(ambs[i]) < max_assignment and excess_assigned < excess)):
                    ambs[i].append(data_stud[j])
                    assigned[j] = True
                    found_match = True
                    if len(ambs[i]) == max_assignment:
                        excess_assigned += 1
                    break
        if not found_match:
            curr_score = curr_score[1:]

    ambs_result = []
    for i in range(len(data_ambs)):
        ambs_result.append((data_ambs[i], ambs[i]))

    def key(amb):
        return amb[0]['Name']

    ambs_result.sort(key=key)


    return ambs_result

def string_student(stud):
    res = ''
    for s in stud:
        res += stud[s] + ','
    return res[:-1]

def print_match_result(ambs_result, name):
    f = open(name, "w+")
    res = 'Ambassador Name,'
    for cat in ambs_result[0][1][0]:
        res += cat + ','
    res = res[:-1] + '\n'

    for ambs_tup in ambs_result:
        amb, studs = ambs_tup
        res += amb['Name'] + ',' + string_student(studs[0]) + '\n'
        for i in range(1, len(studs)):
            res += ',' + string_student(studs[i]) + '\n'

    f.write(res)
    f.close()


data_ambs = load_data.load_data('Email Pairing Interest Form.csv')
data_stud = load_data.load_data('GTIA-EA-2020.csv')

if __name__=='__main__':
    score_matrix, poss_scores = get_scores_matrix(data_ambs, data_stud)
    ambs_results = run_match(data_ambs, data_stud, score_matrix, poss_scores)
    print_match_result(ambs_results, 'results.csv')
    print('done')




#"Timestamp","Name:","Country Preference 1","Country Preference 2","Country Preference 3","Major Preference 1","Major Preference 2"
#Preferred Name,Given Name,Middle Name,Surname,Citz Status,Primary Citizenship,M/F,First Gen College Student,School Name,School - City,School - Country,State (US/Canada),College,Major-Primary,Most Recent Decision,Email Address
