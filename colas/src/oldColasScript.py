# Script to set up the first simulation, regarding the current system in the
# costum area.

from colas import *

##############################
##############################
##############################
###                        ###
###                        ###
###    GLOBAL VARIABLES    ###
###                        ###
###                        ###
##############################
##############################
##############################


############################
# VARIABLES FOR SIMULACION #
############################
TOTAL_NUMBER_OF_TRANSPORTS = 1  # MAXIMUM NUMBER OF TRANSPORTS IN THE SIMULATION
LAMBDAS = [.003404, .020867, .020461, .020144,
		   .003404, .024524, .002688, .022317,
		   .003404, .027704, .029354, .023989,
		   .003404, .028195, .028155, .022686,
		   .003404, .027952, .029158, .022500,
		   .003404, .029355, .029147, .024383,
		   .003404, .027035, .027692, .020855]



#################################
# VARIABLES FOR COLA DE INGRESO #
#################################
COLA_DE_INGRESO_NAME = "COLA DE INGRESO"


######################################
# VARIABLES FOR TRAMITE DE MIGRACION #
######################################
TRAMITE_DE_MIGRACION_NAME  = "TRAMITE DE MIGRACION"
TRAMITE_DE_MIGRACION_CAP   = 3
TRAMITE_DE_MIGRACION_MEDIA = 3.17
TRAMITE_DE_MIGRACION_STDEV = 6.618


#################################
# VARIABLES FOR COLA DE ADUANAS #
#################################
COLA_DE_ADUANAS_NAME = "COLA DE ADUANAS"
COLA_DE_ADUANAS_CAP  = 2

####################################
# VARIABLES FOR TRAMITE DE ADUANAS #
####################################
TRAMITE_DE_ADUANAS_NAME  = "TRAMITE DE ADUANAS"
TRAMITE_DE_ADUANAS_CAP   = 3
TRAMITE_DE_ADUANAS_MEDIA = 21.00
TRAMITE_DE_ADUANAS_STDEV = 18.75

##########################
# VARIABLES FOR COLA PCD #
##########################
COLA_PCD_NAME = "COLA DE PCD"
COLA_PCD_CAP  = 50

################################
# VARIABLES FOR INSPECCION PCD #
################################
TRAMITE_DE_ADUANAS_NAME  = "INSPECCION PCD"
TRAMITE_DE_ADUANAS_CAP   = 1
TRAMITE_DE_ADUANAS_MEDIA = 22.33
TRAMITE_DE_ADUANAS_STDEV = 22.28

####################################
# VARIABLES FOR COLA A AGUJA NORTE #
####################################
COLA_A_AGUJA_NORTE_NAME = "COLA A AGUJA NORTE"
COLA_A_AGUJA_NORTE_CAP  = 40

####################################
# VARIABLES FOR TRAMITE DE ADUANAS #
####################################
TRAMITE_DE_AGUJA_NORTE_NAME  = "TRAMITE DE AGUJA NORTE"
TRAMITE_DE_AGUJA_NORTE_CAP   = 3
TRAMITE_DE_AGUJA_NORTE_MEDIA = 4.17
TRAMITE_DE_AGUJA_NORTE_STDEV = 9.50

########################################
# VARIABLES FOR COLA INGRESO NICARAGUA #
########################################
COLA_INGRESO_NICARAGUA_NAME = "COLA INGRESO NICARAGUA"
COLA_INGRESO_NICARAGUA_CAP  = 4

###################################
# VARIABLES FOR TRAMITE ASPERSION #
###################################
TRAMITE_ASPERSION_NAME  = "ASPERSION"
TRAMITE_ASPERSION_CAP   = 1
TRAMITE_ASPERSION_MEDIA = 30.12
TRAMITE_ASPERSION_STDEV = 9.50

###############################################
# VARIABLES FOR COLA POLICE CONTROL NICARAGUA #
###############################################
COLA_CONTROL_NICARAGUA_NAME = "COLA CONTROL NICARAGUA"
COLA_CONTROL_NICARAGUA_CAP  = 3

##########################################
# VARIABLES FOR POLICE CONTROL NICARAGUA #
##########################################
TRAMITE_CONTROL_NICARAGUA_NAME  = "CONTROL POLICIAL NICARAGUA"
TRAMITE_CONTROL_NICARAGUA_CAP   = 1
TRAMITE_CONTROL_NICARAGUA_MEDIA = 82.5
TRAMITE_CONTROL_NICARAGUA_STDEV = 20.75

##########################################
# VARIABLES FOR COLA MIGRACION NICARAGUA #
##########################################
COLA_MIGRACION_NICARAGUA_NAME = "COLA MIGRACION NICARAGUA"
COLA_MIGRACION_NICARAGUA_CAP  = 1

#####################################
# VARIABLES FOR MIGRACION NICARAGUA #
#####################################
TRAMITE_MIGRACION_NICARAGUA_NAME  = "MIGRACION NICARAGUA"
TRAMITE_MIGRACION_NICARAGUA_CAP   = 1
TRAMITE_MIGRACION_NICARAGUA_MEDIA = 33.3
TRAMITE_MIGRACION_NICARAGUA_STDEV = 8.2

########################################
# VARIABLES FOR COLA ADUANA| NICARAGUA #
########################################
COLA_ADUANA_NICARAGUA_NAME = "COLA ADUANA NICARAGUA"
COLA_ADUANA_NICARAGUA_CAP  = 1

##################################
# VARIABLES FOR ADUANA NICARAGUA #
##################################
TRAMITE_ADUANA_NICARAGUA_NAME  = "ADUANA NICARAGUA"
TRAMITE_ADUANA_NICARAGUA_CAP   = 2
TRAMITE_ADUANA_NICARAGUA_MEDIA = 61.15
TRAMITE_ADUANA_NICARAGUA_STDEV = 15.5

#######################################
# VARIABLES FOR COLA salida NICARAGUA #
#######################################
COLA_SALIDA_NICARAGUA_NAME = "COLA SALIDA NICARAGUA"
COLA_SALIDA_NICARAGUA_CAP  = 41

#####################################
# VARIABLES FOR MIGRACION NICARAGUA #
#####################################
TRAMITE_SALIDA_NICARAGUA_NAME  = "SALIDA NICARAGUA"
TRAMITE_SALIDA_NICARAGUA_CAP   = 2
TRAMITE_SALIDA_NICARAGUA_MEDIA = 161.3
TRAMITE_SALIDA_NICARAGUA_STDEV = 40.3




###################################
###################################
###################################
###                             ###
###                             ###
###    INITIATION OF OBJECTS    ###
###                             ###
###                             ###
###################################
###################################
###################################


##################
##################
##              ##
##  SIMULATION  ##
##              ##
##################
##################

simulacion = Simulacion(TOTAL_NUMBER_OF_TRANSPORTS)
simulacion.setAdditionLambdas(LAMBDAS)


########################
########################
##                    ##
##  COLAS Y PROCESOS  ##
##                    ##
########################
########################

###################
# COLA DE INGRESO #
###################
# 1ER ITEM DE SECUENCIA
simulacion.addSequenceElement(Cola(COLA_DE_INGRESO_NAME, \
								TOTAL_NUMBER_OF_TRANSPORTS))

########################
# TRAMITE DE MIGRACION #
########################
# 2DO ITEM DE SECUENCIA
simulacion.addSequenceElement(Proceso(TRAMITE_DE_MIGRACION_NAME, \
									TRAMITE_DE_MIGRACION_CAP,    \
									TRAMITE_DE_MIGRACION_MEDIA,  \
									TRAMITE_DE_MIGRACION_STDEV))

###################
# COLA DE ADUANAS #
###################
# 3ER ITEM DE SECUENCIA
simulacion.addSequenceElement(Cola(COLA_DE_ADUANAS_NAME,COLA_DE_ADUANAS_CAP))

######################
# TRAMITE DE ADUANAS #
######################
# 4TO ITEM DE SECUENCIA
simulacion.addSequenceElement(Proceso(TRAMITE_DE_ADUANAS_NAME, \
									TRAMITE_DE_ADUANAS_CAP,    \
									TRAMITE_DE_ADUANAS_MEDIA,  \
									TRAMITE_DE_ADUANAS_STDEV))



############################
############################
############################
###                      ###
###                      ###
###    RUN THIS THING    ###
###                      ###
###                      ###
############################
############################
############################

# simulacion.run()
