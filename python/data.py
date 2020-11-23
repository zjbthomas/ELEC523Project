import os
import re
import math

# parameters
RESULT_BASE = 'E:\\eDocs\\PhD\\Y1S1\\ELEC523\\Project\\results\\'
DATASETS = ['brats', 'cjdata'] # cjdata; brats;
METHODS = ['otsun'] # otsu; otsun; fcm; flicm;
CNUMS = [5]
USECACHE = False

# constants
TYPES = ['flair', 't1', 't2', 't1ce']

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

                nan_cnt = 0
                nan_path = []
                nan_proc_cnt = 0
                nan_proc_path = []
                nan_mask_cnt = 0
                nan_mask_path = []

                time_sum = 0.0
                time_proc_sum = 0.0

                dice_sum = 0.0
                dice_mo_sum = 0.0
                dice_proc_sum = 0.0
                dice_proc_mo_sum = 0.0
                dice_mask_sum = 0.0
                dice_mask_mo_sum = 0.0

                jaccard_sum = 0.0
                jaccard_mo_sum = 0.0
                jaccard_proc_sum = 0.0
                jaccard_proc_mo_sum = 0.0
                jaccard_mask_sum = 0.0
                jaccard_mask_mo_sum = 0.0

                TP = 0
                TN = 0
                FP = 0
                FN = 0

                TP_mo = 0
                TN_mo = 0
                FP_mo = 0
                FN_mo = 0

                TP_proc = 0
                TN_proc = 0
                FP_proc = 0
                FN_proc = 0

                TP_proc_mo = 0
                TN_proc_mo = 0
                FP_proc_mo = 0
                FN_proc_mo = 0

                TP_mask = 0
                TN_mask = 0
                FP_mask = 0
                FN_mask = 0

                TP_mask_mo = 0
                TN_mask_mo = 0
                FP_mask_mo = 0
                FN_mask_mo = 0
                
                # for FCM-based
                if (not USECACHE):
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

                            # top offset (empty line included)
                            if (not USECACHE):
                                if (m is 'fcm' or m is 'flicm'):
                                    offset = 5
                                else:
                                    offset = 3
                            else:
                                offset = 1

                            # mask offset
                            if (m is 'otsun' or m is 'fcm' or m is 'flicm'):
                                match = re.search(r'mask ([0-9]+)', lines[offset + 32 * c])
                            else:
                                match = re.search(r'mask ([0-9]+)', lines[offset + 64])
                            mask_offset = 32 * (int(match.group(1)) - 1)

                            if (not USECACHE):
                                # iteration (lines 1 and 3)
                                if (m is 'fcm' or m is 'flicm'):
                                    # iteration (lines 1 and 3)
                                    if (str(0.0000000) not in lines[0] and str(0.0000001) not in lines[0]):
                                        underest_cnt = underest_cnt + 1
                                    if (str(0.0000000) not in lines[2] and str(0.0000001) not in lines[2]):
                                        underest_proc_cnt = underest_proc_cnt + 1
                                
                                    # time (lines 2 and line 4/2)
                                    time_sum = time_sum + float(lines[1].replace('Time: ', '').replace('\n', ''))
                                    time_proc_sum = time_proc_sum + float(lines[3].replace('Time (skull stripped): ', '').replace('\n', ''))
                                else:
                                    # time (lines 1 and line 2)
                                    time_sum = time_sum + float(lines[0].replace('Time: ', '').replace('\n', ''))
                                    time_proc_sum = time_proc_sum + float(lines[1].replace('Time (skull stripped): ', '').replace('\n', ''))

                            # Dice (inside mask lines 2, 12, 22)
                            dice_sum += float(lines[offset + mask_offset + 1].replace('Dice: ', '').replace('\n', ''))
                            dice_proc_sum += float(lines[offset + mask_offset + 11].replace('Dice (skull stripped): ', '').replace('\n', ''))
                            dice_mask_sum += float(lines[offset + mask_offset + 21].replace('Dice (skull stripped on mask): ', '').replace('\n', ''))

                            # Jaccard (inside mask lines 3, 13, 23)
                            jaccard_sum += float(lines[offset + mask_offset + 2].replace('Jaccard: ', '').replace('\n', ''))
                            jaccard_proc_sum += float(lines[offset + mask_offset + 12].replace('Jaccard (skull stripped): ', '').replace('\n', ''))
                            jaccard_mask_sum += jaccard_mask_sum + float(lines[offset + mask_offset + 22].replace('Jaccard (skull stripped on mask): ', '').replace('\n', ''))

                            # statistics (inside mask lines 4, 14, 24)
                            match = re.search(r'TP = ([0-9]+), TN = ([0-9]+), FP = ([0-9]+), FN = ([0-9]+)', lines[offset + mask_offset + 3])
                            TP += int(match.group(1))
                            TN += int(match.group(2))
                            FP += int(match.group(3))
                            FN += int(match.group(4))

                            match = re.search(r'TP = ([0-9]+), TN = ([0-9]+), FP = ([0-9]+), FN = ([0-9]+)', lines[offset + mask_offset + 13])
                            TP_proc += int(match.group(1))
                            TN_proc += int(match.group(2))
                            FP_proc += int(match.group(3))
                            FN_proc += int(match.group(4))

                            match = re.search(r'TP = ([0-9]+), TN = ([0-9]+), FP = ([0-9]+), FN = ([0-9]+)', lines[offset + mask_offset + 23])
                            TP_mask += int(match.group(1))
                            TN_mask += int(match.group(2))
                            FP_mask += int(match.group(3))
                            FN_mask += int(match.group(4))

                            # MO check (use Dice, inside mask line 7, 17, 27)
                            val = float(lines[offset + mask_offset + 6].replace('Dice (MO): ', '').replace('\n', ''))
                            if (math.isnan(val)):
                                nan_cnt = nan_cnt + 1
                                nan_path.append(filename.replace('.txt',''))
                            else:
                                # Dice
                                dice_mo_sum += val
                                # Jaccard (inside mask lines 8)
                                jaccard_mo_sum += float(lines[offset + mask_offset + 7].replace('Jaccard (MO): ', '').replace('\n', ''))
                                # statistics (inside mask lines 9)
                                match = re.search(r'TP = ([0-9]+), TN = ([0-9]+), FP = ([0-9]+), FN = ([0-9]+)', lines[offset + mask_offset + 8])
                                TP_mo += int(match.group(1))
                                TN_mo += int(match.group(2))
                                FP_mo += int(match.group(3))
                                FN_mo += int(match.group(4))

                            val = float(lines[offset + mask_offset + 16].replace('Dice (skull stripped, MO): ', '').replace('\n', ''))
                            if (math.isnan(val)):
                                nan_proc_cnt = nan_proc_cnt + 1
                                nan_proc_path.append(filename.replace('.txt',''))
                            else:
                                # Dice
                                dice_proc_mo_sum += val
                                # Jaccard (inside mask lines 18)
                                jaccard_proc_mo_sum += float(lines[offset + mask_offset + 17].replace('Jaccard (skull stripped, MO): ', '').replace('\n', ''))
                                # statistics (inside mask lines 19)
                                match = re.search(r'TP = ([0-9]+), TN = ([0-9]+), FP = ([0-9]+), FN = ([0-9]+)', lines[offset + mask_offset + 18])
                                TP_proc_mo += int(match.group(1))
                                TN_proc_mo += int(match.group(2))
                                FP_proc_mo += int(match.group(3))
                                FN_proc_mo += int(match.group(4))

                            val = float(lines[offset + mask_offset + 26].replace('Dice (skull stripped on mask, MO): ', '').replace('\n', ''))
                            if (math.isnan(val)):
                                nan_proc_cnt = nan_proc_cnt + 1
                                nan_proc_path.append(filename.replace('.txt',''))
                            else:
                                # Dice
                                dice_mask_mo_sum += val
                                # Jaccard (inside mask lines 28)
                                jaccard_mask_mo_sum += jaccard_mask_sum + float(lines[offset + mask_offset + 27].replace('Jaccard (skull stripped on mask, MO): ', '').replace('\n', ''))
                                # statistics (inside mask lines 29)
                                match = re.search(r'TP = ([0-9]+), TN = ([0-9]+), FP = ([0-9]+), FN = ([0-9]+)', lines[offset + mask_offset + 28])
                                TP_mask_mo += int(match.group(1))
                                TN_mask_mo += int(match.group(2))
                                FP_mask_mo += int(match.group(3))
                                FN_mask_mo += int(match.group(4))

                # output
                fout = open(output_file, 'w')

                if (results_cnt != 0):
                    fout.write('Number of images for ' + m + ': ' + str(results_cnt) + '\n')

                    fout.write('\n')

                    if (not USECACHE):
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

                    cnt = results_cnt - nan_cnt

                    fout.write('Dice (MO) for ' + m + ': ' + str(dice_mo_sum / cnt) + '\n')
                    fout.write('Jaccard (MO) for ' + m + ': ' + str(jaccard_mo_sum / cnt) + '\n')
                    fout.write('TP (MO) for ' + m + ': ' + str(float(TP_mo) / cnt) + '\n')
                    fout.write('TN (MO) for ' + m + ': ' + str(float(TN_mo) / cnt) + '\n')
                    fout.write('FP (MO) for ' + m + ': ' + str(float(FP_mo) / cnt) + '\n')
                    fout.write('FN (MO) for ' + m + ': ' + str(float(FN_mo) / cnt) + '\n')
                    
                    fout.write('Number of images with NaN: ' + str(nan_cnt) + '\n')
                    for p in nan_path:
                        fout.write(p + '\n')

                    fout.write('\n') # an empty line as separation

                    cnt = results_cnt - nan_proc_cnt

                    fout.write('Dice (skull stripped, MO) for ' + m + ': ' + str(dice_proc_mo_sum / cnt) + '\n')
                    fout.write('Jaccard (skull stripped, MO) for ' + m + ': ' + str(jaccard_proc_mo_sum / cnt) + '\n')
                    fout.write('TP (skull stripped, MO) for ' + m + ': ' + str(float(TP_proc_mo) / cnt) + '\n')
                    fout.write('TN (skull stripped, MO) for ' + m + ': ' + str(float(TN_proc_mo) / cnt) + '\n')
                    fout.write('FP (skull stripped, MO) for ' + m + ': ' + str(float(FP_proc_mo) / cnt) + '\n')
                    fout.write('FN (skull stripped, MO) for ' + m + ': ' + str(float(FN_proc_mo) / cnt) + '\n')
                    
                    fout.write('Number of images with NaN: ' + str(nan_proc_cnt) + '\n')
                    for p in nan_proc_path:
                        fout.write(p + '\n')

                    fout.write('\n') # an empty line as separation

                    cnt = results_cnt - nan_mask_cnt

                    fout.write('Dice (skull stripped on mask, MO) for ' + m + ': ' + str(dice_mask_mo_sum / cnt) + '\n')
                    fout.write('Jaccard (skull stripped on mask, MO) for ' + m + ': ' + str(jaccard_mask_mo_sum / cnt) + '\n')
                    fout.write('TP (skull stripped on mask, MO) for ' + m + ': ' + str(float(TP_mask_mo) / cnt) + '\n')
                    fout.write('TN (skull stripped on mask, MO) for ' + m + ': ' + str(float(TN_mask_mo) / cnt) + '\n')
                    fout.write('FP (skull stripped on mask, MO) for ' + m + ': ' + str(float(FP_mask_mo) / cnt) + '\n')
                    fout.write('FN (skull stripped on mask, MO) for ' + m + ': ' + str(float(FN_mask_mo) / cnt) + '\n')

                    fout.write('Number of images with NaN: ' + str(nan_mask_cnt) + '\n')
                    for p in nan_mask_path:
                        fout.write(p + '\n')

                    fout.write('\n') # an empty line as separation

                    # for FCM-based
                    if (not USECACHE):
                        if (m is 'fcm' or m is 'flicm'):
                            fout.write('Number of underestimation for ' + m + ': ' + str(underest_cnt) + '\n')
                            fout.write('Number of underestimation (skull stripped) for ' + m + ': ' + str(underest_proc_cnt) + '\n')

                fout.close()


            elif (d is 'brats'):
                # init
                results_cnt = [0] * len(TYPES)

                nan_cnt = [0] * len(TYPES)
                nan_path = {}

                nan_t_cnt = [0] * len(TYPES)
                nan_t_path = {}

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

                dice_mo_sum = [0.0] * len(TYPES)
                jaccard_mo_sum = [0.0] * len(TYPES)
                TP_mo = [0] * len(TYPES)
                TN_mo = [0] * len(TYPES)
                FP_mo = [0] * len(TYPES)
                FN_mo = [0] * len(TYPES)

                dice_t_mo_sum = [0.0] * len(TYPES)
                jaccard_t_mo_sum = [0.0] * len(TYPES)
                TP_t_mo = [0] * len(TYPES)
                TN_t_mo = [0] * len(TYPES)
                FP_t_mo = [0] * len(TYPES)
                FN_t_mo = [0] * len(TYPES)

                # for FCM-based
                if (not USECACHE):
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

                                    # top offset (empty line included)
                                    if (not USECACHE):
                                        if (m is 'fcm' or m is 'flicm'):
                                            offset = 3
                                        else:
                                            offset = 2
                                    else:
                                        offset = 1

                                    # mask offset
                                    if (m is 'otsun' or m is 'fcm' or m is 'flicm'):
                                        match = re.search(r'mask ([0-9]+)', lines[offset + 22 * c])
                                    else:
                                        match = re.search(r'mask ([0-9]+)', lines[offset + 44])
                                    mask_offset = 22 * (int(match.group(1)) - 1)

                                    if (not USECACHE):
                                        if (m is 'fcm' or m is 'flicm'):
                                            # iteration (line 1)
                                            if (str(0.0000000) not in lines[0] and str(0.0000001) not in lines[0]):
                                                underest_cnt[t_i] = underest_cnt[t_i] + 1
                                            # time (line 2)
                                            time_sum[t_i] = time_sum[t_i] + float(lines[1].replace('Time: ', '').replace('\n', ''))
                                        else:
                                            # time (line 1)
                                            time_sum[t_i] = time_sum[t_i] + float(lines[0].replace('Time: ', '').replace('\n', ''))

                                    # Dice (inside mask lines 2)
                                    dice_sum[t_i] = dice_sum[t_i] + float(lines[offset + mask_offset + 1].replace('Dice: ', '').replace('\n', ''))

                                    # Jaccard (inside mask lines 3)
                                    jaccard_sum[t_i] = jaccard_sum[t_i] + float(lines[offset + mask_offset + 2].replace('Jaccard: ', '').replace('\n', ''))

                                    # statistics (inside mask lines 4)
                                    match = re.search(r'TP = ([0-9]+), TN = ([0-9]+), FP = ([0-9]+), FN = ([0-9]+)', lines[offset + mask_offset + 3])
                                    TP[t_i] = TP[t_i] + int(match.group(1))
                                    TN[t_i] = TN[t_i] + int(match.group(2))
                                    FP[t_i] = FP[t_i] + int(match.group(3))
                                    FN[t_i] = FN[t_i] + int(match.group(4))

                                    # MO check (use Dice, inside mask line 7)
                                    val = float(lines[offset + mask_offset + 6].replace('Dice (MO): ', '').replace('\n', ''))
                                    if (math.isnan(val)):
                                        nan_cnt[t_i] = nan_cnt[t_i] + 1

                                        if (t_i in nan_path.keys()):
                                            l = nan_path[t_i]
                                            l.append(filename.replace('.txt',''))
                                            nan_path[t_i] = l
                                        else:
                                            nan_path[t_i] = [filename.replace('.txt','')]
                                    else:
                                        # Dice
                                        dice_mo_sum[t_i] = dice_mo_sum[t_i] + val
                                        # Jaccard (inside mask lines 8)
                                        jaccard_mo_sum[t_i] = jaccard_mo_sum[t_i] + float(lines[offset + mask_offset + 7].replace('Jaccard (MO): ', '').replace('\n', ''))
                                        # statistics (inside mask lines 9)
                                        match = re.search(r'TP = ([0-9]+), TN = ([0-9]+), FP = ([0-9]+), FN = ([0-9]+)', lines[offset + mask_offset + 8])
                                        TP_mo[t_i] = TP_mo[t_i] + int(match.group(1))
                                        TN_mo[t_i] = TN_mo[t_i] + int(match.group(2))
                                        FP_mo[t_i] = FP_mo[t_i] + int(match.group(3))
                                        FN_mo[t_i] = FN_mo[t_i] + int(match.group(4))

                                    if (t_val is 't1' or t_val is 't1ce' or t_val is 't2'):
                                        # Dice for type (inside mask lines 12)
                                        dice_t_sum[t_i] = dice_t_sum[t_i] + float(lines[offset + mask_offset + 11].replace('Dice (', '').replace(t_val + '): ', '').replace('\n', ''))

                                        # Jaccard for type (inside mask lines 13, 18)
                                        jaccard_t_sum[t_i] = jaccard_t_sum[t_i] + float(lines[offset + mask_offset + 12].replace('Jaccard (', '').replace(t_val + '): ', '').replace('\n', ''))

                                        # statistics for type (inside mask lines 14, 19)
                                        match = re.search(r'TP = ([0-9]+), TN = ([0-9]+), FP = ([0-9]+), FN = ([0-9]+)', lines[offset + mask_offset + 13])
                                        TP_t[t_i] = TP_t[t_i] + int(match.group(1))
                                        TN_t[t_i] = TN_t[t_i] + int(match.group(2))
                                        FP_t[t_i] = FP_t[t_i] + int(match.group(3))
                                        FN_t[t_i] = FN_t[t_i] + int(match.group(4))

                                        # MO check (use Dice, inside mask line 12)
                                        val = float(lines[offset + mask_offset + 16].replace('Dice (', '').replace(t_val + ', MO): ', '').replace('\n', ''))
                                        if (math.isnan(val)):
                                            nan_t_cnt[t_i] = nan_t_cnt[t_i] + 1

                                            if (t_i in nan_t_path.keys()):
                                                l = nan_t_path[t_i]
                                                l.append(filename.replace('.txt',''))
                                                nan_t_path[t_i] = l
                                            else:
                                                nan_t_path[t_i] = [filename.replace('.txt','')]
                                        else:
                                            # # Dice
                                            dice_t_mo_sum[t_i] = dice_t_mo_sum[t_i] + val
                                            # Jaccard (inside mask lines 18)
                                            jaccard_t_mo_sum[t_i] = jaccard_t_mo_sum[t_i] + float(lines[offset + mask_offset + 17].replace('Jaccard (', '').replace(t_val + ', MO): ', '').replace('\n', ''))
                                            # statistics (inside mask lines 19)
                                            match = re.search(r'TP = ([0-9]+), TN = ([0-9]+), FP = ([0-9]+), FN = ([0-9]+)', lines[offset + mask_offset + 18])
                                            TP_t_mo[t_i] = TP_t_mo[t_i] + int(match.group(1))
                                            TN_t_mo[t_i] = TN_t_mo[t_i] + int(match.group(2))
                                            FP_t_mo[t_i] = FP_t_mo[t_i] + int(match.group(3))
                                            FN_t_mo[t_i] = FN_t_mo[t_i] + int(match.group(4))
                
                # output
                fout = open(output_file, 'w')

                for t_i, t_val in enumerate(TYPES):

                    if (results_cnt[t_i] == 0):
                        continue

                    fout.write('Number of images for ' + m + ' on ' + t_val + ': ' + str(results_cnt[t_i]) + '\n')

                    if (not USECACHE):
                        fout.write('Time for ' + m + ' on ' + t_val + ': ' + str(time_sum[t_i] / results_cnt[t_i]) + '\n')

                    fout.write('Dice for ' + m + ' on ' + t_val + ': ' + str(dice_sum[t_i] / results_cnt[t_i]) + '\n')
                    fout.write('Jaccard for ' + m + ' on ' + t_val + ': ' + str(jaccard_sum[t_i] / results_cnt[t_i]) + '\n')

                    fout.write('TP for ' + m + ' on ' + t_val + ': ' + str(float(TP[t_i]) / results_cnt[t_i]) + '\n')
                    fout.write('TN for ' + m + ' on ' + t_val + ': ' + str(float(TN[t_i]) / results_cnt[t_i]) + '\n')
                    fout.write('FP for ' + m + ' on ' + t_val + ': ' + str(float(FP[t_i]) / results_cnt[t_i]) + '\n')
                    fout.write('FN for ' + m + ' on ' + t_val + ': ' + str(float(FN[t_i]) / results_cnt[t_i]) + '\n')
                    
                    fout.write('\n') # an empty line as separation

                    cnt = results_cnt[t_i] - nan_cnt[t_i]

                    fout.write('Dice (MO) for ' + m + ' on ' + t_val + ': ' + str(dice_mo_sum[t_i] / cnt) + '\n')
                    fout.write('Jaccard (MO) for ' + m + ' on ' + t_val + ': ' + str(jaccard_mo_sum[t_i] / cnt) + '\n')

                    fout.write('TP (MO) for ' + m + ' on ' + t_val + ': ' + str(float(TP_mo[t_i]) / cnt) + '\n')
                    fout.write('TN (MO) for ' + m + ' on ' + t_val + ': ' + str(float(TN_mo[t_i]) / cnt) + '\n')
                    fout.write('FP (MO) for ' + m + ' on ' + t_val + ': ' + str(float(FP_mo[t_i]) / cnt) + '\n')
                    fout.write('FN (MO) for ' + m + ' on ' + t_val + ': ' + str(float(FN_mo[t_i]) / cnt) + '\n')

                    fout.write('Number of images with NaN: ' + str(nan_cnt[t_i]) + '\n')
                    if (nan_cnt[t_i] != 0):
                        for p in nan_path[t_i]:
                            fout.write(p + '\n')

                    fout.write('\n') # an empty line as separation
                    
                    if (t_val is 't1' or t_val is 't1ce' or t_val is 't2'):
                        fout.write('Dice for ' + m + ' on ' + t_val + ' (specific): ' + str(dice_t_sum[t_i] / results_cnt[t_i]) + '\n')
                        fout.write('Jaccard for ' + m + ' on ' + t_val + ' (specific): ' + str(jaccard_t_sum[t_i] / results_cnt[t_i]) + '\n')
                        fout.write('TP for ' + m + ' on ' + t_val + ' (specific): ' + str(float(TP_t[t_i]) / results_cnt[t_i]) + '\n')
                        fout.write('TN for ' + m + ' on ' + t_val + ' (specific): ' + str(float(TN_t[t_i]) / results_cnt[t_i]) + '\n')
                        fout.write('FP for ' + m + ' on ' + t_val + ' (specific): ' + str(float(FP_t[t_i]) / results_cnt[t_i]) + '\n')
                        fout.write('FN for ' + m + ' on ' + t_val + ' (specific): ' + str(float(FN_t[t_i]) / results_cnt[t_i]) + '\n')

                        fout.write('\n') # an empty line as separation

                        cnt = results_cnt[t_i] - nan_t_cnt[t_i]

                        fout.write('Dice (MO) for ' + m + ' on ' + t_val + ' (specific): ' + str(dice_t_mo_sum[t_i] / cnt) + '\n')
                        fout.write('Jaccard (MO) for ' + m + ' on ' + t_val + ' (specific): ' + str(jaccard_t_mo_sum[t_i] / cnt) + '\n')
                        fout.write('TP (MO) for ' + m + ' on ' + t_val + ' (specific): ' + str(float(TP_t_mo[t_i]) / cnt) + '\n')
                        fout.write('TN (MO) for ' + m + ' on ' + t_val + ' (specific): ' + str(float(TN_t_mo[t_i]) / cnt) + '\n')
                        fout.write('FP (MO) for ' + m + ' on ' + t_val + ' (specific): ' + str(float(FP_t_mo[t_i]) / cnt) + '\n')
                        fout.write('FN (MO) for ' + m + ' on ' + t_val + ' (specific): ' + str(float(FN_t_mo[t_i]) / cnt) + '\n')

                        fout.write('Number of images with NaN: ' + str(nan_t_cnt[t_i]) + '\n')
                        if (nan_t_cnt[t_i] != 0):
                            for p in nan_t_path[t_i]:
                                fout.write(p + '\n')

                        fout.write('\n') # an empty line as separation

                    # for FCM-based
                    if (not USECACHE):
                        if (m is 'fcm' or m is 'flicm'):
                            fout.write('Number of underestimation for ' + m + ' on ' + t_val + ': ' + str(underest_cnt[t_i]) + '\n')

                    fout.write('\n') # an empty line as separation

                fout.close()