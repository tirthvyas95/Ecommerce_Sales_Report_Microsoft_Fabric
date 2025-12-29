import psycopg2

hostname = 'localhost'
database = 'Test'
username = 'PyApp'
pwd = 'Test@123'
port_id = 5432
conn = None

try:
    with psycopg2.connect(
            host =  hostname,
            dbname = database,
            user = username,
            password = pwd,
            port = port_id) as conn:
                with conn.cursor() as cur:                
                        case = int(input("1 - Insert \n2 - Insert Another\n0 - DELETE\n"))
                        if case == 1:
                            cur.execute("""
                                            INSERT INTO public."Orders"(
                                                "OrderDate", "Quantity", "Discount", "Tax", "ShippingCost", "TotalAmount", "PaymentMethod", "OrderStatus", "OrderID", "CustomerID", "ProductID", "SellerID")
                                            VALUES ('2024-12-30', 2, 0.15, 77.88, 9.31, 1060.73, 'Debit Card', 'Delivered', 100001, 9034, 41, 1273);
                                        """
                        )
                        if case == 2:
                            cur.execute("""
                                            INSERT INTO public."Orders"(
                                                "OrderDate", "Quantity", "Discount", "Tax", "ShippingCost", "TotalAmount", "PaymentMethod", "OrderStatus", "OrderID", "CustomerID", "ProductID", "SellerID")
                                            VALUES ('2024-12-31', 2, 0.15, 77.88, 9.31, 1060.73, 'Debit Card', 'Delivered', 100002, 9034, 41, 1273);
                                        """
                        )
                        if case == 0:
                            cur.execute("""
                                            DELETE FROM public."Orders" as po
                                            WHERE po."OrderID" > 100000;
                                        """
                        )
                        print("Done")

except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()