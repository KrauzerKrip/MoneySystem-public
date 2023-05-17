class technical:
    
    def __init__(self, vk_session, logger, db):
        """
        Set the variables.

        """
        self.vk_session = vk_session
        self.logger = logger
        self.db = db

    
    def senderTechnical(self, exception, d):
        """
        Sends the logs to the special chat.

        """
        
        self.vk_session.method("messages.send", {"peer_id" : "here should be int id", "message" : f"Something went wrong... \n\nDate: {d.day}.{d.month}.{d.year} \n\nTime: {d.hour}:{d.minute}:{d.second} \n\n{exception.__class__.__name__}: {exception}", "random_id" : 0})


    def senderUserWarn(self, user_toWarn_id, notification, message):
        """
        Send to the user with id = user_toWarn_id the message = message.

        """

        # If the message is notification and the user has notifications turned on or if the message isn`t notification (yes, maybe it will be possible in the future).
        if ((notification == True) and (self.db.get_account_info(user_toWarn_id, None)[0][3])) or (notification == False):

            # Trying to send the notification message
            try:

                message_to_send = str(message) + ' \n\nВы можете отключить уведомления коммадой "уведомления выкл"'

                self.vk_session.method("messages.send", {"user_id" : user_toWarn_id, "message" : message_to_send, "random_id" : 0})

                self.logger.info(f'User notification: the user {user_toWarn_id} was notificated with message "{message}".')
            
            # If something went wrong
            except Exception as e:

                # If we don`t have permission to send the message to this user.
                if str(e) == "[901] Can't send messages for users without permission":
                    self.logger.info(f'User notification exception: the user {user_toWarn_id} wasn`t notificated with message "{message}", \nbecause we don`t have permission for this.')
                
                # If other exception.
                else:
                    self.logger.exception("Failed with exit code: 1; \nEB: technical.py/001")

        # If the user turned off the notifications.
        else:
            self.logger.info(f'No user notification: the user {user_toWarn_id} wasn`t notificated with notification "{message}",\nbecause he turned off the notifications.')