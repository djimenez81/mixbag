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
colaDeIngreso = Cola(COLA_DE_INGRESO_NAME, TOTAL_NUMBER_OF_TRANSPORTS)

###################### 
# TRAMITE DE ADUANAS # 
###################### 

# 2DO ITEM DE SECUENCIA
tramiteDeAduanas = Proceso(TRAMITE_DE_MIGRACION_NAME, TRAMITE_DE_MIGRACION_CAP,\
						TRAMITE_DE_MIGRACION_MEDIA, TRAMITE_DE_MIGRACION_STDEV) 

################### 
# COLA DE ADUANAS # 
################### 

# 3ER ITEM DE SECUENCIA
colaDeAduanas = cola(COLA_DE_ADUANAS_NAME,COLA_DE_ADUANAS_CAP)


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

