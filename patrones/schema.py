instructions = [
    'SET FOREIGN_KEY_CHECKS=0;',
    'DROP TABLE IF EXISTS Usuario;',
    'DROP TABLE IF EXISTS Recordatorio;',
    'DROP TABLE IF EXISTS Medicamento;',
    'DROP TABLE IF EXISTS Cita;',
    'DROP TABLE IF EXISTS Mensaje;',
    'DROP TABLE IF EXISTS ObligacionesFinancieras;',
    'DROP TABLE IF EXISTS Pension;',
    'DROP TABLE IF EXISTS historialGastos;',
    'SET FOREIGN_KEY_CHECKS=1;',
    """
        CREATE TABLE Usuario(
            id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            address VARCHAR(100) NOT NULL,
            phone VARCHAR(10) NOT NULL,
            birthdate DATE NOT NULL,
            role INT NOT NULL,
            family VARCHAR(100) NOT NULL
        );
    """,
    """
        CREATE TABLE Recordatorio(
            id INT PRIMARY KEY AUTO_INCREMENT,
            created_by INT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            description TEXT NOT NULL,
            completed BOOLEAN NOT NULL,
            FOREIGN KEY (created_by) REFERENCES Usuario (id)
        );
    """,
    """
        CREATE TABLE Medicamento(
            id INT PRIMARY KEY AUTO_INCREMENT,
            created_by INT NOT NULL,
            medicine VARCHAR(100) NOT NULL,
            description TEXT NOT NULL,
            dose VARCHAR(100) NOT NULL,
            posology VARCHAR(100) NOT NULL,
            price DOUBLE NOT NULL,
            amount INT NOT NULL,
            FOREIGN KEY (created_by) REFERENCES Usuario (id)
        );
    """,
    """
        CREATE TABLE Mensaje(
            id INT PRIMARY KEY AUTO_INCREMENT,
            created_by INT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            Contentmsg VARCHAR(100) NOT NULL,
            FOREIGN KEY (created_by) REFERENCES Usuario (id)    
        );
    """,
    """
        CREATE TABLE Cita(
            id INT PRIMARY KEY AUTO_INCREMENT,
            created_by INT NOT NULL,
            date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            doctor VARCHAR(100) NOT NULL,
            specialization VARCHAR(100) NOT NULL,
            companion VARCHAR(100) NOT NULL,
            FOREIGN KEY (created_by) REFERENCES Usuario (id)
        );
    """,
     """
        CREATE TABLE ObligacionesFinancieras(
            id INT PRIMARY KEY AUTO_INCREMENT,
            created_by INT NOT NULL,
            name VARCHAR(100) NOT NULL,
            bank VARCHAR(100) NOT NULL,
            value DOUBLE NOT NULL,
            Nextpaydate Date NOT NULL,
            FOREIGN KEY (created_by) REFERENCES Usuario (id)    
        );
    """,
     """
        CREATE TABLE Pension(
            id INT PRIMARY KEY AUTO_INCREMENT,
            created_by INT NOT NULL,
            initialvalue double,
            startdate date,
            pensionvalue double,
            FOREIGN KEY (created_by) REFERENCES Usuario (id)    
        );
    """,
     """
        CREATE TABLE historialGastos(
            id INT PRIMARY KEY AUTO_INCREMENT,
            created_by INT NOT NULL,
            pensionactual double,
            expend double,
            expendconcept varchar(100),
            expenddate date,
            FOREIGN KEY (created_by) REFERENCES Usuario (id)    
        );
    """
]