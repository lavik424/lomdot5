import mainPreprocessing




def chooseColumns(currCols,oldCols):
    modeSuffix = 'FillByModeInt'
    onehotSuffix = 'FillByMode_'
    meanSuffix = 'FillByMean'
    meadianSuffix = 'FillByMedian'
    nanSuffix = '_nan'
    # currList= list of original cols name, res= set of cols to continue with
    res = [colName for colName in currCols if onehotSuffix in colName]
    res += [colName for colName in currCols if (meadianSuffix in colName) & (meanSuffix not in colName)]
    currListMode = [colName for colName in oldCols if (colName + modeSuffix) in currCols]
    res += [(colName + modeSuffix) for colName in currListMode]
    currListMean = [colName for colName in oldCols if ((colName + meanSuffix) in currCols) & (colName not in currListMode)]
    res += [(colName + meanSuffix) for colName in currListMean if (colName + meadianSuffix) not in res]
    res = [colName for colName in res if nanSuffix not in colName]
    return res


def chooseRightColumns(colsAfterWork):
    """

    :param colsAfterWork: the names of columns without nan
    :return: list with the relevant features
    """
    rightList = ["Yearly_IncomeKFillByMean" ,"Number_of_valued_Kneset_membersFillByMedian",
                 "Overall_happiness_scoreFillByMean" ,"Garden_sqr_meter_per_person_in_residancy_areaFillByMean",
                 "Most_Important_IssueFillByMode_" ,"Weighted_education_rank",
                 "Will_vote_only_large_partyFillByMode_" ,"Avg_Satisfaction_with_previous_vote"]
    res = []
    for feature in rightList:
        for oldFeat in colsAfterWork:
            if feature in oldFeat:
                res.append(oldFeat)
    return res



def loadEnvirment(onlyRightCols = True):
    """

    :return: 6 dataFrames of train, validarion and test x/y
    """

    df = pd.read_csv("./input/ElectionsData.csv")
    oldCols = df.columns

    ## load tables from prev hw
    x_train = pd.read_csv("./input/x_train.csv" ,index_col=0)
    x_val = pd.read_csv("./input/x_val.csv", index_col=0)
    x_test = pd.read_csv("./input/x_test.csv", index_col=0)
    y_train = pd.read_csv("./input/y_train.csv" ,index_col=0)
    y_val = pd.read_csv("./input/y_val.csv", index_col=0)
    y_test = pd.read_csv("./input/y_test.csv", index_col=0)

    final_test = pd.read_csv("./input/final_test.csv", index_col='IdentityCard_Num')

    # choose the correct set of features
    colsAfterWork = chooseColumns(x_train.columns, oldCols)
    x_train = x_train[colsAfterWork]
    x_val = x_val[colsAfterWork]
    x_test = x_test[colsAfterWork]
    final_test = final_test[colsAfterWork]

    if onlyRightCols:
        rightFeatures = chooseRightColumns(colsAfterWork)
        x_train = x_train[rightFeatures]
        x_val = x_val[rightFeatures]
        x_test = x_test[rightFeatures]
        final_test = final_test[rightFeatures]

    return x_train, x_val, x_test, y_train, y_val, y_test, final_test

def main():
    mainPreprocessing.main(method='replacement')

    (x_train, x_val, x_test, y_train, y_val, y_test, final_test) = loadEnvirment()

if __name__ == '__main__':
    main()