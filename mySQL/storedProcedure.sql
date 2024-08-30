USE `mydb`;
DROP procedure IF EXISTS `new_procedure`;

USE `mydb`;
DROP procedure IF EXISTS `mydb`.`new_procedure`;
;

DELIMITER $$
USE `mydb`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `new_procedure`()
BEGIN
DECLARE currentDate DATE;
    SET currentDate = CURDATE();

   INSERT INTO Benachrichtigung (Datum,Pflanzen_ID, Info)
    SELECT distinct currentDate as Datum,  Gießen.Pflanzen_ID, "Info" as Info
    FROM (SELECT   MAX(Datum) as Datum, Pflanzen_ID  FROM mydb.Gießen group by Pflanzen_ID order by Datum desc )as Gießen, Pflanzen p
    JOIN Label_has_Pflanzen lhp ON p.ID = lhp.Pflanzen_ID
    JOIN Label l ON l.ID = lhp.Label_ID
    WHERE l.Bezeichnung = 'wenig gießen'
      AND DATEDIFF(currentDate, Gießen.Datum) > 12
      AND NOT EXISTS (
          SELECT 1
          FROM Benachrichtigung b
          WHERE b.Pflanzen_ID = Gießen.Pflanzen_ID
      );

    -- Überprüfung für mittel gießen (7 Tage)
   INSERT INTO Benachrichtigung (Datum,Pflanzen_ID, Info)
    SELECT distinct currentDate as Datum,  Gießen.Pflanzen_ID, "Info" as Info
    FROM (SELECT   MAX(Datum) as Datum, Pflanzen_ID  FROM mydb.Gießen group by Pflanzen_ID order by Datum desc )as Gießen, Pflanzen p
    JOIN Label_has_Pflanzen lhp ON p.ID = lhp.Pflanzen_ID
    JOIN Label l ON l.ID = lhp.Label_ID
    WHERE l.Bezeichnung = 'mittel gießen'
      AND DATEDIFF(currentDate, Gießen.Datum) > 7
      AND NOT EXISTS (
          SELECT 1
          FROM Benachrichtigung b
          WHERE b.Pflanzen_ID = Gießen.Pflanzen_ID
      );


    -- Überprüfung für viel gießen (3 Tage)
   INSERT INTO Benachrichtigung (Datum,Pflanzen_ID, Info)
    SELECT distinct currentDate as Datum,  Gießen.Pflanzen_ID, "Info" as Info
    FROM  (SELECT   MAX(Datum) as Datum, Pflanzen_ID  FROM mydb.Gießen group by Pflanzen_ID order by Datum desc )as Gießen, Pflanzen p
    JOIN Label_has_Pflanzen lhp ON p.ID = lhp.Pflanzen_ID
    JOIN Label l ON l.ID = lhp.Label_ID
    WHERE l.Bezeichnung = 'viel gießen'
      AND DATEDIFF(currentDate, Gießen.Datum) > 3
      AND NOT EXISTS (
          SELECT 1
          FROM Benachrichtigung b
          WHERE b.Pflanzen_ID = Gießen.Pflanzen_ID
      );
END$$

DELIMITER ;
;








DELIMITER //

CREATE EVENT `daily_event`
ON SCHEDULE EVERY 1 DAY
STARTS '2024-08-21 02:00:00'  -- Startdatum und -uhrzeit
DO
BEGIN
   call mydb.new_procedure();
END //

DELIMITER ;


INSERT INTO `mydb`.`Label` (`Bezeichnung`) VALUES
('halb sonnig schattig'),
('keine Sonne'),
('mittel gießen'),
('schattig'),
('sonnig'),
('viel gießen'),
('wenig gießen'),
('dungen');
