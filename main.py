import controller as con
import sys

c = con.Controller()
try:
    command = sys.argv[1]
except IndexError:
    c.v.no_command()
else:
    if command == 'print_table':
        try:
            name = sys.argv[2]
        except IndexError:
            c.v.argument_error()
        else:
            c.print(name)

    elif command == 'delete_record':
        try:
            args = {"name": sys.argv[2], "key": sys.argv[3], "val": sys.argv[4]}
        except IndexError:
            c.v.argument_error()
        else:
            c.delete(args["name"], args["key"], args["val"])
#todo
    elif command == 'update_record':
        try:
            args = {"table": sys.argv[2].upper(), "key": sys.argv[3].upper()}
            if args["table"] == 'PRODUCT':
                args["shop_id"], args["photo_url"], args["name"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6]
            elif args["table"] == 'DISCOUNT':
                args["percent"], args["duration"] = \
                    sys.argv[4], sys.argv[5]
            elif args["table"] == 'PRODUCT_DISCOUNT':
                args["product_id"], args["discount_id"] = \
                    sys.argv[4], sys.argv[5]
            elif args["table"] == 'SHOP':
                args["address"], args["manager_name"], args["manager_surname"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6]
            else:
                c.v.wrong_table()
        except IndexError:
            c.v.argument_error()
        else:
            print(args)
            if args["table"] == 'PRODUCT':
                c.update_product(args["key"], args["shop_id"], args["photo_url"], args["name"])
            elif args["table"] == 'DISCOUNT':
                c.update_discount(args["key"], args["percent"], args["duration"])
            elif args["table"] == 'PRODUCT_DISCOUNT':
                c.update_product_discount(args["key"], args["product_id"], args["discount_id"])
            elif args["table"] == 'SHOP':
                c.update_shop(args["key"], args["address"], args["manager_name"], args["manager_surname"])
#todo
    elif command == 'insert_record':
        try:
            args = {"table": sys.argv[2].upper(), "key": sys.argv[3].upper()}
            if args["table"] == 'PRODUCT':
                args["shop_id"], args["photo_url"], args["name"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6]
            elif args["table"] == 'DISCOUNT':
                args["percent"], args["duration"] = \
                    sys.argv[4], sys.argv[5]
            elif args["table"] == 'PRODUCT_DISCOUNT':
                args["product_id"], args["discount_id"] = \
                    sys.argv[4], sys.argv[5]
            elif args["table"] == 'SHOP':
                args["address"], args["manager_name"], args["manager_surname"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6]
            else:
                c.v.wrong_table()
        except IndexError:
            c.v.argument_error()
        else:
            if args["table"] == 'PRODUCT':
                c.insert_product(args["key"], args["shop_id"], args["photo_url"], args["name"])
            elif args["table"] == 'DISCOUNT':
                c.insert_discount(args["key"], args["percent"], args["duration"])
            elif args["table"] == 'PRODUCT_DISCOUNT':
                c.insert_product_discount(args["key"], args["product_id"], args["discount_id"])
            elif args["table"] == 'SHOP':
                c.insert_shop(args["key"], args["address"], args["manager_name"], args["manager_surname"])

    elif command == 'generate_randomly':
        try:
            args = {"name": sys.argv[2], "n": int(sys.argv[3])}
        except (IndexError, Exception):
            print(Exception, IndexError)
        else:
            c.generate(args["name"], args["n"])
#todo
    elif command == 'search_records':
        while True:
            search_num = c.v.get_search_num()
            try:
                search_num = int(search_num)
            except ValueError:
                c.v.invalid_search_num()
            else:
                if search_num in [2, 3, 4]:
                    break
                else:
                    c.v.invalid_search_num()
        if search_num == 2:
            c.search_two()
        elif search_num == 3:
            c.search_three()
        elif search_num == 4:
            c.search_all()




    elif command == 'help':
        c.v.print_help()
    else:
        c.v.wrong_command()
