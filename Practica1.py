import RPi.GPIO as GPIO
import time
 
in1 = 11
in2 = 12
in3 = 13
in4 = 15
in5 = 31
in6 = 33
in7 = 35
in8 = 37
startaz = 0
startel = 0

    # setting up
GPIO.setwarnings(False)
GPIO.setmode( GPIO.BOARD )
GPIO.setup( in1, GPIO.OUT )
GPIO.setup( in2, GPIO.OUT )
GPIO.setup( in3, GPIO.OUT )
GPIO.setup( in4, GPIO.OUT )
GPIO.setup( in5, GPIO.OUT )
GPIO.setup( in6, GPIO.OUT )
GPIO.setup( in7, GPIO.OUT )
GPIO.setup( in8, GPIO.OUT )

    # initializing
GPIO.output( in1, GPIO.LOW )
GPIO.output( in2, GPIO.LOW )
GPIO.output( in3, GPIO.LOW )
GPIO.output( in4, GPIO.LOW )
GPIO.output( in5, GPIO.LOW )
GPIO.output( in6, GPIO.LOW )
GPIO.output( in7, GPIO.LOW )
GPIO.output( in8, GPIO.LOW )
     
#puesta de todos los pines en bajo 
def cleanup():
    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )
    GPIO.output( in5, GPIO.LOW )
    GPIO.output( in6, GPIO.LOW )
    GPIO.output( in7, GPIO.LOW )
    GPIO.output( in8, GPIO.LOW )
    GPIO.cleanup()

while True:
    
    step_sleep = 0.002
    
    #etapa de ingreso de grados de azimut y elevacion
    azimut = float(input('Ingrese azimut entre 0 & 360: '))# 5.625*(1/64), 4096 pasos son 360°
    step_count_az = int(abs(azimut-startaz)*(4096/360)) #conversion de dato ingresado en grados a numero de pasos
    
    elevacion = float(input('Ingrese elevacion entre 0 & 180: '))
    step_count_el = int(abs(elevacion-startel)*(4096/360))
    
    #etapa de guardado de punto de referencia
    if startaz <= azimut:    
        directionaz = True # True giro en un sentido 
        startaz = azimut
    elif startaz >= azimut:
        directionaz = False # False giro en sentido contrario
        startaz = azimut

    if startel <= elevacion:    
        directionel = True 
        startel = elevacion
    elif startel >= elevacion:
        directionel = False 
        startel = elevacion
    
    #configuracion del giro de motor en medio paso
    step_sequence = [[1,0,0,1],
                     [1,0,0,0],
                     [1,1,0,0],
                     [0,1,0,0],
                     [0,1,1,0],
                     [0,0,1,0],
                     [0,0,1,1],
                     [0,0,0,1]]


    #vectores para la sustitucion con respecto a la matriz 
    motor_pins_az = [in1,in2,in3,in4]
    motor_pins_el = [in5,in6,in7,in8]
    motor_step_counter = 0 
     
    
     
     
    #etapa de puesta en marcha del motor
    try:
        #motor encargado del azimut
        i = 0
        for i in range(step_count_az): #dura la cantidad de pasos (grados) que se hayan ingresado
            for pinaz in range(0, len(motor_pins_az)): 
                GPIO.output( motor_pins_az[pinaz], step_sequence[motor_step_counter][pinaz] ) #seleccionamos el pin y el elemento de la matriz 
            if directionaz==True:
                motor_step_counter = (motor_step_counter - 1) % 8 #indicamos si se iniciara de la fila 0 a 7 o de la 7 a 0
                
            elif directionaz==False:
                motor_step_counter = (motor_step_counter + 1) % 8
                
            else: 
                print( "el sentido de la direccion debe ser True o False" )
                cleanup()
                exit( 1 )
            time.sleep( step_sleep )
            
        #motor encargado de elevacion
        j = 0
        for j in range(step_count_el):
            for pinel in range(0, len(motor_pins_el)):
                GPIO.output( motor_pins_el[pinel], step_sequence[motor_step_counter][pinel] )
            if directionel==True:
                motor_step_counter = (motor_step_counter - 1) % 8
            elif directionel==False:
                motor_step_counter = (motor_step_counter + 1) % 8
            else: 
                print( "el sentido de la direccion debe ser True o False" )
                cleanup()
                exit( 1 )
            time.sleep( step_sleep )
     
        
    except KeyboardInterrupt:
        cleanup()
        exit( 1 )
     
cleanup()
exit( 0 )