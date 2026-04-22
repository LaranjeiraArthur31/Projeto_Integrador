/* sertificar-se se possui database*/
CREATE TABLE usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255),
    email VARCHAR(255),
    empresa VARCHAR(255)
);
CREATE TABLE categorias (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255)
 );
 CREATE TABLE prioridades (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nivel VARCHAR(100)
);
CREATE TABLE STATUS (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100)
);

 
CREATE TABLE tickets (
    id INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(255),
    descricao TEXT,
    categoria_id INT,
    prioridade_id INT,
    status_id INT,
    usuario_abertura_id INT,
    usuario_responsavel_id INT,
    data_abertura DATETIME,
    data_atualizacao DATETIME,
    data_fechamento DATETIME,

    
    FOREIGN KEY (categoria_id) REFERENCES categorias(id),
    FOREIGN KEY (prioridade_id) REFERENCES prioridades(id),
    FOREIGN KEY (status_id) REFERENCES STATUS(id),
    FOREIGN KEY (usuario_abertura_id) REFERENCES usuarios(id),
    FOREIGN KEY (usuario_responsavel_id) REFERENCES usuarios(id)
);



CREATE TABLE ticket_historico (
    id INT PRIMARY KEY AUTO_INCREMENT,
    ticket_id INT,
    status_id INT,
    comentario TEXT,
    data DATETIME,

    FOREIGN KEY (ticket_id) REFERENCES tickets(id),
    FOREIGN KEY (status_id) REFERENCES status(id)
);