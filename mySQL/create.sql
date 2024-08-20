-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Pflanzen`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Pflanzen` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Bezeichnung` VARCHAR(80) NOT NULL,
  `UUID` VARCHAR(45) NOT NULL,
  `Angelegt_am` DATETIME NULL,
  `Text` VARCHAR(200) NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Label`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Label` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Bezeichnung` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Label_has_Pflanzen`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Label_has_Pflanzen` (
  `Label_ID` INT NOT NULL,
  `Pflanzen_ID` INT NOT NULL,
  PRIMARY KEY (`Label_ID`, `Pflanzen_ID`),
  INDEX `fk_Label_has_Pflanzen_Pflanzen1_idx` (`Pflanzen_ID` ASC) VISIBLE,
  INDEX `fk_Label_has_Pflanzen_Label_idx` (`Label_ID` ASC) VISIBLE,
  CONSTRAINT `fk_Label_has_Pflanzen_Label`
    FOREIGN KEY (`Label_ID`)
    REFERENCES `mydb`.`Label` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Label_has_Pflanzen_Pflanzen1`
    FOREIGN KEY (`Pflanzen_ID`)
    REFERENCES `mydb`.`Pflanzen` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Bilder(original)`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Bilder(original)` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Bildbezeichnung` VARCHAR(100) NOT NULL,
  `Pfad` VARCHAR(100) NOT NULL,
  `Pflanzen_ID` INT NOT NULL,
  `Datum` DATETIME NULL,
  `Bilder(original)col` VARCHAR(45) NULL,
  PRIMARY KEY (`ID`),
  INDEX `fk_Bilder(original)_Pflanzen1_idx` (`Pflanzen_ID` ASC) VISIBLE,
  CONSTRAINT `fk_Bilder(original)_Pflanzen1`
    FOREIGN KEY (`Pflanzen_ID`)
    REFERENCES `mydb`.`Pflanzen` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Bilder(bearbeitet)`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Bilder(bearbeitet)` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Bildbezeichnung` VARCHAR(100) NOT NULL,
  `Pfad` VARCHAR(100) NOT NULL,
  `Pflanzen_ID` INT NOT NULL,
  `Datum` DATETIME NULL,
  `Bilder(bearbeitet)col` VARCHAR(45) NULL,
  PRIMARY KEY (`ID`),
  INDEX `fk_Bilder(bearbeitet)_Pflanzen1_idx` (`Pflanzen_ID` ASC) VISIBLE,
  CONSTRAINT `fk_Bilder(bearbeitet)_Pflanzen1`
    FOREIGN KEY (`Pflanzen_ID`)
    REFERENCES `mydb`.`Pflanzen` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Messungen`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Messungen` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Messwert` DECIMAL NOT NULL,
  `Empfangen am` DATETIME NULL,
  `Pflanzen_ID` INT NOT NULL,
  PRIMARY KEY (`ID`),
  INDEX `fk_Messungen_Pflanzen1_idx` (`Pflanzen_ID` ASC) VISIBLE,
  CONSTRAINT `fk_Messungen_Pflanzen1`
    FOREIGN KEY (`Pflanzen_ID`)
    REFERENCES `mydb`.`Pflanzen` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Benachrichtigung`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Benachrichtigung` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Datum` DATETIME NULL,
  `Pflanzen_ID` INT NOT NULL,
  `Info` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`ID`),
  INDEX `fk_Benachrichtigung_Pflanzen1_idx` (`Pflanzen_ID` ASC) VISIBLE,
  CONSTRAINT `fk_Benachrichtigung_Pflanzen1`
    FOREIGN KEY (`Pflanzen_ID`)
    REFERENCES `mydb`.`Pflanzen` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Einstellung`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Einstellung` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Grenzwert_Min` DECIMAL NULL,
  `Grenzwert_Max` DECIMAL NULL,
  `Pflanzen_ID` INT NOT NULL,
  PRIMARY KEY (`ID`),
  INDEX `fk_Einstellung_Pflanzen1_idx` (`Pflanzen_ID` ASC) VISIBLE,
  CONSTRAINT `fk_Einstellung_Pflanzen1`
    FOREIGN KEY (`Pflanzen_ID`)
    REFERENCES `mydb`.`Pflanzen` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Gießen`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Gießen` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Gegossen_am` DATE NOT NULL,
  `Pflanzen_ID` INT NOT NULL,
  PRIMARY KEY (`ID`),
  INDEX `fk_Gießen_Pflanzen1_idx` (`Pflanzen_ID` ASC) VISIBLE,
  CONSTRAINT `fk_Gießen_Pflanzen1`
    FOREIGN KEY (`Pflanzen_ID`)
    REFERENCES `mydb`.`Pflanzen` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;


INSERT INTO `mydb`.`Label` (`Bezeichnung`) VALUES
('halb sonnig schattig'),
('keine Sonne'),
('mittel giesen'),
('schattig'),
('sonnig'),
('viel giesen'),
('wenig giesen'),
('dungen');