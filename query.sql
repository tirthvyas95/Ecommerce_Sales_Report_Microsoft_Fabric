

SELECT *
From public."Products"
ORDER BY public."Product"."ProductID" DESC;

SELECT *
From public."Orders"
ORDER BY public."Orders"."OrderID" DESC
LIMIT 1000;

INSERT INTO public."Products" (ProductName, Category, Brand, UnitPrice, ProductID)
Values ("Bluetooth Speaker", "Electronics", "KiddoFun2", 556.68, 51);

INSERT INTO public."Products"(
	"ProductName", "Category", "Brand", "UnitPrice", "ProductID")
	VALUES ('Speaker', 'Electronics', 'KiddoFun2', 556.68, 51);
	
DELETE FROM public."Products" as po
	WHERE po."ProductID" = 51;

DELETE FROM public."Orders" as po
	WHERE po."OrderID" = 100001;

INSERT INTO public."Orders"(
	"OrderDate", "Quantity", "Discount", "Tax", "ShippingCost", "TotalAmount", "PaymentMethod", "OrderStatus", "OrderID", "CustomerID", "ProductID", "SellerID")
	VALUES ('2024-12-30', 2, 0.15, 77.88, 9.31, 1060.73, 'Debit Card', 'Delivered', 100001, 9034, 41, 1273);

GRANT SELECT, DELETE ON ALL TABLES IN SCHEMA public TO pg_write_all_data;