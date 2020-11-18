import os
import re

# parameters
RESULT_BASE = 'E:\\eDocs\\PhD\\Y1S1\\ELEC523\\Project\\results\\'
DATASETS = ['cjdata', 'brats'] # cjdata; brats;
METHODS = ['fcm', 'flicm'] # otsu; fcm; flicm;
CNUMS = [4, 5]

# constants
TYPES = ['t1', 't2', 't1ce']

for d in DATASETS:
    for m in METHODS:
        for c in CNUMS:
            
            if (m is 'otsu'):
                result_dir = RESULT_BASE + '\\' + d + '_' + m + '\\'
                output_file = RESULT_BASE + '\\' + d + '_' + m + '.txt'
            else:
                result_dir = RESULT_BASE + '\\' + d + '_' + m + '_' + str(c) + '\\'
                output_file = RESULT_BASE + '\\' + d + '_' + m + '_' + str(c) + '.txt'

            if (d is 'cjdata'):
                # init
                results_cnt = 0

                time_sum = 0.0
                time_proc_sum = 0.0

                dice_sum = 0.0
                dice_proc_sum = 0.0
                dice_mask_sum = 0.0

                jaccard_sum = 0.0
                jaccard_proc_sum = 0.0
                jaccard_mask_sum = 0.0

                TP = 0
                TN = 0
                FP = 0
                FN = 0

                TP_proc = 0
                TN_proc = 0
                FP_proc = 0
                FN_proc = 0

                TP_mask = 0
                TN_mask = 0
                FP_mask = 0
                FN_mask = 0
                

                # for FCM-based
                if (m is 'fcm' or m is 'flicm'):
                    underest_cnt = 0
                    underest_proc_cnt = 0

                # iterate over files
                for subdir, dirs, files in os.walk(result_dir):
                    for filename in files:
                        filepath = subdir + os.sep + filename

                        if filepath.endswith('.txt'):
                            # update numbers
                            results_cnt = results_cnt + 1

                            # read lines
                            fin = open(filepath, 'r')
                            lines = fin.readlines()
                            fin.close()

                            # offset for FCM-based
                            offset = 0
                            if (m is 'fcm' or m is 'flicm'):
                                offset = 1

                            # iteration (lines 1 and 3)
                            if (offset > 0):
                                if (str(0.0000000) not in lines[0] and str(0.0000001) not in lines[0]):
                                    underest_cnt = underest_cnt + 1
                                if (str(0.0000000) not in lines[2] and str(0.0000001) not in lines[2]):
                                    underest_proc_cnt = underest_proc_cnt + 1
                            
                            # time (lines 2/1 and line 4/2)
                            time_sum = time_sum + float(lines[0 + offset].replace('Time: ', '').replace('\n', ''))
                            time_proc_sum = time_proc_sum + float(lines[1 + 2 * offset].replace('Time (skull stripped): ', '').replace('\n', ''))

                            # Dice (lines 5/3, 10/8, and 15/13)
                            dice_sum = dice_sum + float(lines[2 + 2 * offset].replace('Dice: ', '').replace('\n', ''))
                            dice_proc_sum = dice_proc_sum + float(lines[7 + 2 * offset].replace('Dice (skull stripped): ', '').replace('\n', ''))
                            dice_mask_sum = dice_mask_sum + float(lines[12 + 2 * offset].replace('Dice (skull stripped on mask): ', '').replace('\n', ''))

                            # Jaccard (lines 6/4, 11/9, 16/14)
                            jaccard_sum = jaccard_sum + float(lines[3 + 2 * offset].replace('Jaccard: ', '').replace('\n', ''))
                            jaccard_proc_sum = jaccard_proc_sum + float(lines[8 + 2 * offset].replace('Jaccard (skull stripped): ', '').replace('\n', ''))
                            jaccard_mask_sum = jaccard_mask_sum + float(lines[13 + 2 * offset].replace('Jaccard (skull stripped on mask): ', '').replace('\n', ''))

                            # statistics (lines 7/5, 12/10, 17/15)
                            match = re.search(r'TP = ([0-9]+), TN = ([0-9]+), FP = ([0-9]+), FN = ([0-9]+)', lines[4 + 2 * offset])
                            TP = TP + int(match.group(1))
                            TN = TN + int(match.group(2))
                            FP = FP + int(match.group(3))
                            FN = FN + int(match.group(4))

                            match = re.search(r'TP = ([0-9]+), TN = ([0-9]+), FP = ([0-9]+), FN = ([0-9]+)', lines[9 + 2 * offset])
                            TP_proc = TP_proc + int(match.group(1))
                            TN_proc = TN_proc + int(match.group(2))
                            FP_proc = FP_proc + int(match.group(3))
                            FN_proc = FN_proc + int(match.group(4))

                            match = re.search(r'TP = ([0-9]+), TN = ([0-9]+), FP = ([0-9]+), FN = ([0-9]+)', lines[14 + 2 * offset])
                            TP_mask = TP_mask + int(match.group(1))
                            TN_mask = TN_mask + int(match.group(2))
                            FP_mask = FP_mask + int(match.group(3))
                            FN_mask = FN_mask + int(match.group(4))

                            fin.close()

                # output
                fout = open(output_file, 'w')

                if (results_cnt != 0):
                    fout.write('Number of images for ' + m + ': ' + str(results_cnt) + '\n')

                    fout.write('\n')

                    fout.write('Time for ' + m + ': ' + str(time_sum / results_cnt) + '\n')
                    fout.write('Time (skull stripped) for ' + m + ': ' + str(time_proc_sum / results_cnt) + '\n')

                    fout.write('\n') # an empty line as separation

                    fout.write('Dice for ' + m + ': ' + str(dice_sum / results_cnt) + '\n')
                    fout.write('Jaccard for ' + m + ': ' + str(jaccard_sum / results_cnt) + '\n')
                    fout.write('TP for ' + m + ': ' + str(float(TP) / results_cnt) + '\n')
                    fout.write('TN for ' + m + ': ' + str(float(TN) / results_cnt) + '\n')
                    fout.write('FP for ' + m + ': ' + str(float(FP) / results_cnt) + '\n')
                    fout.write('FN for ' + m + ': ' + str(float(FN) / results_cnt) + '\n')
                    

                    fout.write('\n') # an empty line as separation

                    fout.write('Dice (skull stripped) for ' + m + ': ' + str(dice_proc_sum / results_cnt) + '\n')
                    fout.write('Jaccard (skull stripped) for ' + m + ': ' + str(jaccard_proc_sum / results_cnt) + '\n')
                    fout.write('TP (skull stripped) for ' + m + ': ' + str(float(TP_proc) / results_cnt) + '\n')
                    fout.write('TN (skull stripped) for ' + m + ': ' + str(float(TN_proc) / results_cnt) + '\n')
                    fout.write('FP (skull stripped) for ' + m + ': ' + str(float(FP_proc) / results_cnt) + '\n')
                    fout.write('FN (skull stripped) for ' + m + ': ' + str(float(FN_proc) / results_cnt) + '\n')
                    
                    fout.write('\n') # an empty line as separation

                    fout.write('Dice (skull stripped on mask) for ' + m + ': ' + str(dice_mask_sum / results_cnt) + '\n')
                    fout.write('Jaccard (skull stripped on mask) for ' + m + ': ' + str(jaccard_mask_sum / results_cnt) + '\n')
                    fout.write('TP (skull stripped on mask) for ' + m + ': ' + str(float(TP_mask) / results_cnt) + '\n')
                    fout.write('TN (skull stripped on mask) for ' + m + ': ' + str(float(TN_mask) / results_cnt) + '\n')
                    fout.write('FP (skull stripped on mask) for ' + m + ': ' + str(float(FP_mask) / results_cnt) + '\n')
                    fout.write('FN (skull stripped on mask) for ' + m + ': ' + str(float(FN_mask) / results_cnt) + '\n')

                    fout.write('\n') # an empty line as separation

                    # for FCM-based
                    if (m is 'fcm' or m is 'flicm'):
                        fout.write('Number of underestimation for ' + m + ': ' + str(underest_cnt) + '\n')
                        fout.write('Number of underestimation (skull stripped) for ' + m + ': ' + str(underest_proc_cnt) + '\n')

                fout.close()


            elif (d is 'brats'):
                # init
                results_cnt = [0] * len(TYPES)

                time_sum = [0.0] * len(TYPES)
                
                dice_sum = [0.0] * len(TYPES)
                jaccard_sum = [0.0] * len(TYPES)
                TP = [0] * len(TYPES)
                TN = [0] * len(TYPES)
                FP = [0] * len(TYPES)
                FN = [0] * len(TYPES)

                dice_t_sum = [0.0] * len(TYPES)
                jaccard_t_sum = [0.0] * len(TYPES)
                TP_t = [0] * len(TYPES)
                TN_t = [0] * len(TYPES)
                FP_t = [0] * len(TYPES)
                FN_t = [0] * len(TYPES)

                # for FCM-based
                if (m is 'fcm' or m is 'flicm'):
                    underest_cnt = [0] * len(TYPES)

                # iterate over files
                for subdir, dirs, files in os.walk(result_dir):
                    for filename in files:
                        filepath = subdir + os.sep + filename

                        if filepath.endswith('.txt'):
                            for t_i, t_val in enumerate(TYPES):
                                if (m in filename and t_val in filename):
                                    # a filter to separate t1 and t1ce
                                    if (t_val is 't1' and 't1ce' in filename):
                                        continue

                                    # update numbers
                                    results_cnt[t_i] = results_cnt[t_i] + 1

                                    # read lines
                                    fin = open(filepath, 'r')
                                    lines = fin.readlines()
                                    fin.close()

                                    # offset for FCM-based
                                    offset = 0
                                    if (m is 'fcm' or m is 'flicm'):
                                        offset = 1

                                    # iteration (line 1)
                                    if (offset > 0):
                                        if (str(0.0000000) not in lines[0] and str(0.0000001) not in lines[0]):
                                            underest_cnt[t_i] = underest_cnt[t_i] + 1
                                    
                                    # time (line 2/1)
                                    time_sum[t_i] = time_sum[t_i] + float(lines[0 + offset].replace('Time: ', '').replace('\n', ''))

                                    # Dice (line 3/2)
                                    dice_sum[t_i] = dice_sum[t_i] + float(lines[1 + offset].replace('Dice: ', '').replace('\n', ''))

                                    # Jaccard (line 4/3)
                                    jaccard_sum[t_i] = jaccard_sum[t_i] + float(lines[2 + offset].replace('Jaccard: ', '').replace('\n', ''))

                                    # statistics (line 5/4)
                                    match = re.search(r'TP = ([0-9]+), TN = ([0-9]+), FP = ([0-9]+), FN = ([0-9]+)', lines[3 + offset])
                                    TP[t_i] = TP[t_i] + int(match.group(1))
                                    TN[t_i] = TN[t_i] + int(match.group(2))
                                    FP[t_i] = FP[t_i] + int(match.group(3))
                                    FN[t_i] = FN[t_i] + int(match.group(4))

                                    if (t_val is 't1' or t_val is 't1ce' or t_val is 't2'):
                                        # Dice for type (line 8/7)
                                        dice_t_sum[t_i] = dice_t_sum[t_i] + float(lines[6 + offset].replace('Dice (', '').replace(t_val + '): ', '').replace('\n', ''))

                                        # Jaccard for type (line 9/8)
                                        jaccard_t_sum[t_i] = jaccard_t_sum[t_i] + float(lines[7+ offset].replace('Jaccard (', '').replace(t_val + '): ', '').replace('\n', ''))

                                        # statistics for type (line 10/9)
                                        match = re.search(r'TP = ([0-9]+), TN = ([0-9]+), FP = ([0-9]+), FN = ([0-9]+)', lines[8 + offset])
                                        TP_t[t_i] = TP_t[t_i] + int(match.group(1))
                                        TN_t[t_i] = TN_t[t_i] + int(match.group(2))
                                        FP_t[t_i] = FP_t[t_i] + int(match.group(3))
                                        FN_t[t_i] = FN_t[t_i] + int(match.group(4))
                
                # output
                fout = open(output_file, 'w')

                for t_i, t_val in enumerate(TYPES):

                    if (results_cnt[t_i] == 0):
                        continue

                    fout.write('Number of images for ' + m + ' on ' + t_val + ': ' + str(results_cnt[t_i]) + '\n')

                    fout.write('Time for ' + m + ' on ' + t_val + ': ' + str(time_sum[t_i] / results_cnt[t_i]) + '\n')

                    fout.write('Dice for ' + m + ' on ' + t_val + ': ' + str(dice_sum[t_i] / results_cnt[t_i]) + '\n')
                    fout.write('Jaccard for ' + m + ' on ' + t_val + ': ' + str(jaccard_sum[t_i] / results_cnt[t_i]) + '\n')

                    fout.write('TP for ' + m + ' on ' + t_val + ': ' + str(float(TP[t_i]) / results_cnt[t_i]) + '\n')
                    fout.write('TN for ' + m + ' on ' + t_val + ': ' + str(float(TN[t_i]) / results_cnt[t_i]) + '\n')
                    fout.write('FP for ' + m + ' on ' + t_val + ': ' + str(float(FP[t_i]) / results_cnt[t_i]) + '\n')
                    fout.write('FN for ' + m + ' on ' + t_val + ': ' + str(float(FN[t_i]) / results_cnt[t_i]) + '\n')
                    
                    fout.write('\n') # an empty line as separation
                    
                    if (t_val is 't1' or t_val is 't1ce' or t_val is 't2'):
                        fout.write('Dice for ' + m + ' on ' + t_val + ' (specific): ' + str(dice_t_sum[t_i] / results_cnt[t_i]) + '\n')
                        fout.write('Jaccard for ' + m + ' on ' + t_val + ' (specific): ' + str(jaccard_t_sum[t_i] / results_cnt[t_i]) + '\n')
                        fout.write('TP for ' + m + ' on ' + t_val + ' (specific): ' + str(float(TP_t[t_i]) / results_cnt[t_i]) + '\n')
                        fout.write('TN for ' + m + ' on ' + t_val + ' (specific): ' + str(float(TN_t[t_i]) / results_cnt[t_i]) + '\n')
                        fout.write('FP for ' + m + ' on ' + t_val + ' (specific): ' + str(float(FP_t[t_i]) / results_cnt[t_i]) + '\n')
                        fout.write('FN for ' + m + ' on ' + t_val + ' (specific): ' + str(float(FN_t[t_i]) / results_cnt[t_i]) + '\n')

                    # for FCM-based
                    if (m is 'fcm' or m is 'flicm'):
                        fout.write('Number of underestimation for ' + m + ' on ' + t_val + ': ' + str(underest_cnt[t_i]) + '\n')

                    fout.write('\n') # an empty line as separation

                fout.close()