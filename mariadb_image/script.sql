CREATE TABLE users (
  `id` INT NOT NULL AUTO_INCREMENT,
  `prenom` VARCHAR(255) NULL,
  `nom` VARCHAR(255) NULL,
  `sexe` VARCHAR(45) NULL,
  `pseudo` VARCHAR(255) NULL,
  PRIMARY KEY (`id`));

  INSERT INTO users (prenom, nom, sexe, pseudo) VALUES ('Luc', 'Truc', 'Homme', 'TucLuc');