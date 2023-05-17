class Commands:
    """
    Class for the commands.

    """
    pass  # There will be something here (but it is not certain).


class MoneyTransfer(Commands):
    """
    This class transfers money and returns the result (success or exception) as a str. 
    Also, it logs logs and send the notification to the recipient.

    user_id or vk_id - vk ID
    DB_ID - data base ID

    """

    def __init__(self, db, logger, technical, vk_session):
        """
        Set the variables.

        """
        
        self.db = db                 # Data base.
        self.logger = logger         # Logger.
        self.technical = technical   # Technical. There is senderUserWarn (notification sender to user).
        self.vk_session = vk_session
        self.vk = vk_session.get_api()


    def transfer(self, user_id, msg, sender_account_info, recipient_vk_id, recipient_account_info, cash_posted):
        """
        It transfers money from the sender (user_id) to the recipient (recipient_vk_id).
        Works with transfer_money database method and returns in the format "Transfered [RECIPIENT] [HOW MUCH]".

        """

        try:

            # The result from the data base tranfer_money method.
            db_transfer_method = self.db.transfer_money(user_id, recipient_vk_id, cash_posted)

            # Log the cash sending.
            self.logger.info(f"CASH_SENDING: Chat: {user_id}, User {sender_account_info[0][2]} with VK_ID: {user_id} send {cash_posted} to the user {recipient_account_info[0][2]} with the DB_ID {msg[1]} successfully.")

            # Warn recipient user about the cash sending.
            self.technical.senderUserWarn(recipient_vk_id, True, f"Вам переведено {cash_posted}kr от @id{user_id}({sender_account_info[0][2]}).")

            return db_transfer_method
        
        except Exception as e:
            self.logger.exception("Failed with exit code: 1.")
            return f"Failed! \nexit code: 1. \nException: {e}"


    def main(self, user_id, msg):
        """
        The main. There are many of the checks. 
        After it calls transfer method.

        How does a tag from VK look like: [id000000000|@example] 

        """

        # Info about sender and recipient accounts.
        sender_account_info = self.db.get_account_info(user_id, None)  # The account info of the sender (tuple in list).

        IsDB_ID = False  # If ID is DB_ID.
        IsTag = False  # If ID is from the tag.

        # If ID is DB_ID.
        if all("0" <= s <= "9" for s in msg[1]):
            
            # Check that user_id is 0 or more as an integer.
            if int(msg[1].lower()) >= 0:
                IsDB_ID = True
                cash_posted = ""

                # The account info of the recipint (tuple in list)
                recipient_account_info = self.db.get_account_info(None, msg[1])
                # The vk_id of the recipint (int).
                recipient_vk_id = recipient_account_info[0][0]
        
        # If ID is tag with vk_id.
        elif msg[1].lower()[13] == "@":
            IsTag = True
            user_tag = msg[1].split("@")
            cash_posted = ""

            # Splits, for example, "[id000000000|@example]" (msg[1]) to ['id000000000', '@example]'], get only the first element ('000000000') and convert it to int type.
            recipient_vk_id = int(msg[1].split("id")[1].split("|")[0])
            # The account info of the recipint (tuple in list).
            recipient_account_info = self.db.get_account_info(recipient_vk_id, None)


        # Check that ID is right and it is DB_ID or from the tag.
        if (IsDB_ID == True) or (IsTag == True):

            # If the value of the cash to post is splited by spaces, this loop unites it.
            for i in range(2, len(msg)):
                cash_posted = cash_posted + msg[i]

            # Check that all chars of cash_posted are numbers.
            if all("0" <= s <= "9" for s in cash_posted):  # Check that all chars of cash_posted are numbers.

                # Check that the cash of user is equal of bigger than cash_posted.
                if sender_account_info[0][1] >= int(cash_posted):

                    if (int(cash_posted) > 0):

                        # Check that accounts exists and user_id of the recipient is not user_id of the sender.
                        if (self.db.account_exists(recipient_vk_id, None) == True) and (recipient_vk_id != user_id):

                            # Result from the tranfser command method.
                            transfer_method = self.transfer(user_id, msg, sender_account_info, recipient_vk_id, recipient_account_info, cash_posted)

                            # If all is ok.
                            if transfer_method == "TRANSFERED":
                                return f"Переведено @id{recipient_vk_id}({recipient_account_info[0][2]}) {cash_posted}kr."

                        else: 
                            return "Неверный ID получателя или он принадлежит Вам."
                    else: 
                        return "Некорректное значение суммы."
                else: 
                    return "Недостаточно средств на счёте для перевода."
            else:
                return "Некорректное значение суммы."
        else:
            return "Неверный ID получателя."