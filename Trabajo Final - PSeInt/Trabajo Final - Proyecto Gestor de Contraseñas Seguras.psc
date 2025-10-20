Algoritmo GestorContraseñasSeguras // Alba Sánchez
	
	Definir n, i Como Entero
	Definir usuarios, contrasenas Como Cadena
	Dimension usuarios[100]
	Dimension contrasenas[100]
	Escribir "Cantidad de usuarios a registrar (max 100):"
	Leer n
	Si n<1 Entonces
		Escribir "Nada que registrar."
		n <- 0
	FinSi
	Si n>100 Entonces
		n <- 100
	FinSi
	Para i<-1 Hasta n Con Paso 1 Hacer
		RegistrarUsuario(i, usuarios, contrasenas)
	FinPara
	GenerarAlertas(n, usuarios, contrasenas)
FinAlgoritmo

SubProceso RegistrarUsuario(pos, usuarios Por Referencia, contrasenas Por Referencia)
	Definir u, c Como Cadena
	Escribir "Usuario ", pos, ":"
	Leer u
	Escribir "Contraseña para ", u, ":"
	Leer c
	usuarios[pos] <- u
	contrasenas[pos] <- c
FinSubProceso

Funcion ok <- VerificarContrasena(cadena)
	Definir ok, tieneMayus, tieneMinus, tieneDigito, tieneEspecial Como Logico
	Definir i, L Como Entero
	Definir ch Como Cadena
	ok <- Falso
	tieneMayus <- Falso
	tieneMinus <- Falso
	tieneDigito <- Falso
	tieneEspecial <- Falso
	L <- Longitud(cadena)
	Para i<-1 Hasta L Con Paso 1 Hacer
		ch <- SubCadena(cadena, i, i)
		Si ch>="A" Y ch<="Z" Entonces
			tieneMayus <- Verdadero
		SiNo
			Si ch>="a" Y ch<="z" Entonces
				tieneMinus <- Verdadero
			SiNo
				Si ch>="0" Y ch<="9" Entonces
					tieneDigito <- Verdadero
				SiNo
					tieneEspecial <- Verdadero
				FinSi
			FinSi
		FinSi
	FinPara
	Si L>=8 Y tieneMayus Y tieneMinus Y tieneDigito Y tieneEspecial Entonces
		ok <- Verdadero
	FinSi
FinFuncion

SubProceso GenerarAlertas(n, usuarios Por Referencia, contrasenas Por Referencia)
	Definir i, fuertes, debiles Como Entero
	Definir esFuerte Como Logico
	fuertes <- 0
	debiles <- 0
	Para i<-1 Hasta n Con Paso 1 Hacer
		esFuerte <- VerificarContrasena(contrasenas[i])
		Si No esFuerte Entonces
			Escribir "ALERTA: ", usuarios[i], " tiene contraseña debil."
			debiles <- debiles + 1
		SiNo
			fuertes <- fuertes + 1
		FinSi
	FinPara
	Escribir "Resumen: Fuertes=", fuertes, "  Debiles=", debiles
	
FinSubProceso

	

	


