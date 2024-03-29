import pymysql
import mysql.connector
from mysql.connector import Error

pymysql.install_as_MySQLdb()

try:
    connection = mysql.connector.connect(host='127.0.0.1',
                                        database='eventica',
                                        user='root',
                                        password='password')
    
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
    
    cursor = connection.cursor()

    # drop already existing tables
    result = cursor.execute("DROP TABLE IF EXISTS tags_artist")
    result = cursor.execute("DROP TABLE IF EXISTS tags_event")
    result = cursor.execute("DROP TABLE IF EXISTS follows")
    result = cursor.execute("DROP TABLE IF EXISTS blog")
    result = cursor.execute("DROP TABLE IF EXISTS competes")
    result = cursor.execute("DROP TABLE IF EXISTS performs")
    result = cursor.execute("DROP TABLE IF EXISTS game")
    result = cursor.execute("DROP TABLE IF EXISTS concert")
    result = cursor.execute("DROP TABLE IF EXISTS saves")
    result = cursor.execute("DROP TABLE IF EXISTS joins")
    result = cursor.execute("DROP TABLE IF EXISTS event_category")
    result = cursor.execute("DROP TABLE IF EXISTS in_shopping_cart")
    result = cursor.execute("DROP TABLE IF EXISTS rating")
    result = cursor.execute("DROP TABLE IF EXISTS purchases")
    result = cursor.execute("DROP TABLE IF EXISTS friend")
    result = cursor.execute("DROP TABLE IF EXISTS notification")
    result = cursor.execute("DROP TABLE IF EXISTS admin")
    result = cursor.execute("DROP TABLE IF EXISTS system_report")
    result = cursor.execute("DROP TABLE IF EXISTS card")
    result = cursor.execute("DROP TABLE IF EXISTS blog")
    result = cursor.execute("DROP TABLE IF EXISTS ticket")
    result = cursor.execute("DROP TABLE IF EXISTS event")
    result = cursor.execute("DROP TABLE IF EXISTS team")
    result = cursor.execute("DROP TABLE IF EXISTS user")
    result = cursor.execute("DROP TABLE IF EXISTS venue")
    result = cursor.execute("DROP TABLE IF EXISTS artist")
    
    result = cursor.execute("DROP VIEW IF EXISTS event_view")
    result = cursor.execute("DROP VIEW IF EXISTS my_upcoming_events")
    result = cursor.execute("DROP VIEW IF EXISTS artist_view")

    # create tables in the database
    result = cursor.execute("""
                            create table user(
                            user_id int not null auto_increment,
                            name varchar(50) not null,
                            password varchar(40) not null,
                            email varchar(40) not null,
                            address varchar(100),
                            city varchar(30),
                            phone_number varchar(15),
                            date_of_birth date,
                            balance int default 0, 
                            role varchar(10),
                            CHECK (role in ('admin', 'user')),
                            PRIMARY KEY (user_id)) ENGINE=INNODB;""")
    print("user table created successfully ") 

    result = cursor.execute("""
                            insert into user values(
                                NULL, "Efe Beydogan", "password", "efebeydogan@hotmail.com", "ankara", "ankara", "0555", STR_TO_DATE("03-26-2001","%m-%d-%Y"), 500, "admin"
                            );
                            """)
    result = cursor.execute("""
                            insert into user values(
                                NULL, "Eren Polat", "1", "erenpolat@hotmail.com", "ankara", "ankara", "0555", STR_TO_DATE("03-26-2008","%m-%d-%Y"), 500, "user"
                            );
                            """)
    result = cursor.execute("""
                            insert into user values(
                                NULL, "Berk Türkçapar", "1", "berk@gmail.com", "ankara", "ankara", "0555", STR_TO_DATE("03-26-2001","%m-%d-%Y"), 500, "user"
                            );
                            """)
    result = cursor.execute("""
                            insert into user values(
                                NULL, "Emir M. Erdem", "1", "emir@hotmail.com", "ankara", "ankara", "0555", STR_TO_DATE("03-26-2001","%m-%d-%Y"), 500, "user"
                            );
                            """)

    result = cursor.execute("""
                            create table friend(
                            user_id1 int not null,
                            user_id2 int not null,
                            friends_since DATE not null,
                            FOREIGN KEY (user_id1) REFERENCES user(user_id)
                            ON DELETE CASCADE,
                            FOREIGN KEY (user_id2) REFERENCES user(user_id)
                            ON DELETE CASCADE,
                            PRIMARY KEY (user_id1, user_id2)
                            ) ENGINE=INNODB;
                            """)
    print("friend table created successfully")

    result = cursor.execute("""
                            create table notification(
                            user_id int not null auto_increment,
                            notification_no int not null,
                            title varchar(100) not null,
                            body text(300) not null,
                            date DATE not null,
                            FOREIGN KEY (user_id) REFERENCES user(user_id)
                            ON DELETE CASCADE,
                            PRIMARY KEY (user_id, notification_no)
                            ) ENGINE=INNODB;
                            """)
    print("notification table created successfully")

    result = cursor.execute("""
                            create table admin(
                            user_id int not null,
                            FOREIGN KEY (user_id) REFERENCES user(user_id)
                            ON DELETE CASCADE,
                            PRIMARY KEY (user_id)
                            ) ENGINE=INNODB;
                            """)
    print("admin table created successfully")

    result = cursor.execute("""
                            create table system_report(
                            report_id int not null auto_increment,
                            user_id int not null,
                            title varchar(100) not null,
                            body MEDIUMTEXT not null,
                            date_of_report DATE not null,
                            FOREIGN KEY (user_id) REFERENCES user(user_id)
                            ON DELETE CASCADE,
                            PRIMARY KEY (report_id)
                            ) ENGINE=INNODB;
                            """)
    print("system_report table created successfully")

    result = cursor.execute("""
                            create table card(
                            user_id int not null,
                            card_id int not null auto_increment,
                            name_on_card varchar(50) not null,
                            card_no int not null,
                            expiry_date varchar(10) not null,
                            cvv int not null,
                            FOREIGN KEY (user_id) REFERENCES user(user_id)
                            ON DELETE CASCADE,
                            PRIMARY KEY (card_id, user_id)
                            ) ENGINE=INNODB;
                            """)
    print("card table created successfully")

    result = cursor.execute("""
                            create table blog(
                            blog_id int not null auto_increment,
                            user_id int not null,
                            title varchar(100) not null,
                            body MEDIUMTEXT not null,
                            publish_date DATE not null,
                            FOREIGN KEY (user_id) REFERENCES user(user_id)
                            ON DELETE CASCADE,
                            PRIMARY KEY (blog_id, user_id)
                            ) ENGINE=INNODB;
                            """)
    print("blog table created successfully")

    result = cursor.execute("""
                            create table venue(
                            venue_id int not null auto_increment,
                            name varchar(100) not null,
                            description MEDIUMTEXT not null,
                            city varchar(30) not null,
                            address varchar(100) not null,
                            PRIMARY KEY (venue_id)
                            ) ENGINE=INNODB;
                            """)
    print("venue table created successfully")

    result = cursor.execute("""
                            insert into venue values(
                                NULL, "Bilkent Odeon", "Bilkent Uni", "Ankara", "Bilkent"
                            );
                            """)
    result = cursor.execute("""
                            insert into venue values(
                                NULL, "CSO", "Cankaya", "Ankara", "Cankaya"
                            );
                            """)
    result = cursor.execute("""
                            create table event(
                            event_id int not null auto_increment,
                            name varchar(50) not null,
                            description MEDIUMTEXT not null,
                            date DATETIME not null,
                            event_type varchar(20) not null,
                            status varchar(20),
                            age_limit int,
                            total_quota int not null,
                            remaining_quota int not null,
                            seating_plan varchar(100),
                            venue_id int not null,
                            creator_id int not null,
                            avg_rating int,
                            price int,
                            CHECK (event_type in ('Concert', 'Sports', 'Gathering', 'Art',
                            'Other')),
                            CHECK (remaining_quota >= 0),
                            FOREIGN KEY (creator_id) REFERENCES user(user_id)
                            ON DELETE CASCADE,
                            FOREIGN KEY (venue_id) REFERENCES venue(venue_id)
                            ON DELETE CASCADE,
                            PRIMARY KEY (event_id)
                            ) ENGINE=INNODB;
                            """)
    print("event table created successfully")

    result = cursor.execute("""
                            insert into event values(
                                NULL, "Yalın Concert", "Yalın Şehrinize Geliyor!", "2022-12-29 20:30:00", "Concert", "Available", 18,
                                150, 150, "A, B, C", 1, 1, 0, 100
                            );
                            """)
    result = cursor.execute("""
                            insert into event values(
                                NULL, "Yalın Yılbaşı Konseri", "Yalın Şehrinize Geliyor!", "2022-12-31 20:30:00", "Concert", "Available", 18,
                                150, 150, "A, B, C", 1, 1, 0, 100
                            );
                            """)
    result = cursor.execute("""
                            insert into event values(
                                NULL, "Mor ve Ötesi Odeon'da", "mor ve ötesi", "2022-12-29 20:30:00", "Concert", "Available", 18,
                                150, 150, "A, B, C", 1, 1, 0, 100
                            );
                            """)
    result = cursor.execute("""
                            insert into event values(
                                NULL, "JABBAR", "cesaretsizce olmuyor", "2022-12-29 12:30:00", "Concert", "Available", 13,
                                150, 150, "A, B, C", 1, 1, 0, 0
                            );
                            """)
    result = cursor.execute("""
                            insert into event values(
                                NULL, "Emir Melih Erdem House Gathering", "mantı+sarma ikramımızdır", "2022-12-23 12:30:00", "Gathering", "Available", 13,
                                15, 15, "A, B, C", 1, 1, 0, 0
                            );
                            """)

    result = cursor.execute("""
                            create table ticket(
                            ticket_id int not null auto_increment,
                            event_id int not null,
                            user_id int not null,
                            FOREIGN KEY (event_id) REFERENCES event(event_id),
                            FOREIGN KEY (user_id) REFERENCES user(user_id),
                            PRIMARY KEY (ticket_id)
                            ) ENGINE=INNODB;
                            """)
    print("ticket table created successfully")

    result = cursor.execute("""
                            create table purchases(
                            ticket_id int not null auto_increment,
                            user_id int not null,
                            card_id int not null,
                            FOREIGN KEY (user_id) REFERENCES card(user_id)
                            ON DELETE CASCADE,
                            FOREIGN KEY (card_id) REFERENCES card(card_id)
                            ON DELETE CASCADE,
                            FOREIGN KEY (ticket_id) REFERENCES ticket(ticket_id)
                            ON DELETE CASCADE,
                            PRIMARY KEY (ticket_id)
                            ) ENGINE=INNODB;
                            """)
    print("purchases table created successfully")

    result = cursor.execute("""
                            create table in_shopping_cart(
                            ticket_id int not null auto_increment,
                            user_id int not null,
                            FOREIGN KEY (user_id) REFERENCES user(user_id)
                            ON DELETE CASCADE,
                            FOREIGN KEY (ticket_id) REFERENCES ticket(ticket_id)
                            ON DELETE CASCADE,
                            PRIMARY KEY (ticket_id) 
                            ) ENGINE=INNODB;
                            """)
    print("in_shopping_cart table created successfully")

    result = cursor.execute("""
                            create table rating(
                            rating_id int not null auto_increment,
                            user_id int not null,
                            rating int not null,
                            comment text(500),
                            rating_date DATE not null,
                            event_id int not null,
                            FOREIGN KEY (user_id) REFERENCES user(user_id)
                            ON DELETE CASCADE,
                            FOREIGN KEY (event_id) REFERENCES event(event_id)
                            ON DELETE CASCADE,
                            PRIMARY KEY (rating_id)
                            ) ENGINE=INNODB;
                            """)
    print("rating table created successfully")

    result = cursor.execute("""
                            create table event_category(
                            event_id int not null,
                            ticket_category VARCHAR(30),
                            ticket_price FLOAT(20),
                            FOREIGN KEY (event_id) REFERENCES event(event_id)
                            ON DELETE CASCADE,
                            PRIMARY KEY (event_id, ticket_category)
                            ) ENGINE=INNODB;
                            """)
    print("event_category table created successfully")

    result = cursor.execute("""
                            create table joins(
                            event_id int not null,
                            user_id int not null,
                            FOREIGN KEY (event_id) REFERENCES event(event_id)
                            ON DELETE CASCADE,
                            FOREIGN KEY (user_id) REFERENCES user(user_id)
                            ON DELETE CASCADE,
                            PRIMARY KEY (event_id, user_id)
                            ) ENGINE=INNODB;
                            """)
    print("joins table created successfully")

    result = cursor.execute("""
                            create table saves(
                            user_id int not null,
                            event_id int not null,
                            public_visibility BOOL not null,
                            FOREIGN KEY (user_id) REFERENCES user(user_id)
                            ON DELETE CASCADE,
                            FOREIGN KEY (event_id) REFERENCES event(event_id)
                            ON DELETE CASCADE,
                            PRIMARY KEY (user_id, event_id)
                            ) ENGINE=INNODB;
                            """)
    print("saves table created successfully")

    result = cursor.execute("""
                            create table concert(
                            event_id int not null,
                            genre VARCHAR(30),
                            FOREIGN KEY (event_id) REFERENCES event(event_id)
                            ON DELETE CASCADE,
                            PRIMARY KEY (event_id)
                            ) ENGINE=INNODB;
                            """)
    print("concert table created successfully")

    result = cursor.execute("""
                            create table game(
                            event_id int not null,
                            sport_type VARCHAR(30),
                            FOREIGN KEY (event_id) REFERENCES event(event_id)
                            ON DELETE CASCADE,
                            PRIMARY KEY (event_id)
                            ) ENGINE=INNODB;
                            """)
    print("game table created successfully")

    result = cursor.execute("""
                            create table artist(
                            artist_id int not null auto_increment,
                            name varchar(50) not null,
                            description MEDIUMTEXT not null,
                            image varchar(50),
                            genre varchar(30) not null,
                            follower_count int not null,
                            PRIMARY KEY (artist_id)
                            ) ENGINE=INNODB;
                            """)
    print("artist table created successfully")

    result = cursor.execute("""
                            insert into artist values(
                                NULL,
                                "Yalın", 
                                "Zalim, oyunu bozan, sen de bu büyü de yalan...", 
                                NULL, 
                                "Pop", 
                                0
                            );
                            """)
    result = cursor.execute("""
                            insert into artist values(
                                NULL,
                                "Duman", 
                                "Duman is an amazing group!", 
                                NULL, 
                                "Rock", 
                                0
                            );
                            """)
    result = cursor.execute("""
                            insert into artist values(
                                NULL,
                                "Kenan Doğulu", 
                                "Kenan is an amazing group!", 
                                NULL, 
                                "Pop", 
                                0
                            );
                            """)
    result = cursor.execute("""
                            insert into artist values(
                                NULL,
                                "Mor ve Ötesi", 
                                "MVÖ is an amazing group!", 
                                NULL, 
                                "Rock", 
                                0
                            );
                            """)
    result = cursor.execute("""
                            insert into artist values(
                                NULL,
                                "Ezhel", 
                                "Ezhel is an amazing group!", 
                                NULL, 
                                "Rap", 
                                0
                            );
                            """)
    result = cursor.execute("""
                            insert into artist values(
                                NULL,
                                "Killa Hakan", 
                                "Killa is an amazing group!", 
                                NULL, 
                                "Rap", 
                                0
                            );
                            """)
    print("successfully inserted values")

    result = cursor.execute("""
                            create table performs(
                            event_id int not null,
                            artist_id int not null,
                            FOREIGN KEY (event_id) REFERENCES event(event_id)
                            ON DELETE CASCADE,
                            FOREIGN KEY (artist_id) REFERENCES artist(artist_id)
                            ON DELETE CASCADE,
                            PRIMARY KEY (artist_id, event_id)
                            ) ENGINE=INNODB;
                            """)
    print("performs table created successfully")

    result = cursor.execute("""
                            create table team(
                            team_id int not null auto_increment,
                            name varchar(50) not null,
                            description MEDIUMTEXT not null,
                            image varchar(50),
                            PRIMARY KEY (team_id)
                            ) ENGINE=INNODB;
                            """)
    print("team table created successfully")

    result = cursor.execute("""
                            create table competes(
                            team_id int not null,
                            event_id int not null,
                            FOREIGN KEY (team_id) REFERENCES team(team_id)
                            ON DELETE CASCADE,
                            FOREIGN KEY (event_id) REFERENCES event(event_id)
                            ON DELETE CASCADE,
                            PRIMARY KEY (team_id, event_id)
                            ) ENGINE=INNODB;
                            """)
    print("competes table created successfully")

    result = cursor.execute("""
                            create table follows(
                            artist_id int not null,
                            user_id int not null,
                            FOREIGN KEY (artist_id) REFERENCES artist(artist_id)
                            ON DELETE CASCADE,
                            FOREIGN KEY (user_id) REFERENCES user(user_id)
                            ON DELETE CASCADE,
                            PRIMARY KEY (artist_id, user_id)
                            ) ENGINE=INNODB;
                            """)
    print("follows table created successfully")

    result = cursor.execute("""
                            create table tags_event(
                            event_id int not null,
                            blog_id int not null,
                            FOREIGN KEY (event_id) REFERENCES event(event_id)
                            ON DELETE CASCADE,
                            FOREIGN KEY (blog_id) REFERENCES blog(blog_id)
                            ON DELETE CASCADE,
                            PRIMARY KEY (event_id, blog_id)
                            ) ENGINE=INNODB;
                            """)
    print("tags_event table created successfully")

    result = cursor.execute("""
                            create table tags_artist(
                            artist_id int not null,
                            blog_id int not null,
                            FOREIGN KEY (artist_id) REFERENCES artist(artist_id)
                            ON DELETE CASCADE,
                            FOREIGN KEY (blog_id) REFERENCES blog(blog_id)
                            ON DELETE CASCADE,
                            PRIMARY KEY (blog_id, artist_id)
                            ) ENGINE=INNODB;
                            """)
    print("tags_artist table created successfully")

    # USER VIEW FOR EVENTS
    result = cursor.execute("""
                            CREATE VIEW event_view(event_id, event_name, description, date,
                            event_type, status, age_limit, total_quota,
                            seating_plan, avg_rating, venue_id, event_city,
                            event_adress) AS (
                            SELECT event_id, event.name, event.description, date, event_type,
                            status, age_limit, total_quota, seating_plan, avg_rating,
                            venue.venue_id, venue.city, venue.address
                            FROM event JOIN venue USING (venue_id));
                            """)

    # VIEW TO GET ALL ARTIST'S INFORMATION
    result = cursor.execute("""
                            CREATE VIEW artist_view(artist_id, artist_name, artist_image, artist_genre)
                            AS ( SELECT artist_id, name, image, genre FROM artist);
                            """)

    # TRIGGERS

    # update remaining quota after insert on joins
    result = cursor.execute("""
                            create trigger ticket_count_update
                            after insert on joins
                            for each row  
                            begin
                            UPDATE event
                            SET event.remaining_quota = event.remaining_quota - 1
                            WHERE event.event_id = NEW.event_id;
                            end;
                            """)

    # update remaining quota after delete on joins
    result = cursor.execute("""
                            create trigger ticket_count_update_delete
                            after delete on joins
                            for each row  
                            begin
                            UPDATE event
                            SET event.remaining_quota = event.remaining_quota + 1
                            WHERE event.event_id = OLD.event_id;
                            end;
                            """)

    # update average rating after new rating is added
    result = cursor.execute("""
                            create trigger new_rating
                            after insert on rating
                            for each row
                            begin
                            UPDATE event
                            SET event.avg_rating = (SELECT avg(rating)
                            FROM rating
                            WHERE event_id = NEW.event_id)
                            WHERE event.event_id = NEW.event_id;
                            end;
                            """)

    # Update Average Rating After Rating Is Updated
    result = cursor.execute("""
                            create trigger rating_update
                            after update on rating
                            for each row
                            begin
                            UPDATE event
                            SET event.avg_rating = (SELECT avg(rating)
                            FROM rating
                            WHERE event_id = NEW.event_id)
                            WHERE event.event_id = NEW.event_id;
                            end;
                            """)

    # Update Average Rating After Rating is Deleted
    result = cursor.execute("""
                            create trigger rating_delete
                            before delete on rating
                            for each row
                            begin
                            UPDATE event
                            SET event.avg_rating = (SELECT avg(rating)
                            FROM rating
                            WHERE event_id = OLD.event_id)
                            WHERE event.event_id = OLD.event_id;
                            end;
                            """)

    # Update Follower Count After Insert on Follows
    result = cursor.execute("""
                            create trigger follower_count_update
                            after insert on follows
                            for each row
                            begin
                            UPDATE artist
                            SET artist.follower_count = artist.follower_count + 1
                            WHERE artist.artist_id = NEW.artist_id;
                            end;
                            """)

    # cannot insert two users with same email
    result = cursor.execute("""
                            create trigger email_check
                            before insert on user
                            for each row
                            begin
                            if exists (select * from user where email = NEW.email) then
                            signal sqlstate '45000'
                            SET MESSAGE_TEXT = 'Two users with the same email cannot exist!'; 
                            end if;
                            end;
                            """)

    # when something is deleted from joins, delete it from ticket as well
    result = cursor.execute("""
                            create trigger ticket_check
                            after delete on joins
                            for each row
                            begin
                            DELETE FROM ticket
                            where user_id = OLD.user_id and event_id = OLD.event_id;
                            end;
                            """)

except Error as e:
    print("Error while connecting to MySQL", e)
