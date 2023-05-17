from database import DataBase
# import sqlite3
# from config_work import configWork

#db = DataBase()
#tax_collection = tax_collection_for_individuals_db()

"""
MAYBE IT WILL BE USEFUL IN THE FUTURE, BUT DON`T TOUCH IT NOW. 
THIS FILE DOESN`T WORK.

"""




class taxSystem:
    """docstring for taxSystem"""

    # def __init__(self):
    #     """There are connection to the database and the cursor."""
    #     self.database = sqlite3.connect(".db")
    #     #self.database.row_factory = sqlite3.Row
    #     self.sql = self.database.cursor()

    def tax_collection_for_individuals(self, TaxIndividualCitizen, TaxIndividualMigrant, logger):


        # Make an instance of the class to work with the database.
        tax_collection = DataBase(float(TaxIndividualCitizen), float(TaxIndividualMigrant))

        citizensCashesCommon = 0  # The variable of sum of the cashes of citizens.
        migrantsCashesCommon = 0  # The variable of sum of the cashes of migrants.

        # Select the cashes of citizens and migrants. 
        citizensCashes = tax_collection.citizensCashesDiscover()
        migrantsCashes = tax_collection.migrantsCashesDiscover()

        # Subtract the tax sum from the cash of citizens and migrants.  
        tax_collection.subtractTaxes()

        # Sum the citizens cashes.
        for tuples in citizensCashes:
            for citizenCash in tuples:
                citizensCashesCommon = citizensCashesCommon + int(citizenCash)

        # Sum the migrants cashes.
        for tuples in migrantsCashes:
            logger.info("\nTHE TUPLE IN migrantsCashes LIST --->" + str(tuples))  # Logger
            for migrantCash in tuples:
                logger.info("THE MIGRANT CASH IN TUPLE --->" + str(migrantCash))  # Logger
                migrantsCashesCommon = migrantsCashesCommon + int(migrantCash)

        # Add to the central bank cash the sum of the cashes of citizens and migrants.            
        tax_collection.addToCentralBank(citizensCashesCommon, migrantsCashesCommon)


        # The log system


        logger.info("THE LIST OF CITIZENS` CASHES ---> " + str(citizensCashes))  # Logger
        logger.info("THE LIST OF MIGRANTS` CASHES ---> " + str(migrantsCashes))  # Logger


        logger.info("THE SUM OF CITIZENS` CASHES ---> " + str(citizensCashesCommon * 0.14))  # Logger
        logger.info("THE SUM OF MIGRANTS` CASHES ---> " + str(migrantsCashesCommon * 0.20))  # Logger