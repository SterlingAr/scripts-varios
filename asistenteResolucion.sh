# El script sirve para añadir nuevas resoluciones de manera interactiva 
# En linux, puedo hacer eso usando los comandos 'cvt', 'xrandr', en este script quiero automatizar  este proceso
# Ejemplo : 
# cvt 1440 900 (esto genera una línea de datos que usaré con xrandr, copiar apartir de 'Modeline')
# xrandr --newmode "1440x900_60.00"  106.50  1440 1528 1672 1904  900 903 909 934 -hsync +vsync
# xrandr --addmode VGA-0 "1440x900_60.00" (VGA-0 es la pantalla a la que añado la resolucin)
# xrandr -s 1440x900 
# 

#guardo en una lista los displays conectados
connectedDisplays=($(xrandr | grep -w connected  | awk -F'[ +]' '{print $1}'))
#salvaguardo la resolución actual, guardo en 2 variables los valores actuales del eje X y Y respectivamente
Xaxis=$(xrandr --current | grep '*' | uniq | awk '{print $1}' | cut -d 'x' -f1) #

Yaxis=$(xrandr --current | grep '*' | uniq | awk '{print $1}' | cut -d 'x' -f2)

echo "Selecciona el display sobre el que quieres trabajar."

#muestro en pantalla una lista con los displays conectados
count=0
for i in ${connectedDisplays[@]}
do

	echo "$count.$i"
	count=$((++count))
done

echo -n "Tu selección: "

read displayInput
#leo el input del usuario y me aseguro que es correcto
if [ $displayInput -ge 0 ] || [ $displayInput -le ${#connectedDisplays[@]} ]
then
	#si ha pasado, pido al usuario la resolucin que quiere y guardo los ejes en variables
	echo "Has seleccionado el display: ${connectedDisplays[$displayInput]}"
	
	echo "Introduce la resolución (ej 1440 900):"
        read width height

        echo "Has introducido la siguiente resolución: ${width}x${height}.Deseas continuar?(S/N)"


	read userContinue 
	#si el usuario quiere continuar, proceso la respuesta
	if [ "${userContinue,}" == "s" ] || [ "${userContinue,}" == "y" ]
	then

		#uso la combinacion de comandos cvt + xrandr para crear y aplicar la nueva resolucin al display
        	fullModline=$(cvt $width $height | grep "Modeline" -A 5)
		echo $fullModline > $HOME/modeline.txt
        	modeline=$(grep -oP '(?<=Modeline ).*' ~/modeline.txt)
		lessModeline=$(sed '/Modeline/s/.*Modeline \([^ ][^ ]*\)[ ]*.*/\1/' ~/modeline.txt)
		xrandr --newmode $modeline
		xrandr --addmode ${connectedDisplays[$displayInput]} $lessModeline
		echo "La resolución se ha añadido, desea aplicarla? S/N"
		
		read changeRes
		#si quiere cambiar ya, uso xrandr -s para aplicar la resolución que ha añadido anteriormente
		if [ "${changeRes,}" == "s" ] || [ "${changeRes,}" == "y" ]
		then
			xrandr -s "${width}x${height}"
			echo "La resolución se ha aplicado.Desea revertir los cambios? S/N"
			#en caso de que no le guste, puede revertirla 
			read revertChanges
			if [ "${revertChanges,}" == "s" ] || [ "${revertChanges,}" == "y" ]
			then
				xrandr -s "${Xaxis}x${Yaxis}"
			else
				exit
			fi 
		else
			exit
		fi					

		
	else

	echo "Has salido del programa."
	exit
	fi
else

	echo "Input inválido."
	exit
fi


