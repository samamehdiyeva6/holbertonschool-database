-- Create a table named `store` with the following columns:
DELIMITER $$
CREATE TRIGGER after_adding_items
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END$$
DELIMITER ;
