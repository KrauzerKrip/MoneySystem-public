def forChat(msg, id, user_id, db, vk_session, longpoll, admins, about_system, configWork, logger, technical, help, ts, commands):

    # Send the message with vk_api in the chat.
    def senderChat(id, text):
        vk_session.method("messages.send", {"peer_id" : id, "message" : text, "random_id" : 0})

    # If the user already has an account, it writes about this fact, if the user typed "регистрация" ("registation") or other like this.  
    if (msg[0].lower() == "регистрация" or msg[0].lower() == "рег" or msg[0].lower() == "регистрируюсь") and (db.account_exists(user_id, None) == True):
        senderChat(id, f'У Вас уже есть лицевой счёт.')

    # Check than account exists in the system.
    if db.account_exists(user_id, None) == False:
        pass

    else:

        tag = f"@id{user_id}({db.get_account_info(user_id, None)[0][2]})"  # mention of the user with the database name.
        
        # Write the info about the account.
        if ((msg[0].lower() == "мой") and ((msg[1].lower() == "счёт") or (msg[1].lower() == "счет"))) or (msg[0].lower() == "профиль") or (msg[0].lower() == "баланс"):
            senderChat(id, f"{tag}, здравствуйте! Ваш лицевой счёт: \n\n🆔 ID: {db.get_account_info(user_id, None)[0][0]} \n💳 Средства: {round(db.get_account_info(user_id, None)[0][1])}")

        # Transfer money command. Sample: "Перевести 11 1 000"
        elif msg[0].lower() == "перевести":
            senderChat(id, commands.MoneyTransfer(db, logger, technical, vk_session).main(user_id, msg))
        
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
                                senderChat(id, db.business_withdraw(user_id, msg[1], cash_interact))
                            
                            # If the user want to credit.
                            if msg[2].lower() == "зачислить":
                                senderChat(id, db.business_crediting(user_id, msg[1], cash_interact))
                        else:
                            senderChat(id, "Некорректное значение суммы.")
    
                # If the user wants to see the info about a business.
                elif len(msg) == 2:
    
                    info = db.business_info(user_id, msg[1])  # Business info: name, type and cash.
        
                    # Check that all right and the method retudned a list or a tuple (all ok).
                    if isinstance(info, (list, tuple)):
        
                        business_name = info[0][0]  # Name
                        business_type = info[0][1]  # Type
                        business_cash = info[0][2]  # Cash
                        
                        # Send the info.
                        senderChat(id, f"Здравствуйте, {tag}! Информация о бизнесе {msg[1]}: \n\nНазвание: {business_name} \n\nТип: {business_type} \n\nСредства: {round(business_cash)}")
        
                    # If the user doesn`t has the access to this business account.
                    elif info == "BUSINESS_HAVE_NOT_ACCESS":
                        senderChat(id, "Не удалось получить информацию о бизнесе: нет доступа к счёту данного бизнеса.")
                    
                    # If the business doesn`t exist or user typed the wrong ID.
                    elif info == "BUSINESS_DOES_NOT_EXIST":
                        senderChat(id, "Не удалось получить информацию о бизнесе: данный бизнес отсутствует в базе данных или введён неправильный ID.")

                else:
                    senderChat(id, "Команда некорректна, должна быть: \nБизнес [ID БИЗНЕСА]")
                
            elif len(msg) == 1:
                senderChat(id, f"{tag}, чтобы зарегистрировать бизнес, сначала обратитесь в налоговую службу. После регистрации в налоговой службе, Вам следует обратиться в техническую поддержку Sigma Research Inc. Не забудьте заранее приготовить необходимые документы: паспорт, регистрация в налоговой." + db.business_user(user_id))

            else: 
                senderChat(id, f'{tag}, для бизнеса существуют данные команды: \n\nБизнес, \n\nБизнес [ID БИЗНЕСА], \n\nБизнес [ID БИЗНЕСА] снять/зачислить [СРЕДСТВА].')

        
        # Help info
        elif msg[0].lower() == "помощь":
            senderChat(id, f"Здравствуйте, {tag}! Вот основные команды: \n\n" + " \n\n".join(help))

        # About the system info
        elif (msg[0].lower() == "о") and (msg[1].lower() == "системе"):
            senderChat(id, f'Если вы хотели получить помошь, то пропишите "помощь".')                            
            senderChat(id, about_system)

        # Posts info
        elif (msg[0].lower() == "должности"):
            senderChat(id, f'Должности: \n\n\n🎩 Премьер-министр: {db.get_posts("premier")[0][1]}\n\n🛡 Министр обороны: {db.get_posts("dm")[0][1]}\n\n🔒 Министр Внутренних Дел: {db.get_posts("mia")[0][1]}\n\n⚕ Министр здравоохранения: {db.get_posts("mh")[0][1]}\n\n💹 Министр финансов: {db.get_posts("mf")[0][1]}')


        # Admin commands.
        elif list(msg[0].lower())[0] == "!":
            try:

                # Check that the user is an admin.
                if str(user_id) in admins:

                    # Turn of the system.
                    if msg[0].lower() == "!выкл":
                        senderChat(id, f"Система отключена.")
                        raise SystemExit(0)

                    # Return the id of the chat.
                    elif msg[0].lower() == "!id":
                        senderChat(id, f"ID чата: {id}")

                    # Set the cash.
                    elif msg[0].lower() == "!средства":
                        senderChat(id, f"Установлены средства @id{db.set_money(msg[1], msg[2])[0][0]}({db.get_account_info(None, msg[1])[0][2]}) {msg[2]}.")
                    
                    # Work with the config.
                    elif msg[0].lower().split("_")[0] == "!config":
                        if msg[0].lower().split("_")[1] == "set":
                            if (msg[2] == "True") or (msg[2] == "False"):
                                senderChat(id, configWork.changeValue("Settings", msg[1], msg[2]))
                        elif msg[0].lower().split("_")[1] == "check":
                            senderChat(id, f"{msg[1]}: {msg[2]} == " + configWork.readValue(msg[1], msg[2]))
                    
                    # Work with the posts.
                    elif msg[0].lower() == "!должность":
                            db.set_post(msg[1], msg[2] + " " + msg[3])
                            senderChat(id, f"Установлена должность {msg[1]} пользователю {msg[2]} {msg[3]}.")

                    # With this we can to collect the taxes with custom coefficients.
                    elif msg[0].lower() == "!налоги":
                        if len(msg) == 3:
                            ts.tax_collection_for_individuals(float(msg[1]), float(msg[2]))
                            senderChat(id, f"Налоги собраны. Коэффициенты: {float(msg[1])}, {float(msg[2])}")
                        else:
                            senderChat(id, "!налоги [КОЭФФИЦИЕНТ ГРАЖДАНЕ] [КОЭФФИЦИЕНТ МИГРАНТЫ]")

            
            except Exception as e: 
                senderChat(id, f"Failed! \nexit code: 1. \nException: {e}.")
                logger.exception(f"Failed with exit code: 1.") 


        # Map
        elif (msg[0].lower() == "карта"):
            map_message = "[ДАННЫЕ УДАЛЕНЫ]"
            vk_session.method("messages.send", {"peer_id": id, "message": map_message, "attachment": "photo-█████████_█████████", "random_id": 0})