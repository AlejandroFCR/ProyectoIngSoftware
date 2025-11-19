USE proyectVegtablePatch;

CREATE TABLE Usuario(
	idUsuario INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    correo VARCHAR(40) NOT NULL UNIQUE,
    nombreUsuario	VARCHAR(50) NOT NULL,
    validacion BOOL DEFAULT FALSE
);

CREATE TABLE Planta(
	idPlanta INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombrePlanta CHAR(20) UNIQUE NOT NULL,
    phInitRecomendado float NOT NULL DEFAULT 7.0,
    phFinRecomendado float NOT NULL DEFAULT 7.1,
    temperaturaInitRecomendada float NOT NULL DEFAULT 0,
    temperaturaFinRecomendada float NOT NULL DEFAULT 1,
    humedadInitRecomendada float NOT NULL DEFAULT 0,
    humedadFinRecomendada float NOT NULL DEFAULT 1
);

CREATE TABLE Sensor(
	idSensor INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    idUsuario INT UNSIGNED,
    idPlanta INT UNSIGNED,
    MAC CHAR(17) UNIQUE NOT NULL,
    rangoInitPh FLOAT,
    rangoFinPh FLOAT,
    rangoInitTemperatura FLOAT,
    rangoFinTemperatura FLOAT,
    rangoInitHumedad FLOAT,
    rangoFinHumedad FLOAT,
    CONSTRAINT fkSensorUsuario
		FOREIGN KEY (idUsuario)
        REFERENCES Usuario (idUsuario),
	CONSTRAINT fkSensorPlanta
		FOREIGN KEY (idPlanta)
		REFERENCES Planta (idPlanta)
);

CREATE TABLE Bitacora(
	idBitacora INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    idSensor INT UNSIGNED NOT NULL,
    idPlanta INT UNSIGNED,
    temperaturaTomada FLOAT,
    humedadTomada FLOAT,
    phTomado FLOAT,
    fechaHoraCaptura FLOAT,
    limiteInitTemperatura FLOAT,
    limiteFinTemperatura FLOAT,
    limiteInitPh FLOAT,
    limiteFinPh FLOAT,
    limiteInitHumedad FLOAT,
    limiteFinHumedad FLOAT,
    
    CONSTRAINT fkBitacoraSensor
		FOREIGN KEY (idSensor)
		REFERENCES Sensor(idSensor),
        
	CONSTRAINT fkBitacoraPlanta
		FOREIGN KEY (idPlanta)
        REFERENCES Planta(idPlanta)
);