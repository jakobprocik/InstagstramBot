def follow_day():
    """
    Is following 3 Days X Accounts from the UserAccountsToFollow.
    :return:
    """
    import random
    from datetime import datetime
    import time
    import InstaBotClass
    day_counter = 3
    follow_counter = random.randint(150, 180)
    bot = InstaBotClass.Instagrambot('<Email>', "<Password>")
    bot.sign_in()
    while day_counter > 0:
        if follow_counter > 0:
            with open("UserAccountsToFollow.txt", "r+") as old:
                with open("Followed.txt", "a") as new:
                    all_lines = old.readlines()
                    follow_line = all_lines[0]
                    #follow_line is the  User
                    if bot.follow_user(follow_line):
                        new.write(follow_line)
                        #Deleting the User from UserAccountsToFollow
                        delete_von_follower_sammlung1(follow_line)
                        print("I followed {0} ".format(follow_line))
                        follow_counter = follow_counter - 1
                        old.close()
                        new.close()
                        time.sleep(random.randint(180, 500))
                    else:
                        delete_von_follower_sammlung1(follow_line)
        elif follow_counter == 0:
            while True:
                now = datetime.now()
                current_time = now.strftime("%H:%M")
                if current_time == "23:59":
                    time.sleep(random.randint(180, 300))
                    follow_counter = random.randint(150, 180)
                    day_counter = day_counter - 1
                    break
                time.sleep(60)


def unfollowday():
    """
    Is unfollowing 3 Days X Accounts from the UserAccountsToFollow.
    :return:
    """
    import random
    from datetime import datetime
    import time
    import InstaBotClass
    day_counter = 3
    unffollow_counter = random.randint(120, 140)
    bot = InstaBotClass.Instagrambot('<Usermail>', "<Password>")
    bot.sign_in()
    while day_counter > 0:
        if unffollow_counter > 0:
            with open("Followed.txt", "r+") as old:
                with open("Unfollow.txt", "a") as new:
                    time.sleep(random.randint(180, 500))
                    all_lines = old.readlines()
                    unfollow_line = all_lines[0]
                    new.write(unfollow_line)
                    bot.unfollow_user(unfollow_line)
                    #Deleting User in Followed.Txt
                    delete_von_gefolgt(unfollow_line)
                    print("I unfollowed {0} ".format(unfollow_line))
                    unffollow_counter = unffollow_counter - 1
                    old.close()
                    new.close()
        elif unffollow_counter == 0:
            while True:
                now = datetime.now()
                current_time = now.strftime("%H:%M")
                if current_time == "23:59":
                    time.sleep(random.randint(180, 300))
                    unffollow_counter = random.randint(120, 140)
                    day_counter = day_counter - 1
                    break
                time.sleep(60)


def delete_von_follower_sammlung1(line_to_find):
    """
    Is following deleting the followed Account from UserAccountsToFollow.txt
    :return:
    """
    with open('UserAccountsToFollow.txt', "r+") as f:
        t = f.read()
        to_delete = line_to_find.strip()
        f.seek(0)
        for line in t.split('\n'):
            if line != to_delete:
                f.write(line + '\n')
        f.truncate()


def delete_von_gefolgt(line_to_find):
    """
    Is following deleting the followed Account from Followed.txt
    :return:
    """
    with open('Followed.txt', 'r+') as f:
        t = f.read()
        to_delete = line_to_find.strip()
        f.seek(0)
        for line in t.split('\n'):
            if line != to_delete:
                f.write(line + '\n')
        f.truncate()
