import os

# parameters
RESULT_DIR = 'E:\\eDocs\\PhD\\Y1S1\\ELEC523\\Project\\results\\brats\\'
OUTPUT_FILE = 'E:\\eDocs\\PhD\\Y1S1\\ELEC523\\Project\\results\\brats.txt'
DATASET = 'brats' # cjdata;brats

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
                            if ('Jaccard:' in line):
                                jaccard_sum[m_i] = jaccard_sum[m_i] + float(line.replace('Jaccard: ', '').replace('\n', ''))
                                continue
                            if ('Dice (skull stripped):' in line):
                                dice_proc_sum[m_i] = dice_proc_sum[m_i] + float(line.replace('Dice (skull stripped): ', '').replace('\n', ''))
                                continue
                            if ('Jaccard (skull stripped):' in line):
                                jaccard_proc_sum[m_i] = jaccard_proc_sum[m_i] + float(line.replace('Jaccard (skull stripped): ', '').replace('\n', ''))
                                continue

                        fin.close()

    # output
    fout = open(OUTPUT_FILE, 'w')

    for m_i, m_val in enumerate(METHODS):
        fout.write('Dice for ' + m_val + ': ' + str(dice_sum[m_i] / results_cnt[m_i]) + '\n')
        fout.write('Jaccard for ' + m_val + ': ' + str(jaccard_sum[m_i] / results_cnt[m_i]) + '\n')
        fout.write('Dice (skull stripped) for ' + m_val + ': ' + str(dice_proc_sum[m_i] / results_cnt[__BuiltinMethodDescriptor__]) + '\n')
        fout.write('Jaccard (skull stripped) for ' + m_val + ': ' + str(jaccard_sum[m_i] / results_cnt[m_i]) + '\n')

    fout.close()


elif (DATASET is 'brats'):
    # init
    results_cnt = [0] * len(METHODS) * len(TYPES)
    dice_sum = [0.0] * len(METHODS) * len(TYPES)
    jaccard_sum = [0.0] * len(METHODS) * len(TYPES)

    # iterate over files
    for subdir, dirs, files in os.walk(RESULT_DIR):
        for filename in files:
            filepath = subdir + os.sep + filename

            if filepath.endswith('.txt'):
                for m_i, m_val in enumerate(METHODS):
                    for t_i, t_val in enumerate(TYPES):
                        if (m_val in filename and t_val in filename):
                            results_cnt[m_i * len(TYPES) + t_i] = results_cnt[m_i * len(TYPES) + t_i] + 1

                            fin = open(filepath, 'r')
                            lines = fin.readlines()

                            for line in lines:
                                if ('Dice:' in line):
                                    dice_sum[m_i * len(TYPES) + t_i] = dice_sum[m_i * len(TYPES) + t_i] + float(line.replace('Dice: ', '').replace('\n', ''))
                                    continue
                                if ('Jaccard:' in line):
                                    jaccard_sum[m_i * len(TYPES) + t_i] = jaccard_sum[m_i * len(TYPES) + t_i] + float(line.replace('Jaccard: ', '').replace('\n', ''))
                                    continue

                            fin.close()

    # output
    fout = open(OUTPUT_FILE, 'w')

    for m_i, m_val in enumerate(METHODS):
        for t_i, t_val in enumerate(TYPES):
            fout.write('Dice for ' + m_val + ' on ' + t_val + ': ' + str(dice_sum[m_i * len(TYPES) + t_i] / results_cnt[m_i * len(TYPES) + t_i]) + '\n')
            fout.write('Jaccard for ' + m_val + ' on ' + t_val + ': ' + str(jaccard_sum[m_i * len(TYPES) + t_i] / results_cnt[m_i * len(TYPES) + t_i]) + '\n')

    fout.close()