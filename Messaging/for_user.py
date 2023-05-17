def forUser(msg, id, db, vk_session, longpoll, admins, about_system, configWork, logger, technical, help, ts, commands):

    # Send the message with vk_api in the user chat.
    def senderUser(id, text):
        vk_session.method("messages.send", {"user_id" : id, "message" : text, "random_id" : 0})

    # If the user writes any, except "регистрация" (registration) and doesn`t has an account, the system ask for create the account.
    if (msg[0].lower() != "регистрация" and msg[0].lower() != "рег" and msg[0].lower() != "регистрируюсь") and (db.account_exists(id, None) == False) and (len(msg) == 2):
        senderUser(id, f'Для начала откройте лицевой счёт, прописав команду "регистрация" и далее никнейм одним словом. \nНапример: "регистрация Котик".') 

    # "You successfully opened the account!"
    elif (msg[0].lower() == "регистрация" or msg[0].lower() == "рег" or msg[0].lower() == "регистрируюсь") and (db.account_exists(id, None) == False) and (len(msg) == 2):
        db.add_account(id, msg[1])
        senderUser(id, f'Вы успешно открыли лицевой счёт. \nВаш ID: {db.get_account_info(id, None)[0][0]}. \n\nПожалуйста, если Вы имеете гражданство, обратитесь в Sigma Research Inc. для привязки граждантсва к Вашему счёту, приложив в сообщение Ваш паспорт и ID в системе.')

    # If the user already has an account, it writes about this fact, if the user typed "регистрация" ("registation") or other like this.  
    elif (msg[0].lower() == "регистрация" or msg[0].lower() == "рег" or msg[0].lower() == "регистрируюсь") and (db.account_exists(id, None) == True):
        senderUser(id, f'У Вас уже есть лицевой счёт.')

    # If the user didn`t write the nickname after "регистрация" (registation).
    elif (msg[0].lower() == "регистрация" or msg[0].lower() == "рег" or msg[0].lower() == "регистрируюсь") and (db.account_exists(id, None) == False) and (len(msg) != 2):
        senderUser(id, 'Пожалуйста, введите после слова "регистрация" желаемый никнейм одним словом.')

    # Write the info about the account.
    elif ((msg[0].lower() == "мой") and ((msg[1].lower() == "счёт") or (msg[1].lower() == "счет"))) or (msg[0].lower() == "профиль") or (msg[0].lower() == "баланс"):
        senderUser(id, f"Здравствуйте! Ваш лицевой счёт: \n\n🆔 ID: {db.get_account_info(id, None)[0][0]} \n💳 Средства: {round(db.get_account_info(id, None)[0][1])}")


    elif (msg[0].lower() == "паспорт"):
        if len(msg) > 1:
            pass

        else: 
            senderUser(id, "Команды паспортной системы: \n\nПаспорт получить - получение паспорта \n\n")

    # Transfer money command. Sample: "Перевести 11 1 000"
    elif msg[0].lower() == "перевести":
        senderUser(id, commands.MoneyTransfer(db, logger, technical, vk_session).main(id, msg))

    # Business commands. Sample: "Бизнес SGRE зачислить 1 000 000".           
    elif msg[0].lower() == "бизнес":

        if len(msg) > 1:

            # Check than in the message is four words: key word, business_id, key word, cash_interact.
            if len(msg) == 4:

                # Check that the user want to withdraw or credit cash.
                if (msg[2].lower() == "снять") or (msg[2].lower() == "зачислить"):
    
                    cash_interact = ""  # It is the withdraw or credit cash. 

                    # If the value of the cash to post is splited by spaces, this loop unites it.
                    for i in range(3, len(msg)):

                        cash_interact = cash_interact + msg[i]

                    # Check that all chars of cash_posted are numbers.
                    if all("0" <= s <= "9" for s in cash_interact):

                        # If the user want to withdraw.
                        if msg[2].lower() == "снять":
                            senderUser(id, db.business_withdraw(id, msg[1], cash_interact))
                        
                        # If the user want to credit.
                        if msg[2].lower() == "зачислить":
                            senderUser(id, db.business_crediting(id, msg[1], cash_interact))
                    else:
                        senderUser(id, "Некорректное значение суммы.")

            # If the user wants to see the info about a business.
            elif len(msg) == 2:

                info = db.business_info(id, msg[1])  # Business info: name, type and cash.
    
                # Check that all right and the method retudned a list or a tuple.
                if isinstance(info, (list, tuple)):
    
                    business_name = info[0][0]  # Name
                    business_type = info[0][1]  # Type
                    business_cash = info[0][2]  # Cash
                    
                    # Send the info.
                    senderUser(id, f"Здравствуйте! Информация о бизнесе {msg[1]}: \n\nНазвание: {business_name} \n\nТип: {business_type} \n\nСредства: {round(business_cash)}")
    
                # If the user doesn`t has the access to this business account.
                elif info == "BUSINESS_HAVE_NOT_ACCESS":
                    senderUser(id, "Не удалось получить информацию о бизнесе: нет доступа к счёту данного бизнеса.")
                
                # If the business doesn`t exist or user typed the wrong ID.
                elif info == "BUSINESS_DOES_NOT_EXIST":
                    senderUser(id, "Не удалось получить информацию о бизнесе: данный бизнес отсутствует в базе данных или введён неправильный ID.")
            else:
                senderUser(id, "Команда некорректна, должна быть: \nБизнес ID БИЗНЕСА]")
            
        elif len(msg) == 1:
            senderUser(id, f"Чтобы зарегистрировать бизнес, сначала обратитесь в налоговую службу. После регистрации в налоговой службе, Вам следует обратиться в техническую поддержку Sigma Research Inc. Не забудьте заранее приготовить необходимые документы: паспорт, регистрация в налоговой." + db.business_user(id))

        else: 
            senderUser(id, f'Для бизнеса существуют данные команды: \n\nБизнес, \n\nБизнес [ID БИЗНЕСА], \n\nБизнес [ID БИЗНЕСА] снять/зачислить [СРЕДСТВА].')


    # User notification turning off or on.
    elif msg[0].lower() == "уведомления":

        if len(msg) == 2:
            
            # If the user wants to turn on notifications.
            if msg[1].lower() == "вкл":
                db.user_notification_update(id, True)
                senderUser(id, "Уведомления включены.")
                logger.info(f"User {id} turned on the notification for him.")

            elif msg[1].lower() == "выкл":
            # If the user wants to turn off notifications.
                db.user_notification_update(id, False)
                senderUser(id, "Уведомления выключены.")
                logger.info(f"User {id} turned off the notification for him.")

            else:
                senderUser(id, 'Второй аргумент может быть только "вкл" или "выкл".')
        else:
            senderUser(id, "Некорректная комманда: должна быть вида \nУведомления вкл/выкл")


    # Help info
    elif msg[0].lower() == "помощь":
        senderUser(id, f"Здравствуйте, @id{id}({db.get_account_info(id, None)[0][2]})! Вот основные команды: \n\n" + " \n\n".join(help))

    # About the system info
    elif (msg[0].lower() == "о") and (msg[1].lower() == "системе"):
        senderUser(id, f'Если вы хотели получить помошь, то пропишите "помощь".')                            
        senderUser(id, about_system)  

    elif (msg[0].lower() == "пользовательское") and (msg[1].lower() == "соглашение"):
        pass


    # Admin commands.
    elif list(msg[0].lower())[0] == "!":
        try:

            # Check that the user is an admin.
            if str(id) in admins:

                # Turn of the system.
                if msg[0].lower() == "!выкл":
                    senderUser(id, f"Система отключена.")
                    raise SystemExit(0)

                # Return the id of the chat.
                elif msg[0].lower() == "!id":
                    senderUser(id, f"ID чата: {id}")

                # Set the cash.
                elif msg[0].lower() == "!средства":
                    senderUser(id, f"Установлены средства @id{db.set_money(msg[1], msg[2])[0][0]}({db.get_account_info(None, msg[1])[0][2]}) {msg[2]}.")
                
                # Work with the config.
                elif msg[0].lower().split("_")[0] == "!config":
                    if msg[0].lower().split("_")[1] == "set":
                        if (msg[2] == "True") or (msg[2] == "False"):
                            senderUser(id, configWork.changeValue("Settings", msg[1], msg[2]))
                    elif msg[0].lower().split("_")[1] == "check":
                        senderUser(id, f"{msg[1]}: {msg[2]} == " + configWork.readValue(msg[1], msg[2]))
                
                # Work with the posts.
                elif msg[0].lower() == "!должность":
                        db.set_post(msg[1], msg[2] + " " + msg[3])
                        senderUser(id, f"Установлена должность {msg[1]} пользователю {msg[2]} {msg[3]}.")

                # With this we can to collect the taxes with custom coefficients.
                elif msg[0].lower() == "!налоги":
                    if len(msg) == 3:
                        ts.tax_collection_for_individuals(float(msg[1]), float(msg[2]))
                        senderUser(id, f"Налоги собраны. Коэффициенты: {float(msg[1])}, {float(msg[2])}")
                    else:
                        senderUser(id, "!налоги [КОЭФФИЦИЕНТ ГРАЖДАНЕ] [КОЭФФИЦИЕНТ МИГРАНТЫ]")
                
                # Admin command to use sqlite3.
                elif msg[0].lower() == "!db":
                    cmd = msg.split("!db ")[1]

                # Business admin commands like add a business or delete a business.
                elif msg[0].lower().split("_")[0] == "!business":

                    if len(msg) == 1:
                        senderUser(id, "!business_add [ID] [NAME] [TYPE] [LEADER_VK_ID]\n\n!business_delete [ID]")

                    if msg[0].lower().split("_")[1] == "add":
                        if len(msg) == 5:
                            senderUser(id, db.business_add(msg[1], msg[2], msg[3], int(msg[4])))

                    elif msg[0].lower().split("_")[1] == "delete":
                        senderUser(id, db.business_delete(msg[1]))

                #  Set the citizenship value.
                elif msg[0].lower() == "!citizenship":

                    if len(msg) == 1: 
                        senderUser(id, "!citizenship [DB_ID] [VALUE]")

                    if len(msg) == 3:
                        db.citizenship(msg[1], bool(msg[2]))
                        senderUser(id, f"CITIZEN SHIP {int(msg[1])} ({db.get_account_info(None, int(msg[1]))[0][2]}) SET TO {bool(msg[2])}.")                    


        except Exception as e: 
            senderUser(id, f"Failed! \nexit code: 1. \nException: {e}.")
            logger.exception(f"Failed with exit code: 1; \nEB: for_user.py/001")

    # Map
    elif (msg[0].lower() == "карта"):
        map_message = "[ДАННЫЕ УДАЛЕНЫ]"
        vk_session.method("messages.send", {"peer_id": id, "message": map_message, "attachment": "photo-█████████_█████████", "random_id": 0})

    else:
        senderUser(id, 'Неизвестная команда. Пропишите "помощь" для получения списка команд.')
        # raise TypeError("Test exception.")