CREATE SCHEMA IF NOT EXISTS `bd_sgl` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `bd_sgl` ;

-- -----------------------------------------------------
-- Table `bd_sgl`.`livros`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd_sgl`.`livros` (
  `idlivro` INT NOT NULL AUTO_INCREMENT COMMENT 'Identificando da tabela de livros',
  `titulo` VARCHAR(255) NOT NULL COMMENT 'Título do livro cadastrado',
  `autor` VARCHAR(255) NOT NULL COMMENT 'Auto do livro',
  `ano_publicacao` INT NULL DEFAULT NULL COMMENT 'Ano da publicação do livro',
  `genero` VARCHAR(100) NULL DEFAULT NULL COMMENT 'Gênero do livro',
  `bloqueado` CHAR(1) NOT NULL DEFAULT 'N' COMMENT 'Campo que informa se o livro está bloqueado devido ao aluguel. S-Bloqueado / N-Desbloqueado',
  PRIMARY KEY (`idlivro`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `bd_sgl`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd_sgl`.`usuarios` (
  `idusuario` INT NOT NULL AUTO_INCREMENT COMMENT 'Identificador da tabela de usuário',
  `nome` VARCHAR(60) NULL DEFAULT NULL COMMENT 'Nome do usuário no sistema',
  `login` VARCHAR(20) NULL DEFAULT NULL COMMENT 'Login do usuário no sistema',
  `password` VARCHAR(200) NULL DEFAULT NULL COMMENT 'Senha do usuário no sistema',
  `dataAniversario` DATE NULL DEFAULT NULL COMMENT 'Data do aniversário do usuário',
  `ativo` CHAR(1) NULL DEFAULT 'A' COMMENT 'A - Ativo\\\\n I - Inativado',
  PRIMARY KEY (`idusuario`),
  INDEX `USU_SQ1` (`login` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 12
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `bd_sgl`.`livrosAlugados`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd_sgl`.`livrosAlugados` (
  `idLivrosAlugados` INT NOT NULL AUTO_INCREMENT COMMENT 'Identificado da tabela Livros Alugados',
  `idusuario` INT NOT NULL COMMENT 'Identificador do usuário',
  `idlivro` INT NOT NULL COMMENT 'Identificador do livro\n',
  `dataAluguel` DATE NOT NULL COMMENT 'Data em que o usuário alugou o livro',
  `dataDevolucao` DATE NULL COMMENT 'Data em que o usuário devolveu o livro',
  `dataEntrega` DATE NULL COMMENT 'Data da previsão da entrega do livro',
  PRIMARY KEY (`idLivrosAlugados`, `idusuario`, `idlivro`),
  INDEX `fk_usuarios_has_livros_livros1_idx` (`idlivro` ASC) VISIBLE,
  INDEX `fk_usuarios_has_livros_usuarios_idx` (`idusuario` ASC) VISIBLE,
  CONSTRAINT `fk_usuarios_has_livros_usuarios`
    FOREIGN KEY (`idusuario`)
    REFERENCES `bd_sgl`.`usuarios` (`idusuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_usuarios_has_livros_livros1`
    FOREIGN KEY (`idlivro`)
    REFERENCES `bd_sgl`.`livros` (`idlivro`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `bd_sgl`.`settings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd_sgl`.`settings` (
  `idsettings` INT NOT NULL AUTO_INCREMENT COMMENT 'Identificador da tabela de settings',
  `diasLivroEmprestado` INT NULL COMMENT 'Quantidade de dias que um livro poderá permanecer emprestado',
  `createdAt` DATE NULL DEFAULT curdate() COMMENT 'Data de criação do registro',
  `updatedAt` DATE NULL COMMENT 'Data de atualização do registro',
  PRIMARY KEY (`idsettings`))
ENGINE = InnoDB;
