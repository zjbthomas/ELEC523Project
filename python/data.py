import os

# parameters
RESULT_DIR = 'E:\\eDocs\\PhD\\Y1S1\\ELEC523\\Project\\results\\cjdata\\'
OUTPUT_FILE = 'E:\\eDocs\\PhD\\Y1S1\\ELEC523\\Project\\results\\cjdata.txt'
DATASET = 'cjdata' # cjdata; brats
METHOD = 'flicm' # otsu; flicm
FLICM_ITER = 300
FLICM_THRES = 0.0000001

# constants
METHODS = ['otsu', 'flicm']
TYPES = ['flair', 't1', 't2']

if (DATASET is 'cjdata'):
    # init
    results_cnt = [0] * len(METHODS)
    dice_sum = [0.0] * len(METHODS)
    dice_proc_sum = [0.0] * len(METHODS)
    jaccard_sum = [0.0] * len(METHODS)
    jaccard_proc_sum = [0.0] * len(METHODS)
    time_sum = [0.0] * len(METHODS)
    time_proc_sum = [0.0] * len(METHODS)

    # for FLICM
    if (METHOD is 'flicm'):
        underest_cnt = [0] * len(METHODS)

    # iterate over files
    for subdir, dirs, files in os.walk(RESULT_DIR):
        for filename in files:
            filepath = subdir + os.sep + filename

            if filepath.endswith('.txt'):
                for m_i, m_val in enumerate(METHODS):
                    if (m_val in filename):
                        results_cnt[m_i] = results_cnt[m_i] + 1

                        fin = open(filepath, 'r')
                        lines = fin.readlines()

                        for line in lines:
                            if ('Dice:' in line):
                                dice_sum[m_i] = dice_sum[m_i] + float(line.replace('Dice: ', '').replace('\n', ''))
                                continue
                            if ('Dice (skull stripped):' in line):
                                dice_proc_sum[m_i] = dice_proc_sum[m_i] + float(line.replace('Dice (skull stripped): ', '').replace('\n', ''))
                                continue
                            if ('Jaccard:' in line):
                                jaccard_sum[m_i] = jaccard_sum[m_i] + float(line.replace('Jaccard: ', '').replace('\n', ''))
                                continue 
                            if ('Jaccard (skull stripped):' in line):
                                jaccard_proc_sum[m_i] = jaccard_proc_sum[m_i] + float(line.replace('Jaccard (skull stripped): ', '').replace('\n', ''))
                                continue
                            if ('Time:' in line):
                                time_sum[m_i] = time_sum[m_i] + float(line.replace('Time: ', '').replace('\n', ''))
                                continue
                            if ('Time (skull stripped):' in line):
                                time_proc_sum[m_i] = time_proc_sum[m_i] + float(line.replace('Time (skull stripped): ', '').replace('\n', ''))
                                continue

                            # for FLICM
                            if (METHOD is 'flicm' and ('Iteration ' + str(FLICM_ITER)) in line):
                                if (str(FLICM_THRES) is line.replace('Iteration ' + str(FLICM_ITER) + ', diff ', '').replace('\n', '')):
                                    underest_cnt[m_i] = underest_cnt[m_i] + 1
                                    continue

                        fin.close()

    # output
    fout = open(OUTPUT_FILE, 'w')

    for m_i, m_val in enumerate(METHODS):
        if (results_cnt[m_i] == 0):
                continue

        fout.write('Number of images for ' + m_val + ': ' + str(results_cnt[m_i]))
        fout.write('Dice for ' + m_val + ': ' + str(dice_sum[m_i] / results_cnt[m_i]) + '\n')
        fout.write('Jaccard for ' + m_val + ': ' + str(jaccard_sum[m_i] / results_cnt[m_i]) + '\n')
        fout.write('Time for ' + m_val + ': ' + str(time_sum[m_i] / results_cnt[m_i]) + '\n')
        fout.write('Dice (skull stripped) for ' + m_val + ': ' + str(dice_proc_sum[m_i] / results_cnt[m_i]) + '\n')
        fout.write('Jaccard (skull stripped) for ' + m_val + ': ' + str(jaccard_sum[m_i] / results_cnt[m_i]) + '\n')
        fout.write('Time (skull stripped) for ' + m_val + ': ' + str(time_proc_sum[m_i] / results_cnt[m_i]) + '\n')

        # for FLICM
        if (METHOD is 'flicm'):
            fout.write('Number of underestimation in FLICM for ' + m_val + ': ' + str(underest_cnt[m_i]) + '\n')

    fout.close()


elif (DATASET is 'brats'):
    # init
    results_cnt = [0] * len(METHODS) * len(TYPES)
    dice_sum = [0.0] * len(METHODS) * len(TYPES)
    jaccard_sum = [0.0] * len(METHODS) * len(TYPES)
    time_sum = [0.0] * len(METHODS) * len(TYPES)

    # for FLICM
    if (METHOD is 'flicm'):
        underest_cnt = [0] * len(METHODS) * len(TYPES)

    # iterate over files
    for subdir, dirs, files in os.walk(RESULT_DIR):
        for filename in files:
            filepath = subdir + os.sep + filename

            if filepath.endswith('.txt'):
                for m_i, m_val in enumerate(METHODS):
                    for t_i, t_val in enumerate(TYPES):
                        i = m_i * len(TYPES) + t_i

                        if (m_val in filename and t_val in filename):
                            results_cnt[i] = results_cnt[i] + 1

                            fin = open(filepath, 'r')
                            lines = fin.readlines()

                            for line in lines:
                                if ('Dice:' in line):
                                    dice_sum[i] = dice_sum[i] + float(line.replace('Dice: ', '').replace('\n', ''))
                                    continue
                                if ('Jaccard:' in line):
                                    jaccard_sum[i] = jaccard_sum[i] + float(line.replace('Jaccard: ', '').replace('\n', ''))
                                    continue
                                if ('Time:' in line):
                                    time_sum[i] = time_sum[i] + float(line.replace('Time: ', '').replace('\n', ''))
                                    continue
                                
                                # for FLICM
                                if (METHOD is 'flicm' and ('Iteration ' + str(FLICM_ITER)) in line):
                                    if (str(FLICM_THRES) is not line.replace('Iteration ' + str(FLICM_ITER) + ', diff ', '').replace('\n', '')):
                                        underest_cnt[i] = underest_cnt[i] + 1
                                        continue

                            fin.close()

    # output
    fout = open(OUTPUT_FILE, 'w')

    for m_i, m_val in enumerate(METHODS):
        for t_i, t_val in enumerate(TYPES):
            i = m_i * len(TYPES) + t_i

            if (results_cnt[i] == 0):
                continue

            fout.write('Number of images for ' + m_val + ' on ' + t_val + ': ' + str(results_cnt[i]) + '\n')
            fout.write('Dice for ' + m_val + ' on ' + t_val + ': ' + str(dice_sum[i] / results_cnt[i]) + '\n')
            fout.write('Jaccard for ' + m_val + ' on ' + t_val + ': ' + str(jaccard_sum[i] / results_cnt[i]) + '\n')
            fout.write('Time for ' + m_val + ' on ' + t_val + ': ' + str(time_sum[i] / results_cnt[i]) + '\n')

            # for FLICM
            if (METHOD is 'flicm'):
                fout.write('Number of underestimation in FLICM for ' + m_val + ' on ' + t_val + ': ' + str(underest_cnt[i]) + '\n')

    fout.close()