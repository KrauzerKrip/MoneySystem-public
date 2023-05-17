import sqlite3 


class DataBase:
    """
    For the work with the MyMoney database.

    """


    def __init__(self, TaxIndividualCitizen, TaxIndividualMigrant, logger, database_path):
        """
        There are connection to the database and the cursor.

        """
        self.database = sqlite3.connect(database_path)
        #self.database.row_factory = sqlite3.Row
        self.sql = self.database.cursor() #self.database.cursor()
        self.TaxIndividualCitizen = TaxIndividualCitizen
        self.TaxIndividualMigrant = TaxIndividualMigrant
        self.logger = logger


    def command(self, cmd):
        """
        For admin commands for the database.

        """
        with self.database:
            pass

    def citizenship(self, db_id, value):
        """
        For admin command to change the citizenship value.

        """
        with self.database:
            return self.sql.execute("UPDATE personal_accounts SET citizenship = ? WHERE id = ?", (value, int(db_id)))


    def add_account(self, user_id, name):
        """
        It can to add the new account to the database.

        """
        with self.database:
            return self.sql.execute("INSERT INTO personal_accounts (user_id, name) VALUES (?, ?)", (user_id, name))


    def account_exists(self, user_id, bd_id):
        """
        It can to check account existence.

        """
        with self.database:
            if user_id != None: 
                result = self.sql.execute("SELECT * FROM personal_accounts WHERE user_id = ?", (user_id,)).fetchall()
                return bool(len(result))
                return result
            elif bd_id != None:
                result = self.sql.execute("SELECT * FROM personal_accounts WHERE id = ?", (bd_id,)).fetchall()
                return bool(len(result))
                return result 


    def get_account_info(self, user_id, bd_id): 
        """
        Can get account info: id, cash, name and notificate.

        """
        with self.database:
            if user_id != None:
                result = self.sql.execute("SELECT id, cash, name, notificate FROM personal_accounts WHERE user_id = ?", (user_id,)).fetchall()
                return result
            elif user_id == None: 
                result = self.sql.execute("SELECT user_id, cash, name, notificate FROM personal_accounts WHERE id = ?", (bd_id,)).fetchall()
                return result


    def get_all_accounts(self, citizenship):
        """
        Can get user_id of all accounts which are migrants or citizens.

        """
        with self.database:
                return self.sql.execute("SELECT user_id FROM personal_accounts WHERE citizenship = ?", (citizenship,)).fetchall()


    def transfer_money(self, user_id, recipient_vk_id, cash_posted):
        """
        Transfers money (cash_posted) from user_id to recipient_id, where user_id - vk ID, but recipient_id - database ID.
        Returns: one list with one tuple inside, and inside this tuple is vk_id (int) of the recipient: ({1234567890}).

        """
        with self.database:
            self.sql.execute("UPDATE personal_accounts SET cash = cash+? WHERE user_id = ?", (int(cash_posted), recipient_vk_id))
            self.sql.execute("UPDATE personal_accounts SET cash = cash-? WHERE user_id = ?", (int(cash_posted), user_id))
            
            return "TRANSFERED"


    def set_money(self, id, cash_set):
        """
        Sets the cash to the user (id). It uses the database id.

        """
        with self.database:
            self.sql.execute("UPDATE personal_accounts SET cash = ? WHERE id = ?", (int(cash_set), id))

            return self.sql.execute("SELECT user_id FROM personal_accounts WHERE id = ?", (id,)).fetchall()


    def user_notification_update(self, user_id, notificate):
        """
        Updates the "notificate" column in the database. With this the user can turn on or turn off the notification.

        """
        with self.database:
            return self.sql.execute("UPDATE personal_accounts SET notificate = ? WHERE user_id = ?", (bool(notificate), int(user_id)))


    # Below is for the posts system

    def get_posts(self, post):
        """
        Get the list of posts.

        """
        with self.database:
            return self.sql.execute("SELECT * FROM posts WHERE post = ?", (post,)).fetchall()


    def set_post(self, post, worker):
        """
        Set the worker (worker) for the post (post).

        """        
        with self.database:
            return self.sql.execute("UPDATE posts SET worker = ? WHERE post = ?", (worker, post))


    # Below is for the tax system 

    def citizensCashesDiscover(self):
        """
        With this we can to know the cashes of all citizens.

        """
        with self.database:
            return self.sql.execute("SELECT user_id, cash FROM personal_accounts WHERE citizenship = ?", (True,)).fetchall()


    def migrantsCashesDiscover(self):
        """
        With this we can to know the cashes of all migrants.

        """
        with self.database:
            return self.sql.execute("SELECT user_id, cash FROM personal_accounts WHERE citizenship = ?", (False,)).fetchall()


    def subtractTaxes(self):
        """
        It subtracts the taxes summ from the cashes.

        """
        with self.database:
            self.sql.execute("UPDATE personal_accounts SET cash = cash-(cash*?) WHERE citizenship = ?", (self.TaxIndividualCitizen, True))
            self.sql.execute("UPDATE personal_accounts SET cash = cash-(cash*?) WHERE citizenship = ?", (self.TaxIndividualMigrant, False))


    def addToCentralBank(self, citizensCashesCommon, migrantsCashesCommon):
        """
        It adds to the central bank`s cash the all sum from the taxes.

        """

        taxSumFromCitizens = citizensCashesCommon * self.TaxIndividualCitizen
        taxSumFromMigrants = migrantsCashesCommon * self.TaxIndividualMigrant
        
        with self.database:

            # Adds taxes` sum from citizens to the central bank`s cash.
            self.sql.execute("UPDATE financial_system SET cb_cash = cb_cash+?", (taxSumFromCitizens,))

            # Adds taxes` sum from migrants to the central bank`s cash
            self.sql.execute("UPDATE financial_system SET cb_cash = cb_cash+?", (taxSumFromMigrants,))


    # Below is for the business system

    def business_add(self, business_id, business_name, business_type, business_leader):
        """
        Add the business to the business table. 

        """
        with self.database:
            self.sql.execute("INSERT INTO business (id, business_name, type, leader_id) VALUES (?, ?, ?, ?)", (business_id, business_name, business_type, business_leader))
            return f"BUSINESS ADD: \n\nID: {business_id}, \n\nNAME: {business_name}, \n\nTYPE: {business_type}, \n\nLEADER_VK_ID: {business_leader}."


    def business_delete(self, business_id):
        """
        Delete the business from the business table.

        """
        with self.database:
            business = self.sql.execute("SELECT * FROM business WHERE id = ?", (business_id,)).fetchall()

            # Check that business exists.
            if bool(len(business)) == True:
                self.sql.execute("DELETE FROM business WHERE id = ?", (business_id,))
                return f"BUSINESS DELETE: \n\n ID: {business_id}"

            else:
                return f"BUSINESS {business_id} DOESN`T EXIST."


    def business_withdraw(self, user_id, business_id, cash_withdraw):
        """
        It withdraws money from the business account and returns the result.

        """
        with self.database:

            # Check that the business account exists.
            if self.sql.execute("SELECT * FROM business WHERE id = ?", (business_id,)).fetchone() != None:
                
                if str(user_id) == str((self.sql.execute("SELECT leader_id FROM business WHERE id = ?", (business_id,)).fetchall())[0][0]):  # Chech that the user who want to withdraw is leader 
                    
                    if int(self.sql.execute("SELECT business_cash FROM business WHERE id = ?", (business_id,)).fetchall()[0][0]) >= int(cash_withdraw):  # Chech that the cash of the business is equal or bigger than the withdraw cash
                        
                        if int(cash_withdraw) > 0:  # Check that withdraw cash is bigger than zero
    
                            # Withdraw
                            self.sql.execute("UPDATE business SET business_cash = business_cash-? WHERE id = ?", (int(cash_withdraw), business_id))
                            self.sql.execute("UPDATE personal_accounts SET cash = cash+? WHERE user_id = ?", (int(cash_withdraw), int(user_id)))
    
                            # Returning: success.
                            return f'Со счёта бизнеса "{self.sql.execute("SELECT business_name FROM business WHERE id = ?", (business_id,)).fetchall()[0][0]}" снято {cash_withdraw}kr!'
    
                        else:
                            # Returning: cash_withraw must be > 0.
                            return "Не удалось снять средства: значаение должно быть больше нуля."
    
                    else:
                        # Returning: business_cash must be >= cash_withdraw.
                        return "Не удалось снять средства: недостаточно средств на счёте бизнеса."
    
                else:
                    # Returning: don`t have access to this business account.
                    return "Не удалось снять средства: нет доступа к счёту данного бизнеса."
 
            else:
                # Returning: the business account doesn`s exist.
                return "Не удалось снять средства: данный бизнес отсутствует в базе данных."


    def business_crediting(self, user_id, business_id, cash_credit):
        """
        It credits money to the business account and returns the result.

        """
        with self.database:

            # Check that the business account exists.
            if self.sql.execute("SELECT * FROM business WHERE id = ?", (business_id,)).fetchone() != None:
                
                if str(user_id) == str((self.sql.execute("SELECT leader_id FROM business WHERE id = ?", (business_id,)).fetchall())[0][0]):  # Check that the user who want to credit is leader 
                    
                    if int(self.sql.execute("SELECT cash FROM personal_accounts WHERE user_id = ?", (int(user_id),)).fetchall()[0][0]) >= int(cash_credit):  # Check that the cash of the user is equal or bigger than the credit cash
                        
                        if int(cash_credit) > 0:  # Check that credit cash is bigger than zero
    
                            # Credit
                            self.sql.execute("UPDATE personal_accounts SET cash = cash-? WHERE user_id = ?", (int(cash_credit), int(user_id)))
                            self.sql.execute("UPDATE business SET business_cash = business_cash+? WHERE id = ?", (int(cash_credit), business_id))
    
                            # Returning: success.
                            return f'На счёт бизнеса "{self.sql.execute("SELECT business_name FROM business WHERE id = ?", (business_id,)).fetchall()[0][0]}" зачислено {cash_credit}kr!'
    
                        else:
                            # Returning: cash_withraw must be > 0.
                            return "Не удалось зачислить средства: значаение должно быть больше нуля."
    
                    else:
                        # Returning: business_cash must be >= cash_withdraw.
                        return "Не удалось зачислить средства: недостаточно средств на счёте."
    
                else:
                    # Returning: don`t have access to this business cash.
                    return "Не удалось зачислить средства: нет доступа к счёту данного бизнеса."

            else:
                # Returning: the business account doesn`s exist.
                return "Не удалось снять средства: данный бизнес отсутствует в базе данных или введён неправильный ID."


    def business_info(self, user_id, business_id):
        """
        Get the business account info: name, type, cash.

        """

        with self.database:

            # Check that the business account exists.
            if self.sql.execute("SELECT * FROM business WHERE id = ?", (business_id,)).fetchone() != None:

                # Check that the user who want to credit is leader
                if str(user_id) == str((self.sql.execute("SELECT leader_id FROM business WHERE id = ?", (business_id,)).fetchall())[0][0]):

                    return self.sql.execute("SELECT business_name, type, business_cash FROM business WHERE id = ?", (business_id,)).fetchall()

                else:
                    # Returning: don`t have access to this business cash.
                    return "BUSINESS_HAVE_NOT_ACCESS"

            else: 
                # Returning: the business account doesn`s exist.
                return "BUSINESS_DOES_NOT_EXIST"


    def business_user(self, user_id): 
        """
        Get the all business of the user with id = user_id

        """

        with self.database:

            # All business of the user with id = user_id
            user_business = self.sql.execute("SELECT id, business_name FROM business WHERE leader_id = ?", (user_id,)).fetchall()

            # Check that the user has some business
            if user_business != None:

                user_business_strs = []

                for tuple in user_business:
                    user_business_strs.append(f"{tuple[1]} ({tuple[0]})")

                return "\n\nВаш бизнес: \n\n" + '\n🔵 '.join(user_business_strs)