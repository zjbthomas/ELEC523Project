import os

# parameters
RESULT_DIR = 'E:\\eDocs\\PhD\\Y1S1\\ELEC523\\Project\\results\\brats\\'
OUTPUT_FILE = 'E:\\eDocs\\PhD\\Y1S1\\ELEC523\\Project\\results\\brats.txt'
DATASET = 'brats' # cjdata; brats;
METHOD = 'flicm' # otsu; fcm; flicm;

# constants
TYPES = ['flair', 't1', 't2', 't1ce']

if (DATASET is 'cjdata'):
    # init
    results_cnt = 0
    dice_sum = 0.0
    dice_proc_sum = 0.0
    dice_mask_sum = 0.0
    jaccard_sum = 0.0
    jaccard_proc_sum = 0.0
    jaccard_mask_sum = 0.0
    time_sum = 0.0
    time_proc_sum = 0.0

    # for FCM-based
    if (METHOD is 'fcm' or METHOD is 'flicm'):
        underest_cnt = 0
        underest_proc_cnt = 0

    # iterate over files
    for subdir, dirs, files in os.walk(RESULT_DIR):
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
                offset = False
                if (METHOD is 'fcm' or METHOD is 'flicm'):
                    offset = True

                # iteration (lines 1 and 3)
                if (offset):
                    if (str(0.0000000) not in lines[0] and str(0.0000001) not in lines[0]):
                        underest_cnt = underest_cnt + 1
                    if (str(0.0000000) not in lines[2] and str(0.0000001) not in lines[2]):
                        underest_proc_cnt = underest_proc_cnt + 1
                
                # time (lines 2/1 and line 4/2)
                if (offset):
                    time_sum = time_sum + float(lines[1].replace('Time: ', '').replace('\n', ''))
                    time_proc_sum = time_proc_sum + float(lines[3].replace('Time (skull stripped): ', '').replace('\n', ''))
                else:
                    time_sum = time_sum + float(lines[0].replace('Time: ', '').replace('\n', ''))
                    time_proc_sum = time_proc_sum + float(lines[1].replace('Time (skull stripped): ', '').replace('\n', ''))

                # Dice (lines 5/3, 7/5, and 9/7)
                if (offset):
                    dice_sum = dice_sum + float(lines[4].replace('Dice: ', '').replace('\n', ''))
                    dice_proc_sum = dice_proc_sum + float(lines[6].replace('Dice (skull stripped): ', '').replace('\n', ''))
                    dice_mask_sum = dice_mask_sum + float(lines[8].replace('Dice (skull stripped on mask): ', '').replace('\n', ''))
                else:
                    dice_sum = dice_sum + float(lines[2].replace('Dice: ', '').replace('\n', ''))
                    dice_proc_sum = dice_proc_sum + float(lines[4].replace('Dice (skull stripped): ', '').replace('\n', ''))
                    dice_mask_sum = dice_mask_sum + float(lines[6].replace('Dice (skull stripped on mask): ', '').replace('\n', ''))

                # Jaccard (lines 6/4, 8/6, 10/8)
                if (offset):
                    jaccard_sum = jaccard_sum + float(lines[5].replace('Jaccard: ', '').replace('\n', ''))
                    jaccard_proc_sum = jaccard_proc_sum + float(lines[7].replace('Jaccard (skull stripped): ', '').replace('\n', ''))
                    jaccard_mask_sum = jaccard_mask_sum + float(lines[9].replace('Jaccard (skull stripped on mask): ', '').replace('\n', ''))
                else:
                    jaccard_sum = jaccard_sum + float(lines[3].replace('Jaccard: ', '').replace('\n', ''))
                    jaccard_proc_sum = jaccard_proc_sum + float(lines[5].replace('Jaccard (skull stripped): ', '').replace('\n', ''))
                    jaccard_mask_sum = jaccard_mask_sum + float(lines[7].replace('Jaccard (skull stripped on mask): ', '').replace('\n', ''))

                fin.close()

    # output
    fout = open(OUTPUT_FILE, 'w')

    if (results_cnt != 0):
        fout.write('Number of images for ' + METHOD + ': ' + str(results_cnt) + '\n')

        fout.write('\n')

        fout.write('Dice for ' + METHOD + ': ' + str(dice_sum / results_cnt) + '\n')
        fout.write('Jaccard for ' + METHOD + ': ' + str(jaccard_sum / results_cnt) + '\n')
        fout.write('Time for ' + METHOD + ': ' + str(time_sum / results_cnt) + '\n')

        fout.write('\n')

        fout.write('Dice (skull stripped) for ' + METHOD + ': ' + str(dice_proc_sum / results_cnt) + '\n')
        fout.write('Jaccard (skull stripped) for ' + METHOD + ': ' + str(jaccard_proc_sum / results_cnt) + '\n')
        fout.write('Time (skull stripped) for ' + METHOD + ': ' + str(time_proc_sum / results_cnt) + '\n')

        fout.write('\n')

        fout.write('Dice (skull stripped on mask) for ' + METHOD + ': ' + str(dice_mask_sum / results_cnt) + '\n')
        fout.write('Jaccard (skull stripped on mask) for ' + METHOD + ': ' + str(jaccard_mask_sum / results_cnt) + '\n')

        fout.write('\n')

        # for FCM-based
        if (METHOD is 'fcm' or METHOD is 'flicm'):
            fout.write('Number of underestimation for ' + METHOD + ': ' + str(underest_cnt) + '\n')
            fout.write('Number of underestimation (skull stripped) for ' + METHOD + ': ' + str(underest_proc_cnt) + '\n')

    fout.close()


elif (DATASET is 'brats'):
    # init
    results_cnt = [0] * len(TYPES)
    dice_sum = [0.0] * len(TYPES)
    jaccard_sum = [0.0] * len(TYPES)
    time_sum = [0.0] * len(TYPES)

    # for FCM-based
    if (METHOD is 'fcm' or METHOD is 'flicm'):
        underest_cnt = [0] * len(TYPES)

    # iterate over files
    for subdir, dirs, files in os.walk(RESULT_DIR):
        for filename in files:
            filepath = subdir + os.sep + filename

            if filepath.endswith('.txt'):
                for t_i, t_val in enumerate(TYPES):
                    if (METHOD in filename and t_val in filename):
                        # update numbers
                        results_cnt[t_i] = results_cnt[t_i] + 1

                        # read lines
                        fin = open(filepath, 'r')
                        lines = fin.readlines()
                        fin.close()

                        # offset for FCM-based
                        offset = False
                        if (METHOD is 'fcm' or METHOD is 'flicm'):
                            offset = True

                        # iteration (line 1)
                        if (offset):
                            if (str(0.0000000) not in lines[0] and str(0.0000001) not in lines[0]):
                                underest_cnt[t_i] = underest_cnt[t_i] + 1
                        
                        # time (line 2/1)
                        if (offset):
                            time_sum[t_i] = time_sum[t_i] + float(lines[1].replace('Time: ', '').replace('\n', ''))
                        else:
                            time_sum[t_i] = time_sum[t_i] + float(lines[0].replace('Time: ', '').replace('\n', ''))

                        # Dice (line 3/2)
                        if (offset):
                            dice_sum[t_i] = dice_sum[t_i] + float(lines[2].replace('Dice: ', '').replace('\n', ''))
                        else:
                            dice_sum[t_i] = dice_sum[t_i] + float(lines[1].replace('Dice: ', '').replace('\n', ''))

                        # Jaccard (line 4/3)
                        if (offset):
                            jaccard_sum[t_i] = jaccard_sum[t_i] + float(lines[3].replace('Jaccard: ', '').replace('\n', ''))
                        else:
                            jaccard_sum[t_i] = jaccard_sum[t_i] + float(lines[2].replace('Jaccard: ', '').replace('\n', ''))
    # output
    fout = open(OUTPUT_FILE, 'w')

    for t_i, t_val in enumerate(TYPES):

        if (results_cnt[t_i] == 0):
            continue

        fout.write('Number of images for ' + METHOD + ' on ' + t_val + ': ' + str(results_cnt[t_i]) + '\n')
        fout.write('Dice for ' + METHOD + ' on ' + t_val + ': ' + str(dice_sum[t_i] / results_cnt[t_i]) + '\n')
        fout.write('Jaccard for ' + METHOD + ' on ' + t_val + ': ' + str(jaccard_sum[t_i] / results_cnt[t_i]) + '\n')
        fout.write('Time for ' + METHOD + ' on ' + t_val + ': ' + str(time_sum[t_i] / results_cnt[t_i]) + '\n')

        # for FCM-based
        if (METHOD is 'fcm' or METHOD is 'flicm'):
            fout.write('Number of underestimation for ' + METHOD + ' on ' + t_val + ': ' + str(underest_cnt[t_i]) + '\n')

        fout.write('\n') # an empty line as separation

    fout.close()