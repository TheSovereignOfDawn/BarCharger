def getPlatesManagement(desiredWeight, isBodyweightMovement, areCalibratedStopPlatesUsed, isRecord):
    availablePlateWeightList = [25, 20, 15, 10, 5, 2.5, 1.25]
    nPlateWeightRequiredDict = {}
    isDesiredWeightOk = True
    minimumBodyweightMovementIncrement = 1.25
    if (isRecord):
        minimumBodyweightMovementIncrement = 0.25
        recordPlates = [0.5, 0.25]
        for plate in recordPlates:
            availablePlateWeightList.append(plate)
    minimumBarMovementIncrement = 2 * minimumBodyweightMovementIncrement
    if (isBodyweightMovement == True and desiredWeight % minimumBodyweightMovementIncrement == 0):
        restWeight = desiredWeight
        for plateWeight in availablePlateWeightList:
            nPlateWeightRequiredDict[str(plateWeight)], restWeight = getNumberOfSimilarPlates(restWeight, plateWeight)
    elif (desiredWeight % minimumBarMovementIncrement == 0):
        if (areCalibratedStopPlatesUsed):
            restWeight = ((desiredWeight - 20) / 2) - 2.5
        else:
            restWeight = (desiredWeight - 20) / 2
        for plateWeight in availablePlateWeightList:
            nPlateWeightRequiredDict[str(plateWeight)], restWeight = getNumberOfSimilarPlates(restWeight, plateWeight)
    else:
        isDesiredWeightOk = False

    return nPlateWeightRequiredDict, isDesiredWeightOk

def getNumberOfSimilarPlates(restWeight, desiredPlateWeight):
    nPlate = int(restWeight / desiredPlateWeight)
    restWeight = restWeight % desiredPlateWeight

    return nPlate, restWeight



