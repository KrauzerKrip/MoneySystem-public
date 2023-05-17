import sys

from Database import database


class taxSystem:
    """docstring for taxSystem"""

    def __init__(self, logger, technical, database_path):
        self.logger = logger
        self.technical = technical
        self.database_path = database_path


    def tax_collection_for_individuals(self, TaxIndividualCitizen, TaxIndividualMigrant):


        # Make an instance of the class to work with the database.
        tax_collection = database.DataBase(float(TaxIndividualCitizen), float(TaxIndividualMigrant), self.logger, self.database_path)

        citizensCashesCommon = 0  # The variable of sum of the cashes of citizens.
        migrantsCashesCommon = 0  # The variable of sum of the cashes of migrants.

        # Select the cashes of citizens and migrants. 
        citizensCashes = tax_collection.citizensCashesDiscover()
        migrantsCashes = tax_collection.migrantsCashesDiscover()

        # Subtract the tax sum from the cash of citizens and migrants.  
        tax_collection.subtractTaxes()

        NotifCitizensDict = {}  # The dictionary with VK IDs (keys) of citizens and the theirs tax sums (cash - cash * TaxIndividualCitizen) (values).
        NotifMigrantsDict = {}  # The dictionary with VK IDs (keys) of migrants and the theirs tax sums (cash - cash * TaxIndividualMigrant) (values).

        # Sum the citizens cashes.
        for tuples in citizensCashes:

            # Logger
            self.logger.info("\nTHE TUPLE IN citizensCashes LIST --->" + str(tuples))
            self.logger.info("THE CITIZEN CASH IN TUPLE --->" + str(tuples[1]))

            # The sum of the all citizenss cashes
            citizensCashesCommon = citizensCashesCommon + int(tuples[1])

            # Dictionary with citizens to notificate: {user_id : his tax sum}
            NotifCitizensDict[tuples[0]] = (tuples[1] * float(TaxIndividualCitizen))  # In the fact it is "cash * TaxIndividualCitizen".


        # Sum the migrants cashes.
        for tuples in migrantsCashes:

            # Logger
            self.logger.info("\nTHE TUPLE IN migrantsCashes LIST --->" + str(tuples))
            self.logger.info("THE MIGRANT CASH IN TUPLE --->" + str(tuples[1]))

            # The sum of the all migrants cashes
            migrantsCashesCommon = migrantsCashesCommon + int(tuples[1])

            # Dictionary with migrants to notificate: {user_id : his tax sum}
            NotifMigrantsDict[tuples[0]] = (tuples[1] * float(TaxIndividualMigrant))  # In the fact it is "cash * TaxIndividualMigrant".


        # Add to the central bank cash the sum of the cashes of citizens and migrants.            
        tax_collection.addToCentralBank(citizensCashesCommon, migrantsCashesCommon)


        # The log system

        self.logger.info("THE LIST OF CITIZENS` CASHES ---> " + str(citizensCashes))  # Logger
        self.logger.info("THE LIST OF MIGRANTS` CASHES ---> " + str(migrantsCashes))  # Logger


        self.logger.info("THE SUM OF CITIZENS` CASHES ---> " + str(citizensCashesCommon * 0.14))  # Logger
        self.logger.info("THE SUM OF MIGRANTS` CASHES ---> " + str(migrantsCashesCommon * 0.20))  # Logger


        # Notificate the citizens
        for key in NotifCitizensDict:

            self.technical.senderUserWarn(int(key), True, f"Здравствуйте! \nАвтоплатёж НФЛ: {round(NotifCitizensDict[key])}kr. \nСчастливого Вам дня!")

        # Notificate the migrants
        for key in NotifMigrantsDict:

            self.technical.senderUserWarn(int(key), True, f"Здравствуйте! \nАвтоплатёж НФЛ: {round(NotifMigrantsDict[key])}kr. \nСчастливого Вам дня!")